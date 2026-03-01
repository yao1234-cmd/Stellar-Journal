# -*- coding: utf-8 -*-
"""
配置管理器 - 负责加载和管理测试配置
"""

import os
import yaml
from typing import Dict, Any
from pathlib import Path


class ConfigManager:
    """配置管理器"""
    
    def __init__(self, config_file: str = None):
        """
        初始化配置管理器
        
        Args:
            config_file: 配置文件路径，默认为config/config.yaml
        """
        if config_file is None:
            config_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config', 'config.yaml')
        
        self.config_file = config_file
        self._config = self._load_config()
    
    def _load_config(self) -> Dict[str, Any]:
        """加载配置文件"""
        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        except FileNotFoundError:
            raise FileNotFoundError(f"配置文件未找到: {self.config_file}")
        except yaml.YAMLError as e:
            raise ValueError(f"配置文件格式错误: {e}")
    
    def get(self, key: str, default=None):
        """
        获取配置值，支持点号分隔的嵌套键
        
        Args:
            key: 配置键，支持 'section.subsection.key' 格式
            default: 默认值
        
        Returns:
            配置值
        """
        keys = key.split('.')
        value = self._config
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        
        return value
    
    def get_base_url(self) -> str:
        """获取基础URL"""
        return self.get('test_env.base_url', 'http://localhost:8000')
    
    def get_timeout(self) -> int:
        """获取请求超时时间"""
        return self.get('test_env.timeout', 30)
    
    def get_retry_count(self) -> int:
        """获取重试次数"""
        return self.get('test_env.retry_count', 3)
    
    def get_test_data(self, data_type: str) -> Dict[str, Any]:
        """
        获取测试数据
        
        Args:
            data_type: 数据类型，如 'valid_medicine', 'valid_patient' 等
        
        Returns:
            测试数据字典
        """
        return self.get(f'test_data.{data_type}', {})
    
    def get_allure_results_dir(self) -> str:
        """获取Allure结果目录"""
        return self.get('report.allure_results_dir', './reports/allure-results')
    
    def get_html_report_path(self) -> str:
        """获取HTML报告路径"""
        return self.get('report.html_report_path', './reports/report.html')


# 全局配置实例
config = ConfigManager()