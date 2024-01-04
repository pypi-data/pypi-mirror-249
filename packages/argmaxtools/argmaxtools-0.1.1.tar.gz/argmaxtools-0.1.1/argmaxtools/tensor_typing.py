#
# For licensing see accompanying LICENSE.md file.
# Copyright (C) 2023 Argmax, Inc. All Rights Reserved.
#

from beartype.typing import Tuple
from jaxtyping import Float
from torch import Tensor


# nn.Attention type hints
# Inputs
InputEmbedsType = Float[Tensor, "batch embed_dim 1 q_seq_len"]
AttentionMaskType = Float[Tensor, "batch kv_seq_len"]
KVCacheType = Float[Tensor, "batch embed_dim 1 kv_proj_embed_dim"]
EncoderOutputEmbedsType = Float[Tensor, "batch embed_dim 1 _"]

# Outputs
SelfAttentionReturnType = Tuple[Float[Tensor, "batch embed_dim 1 q_seq_len"]]
EncoderDecoderAttentionReturnType = Tuple[Float[Tensor, "batch embed_dim 1 q_seq_len"]]
KVCachedSelfAttentionReturnType = Tuple[
    Float[Tensor, "batch embed_dim 1 q_seq_len"],  # outputs
    Float[Tensor, "batch embed_dim 1 q_seq_len"],  # current_key
    Float[Tensor, "batch embed_dim 1 q_seq_len"]   # current_value
]
