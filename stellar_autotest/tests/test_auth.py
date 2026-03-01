# -*- coding: utf-8 -*-
"""
认证模块接口用例
覆盖：注册 / 登录 / 获取当前用户信息
"""
import pytest
import allure

from utils.assertion_helper import assert_helper


@allure.feature("认证模块")
class TestRegister:

    @allure.story("注册")
    @allure.title("正向：注册新账号成功")
    @pytest.mark.smoke
    @pytest.mark.positive
    @pytest.mark.auth
    def test_register_success(self, anon_client, register_payload):
        """用随机邮箱注册，期望 201，响应包含 email 字段"""
        response = anon_client.post("/auth/register", json_data=register_payload)
        assert_helper.assert_status_code(response, 201)
        assert_helper.assert_json_keys(response, ["email"])
        assert_helper.assert_json_value(response, "email", register_payload["email"])

    @allure.story("注册")
    @allure.title("负向：邮箱已注册 → 409")
    @pytest.mark.negative
    @pytest.mark.auth
    def test_register_duplicate_email(self, anon_client):
        """使用 config.yaml 里已存在的测试账号邮箱注册，期望 409"""
        from utils.config_manager import config
        user = config.get_test_user()
        payload = {
            "username": "duplicate_user",
            "email": user["email"],
            "password": "SomePass123",
        }
        response = anon_client.post("/auth/register", json_data=payload)
        assert_helper.assert_status_code(response, 409)

    @allure.story("注册")
    @allure.title("负向：缺少必填字段 → 422")
    @pytest.mark.negative
    @pytest.mark.auth
    def test_register_missing_fields(self, anon_client):
        """只传 email，缺 username 和 password，期望 422"""
        response = anon_client.post("/auth/register", json_data={"email": "x@x.com"})
        assert_helper.assert_status_code(response, 422)


@allure.feature("认证模块")
class TestLogin:

    @allure.story("登录")
    @allure.title("正向：正确账号密码登录成功")
    @pytest.mark.smoke
    @pytest.mark.positive
    @pytest.mark.auth
    def test_login_success(self, anon_client):
        """使用 config.yaml 里的测试账号，期望 200，响应包含 access_token"""
        from utils.config_manager import config
        user = config.get_test_user()
        response = anon_client.post("/auth/login", json_data={
            "email": user["email"],
            "password": user["password"],
        })
        assert_helper.assert_status_code(response, 200)
        assert_helper.assert_json_keys(response, ["access_token", "token_type"])
        assert_helper.assert_json_value(response, "token_type", "bearer")
        assert_helper.assert_json_not_none(response, "access_token")

    @allure.story("登录")
    @allure.title("负向：密码错误 → 401")
    @pytest.mark.negative
    @pytest.mark.auth
    def test_login_wrong_password(self, anon_client):
        """密码错误，期望 401"""
        from utils.config_manager import config
        user = config.get_test_user()
        response = anon_client.post("/auth/login", json_data={
            "email": user["email"],
            "password": "WrongPassword!",
        })
        assert_helper.assert_status_code(response, 401)

    @allure.story("登录")
    @allure.title("负向：邮箱不存在 → 401")
    @pytest.mark.negative
    @pytest.mark.auth
    def test_login_nonexistent_email(self, anon_client):
        """不存在的邮箱，期望 401"""
        response = anon_client.post("/auth/login", json_data={
            "email": "no_such_user@stellar.auto",
            "password": "Whatever123",
        })
        assert_helper.assert_status_code(response, 401)

    @allure.story("登录")
    @allure.title("负向：缺少 password 字段 → 422")
    @pytest.mark.negative
    @pytest.mark.auth
    def test_login_missing_password(self, anon_client):
        """只传 email，期望 422"""
        response = anon_client.post("/auth/login", json_data={"email": "a@b.com"})
        assert_helper.assert_status_code(response, 422)


@allure.feature("认证模块")
class TestMe:

    @allure.story("当前用户信息")
    @allure.title("正向：带 token 获取当前用户信息")
    @pytest.mark.smoke
    @pytest.mark.positive
    @pytest.mark.auth
    def test_get_me_success(self, http_client):
        """带有效 token，期望 200，响应包含 email / id"""
        response = http_client.get("/auth/me")
        assert_helper.assert_status_code(response, 200)
        assert_helper.assert_json_keys(response, ["id", "email"])
        assert_helper.assert_response_time(response, 3.0)

    @allure.story("当前用户信息")
    @allure.title("负向：不带 token → 401")
    @pytest.mark.negative
    @pytest.mark.auth
    def test_get_me_no_token(self, anon_client):
        """不带 token，期望 401"""
        response = anon_client.get("/auth/me")
        assert_helper.assert_status_code(response, 401)
