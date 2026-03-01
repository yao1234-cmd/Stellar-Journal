# -*- coding: utf-8 -*-
"""
依赖安装脚本 - 安装测试框架所需的依赖
"""

import subprocess
import sys
import os
from pathlib import Path


def run_command(cmd, description):
    """执行命令"""
    print(f"\n🔄 {description}...")
    try:
        result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description}成功")
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description}失败")
        print(f"错误信息: {e.stderr}")
        return False


def install_python_dependencies():
    """安装Python依赖"""
    project_root = Path(__file__).parent.parent
    requirements_file = project_root / "requirements.txt"
    
    if not requirements_file.exists():
        print(f"❌ requirements.txt文件不存在: {requirements_file}")
        return False
    
    cmd = f"{sys.executable} -m pip install -r {requirements_file}"
    return run_command(cmd, "安装Python依赖")


def install_allure():
    """安装Allure命令行工具"""
    print("\n📋 检查Allure安装状态...")
    
    # 检查是否已安装
    try:
        result = subprocess.run(["allure", "--version"], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Allure已安装: {result.stdout.strip()}")
            return True
    except FileNotFoundError:
        pass
    
    print("⚠️  Allure未安装，需要手动安装")
    
    # 根据操作系统提供安装指导
    import platform
    system = platform.system().lower()
    
    if system == "darwin":  # macOS
        print("\n🍎 macOS安装方法:")
        print("1. 使用Homebrew: brew install allure")
        print("2. 或下载安装包: https://github.com/allure-framework/allure2/releases")
    elif system == "linux":
        print("\n🐧 Linux安装方法:")
        print("1. 下载并解压: https://github.com/allure-framework/allure2/releases")
        print("2. 添加到PATH环境变量")
        print("3. 或使用包管理器安装")
    elif system == "windows":
        print("\n🪟 Windows安装方法:")
        print("1. 使用Scoop: scoop install allure")
        print("2. 或下载安装包: https://github.com/allure-framework/allure2/releases")
    else:
        print(f"\n❓ 未知操作系统: {system}")
        print("请访问 https://docs.qameta.io/allure/ 获取安装指导")
    
    print("\n安装完成后，请重新运行此脚本验证")
    return False


def check_python_version():
    """检查Python版本"""
    version = sys.version_info
    print(f"🐍 Python版本: {version.major}.{version.minor}.{version.micro}")
    
    if version.major < 3 or (version.major == 3 and version.minor < 7):
        print("❌ Python版本过低，需要Python 3.7+")
        return False
    
    print("✅ Python版本符合要求")
    return True


def create_directories():
    """创建必要的目录"""
    project_root = Path(__file__).parent.parent
    directories = [
        project_root / "reports",
        project_root / "reports" / "allure-results", 
        project_root / "reports" / "allure-report",
        project_root / "logs"
    ]
    
    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)
        print(f"📁 创建目录: {directory}")
    
    return True


def main():
    """主函数"""
    print("=" * 60)
    print("🛠️  自动化测试框架环境安装")
    print("=" * 60)
    
    success = True
    
    # 检查Python版本
    if not check_python_version():
        success = False
    
    # 创建目录
    if not create_directories():
        success = False
    
    # 安装Python依赖
    if not install_python_dependencies():
        success = False
    
    # 安装Allure
    if not install_allure():
        print("⚠️  Allure未安装，部分功能可能受限")
    
    print("\n" + "=" * 60)
    if success:
        print("✅ 环境安装完成!")
    else:
        print("⚠️  环境安装部分失败，请检查错误信息")
    
    print("\n📚 使用说明:")
    print("1. 运行所有测试: python scripts/run_tests.py")
    print("2. 运行冒烟测试: python scripts/run_tests.py -m smoke")
    print("3. 运行指定模块: python scripts/run_tests.py -t tests/test_medicine_api.py")
    print("4. 生成测试用例: python scripts/generate_test_cases.py")
    print("=" * 60)


if __name__ == "__main__":
    main()