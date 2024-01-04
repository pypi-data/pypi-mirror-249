#
# For licensing see accompanying LICENSE.md file.
# Copyright (C) 2023 Argmax, Inc. All Rights Reserved.
#
# noqa: F722

from beartype import beartype
from beartype.typing import Optional, Tuple, Union
from enum import Enum

import torch
import torch.nn as nn

from argmaxtools import tensor_typing as tt
from argmaxtools.utils import get_logger

logger = get_logger(__name__)


class AttentionType(Enum):
    SelfAttention = 1
    CausalSelfAttention = 2
    KVCachedSelfAttention = 3
    EncoderDecoderCrossAttention = 4


class AttentionHeadType(Enum):
    MultiHead = 1     # MHA: https://arxiv.org/abs/1706.03762
    GroupQuery = 2    # GQA: https://arxiv.org/abs/2305.13245
    MultiQuery = 3    # MQA: https://arxiv.org/pdf/1911.02150


class AttentionImplementation(Enum):
    SplitEinsum = 1
    CatBMM = 2


DEFAULT_ATTENTION_IMPLEMENTATION = AttentionImplementation.CatBMM


@beartype
class Attention(nn.Module):
    """ Argmax reference attention implementation
    """
    def __init__(self,
                 embed_dim: int,
                 n_heads: int,
                 attention_type: AttentionType,
                 n_kv_heads: Optional[int] = None) -> None:
        """
        Args:
            embed_dim:          Number of embedding dimensions
            n_heads:            Number of attention heads
            attention_type:     Attention type
            n_kv_heads:         MHA if None, GQA if 1<n_kv_heads<n_heads
                                and MQA if n_kv_heads=1
        """
        super().__init__()

        # Configure dimensions
        self.embed_dim = embed_dim
        self.n_heads = n_heads

        assert self.embed_dim % self.n_heads == 0, embed_dim
        self.per_head_dim = self.embed_dim // self.n_heads
        self.qk_denom = (self.embed_dim / self.n_heads) ** -0.5

        # Configure head type
        self.n_kv_heads = n_kv_heads
        if n_kv_heads is None or n_kv_heads == n_heads:
            self.head_type = AttentionHeadType.MultiHead
        elif n_kv_heads == 1:
            self.head_type = AttentionHeadType.MultiQuery
        elif n_kv_heads > 1:
            assert n_kv_heads <= n_heads and n_heads % n_kv_heads == 0
            self.head_type = AttentionHeadType.GroupQuery
        else:
            raise ValueError(f"Invalid n_kv_heads ({n_kv_heads})")

        logger.debug(f"AttentionHeadType: {self.head_type}")

        # Initialize layers
        self.kv_proj_embed_dim = self.per_head_dim * (n_kv_heads or n_heads)

        # Note: key bias is redundant due to softmax invariance
        self.k_proj = nn.Conv2d(embed_dim, self.kv_proj_embed_dim, 1, bias=False)
        self.q_proj = nn.Conv2d(embed_dim, embed_dim, 1)
        self.v_proj = nn.Conv2d(embed_dim, self.kv_proj_embed_dim, 1)
        self.o_proj = nn.Conv2d(embed_dim, embed_dim, 1)

        # Select attention_implementation (model interface and function do not change)
        # and attention_type (module interface and function might change)
        self._attention_implementation = DEFAULT_ATTENTION_IMPLEMENTATION
        self.attention_type = attention_type

    @property
    def attention_implementation(self):
        return self._attention_implementation

    @attention_implementation.setter
    def attention_implementation(self, value):
        assert isinstance(value, AttentionImplementation)
        self._attention_implementation = value

    def _maybe_tile(self,
                    key: torch.Tensor,
                    value: torch.Tensor) -> Tuple[torch.Tensor, torch.Tensor]:
        """ Tile key and value tensors before _sdpa() if head_type is GQA or MQA
        """

        if self.head_type != AttentionHeadType.MultiHead:
            repeats = self.embed_dim // self.kv_proj_embed_dim
            if key.shape[1] == self.kv_proj_embed_dim:
                key = key.repeat(1, repeats, 1, 1)
            if value.shape[1] == self.kv_proj_embed_dim:
                value = value.repeat(1, repeats, 1, 1)

        return key, value

    def forward(self,
                input_embeds: tt.InputEmbedsType,
                key_padding_mask: Optional[tt.AttentionMaskType] = None,
                key_cache: Optional[tt.KVCacheType] = None,
                value_cache: Optional[tt.KVCacheType] = None,
                kv_cache_update_mask: Optional[tt.AttentionMaskType] = None,
                encoder_output_embeds: Optional[tt.EncoderOutputEmbedsType] = None
                ) -> Union[
                    tt.SelfAttentionReturnType,
                    tt.EncoderDecoderAttentionReturnType,
                    tt.KVCachedSelfAttentionReturnType]:

        # Project input_embds to query, key and value
        query, current_key, current_value = self._qkv_proj(input_embeds,
                                                           encoder_output_embeds,
                                                           kv_cache_update_mask)
        # Configure the key and value tensors based on attention type
        key, value = self._finalize_kv(key_cache,
                                       value_cache,
                                       current_key,
                                       current_value,
                                       kv_cache_update_mask,
                                       encoder_output_embeds)

        # Compute scaled dot product attention
        attn, mh_w = self._sdpa(query,
                                key,
                                value,
                                key_padding_mask)

        outputs = (attn,)

        # If KV cached attention, return current key and value for cache updates
        if self.attention_type == AttentionType.KVCachedSelfAttention:
            outputs += (current_key, current_value)

        return outputs

    def _qkv_proj(self,
                  input_embeds,
                  encoder_output_embeds,
                  kv_cache_update_mask):
        """ Compute qkv projections prescribed by currently active input configurations
        """
        if encoder_output_embeds is not None:
            if self.attention_type != AttentionType.EncoderDecoderCrossAttention:
                raise ValueError(
                    "`encoder_output_embeds` is only compatible with the "
                    "AttentionType.EncoderDecoderCrossAttention configuration")

            kv_proj_inputs = encoder_output_embeds
        else:
            kv_proj_inputs = input_embeds

        query = self.q_proj(input_embeds)

        # TODO(atila): Support KVCachedEncoderDecoderCrossAttention
        current_key = self.k_proj(kv_proj_inputs)
        current_value = self.v_proj(kv_proj_inputs)

        return query, current_key, current_value

    def _finalize_kv(self,
                     key_cache,
                     value_cache,
                     current_key,
                     current_value,
                     kv_cache_update_mask,
                     encoder_output_embeds):
        """ Determine the key and value tensors based on attention type. If head_type is GQA or MQA,
        repeat key and value tensors to match the query tensor embedding dimensionality.
        """
        if self.attention_type == AttentionType.KVCachedSelfAttention:
            # Cache updates
            kv_cache_update_mask = kv_cache_update_mask[:, None, None, :]
            key = current_key * kv_cache_update_mask + key_cache * (1. - kv_cache_update_mask)
            value = current_value * kv_cache_update_mask + value_cache * (1. - kv_cache_update_mask)

        elif self.attention_type == AttentionType.EncoderDecoderCrossAttention:
            # Reuse static (encoder) cache
            if key_cache is not None or value_cache is not None:
                if encoder_output_embeds is not None:
                    "Can not provide encoder_output_embeds and {key,value}_cache simultaneously"

                logger.warning(
                    "EncoderDecoderCrossAttention receiving {key,value}_cache inputs "
                    "imply that decoder key and value projections were precomputed.")

                key = key_cache
                value = value_cache

            elif encoder_output_embeds is not None:
                key = current_key
                value = current_value
            else:
                raise ValueError

        elif self.attention_type in [AttentionType.SelfAttention,
                                     AttentionType.CausalSelfAttention]:
            key = current_key
            value = current_value
        else:
            raise ValueError(self.attention_type)

        # If not tiled upstream already
        key, value = self._maybe_tile(key, value)

        return key, value

    def _sdpa(self, query, key, value, key_padding_mask):
        """ Compute Scaled Dot Product Attention
        """
        if self.attention_implementation == AttentionImplementation.CatBMM:
            # Multi-Head Reshape
            batch_size = query.shape[0]

            bhcx = (batch_size, self.n_heads, self.per_head_dim, -1)
            mh_q = query.view(*bhcx) * self.qk_denom
            mh_k = key.view(*bhcx)
            mh_v = value.view(*bhcx)

            # Scaled Dot-Product Attention
            mh_w = torch.einsum('bhcq,bhck->bhqk', mh_q, mh_k)
            mh_w = self._maybe_mask_attention(mh_w, key_padding_mask)

            mh_w = mh_w.softmax(dim=3)
            attn = torch.einsum("bhqk,bhck->bhcq", [mh_w, mh_v])
            attn = attn.reshape(batch_size, self.embed_dim, 1, -1)

        elif self.attention_implementation == AttentionImplementation.SplitEinsum:
            # Multi-Head Split
            mh_q = query.mul(self.qk_denom).split(self.per_head_dim, dim=1)
            mh_k = key.transpose(1, 3).split(self.per_head_dim, dim=3)
            mh_v = value.split(self.per_head_dim, dim=1)

            # Scaled Dot-Product Attention
            mh_w = [
                torch.einsum('bchq,bkhc->bkhq', [qi, ki])
                for qi, ki in zip(mh_q, mh_k)]

            for h in range(self.n_heads):
                mh_w[h] = self._maybe_mask_attention(mh_w[h], key_padding_mask)

            mh_w = [wi.softmax(dim=1) for wi in mh_w]
            attn = torch.cat([
                torch.einsum('bkhq,bchk->bchq', wi, vi)
                for wi, vi in zip(mh_w, mh_v)], dim=1)
        else:
            raise ValueError(self.attention_implementation)

        attn = self.o_proj(attn)

        return attn, mh_w

    def _maybe_mask_attention(self, qk, key_padding_mask=None):
        """ Apply attention mask prior to softmax (if configured to do so)
        """
        if self.attention_implementation == AttentionImplementation.CatBMM:
            if key_padding_mask is not None:
                qk = qk + key_padding_mask[:, None, None, :]  # bhqk format

            if self.attention_type == AttentionType.CausalSelfAttention:
                seq_len = qk.shape[-1]
                causal_mask = torch.triu(
                    torch.ones(seq_len, seq_len, device=qk.device), 1
                )[None, None, :, :] * -1e4
                qk = qk + causal_mask

        elif self.attention_implementation == AttentionImplementation.SplitEinsum:
            if key_padding_mask is not None:
                qk = qk + key_padding_mask[:, :, None, None]  # bkhq format

            if self.attention_type == AttentionType.CausalSelfAttention:
                seq_len = qk.shape[-1]
                causal_mask = torch.tril(
                    torch.ones(seq_len, seq_len, device=qk.device), -1
                )[None, :, None, :] * -1e4
                qk = qk + causal_mask
        else:
            raise ValueError(self.attention_implementation)

        return qk


