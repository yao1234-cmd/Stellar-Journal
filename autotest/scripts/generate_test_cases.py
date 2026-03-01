# -*- coding: utf-8 -*-
"""
测试用例生成脚本 - 自动生成测试用例
"""

import os
import sys
import json
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from utils.api_parser import APIParser
from utils.logger import logger


def generate_test_cases():
    """生成测试用例"""
    logger.info("开始生成测试用例...")
    
    # 获取main.py文件路径
    main_file_path = project_root.parent / "main.py"
    
    if not main_file_path.exists():
        logger.error(f"主文件不存在: {main_file_path}")
        return
    
    # 解析API接口
    parser = APIParser(str(main_file_path))
    apis = parser.parse_fastapi_routes()
    
    if not apis:
        logger.error("未找到API接口")
        return
    
    # 按模块分组
    modules = parser.get_all_modules()
    logger.info(f"发现模块: {modules}")
    
    # 生成测试场景
    all_scenarios = []
    for api in apis:
        scenarios = parser.generate_test_scenarios(api)
        all_scenarios.extend(scenarios)
    
    # 保存到JSON文件
    output_file = project_root / "generated_test_scenarios.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump({
            'total_apis': len(apis),
            'total_scenarios': len(all_scenarios),
            'modules': modules,
            'apis': apis,
            'scenarios': all_scenarios
        }, f, ensure_ascii=False, indent=2)
    
    logger.info(f"测试用例生成完成!")
    logger.info(f"总计API: {len(apis)}个")
    logger.info(f"总计测试场景: {len(all_scenarios)}个")
    logger.info(f"结果保存到: {output_file}")
    
    # 打印统计信息
    print("\n=== API接口统计 ===")
    for module in modules:
        module_apis = parser.get_apis_by_module(module) 
        print(f"{module}: {len(module_apis)}个接口")
    
    print(f"\n=== 测试场景统计 ===")
    scenario_types = {}
    for scenario in all_scenarios:
        scenario_type = scenario['type']
        scenario_types[scenario_type] = scenario_types.get(scenario_type, 0) + 1
    
    for scenario_type, count in scenario_types.items():
        print(f"{scenario_type}: {count}个场景")


if __name__ == "__main__":
    generate_test_cases()