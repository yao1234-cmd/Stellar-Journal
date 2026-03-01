# -*- coding: utf-8 -*-
"""
日志工具 - 统一的日志配置
"""
import logging
import os
from pathlib import Path
from .config_manager import config


def _setup_logger() -> logging.Logger:
    log_dir = Path(__file__).resolve().parent.parent / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)

    log_file = config.get("logging.file_path", "./logs/test.log")
    log_level = config.get("logging.level", "INFO")

    logger = logging.getLogger("stellar_autotest")
    logger.setLevel(getattr(logging, log_level.upper(), logging.INFO))

    if not logger.handlers:
        fmt = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

        # 控制台
        ch = logging.StreamHandler()
        ch.setFormatter(fmt)
        logger.addHandler(ch)

        # 文件
        abs_log = (Path(__file__).resolve().parent.parent / log_file.lstrip("./"))
        fh = logging.FileHandler(str(abs_log), encoding="utf-8")
        fh.setFormatter(fmt)
        logger.addHandler(fh)

    return logger


logger = _setup_logger()
