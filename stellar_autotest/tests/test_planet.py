# -*- coding: utf-8 -*-
"""
星球模块接口用例
覆盖：获取星球状态 / 历史 / 统计
"""
import pytest
import allure

from utils.assertion_helper import assert_helper


@allure.feature("星球模块")
class TestPlanetState:

    @allure.story("星球状态")
    @allure.title("正向：获取今日星球状态")
    @pytest.mark.smoke
    @pytest.mark.positive
    @pytest.mark.planet
    def test_get_planet_state_success(self, http_client):
        """获取星球状态，期望 200，响应含 atmosphere_color / stars / trees"""
        response = http_client.get("/planet/state")
        assert_helper.assert_status_code(response, 200)
        assert_helper.assert_json_keys(response, ["atmosphere_color", "stars", "trees"])
        assert_helper.assert_field_type(response, "stars", list)
        assert_helper.assert_field_type(response, "trees", list)
        assert_helper.assert_response_time(response, 5.0)

    @allure.story("星球状态")
    @allure.title("负向：不带 token → 401")
    @pytest.mark.negative
    @pytest.mark.planet
    def test_get_planet_state_no_token(self, anon_client):
        """不带 token 获取星球状态，期望 401"""
        response = anon_client.get("/planet/state")
        assert_helper.assert_status_code(response, 401)

    @allure.story("星球状态")
    @allure.title("正向：创建 mood 记录后，atmosphere_color 不为 None")
    @pytest.mark.positive
    @pytest.mark.planet
    def test_planet_state_after_mood_record(self, http_client, mood_payload):
        """先创建一条 mood 记录，再查星球状态，atmosphere_color 应该有值"""
        http_client.post("/records/", json_data=mood_payload)
        response = http_client.get("/planet/state")
        assert_helper.assert_status_code(response, 200)
        assert_helper.assert_json_not_none(response, "atmosphere_color")


@allure.feature("星球模块")
class TestPlanetHistory:

    @allure.story("历史记录")
    @allure.title("正向：获取星球历史")
    @pytest.mark.positive
    @pytest.mark.planet
    def test_get_planet_history_success(self, http_client):
        """获取历史，期望 200，响应是列表结构"""
        response = http_client.get("/planet/history")
        assert_helper.assert_status_code(response, 200)
        assert_helper.assert_field_type(response, "history", list)

    @allure.story("历史记录")
    @allure.title("负向：不带 token → 401")
    @pytest.mark.negative
    @pytest.mark.planet
    def test_get_planet_history_no_token(self, anon_client):
        """不带 token，期望 401"""
        response = anon_client.get("/planet/history")
        assert_helper.assert_status_code(response, 401)


@allure.feature("星球模块")
class TestPlanetStats:

    @allure.story("统计数据")
    @allure.title("正向：获取星球统计信息")
    @pytest.mark.positive
    @pytest.mark.planet
    def test_get_planet_stats_success(self, http_client):
        """获取统计，期望 200，响应含 total_records / mood_count 等字段"""
        response = http_client.get("/planet/stats")
        assert_helper.assert_status_code(response, 200)
        assert_helper.assert_json_keys(response, ["total_records"])

    @allure.story("统计数据")
    @allure.title("负向：不带 token → 401")
    @pytest.mark.negative
    @pytest.mark.planet
    def test_get_planet_stats_no_token(self, anon_client):
        """不带 token，期望 401"""
        response = anon_client.get("/planet/stats")
        assert_helper.assert_status_code(response, 401)
