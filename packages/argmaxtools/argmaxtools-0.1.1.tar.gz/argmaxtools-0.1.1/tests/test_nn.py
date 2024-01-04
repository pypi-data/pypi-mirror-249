#
# For licensing see accompanying LICENSE.md file.
# Copyright (C) 2023 Argmax, Inc. All Rights Reserved.
#

import coremltools as ct
import json
import numpy as np
import os
import random
import torch
import torch.nn.functional as F
import unittest

from argmaxtools.nn import Attention, AttentionType, AttentionHeadType
from argmaxtools.utils import get_logger, get_fastest_device
from tests import utils, coreml

logger = get_logger(__name__)

torch.set_grad_enabled(False)
torch.use_deterministic_algorithms(True)

# Test configuration
ARCH_CFG = dict(n_heads=32, embed_dim=4096, n_kv_heads=None)
INPUT_CFG = dict(batch_size=1, kv_seq_len=1024, q_seq_len=1)

TEST_DEV = get_fastest_device()
TEST_PSNR_THR = 40
TEST_TORCH_DTYPE = torch.float32
TEST_COREML_IO_DTYPE = np.float16
TEST_COMPUTE_UNIT = ct.ComputeUnit.CPU_AND_GPU
TEST_CACHE_DIR = os.getenv("TEST_CACHE_DIR", None) or "/tmp"


class TestKVCachedSelfAttention(coreml.CoreMLTestsMixin, unittest.TestCase):
    """ Unit tests for `argmaxtools.nn.Attention` with
    `attention_type=AttentionType.KVCachedSelfAttention`
    """
    @classmethod
    def setUpClass(cls):
        cls.test_torch_model = Attention(
            **ARCH_CFG,
            attention_type=AttentionType.KVCachedSelfAttention,
        ).to(TEST_TORCH_DTYPE).to(TEST_DEV).eval()

        # Decode a random token index (implies a random valid KV cache length)
        cls.decode_idx = random.randint(1, INPUT_CFG["kv_seq_len"])
        logger.info(
            f"Decoding {cls.decode_idx}th token of {INPUT_CFG['kv_seq_len']} "
            "max tokens for AttentionType.KVCachedSelfAttention"
        )

        cls.test_output_names = [
            "attention_output",
            "key_cache_update",
            "value_cache_update",
        ]

        cls.test_torch_inputs = dict(
            input_embeds=torch.randn(
                INPUT_CFG["batch_size"],
                ARCH_CFG["embed_dim"],
                1,
                INPUT_CFG["q_seq_len"]
            ),
            # 0: not masked, -1e4: masked
            key_padding_mask=torch.cat([
                    torch.zeros((
                        INPUT_CFG["batch_size"],
                        cls.decode_idx
                    )),
                    torch.ones((
                        INPUT_CFG["batch_size"],
                        INPUT_CFG["kv_seq_len"] - cls.decode_idx)
                    ) * -1e4
                ],
                dim=1,
            ),
            key_cache=torch.randn(
                INPUT_CFG["batch_size"],
                cls.test_torch_model.kv_proj_embed_dim,
                1,
                INPUT_CFG["kv_seq_len"]
            ),
            value_cache=torch.randn(
                INPUT_CFG["batch_size"],
                cls.test_torch_model.kv_proj_embed_dim,
                1,
                INPUT_CFG["kv_seq_len"]
            ),
            kv_cache_update_mask=torch.zeros(
                INPUT_CFG["batch_size"],
                INPUT_CFG["kv_seq_len"]
            ),
        )
        # Update the mask to indicate the current decode index
        cls.test_torch_inputs[
            "kv_cache_update_mask"][:, cls.decode_idx - 1] = 1.

        cls.test_torch_inputs = {
            k: v.to(TEST_TORCH_DTYPE).to(TEST_DEV)
            for k, v in cls.test_torch_inputs.items()
        }

        cls.test_cache_dir = TEST_CACHE_DIR
        cls.model_name = "KVCachedSelfAttention"

        # Setup CoreMLTestMixin
        super().setUpClass()

        cls.results = {}
        cls.results["config"] = {"architecture": ARCH_CFG, "input": INPUT_CFG}
        cls.results["bench"] = {
            "torch": utils.median_user_latency(
                lambda: cls.test_torch_model(**cls.test_torch_inputs),
                return_flops=True,
            ),
            "coreml": utils.median_user_latency(
                lambda: cls.test_coreml_model.predict(cls.test_coreml_inputs)
            ),
        }

        out_path = os.path.join(
            TEST_CACHE_DIR,
            f"test_{cls.__class__.__name__}.json"
        )

        with open(out_path, "w") as f:
            json.dump(cls.results, f, indent=2)

    @classmethod
    def tearDownClass(cls):
        cls.test_torch_model = None
        cls.test_output_names = None
        cls.test_torch_inputs = None
        cls.test_cache_dir = None
        cls.decode_idx = None
        cls.results = None

        super().tearDownClass()


