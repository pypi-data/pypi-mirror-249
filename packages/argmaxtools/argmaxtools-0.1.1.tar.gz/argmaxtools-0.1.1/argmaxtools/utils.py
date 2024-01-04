#
# For licensing see accompanying LICENSE.md file.
# Copyright (C) 2023 Argmax, Inc. All Rights Reserved.
#
import logging
import torch


def get_logger(name: str, level: int = logging.INFO) -> logging.RootLogger:
    logging.basicConfig()
    logger = logging.getLogger(name)
    logger.setLevel(level)
    return logger


logger = get_logger(__name__)


def get_fastest_device():
    device = "cpu"
    if torch.backends.mps.is_available():
        device = "mps"
    elif torch.backends.cudnn.is_available():
        device = "cuda"
    return device
