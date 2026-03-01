# -*- coding: utf-8 -*-
"""
pytest配置文件 - 全局fixtures和配置
"""

import pytest
import allure
from typing import Generator
from utils.config_manager import config
from utils.http_client import HTTPClient
from utils.logger import logger
from utils.data_generator import data_generator


@pytest.fixture(scope="session")
def http_client() -> HTTPClient:
    """HTTP客户端fixture"""
    client = HTTPClient()
    logger.info(f"创建HTTP客户端，基础URL: {client.base_url}")
    return client


@pytest.fixture(scope="session")
def test_config():
    """测试配置fixture"""
    return config


@pytest.fixture(scope="function")
def test_data():
    """测试数据生成器fixture"""
    return data_generator


@pytest.fixture(scope="function", autouse=True)
def test_setup_teardown(request):
    """测试用例前后置处理"""
    test_name = request.node.name
    
    # 前置处理
    logger.info(f"开始执行测试用例: {test_name}")
    
    with allure.step("测试用例初始化"):
        allure.attach(
            test_name,
            name="测试用例名称",
            attachment_type=allure.attachment_type.TEXT
        )
    
    yield
    
    # 后置处理
    logger.info(f"测试用例执行完成: {test_name}")


@pytest.fixture(scope="function")
def medicine_test_data():
    """药物测试数据fixture"""
    return {
        'valid_data': data_generator.generate_medicine_data(),
        'invalid_data': {
            'name': '',
            'price': -10,
            'stock': -5
        },
        'boundary_data': {
            'min_price': 0,
            'max_price': 99999.99,
            'min_stock': 0,
            'max_stock': 999999
        }
    }


@pytest.fixture(scope="function")
def patient_test_data():
    """患者测试数据fixture"""
    return {
        'valid_data': data_generator.generate_patient_data(),
        'invalid_data': {
            'patient_name': '',
            'age': -1,
            'phone': '123'
        },
        'boundary_data': {
            'min_age': 0,
            'max_age': 150
        }
    }


@pytest.fixture(scope="function")
def doctor_test_data():
    """医生测试数据fixture"""
    return {
        'valid_data': data_generator.generate_doctor_data(),
        'invalid_data': {
            'doctor_name': '',
            'years_of_experience': -1,
            'email': 'invalid_email'
        }
    }


@pytest.fixture(scope="function")
def consultation_test_data():
    """就诊测试数据fixture"""
    return {
        'valid_data': data_generator.generate_consultation_data(),
        'invalid_data': {
            'patient_id': -1,
            'patient_name': ''
        }
    }


@pytest.fixture(scope="function")
def appointment_test_data():
    """预约测试数据fixture"""
    return {
        'valid_data': data_generator.generate_appointment_data(),
        'invalid_data': {
            'patient_name': '',
            'appointment_date': 'invalid_date'
        }
    }


def pytest_configure(config):
    """pytest配置钩子"""
    # 添加自定义标记
    config.addinivalue_line(
        "markers", "smoke: 冒烟测试用例"
    )
    config.addinivalue_line(
        "markers", "regression: 回归测试用例"
    )
    config.addinivalue_line(
        "markers", "api: API接口测试用例"
    )


def pytest_collection_modifyitems(config, items):
    """修改测试用例收集"""
    for item in items:
        # 为所有测试用例添加api标记
        item.add_marker(pytest.mark.api)
        
        # 根据测试用例名称添加模块标记
        if "medicine" in item.name.lower():
            item.add_marker(pytest.mark.medicine)
        elif "patient" in item.name.lower():
            item.add_marker(pytest.mark.patient)
        elif "consultation" in item.name.lower():
            item.add_marker(pytest.mark.consultation)
        elif "doctor" in item.name.lower():
            item.add_marker(pytest.mark.doctor)
        elif "appointment" in item.name.lower():
            item.add_marker(pytest.mark.appointment)


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """生成测试报告钩子"""
    outcome = yield
    rep = outcome.get_result()
    
    # 为失败的测试用例添加截图或日志
    if rep.when == "call" and rep.failed:
        # 可以在这里添加失败时的额外信息
        logger.error(f"测试用例失败: {item.name}")
        
        # 将失败信息附加到Allure报告
        if hasattr(item, 'funcargs'):
            with allure.step("测试失败信息"):
                allure.attach(
                    str(rep.longrepr),
                    name="失败详情",
                    attachment_type=allure.attachment_type.TEXT
                )