class TestSelfAttention(coreml.CoreMLTestsMixin, unittest.TestCase):
    """ Unit tests for `argmaxtools.nn.Attention` with
    `attention_type=AttentionType.SelfAttention`
    """
    @classmethod
    def setUpClass(cls):
        cls.test_torch_model = Attention(
            **ARCH_CFG,
            attention_type=AttentionType.SelfAttention,
        ).to(TEST_TORCH_DTYPE).to(TEST_DEV).eval()

        cls.test_output_names = ["attention_output"]
        cls.active_seq_len = random.randint(0, INPUT_CFG["kv_seq_len"])
        cls.test_torch_inputs = dict(
            input_embeds=torch.randn(
                INPUT_CFG["batch_size"],
                ARCH_CFG["embed_dim"],
                1,
                INPUT_CFG["kv_seq_len"]
            ),
            key_padding_mask=F.pad(
                torch.zeros(INPUT_CFG["batch_size"], cls.active_seq_len),
                (0, INPUT_CFG["kv_seq_len"] - cls.active_seq_len),
                value=-1e4
            )
        )

        cls.test_torch_inputs = {
            k: v.to(TEST_TORCH_DTYPE).to(TEST_DEV)
            for k, v in cls.test_torch_inputs.items()
        }

        cls.test_cache_dir = TEST_CACHE_DIR
        cls.model_name = "SelfAttention"

        # Setup CoreMLTestMixin
        super().setUpClass()

        cls.results = {}
        cls.results["config"] = {"architecture": ARCH_CFG, "input": INPUT_CFG}
        cls.results["bench"] = {
            "torch": utils.median_user_latency(
                lambda: cls.test_torch_model(**cls.test_torch_inputs),
                return_flops=True,
            ),
            "coreml": utils.median_user_latency(
                lambda: cls.test_coreml_model.predict(cls.test_coreml_inputs)
            ),
        }

        out_path = os.path.join(
            TEST_CACHE_DIR,
            f"test_{cls.__class__.__name__}.json"
        )

        with open(out_path, "w") as f:
            json.dump(cls.results, f, indent=2)

    @classmethod
    def tearDownClass(cls):
        cls.test_torch_model = None
        cls.test_output_names = None
        cls.test_torch_inputs = None
        cls.decode_idx = None
        cls.results = None

        super().tearDownClass()


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--persistent-cache-dir", default=None, type=str)
    parser.add_argument(
        "--head-type",
        choices=tuple(AttentionHeadType._member_names_),
        required=True
    )

    args = parser.parse_args()

    head_type = AttentionHeadType[args.head_type]
    if head_type == AttentionHeadType.MultiQuery:
        n_kv_heads = 1
    elif head_type == AttentionHeadType.GroupQuery:
        n_kv_heads = ARCH_CFG["n_heads"] // 4
    elif head_type == AttentionHeadType.MultiHead:
        n_kv_heads = None

    ARCH_CFG["n_kv_heads"] = n_kv_heads

    maybe_dir = args.persistent_cache_dir
    with utils._get_test_cache_dir(maybe_dir) as TEST_CACHE_DIR:
        suite = unittest.TestSuite()
        suite.addTest(TestKVCachedSelfAttention("test_baseline_module"))
        suite.addTest(TestSelfAttention("test_baseline_module"))

        if os.getenv("DEBUG", False):
            suite.debug()
        else:
            runner = unittest.TextTestRunner()
            runner.run(suite)
