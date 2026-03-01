# -*- coding: utf-8 -*-
"""
记录模块接口用例
覆盖：创建记录（mood / spark / thought）/ 查询列表 / 查询单条 / 删除
"""
import pytest
import allure

from utils.assertion_helper import assert_helper


@allure.feature("记录模块")
class TestCreateRecord:

    @allure.story("创建记录")
    @allure.title("正向：创建 mood 记录成功")
    @pytest.mark.smoke
    @pytest.mark.positive
    @pytest.mark.records
    def test_create_mood_success(self, http_client, mood_payload):
        """创建心情记录，期望 201，响应包含 id / type / color_hex"""
        response = http_client.post("/records/", json_data=mood_payload)
        assert_helper.assert_status_code(response, 201)
        assert_helper.assert_json_keys(response, ["id", "type", "content", "color_hex"])
        assert_helper.assert_json_value(response, "type", "mood")
        assert_helper.assert_json_not_none(response, "color_hex")
        assert_helper.assert_response_time(response, 10.0)  # AI 分析可能稍慢

    @allure.story("创建记录")
    @allure.title("正向：创建 spark 记录成功")
    @pytest.mark.positive
    @pytest.mark.records
    def test_create_spark_success(self, http_client, spark_payload):
        """创建灵感记录，期望 201，响应包含 keywords"""
        response = http_client.post("/records/", json_data=spark_payload)
        assert_helper.assert_status_code(response, 201)
        assert_helper.assert_json_keys(response, ["id", "type", "keywords"])
        assert_helper.assert_json_value(response, "type", "spark")

    @allure.story("创建记录")
    @allure.title("正向：创建 thought 记录成功")
    @pytest.mark.positive
    @pytest.mark.records
    def test_create_thought_success(self, http_client, thought_payload):
        """创建思考记录，期望 201，响应包含 position_data"""
        response = http_client.post("/records/", json_data=thought_payload)
        assert_helper.assert_status_code(response, 201)
        assert_helper.assert_json_keys(response, ["id", "type", "position_data"])
        assert_helper.assert_json_value(response, "type", "thought")

    @allure.story("创建记录")
    @allure.title("负向：不带 token → 401")
    @pytest.mark.negative
    @pytest.mark.records
    def test_create_record_no_token(self, anon_client, mood_payload):
        """不带 token 创建记录，期望 401"""
        response = anon_client.post("/records/", json_data=mood_payload)
        assert_helper.assert_status_code(response, 401)

    @allure.story("创建记录")
    @allure.title("负向：type 非法 → 422")
    @pytest.mark.negative
    @pytest.mark.records
    def test_create_record_invalid_type(self, http_client, invalid_payloads):
        """传入非法 type，期望 422"""
        response = http_client.post("/records/", json_data=invalid_payloads["invalid_type"])
        assert_helper.assert_status_code(response, 422)

    @allure.story("创建记录")
    @allure.title("负向：缺少 content → 422")
    @pytest.mark.negative
    @pytest.mark.records
    def test_create_record_missing_content(self, http_client, invalid_payloads):
        """缺少 content 字段，期望 422"""
        response = http_client.post("/records/", json_data=invalid_payloads["missing_content"])
        assert_helper.assert_status_code(response, 422)

    @allure.story("创建记录")
    @allure.title("边界：content 超长（5001字符）→ 422")
    @pytest.mark.boundary
    @pytest.mark.records
    def test_create_record_too_long_content(self, http_client, invalid_payloads):
        """content 超过 5000 字符，期望 422"""
        response = http_client.post("/records/", json_data=invalid_payloads["too_long_content"])
        assert_helper.assert_status_code(response, 422)


@allure.feature("记录模块")
class TestListRecords:

    @allure.story("查询记录列表")
    @allure.title("正向：查询当天记录列表")
    @pytest.mark.smoke
    @pytest.mark.positive
    @pytest.mark.records
    def test_list_records_success(self, http_client):
        """查询记录列表，期望 200，响应包含 records 字段"""
        response = http_client.get("/records/")
        assert_helper.assert_status_code(response, 200)
        assert_helper.assert_json_keys(response, ["records"])
        assert_helper.assert_field_type(response, "records", list)

    @allure.story("查询记录列表")
    @allure.title("负向：不带 token → 401")
    @pytest.mark.negative
    @pytest.mark.records
    def test_list_records_no_token(self, anon_client):
        """不带 token 查询列表，期望 401"""
        response = anon_client.get("/records/")
        assert_helper.assert_status_code(response, 401)


@allure.feature("记录模块")
class TestGetAndDeleteRecord:

    @allure.story("查询单条 / 删除")
    @allure.title("正向：创建后立即查询单条")
    @pytest.mark.positive
    @pytest.mark.records
    def test_get_single_record(self, http_client, mood_payload):
        """先创建一条记录，再用返回的 id 查询，期望 200"""
        create_resp = http_client.post("/records/", json_data=mood_payload)
        assert_helper.assert_status_code(create_resp, 201)
        record_id = create_resp.json()["id"]

        get_resp = http_client.get(f"/records/{record_id}")
        assert_helper.assert_status_code(get_resp, 200)
        assert_helper.assert_json_value(get_resp, "id", record_id)

    @allure.story("查询单条 / 删除")
    @allure.title("负向：查询不存在的记录 → 404")
    @pytest.mark.negative
    @pytest.mark.records
    def test_get_nonexistent_record(self, http_client):
        """查询一个不存在的 id，期望 404"""
        response = http_client.get("/records/99999999")
        assert_helper.assert_status_code(response, 404)

    @allure.story("查询单条 / 删除")
    @allure.title("正向：创建后删除，再查询 → 404")
    @pytest.mark.positive
    @pytest.mark.records
    def test_delete_record(self, http_client, spark_payload):
        """先创建，再删除，再查同一 id 期望 404"""
        create_resp = http_client.post("/records/", json_data=spark_payload)
        assert_helper.assert_status_code(create_resp, 201)
        record_id = create_resp.json()["id"]

        del_resp = http_client.delete(f"/records/{record_id}")
        assert_helper.assert_status_code(del_resp, 200)

        get_resp = http_client.get(f"/records/{record_id}")
        assert_helper.assert_status_code(get_resp, 404)