class FFN(nn.Module):
    def __init__(self, embed_dim, expansion_factor, activation_fn):
        super().__init__()
        self.fc1 = nn.Conv2d(embed_dim, embed_dim * expansion_factor, 1)
        self.act_fn = activation_fn
        self.fc2 = nn.Conv2d(embed_dim * expansion_factor, embed_dim, 1)

    def forward(self, x):
        return self.fc2(self.act_fn(self.fc1(x)))


# Reference:
# https://github.com/apple/ml-ane-transformers/blob/main/ane_transformers/reference/layer_norm.py
class LayerNorm(nn.Module):
    def __init__(self,
                 num_channels,
                 clip_mag=None,
                 eps=1e-5,
                 elementwise_affine=True):

        super().__init__()
        self.num_channels = num_channels
        self.eps = eps
        self.clip_mag = clip_mag
        self.elementwise_affine = elementwise_affine

        if self.elementwise_affine:
            self.weight = nn.Parameter(torch.Tensor(num_channels))
            self.bias = nn.Parameter(torch.Tensor(num_channels))

            self.weight.data = torch.ones_like(self.weight.data)
            self.bias.data = torch.zeros_like(self.bias.data)

    def forward(self, inputs):
        input_rank = len(inputs.size())
        if input_rank != 4:
            raise ValueError(f"Incorrect input rank (Expected 4, got {input_rank})")

        if self.clip_mag is not None:
            inputs.clamp_(-self.clip_mag, self.clip_mag)

        channels_mean = inputs.mean(dim=1, keepdims=True)

        zero_mean = inputs - channels_mean
        zero_mean_sq = zero_mean * zero_mean

        denom = (zero_mean_sq.mean(dim=1, keepdims=True) + self.eps).rsqrt()

        out = zero_mean * denom

        if self.elementwise_affine:
            w = self.weight.view(1, self.num_channels, 1, 1)
            b = self.bias.view(1, self.num_channels, 1, 1)
            out = w * out + b

        return out
