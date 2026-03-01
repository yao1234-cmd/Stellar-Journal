# -*- coding: utf-8 -*-
"""
预约管理API测试用例
"""

import pytest
import allure
from utils.http_client import HTTPClient
from utils.assertion_helper import assert_helper


@allure.epic("云医疗系统")
@allure.feature("预约管理")
class TestAppointmentAPI:
    """预约管理API测试类"""
    
    @allure.story("获取预约列表")
    @allure.title("获取预约列表 - 正常场景")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    @pytest.mark.positive
    def test_get_appointments_success(self, http_client: HTTPClient):
        """测试获取预约列表的正常功能"""
        with allure.step("发送获取预约列表请求"):
            response = http_client.get("/api/appointments")
        
        with allure.step("验证响应"):
            assert_helper.assert_status_code(response, 200)
            assert_helper.assert_response_time(response, 5.0)
            assert_helper.assert_json_structure(response, ['code', 'data', 'total'])
            assert_helper.assert_json_value(response, 'code', 0)
    
    @allure.story("获取预约列表")
    @allure.title("按状态筛选预约")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    @pytest.mark.positive
    @pytest.mark.parametrize("status", ["待确认", "已确认", "已完成", "已取消"])
    def test_get_appointments_by_status(self, http_client: HTTPClient, status):
        """测试按状态筛选预约"""
        with allure.step(f"发送按状态'{status}'筛选的请求"):
            response = http_client.get("/api/appointments", params={"status": status})
        
        with allure.step("验证响应"):
            assert_helper.assert_status_code(response, 200)
            assert_helper.assert_json_structure(response, ['code', 'data', 'total'])
            assert_helper.assert_json_value(response, 'code', 0)
            
            # 验证返回的预约状态正确
            json_data = response.json()
            appointments = json_data['data']
            
            for appointment in appointments:
                assert appointment.get('status') == status, f"预约状态应为{status}"
    
    @allure.story("获取预约列表")
    @allure.title("按日期筛选预约")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    @pytest.mark.positive
    def test_get_appointments_by_date(self, http_client: HTTPClient):
        """测试按日期筛选预约"""
        test_date = "2024-01-15"
        
        with allure.step(f"发送按日期'{test_date}'筛选的请求"):
            response = http_client.get("/api/appointments", params={"date": test_date})
        
        with allure.step("验证响应"):
            assert_helper.assert_status_code(response, 200)
            assert_helper.assert_json_structure(response, ['code', 'data', 'total'])
            assert_helper.assert_json_value(response, 'code', 0)
            
            # 验证返回的预约日期正确
            json_data = response.json()
            appointments = json_data['data']
            
            for appointment in appointments:
                assert appointment.get('appointment_date') == test_date, f"预约日期应为{test_date}"
    
    @allure.story("获取预约列表")
    @allure.title("按科室筛选预约")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    @pytest.mark.positive
    @pytest.mark.parametrize("department", ["内科", "外科", "儿科", "妇产科", "眼科"])
    def test_get_appointments_by_department(self, http_client: HTTPClient, department):
        """测试按科室筛选预约"""
        with allure.step(f"发送按科室'{department}'筛选的请求"):
            response = http_client.get("/api/appointments", params={"department": department})
        
        with allure.step("验证响应"):
            assert_helper.assert_status_code(response, 200)
            assert_helper.assert_json_structure(response, ['code', 'data', 'total'])
            assert_helper.assert_json_value(response, 'code', 0)
            
            # 验证返回的预约科室正确
            json_data = response.json()
            appointments = json_data['data']
            
            for appointment in appointments:
                assert appointment.get('department') == department, f"预约科室应为{department}"
    
    @allure.story("获取预约详情")
    @allure.title("获取预约详情 - 正常场景")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.smoke
    @pytest.mark.positive
    def test_get_appointment_detail_success(self, http_client: HTTPClient):
        """测试获取预约详情的正常功能"""
        appointment_id = 1
        
        with allure.step(f"发送获取预约详情请求 (ID: {appointment_id})"):
            response = http_client.get(f"/api/appointments/{appointment_id}")
        
        with allure.step("验证响应"):
            # 可能返回404（记录不存在）或200（记录存在）
            if response.status_code == 200:
                assert_helper.assert_json_structure(response, ['code', 'data'])
                assert_helper.assert_json_value(response, 'code', 0)
                
                # 验证预约记录字段
                json_data = response.json()
                appointment = json_data['data']
                expected_fields = ['id', 'patient_name', 'doctor_name', 'department', 'status']
                
                for field in expected_fields:
                    assert field in appointment, f"预约记录应包含{field}字段"
            elif response.status_code == 404:
                assert_helper.assert_json_structure(response, ['detail'])
            else:
                pytest.fail(f"意外的状态码: {response.status_code}")
    
    @allure.story("获取预约详情")
    @allure.title("获取不存在的预约详情")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.negative
    def test_get_appointment_detail_not_found(self, http_client: HTTPClient):
        """测试获取不存在的预约详情"""
        non_existent_id = 99999
        
        with allure.step(f"发送获取不存在预约详情请求 (ID: {non_existent_id})"):
            response = http_client.get(f"/api/appointments/{non_existent_id}")
        
        with allure.step("验证响应"):
            assert_helper.assert_status_code(response, 404)
            assert_helper.assert_json_structure(response, ['detail'])
    
    @allure.story("更新预约状态")
    @allure.title("更新预约状态 - 正常场景")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    @pytest.mark.positive
    @pytest.mark.parametrize("new_status", ["待确认", "已确认", "已完成", "已取消"])
    def test_update_appointment_status_success(self, http_client: HTTPClient, new_status):
        """测试更新预约状态的正常功能"""
        appointment_id = 1
        
        with allure.step(f"发送更新预约状态请求 (ID: {appointment_id}, 状态: {new_status})"):
            response = http_client.put(
                f"/api/appointments/{appointment_id}/status",
                params={"status": new_status}
            )
        
        with allure.step("验证响应"):
            # 可能返回404（记录不存在）或200（更新成功）
            if response.status_code == 200:
                assert_helper.assert_json_structure(response, ['code', 'message'])
                assert_helper.assert_json_value(response, 'code', 0)
                assert_helper.assert_json_contains(response, 'message', '成功')
            elif response.status_code == 404:
                assert_helper.assert_json_structure(response, ['detail'])
            else:
                pytest.fail(f"意外的状态码: {response.status_code}")
    
    @allure.story("获取预约统计")
    @allure.title("获取预约统计数据 - 正常场景")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    @pytest.mark.positive
    def test_get_appointment_stats_success(self, http_client: HTTPClient):
        """测试获取预约统计数据的正常功能"""
        with allure.step("发送获取预约统计请求"):
            response = http_client.get("/api/appointments/stats/summary")
        
        with allure.step("验证响应"):
            assert_helper.assert_status_code(response, 200)
            assert_helper.assert_response_time(response, 5.0)
            assert_helper.assert_json_structure(response, ['code', 'data'])
            assert_helper.assert_json_value(response, 'code', 0)
            
            # 验证统计数据结构
            expected_stats_keys = [
                'total_appointments',
                'today_appointments',
                'pending_appointments',
                'confirmed_appointments',
                'department_stats'
            ]
            
            json_data = response.json()
            stats_data = json_data['data']
            
            for key in expected_stats_keys:
                assert key in stats_data, f"统计数据缺少字段: {key}"
    
    @allure.story("获取预约统计")
    @allure.title("验证预约统计数据类型")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    @pytest.mark.positive
    def test_appointment_stats_data_types(self, http_client: HTTPClient):
        """测试预约统计数据的数据类型"""
        with allure.step("发送获取预约统计请求"):
            response = http_client.get("/api/appointments/stats/summary")
        
        with allure.step("验证数据类型"):
            assert_helper.assert_status_code(response, 200)
            
            json_data = response.json()
            stats_data = json_data['data']
            
            # 验证数值类型字段
            numeric_fields = [
                'total_appointments',
                'today_appointments',
                'pending_appointments',
                'confirmed_appointments'
            ]
            
            for field in numeric_fields:
                assert isinstance(stats_data[field], int), f"{field} 应该是整数类型"
                assert stats_data[field] >= 0, f"{field} 应该是非负数"
            
            # 验证科室统计数组
            department_stats = stats_data['department_stats']
            assert isinstance(department_stats, list), "department_stats 应该是数组类型"
    
    @allure.story("数据验证")
    @allure.title("预约记录数据结构验证")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    @pytest.mark.positive
    def test_appointment_data_structure(self, http_client: HTTPClient):
        """测试预约记录数据结构的完整性"""
        with allure.step("发送获取预约列表请求"):
            response = http_client.get("/api/appointments")
        
        with allure.step("验证数据结构"):
            assert_helper.assert_status_code(response, 200)
            
            json_data = response.json()
            appointments = json_data['data']
            
            # 如果有预约记录，验证数据结构
            if len(appointments) > 0:
                appointment = appointments[0]
                expected_fields = [
                    'id', 'patient_id', 'patient_name', 'doctor_id', 'doctor_name',
                    'department', 'appointment_date', 'appointment_time', 'reason',
                    'status', 'notes'
                ]
                
                for field in expected_fields:
                    if field in appointment:
                        # 验证字段类型
                        if field in ['id', 'patient_id', 'doctor_id']:
                            assert isinstance(appointment[field], int), f"{field}应为整数类型"
                        elif field in ['patient_name', 'doctor_name', 'department', 'status']:
                            assert isinstance(appointment[field], str), f"{field}应为字符串类型"
                        
                        # 验证日期格式
                        if field == 'appointment_date' and appointment[field]:
                            import re
                            date_pattern = r'^\d{4}-\d{2}-\d{2}$'
                            assert re.match(date_pattern, appointment[field]), f"日期格式错误: {appointment[field]}"
                        
                        # 验证时间格式
                        if field == 'appointment_time' and appointment[field]:
                            import re
                            time_pattern = r'^\d{2}:\d{2}$'
                            assert re.match(time_pattern, appointment[field]), f"时间格式错误: {appointment[field]}"
    
    @allure.story("组合筛选")
    @allure.title("预约列表 - 多条件筛选")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.positive
    def test_get_appointments_multiple_filters(self, http_client: HTTPClient):
        """测试同时使用多个条件筛选预约"""
        params = {
            "status": "已确认",
            "department": "内科",
            "date": "2024-01-15"
        }
        
        with allure.step("发送多条件筛选请求"):
            response = http_client.get("/api/appointments", params=params)
        
        with allure.step("验证响应"):
            assert_helper.assert_status_code(response, 200)
            assert_helper.assert_json_structure(response, ['code', 'data', 'total'])
            assert_helper.assert_json_value(response, 'code', 0)
            
            # 验证返回的预约同时满足所有条件
            json_data = response.json()
            appointments = json_data['data']
            
            for appointment in appointments:
                assert appointment.get('status') == params['status'], f"状态应为{params['status']}"
                assert appointment.get('department') == params['department'], f"科室应为{params['department']}"
                assert appointment.get('appointment_date') == params['date'], f"日期应为{params['date']}"
    
    @allure.story("性能测试")
    @allure.title("获取预约列表 - 响应时间测试")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.performance
    def test_get_appointments_performance(self, http_client: HTTPClient):
        """测试获取预约列表的性能"""
        with allure.step("发送性能测试请求"):
            response = http_client.get("/api/appointments")
        
        with allure.step("验证响应时间"):
            assert_helper.assert_status_code(response, 200)
            assert_helper.assert_response_time(response, 3.0)  # 要求3秒内响应
            
            # 记录实际响应时间
            actual_time = response.elapsed.total_seconds()
            allure.attach(
                f"{actual_time:.3f}秒",
                name="实际响应时间",
                attachment_type=allure.attachment_type.TEXT
            )
    
    @allure.story("边界测试")
    @allure.title("预约列表 - 未来日期筛选")
    @allure.severity(allure.severity_level.MINOR)
    @pytest.mark.boundary
    def test_get_appointments_future_date(self, http_client: HTTPClient):
        """测试筛选未来日期的预约"""
        from datetime import datetime, timedelta
        
        future_date = (datetime.now() + timedelta(days=30)).strftime('%Y-%m-%d')
        
        with allure.step(f"发送未来日期'{future_date}'筛选请求"):
            response = http_client.get("/api/appointments", params={"date": future_date})
        
        with allure.step("验证响应"):
            assert_helper.assert_status_code(response, 200)
            assert_helper.assert_json_structure(response, ['code', 'data', 'total'])
            assert_helper.assert_json_value(response, 'code', 0)
    
    @allure.story("排序验证")
    @allure.title("预约列表排序验证")
    @allure.severity(allure.severity_level.MINOR)
    @pytest.mark.positive
    def test_appointments_list_sorting(self, http_client: HTTPClient):
        """测试预约列表的排序功能"""
        with allure.step("发送获取预约列表请求"):
            response = http_client.get("/api/appointments")
        
        with allure.step("验证排序"):
            assert_helper.assert_status_code(response, 200)
            
            json_data = response.json()
            appointments = json_data['data']
            
            # 验证按日期和时间倒序排序（根据API文档）
            if len(appointments) > 1:
                # 检查日期排序
                dates = [appointment.get('appointment_date', '') for appointment in appointments]
                # 过滤掉空值后检查排序
                valid_dates = [date for date in dates if date]
                if len(valid_dates) > 1:
                    assert valid_dates == sorted(valid_dates, reverse=True), "预约列表应按日期倒序排列"