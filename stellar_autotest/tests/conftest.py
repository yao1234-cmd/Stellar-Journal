# -*- coding: utf-8 -*-
"""
pytest 全局配置文件
- 提供带鉴权的 http_client fixture（session 级，整轮测试只登录一次）
- 提供不带 token 的 anon_client fixture（用于测 401 场景）
- 提供各业务测试数据 fixture
- 提供用例前后置日志 + Allure 钩子
"""
import uuid
import pytest
import allure

from utils.http_client import HTTPClient
from utils.config_manager import config
from utils.logger import logger


# =============================================================================
# HTTP 客户端 fixture
# =============================================================================

@pytest.fixture(scope="session")
def http_client() -> HTTPClient:
    """
    带有效 Bearer token 的 HTTP 客户端（整轮测试只登录一次）。
    从 config.yaml 的 test_user 读账号，调 POST /auth/login 拿 access_token。
    如果登录失败会直接报错，避免后续用例全部带着「无 token」运行。
    """
    client = HTTPClient()
    user = config.get_test_user()

    logger.info(f"[conftest] 开始登录，账号: {user['email']}")
    response = client.post("/auth/login", json_data={
        "email": user["email"],
        "password": user["password"],
    })

    assert response.status_code == 200, (
        f"登录失败，状态码: {response.status_code}，响应: {response.text}\n"
        f"请确认 config.yaml 里的 test_user 账号已注册且密码正确。"
    )

    token = response.json().get("access_token")
    assert token, "登录成功但响应中未找到 access_token"

    client.set_bearer_token(token)
    logger.info("[conftest] 登录成功，Bearer token 已设置")
    return client


@pytest.fixture(scope="function")
def anon_client() -> HTTPClient:
    """
    不带任何 token 的匿名客户端，用于验证「未登录 → 401」的负向场景。
    每个用例独立一个实例，互不干扰。
    """
    return HTTPClient()


# =============================================================================
# 测试数据 fixture
# =============================================================================

@pytest.fixture(scope="function")
def mood_payload() -> dict:
    """创建一条心情记录的请求体"""
    return {
        "type": "mood",
        "content": "今天项目进展顺利，心情很好，晚上看到了漂亮的夕阳。",
    }


@pytest.fixture(scope="function")
def spark_payload() -> dict:
    """创建一条灵感记录的请求体"""
    return {
        "type": "spark",
        "content": "用情绪驱动的颜色系统可以做成一款治愈系桌面壁纸生成器。",
    }


@pytest.fixture(scope="function")
def thought_payload() -> dict:
    """创建一条思考记录的请求体"""
    return {
        "type": "thought",
        "content": "记录这件事本身就是一种仪式感，它让我意识到每天的微小变化。",
    }


@pytest.fixture(scope="function")
def register_payload() -> dict:
    """
    随机生成注册请求体，每次用例独立一个账号，
    避免「邮箱已注册」导致用例互相影响。
    """
    uid = uuid.uuid4().hex[:8]
    return {
        "username": f"testuser_{uid}",
        "email": f"test_{uid}@stellar.auto",
        "password": "AutoTest1234",
    }


@pytest.fixture(scope="function")
def invalid_payloads() -> dict:
    """常见非法请求体，用于负向测试"""
    return {
        # content 缺失
        "missing_content": {"type": "mood"},
        # type 非法
        "invalid_type": {"type": "unknown", "content": "some content"},
        # content 为空字符串（min_length=1 校验）
        "empty_content": {"type": "mood", "content": ""},
        # content 超长（max_length=5000）
        "too_long_content": {"type": "mood", "content": "a" * 5001},
    }


# =============================================================================
# 用例前后置
# =============================================================================

@pytest.fixture(scope="function", autouse=True)
def test_lifecycle(request):
    """每条用例：执行前打印名称，执行后打印结果，Allure 挂附件"""
    name = request.node.name
    logger.info(f"[START] {name}")
    with allure.step("用例初始化"):
        allure.attach(name, name="用例名称", attachment_type=allure.attachment_type.TEXT)
    yield
    logger.info(f"[END]   {name}")


# =============================================================================
# pytest 标记与钩子
# =============================================================================

def pytest_configure(config_obj):
    """注册自定义标记，避免 --strict-markers 报 warning"""
    marks = [
        ("smoke",      "冒烟测试用例"),
        ("regression", "回归测试用例"),
        ("positive",   "正向测试用例"),
        ("negative",   "负向测试用例"),
        ("boundary",   "边界测试用例"),
        ("auth",       "认证模块"),
        ("records",    "记录模块"),
        ("planet",     "星球模块"),
    ]
    for name, desc in marks:
        config_obj.addinivalue_line("markers", f"{name}: {desc}")


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """用例失败时将错误信息挂到 Allure"""
    outcome = yield
    rep = outcome.get_result()
    if rep.when == "call" and rep.failed:
        logger.error(f"[FAIL] {item.name}")
        with allure.step("失败信息"):
            allure.attach(
                str(rep.longrepr),
                name="错误详情",
                attachment_type=allure.attachment_type.TEXT,
            )
