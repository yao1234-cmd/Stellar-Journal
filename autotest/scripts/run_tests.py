# -*- coding: utf-8 -*-
"""
测试运行脚本 - 运行测试并生成报告
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path
from datetime import datetime

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from utils.logger import logger
from utils.config_manager import config


def setup_directories():
    """创建必要的目录"""
    directories = [
        project_root / "reports",
        project_root / "reports" / "allure-results",
        project_root / "reports" / "allure-report",
        project_root / "logs"
    ]
    
    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)
        logger.info(f"创建目录: {directory}")


def clean_old_reports():
    """清理旧的测试报告"""
    try:
        allure_results_dir = project_root / "reports" / "allure-results"
        if allure_results_dir.exists():
            shutil.rmtree(allure_results_dir)
            allure_results_dir.mkdir()
            logger.info("清理旧的Allure结果文件")
        
        html_report = project_root / "reports" / "report.html"
        if html_report.exists():
            html_report.unlink()
            logger.info("清理旧的HTML报告文件")
            
    except Exception as e:
        logger.warning(f"清理旧报告文件失败: {e}")


def run_pytest(test_markers=None, test_path=None):
    """
    运行pytest测试
    
    Args:
        test_markers: 测试标记，如 'smoke' 或 'smoke and positive'
        test_path: 测试路径，如 'tests/test_medicine_api.py'
    """
    cmd = ["python", "-m", "pytest"]
    
    # 添加测试路径
    if test_path:
        cmd.append(test_path)
    else:
        cmd.append("tests/")
    
    # 添加标记筛选
    if test_markers:
        cmd.extend(["-m", test_markers])
    
    # 添加其他参数
    cmd.extend([
        "--alluredir=reports/allure-results",
        "--html=reports/report.html",
        "--self-contained-html",
        "-v",
        "--tb=short",
        "--strict-markers"
    ])
    
    logger.info(f"执行命令: {' '.join(cmd)}")
    
    try:
        # 切换到项目根目录
        os.chdir(project_root)
        
        # 运行pytest
        result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8')
        
        # 输出结果
        if result.stdout:
            print("STDOUT:")
            print(result.stdout)
        
        if result.stderr:
            print("STDERR:")
            print(result.stderr)
        
        logger.info(f"pytest执行完成，退出码: {result.returncode}")
        return result.returncode == 0
        
    except Exception as e:
        logger.error(f"运行pytest失败: {e}")
        return False


def generate_allure_report():
    """生成Allure报告"""
    try:
        # 检查是否安装了allure
        allure_check = subprocess.run(["allure", "--version"], capture_output=True)
        if allure_check.returncode != 0:
            logger.warning("Allure命令行工具未安装，跳过Allure报告生成")
            logger.info("安装方法: brew install allure (macOS) 或访问 https://docs.qameta.io/allure/")
            return False
        
        # 生成Allure报告
        cmd = [
            "allure", "generate", 
            "reports/allure-results", 
            "-o", "reports/allure-report", 
            "--clean"
        ]
        
        logger.info(f"生成Allure报告: {' '.join(cmd)}")
        
        result = subprocess.run(cmd, capture_output=True, text=True, cwd=project_root)
        
        if result.returncode == 0:
            logger.info("Allure报告生成成功")
            logger.info(f"报告路径: {project_root}/reports/allure-report/index.html")
            return True
        else:
            logger.error(f"Allure报告生成失败: {result.stderr}")
            return False
            
    except Exception as e:
        logger.error(f"生成Allure报告异常: {e}")
        return False


def open_allure_report():
    """打开Allure报告"""
    try:
        # 启动Allure服务器
        cmd = ["allure", "serve", "reports/allure-results"]
        
        logger.info("启动Allure报告服务器...")
        logger.info("报告将在浏览器中自动打开")
        logger.info("按 Ctrl+C 停止服务器")
        
        subprocess.run(cmd, cwd=project_root)
        
    except KeyboardInterrupt:
        logger.info("Allure服务器已停止")
    except Exception as e:
        logger.error(f"启动Allure服务器失败: {e}")


def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description="运行自动化测试")
    parser.add_argument("-m", "--markers", help="测试标记筛选，如: smoke, regression, 'smoke and positive'")
    parser.add_argument("-t", "--test", help="指定测试文件或目录")
    parser.add_argument("--clean", action="store_true", help="清理旧的测试报告")
    parser.add_argument("--no-report", action="store_true", help="不生成Allure报告")
    parser.add_argument("--serve", action="store_true", help="生成报告后启动Allure服务器")
    
    args = parser.parse_args()
    
    print("=" * 60)
    print("🚀 云医疗系统自动化测试框架")
    print("=" * 60)
    
    # 设置目录
    setup_directories()
    
    # 清理旧报告
    if args.clean:
        clean_old_reports()
    
    # 运行测试
    logger.info("开始运行测试...")
    start_time = datetime.now()
    
    success = run_pytest(test_markers=args.markers, test_path=args.test)
    
    end_time = datetime.now()
    duration = end_time - start_time
    
    print(f"\n测试执行完成！")
    print(f"执行时间: {duration}")
    print(f"测试结果: {'✅ 成功' if success else '❌ 失败'}")
    
    # 生成报告
    if not args.no_report:
        logger.info("生成测试报告...")
        
        # HTML报告
        html_report_path = project_root / "reports" / "report.html"
        if html_report_path.exists():
            print(f"📊 HTML报告: {html_report_path}")
        
        # Allure报告
        if generate_allure_report():
            allure_report_path = project_root / "reports" / "allure-report" / "index.html"
            print(f"📈 Allure报告: {allure_report_path}")
            
            if args.serve:
                open_allure_report()
        else:
            print("⚠️  Allure报告生成失败，请检查Allure是否正确安装")
    
    print("\n" + "=" * 60)
    print("✨ 测试执行完成!")
    print("=" * 60)


if __name__ == "__main__":
    main()