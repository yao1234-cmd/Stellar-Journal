# -*- coding: utf-8 -*-
"""
配置管理 - 读取 config/config.yaml，供 base_url、超时、测试账号等使用
"""
import os
import yaml
from pathlib import Path
from typing import Any, Dict


class ConfigManager:
    def __init__(self, config_file: str = None):
        if config_file is None:
            root = Path(__file__).resolve().parent.parent
            config_file = root / "config" / "config.yaml"
        self.config_file = str(config_file)
        self._config = self._load_config()

    def _load_config(self) -> Dict[str, Any]:
        with open(self.config_file, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)

    def get(self, key: str, default: Any = None) -> Any:
        keys = key.split(".")
        value = self._config
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        return value

    def get_base_url(self) -> str:
        return self.get("test_env.base_url", "http://localhost:8000/api/v1").rstrip("/")

    def get_timeout(self) -> int:
        return self.get("test_env.timeout", 30)

    def get_retry_count(self) -> int:
        return self.get("test_env.retry_count", 3)

    def get_test_user(self) -> Dict[str, str]:
        return self.get("test_user", {"email": "", "password": ""})

    def get_allure_results_dir(self) -> str:
        return self.get("report.allure_results_dir", "./reports/allure-results")


config = ConfigManager()
