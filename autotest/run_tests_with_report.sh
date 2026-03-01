#!/bin/bash

echo "========================================"
echo "冰酱云医疗管理系统 - 自动化测试执行"
echo "========================================"

# 进入项目目录
cd "$(dirname "$0")"

echo "1. 清理旧的测试结果..."
rm -rf ./reports/allure-results/*
rm -rf ./reports/allure-report/*

echo "2. 运行自动化测试用例..."
python3 -m pytest tests/ --alluredir=./reports/allure-results --clean-alluredir

# 检查测试执行结果
if [ $? -eq 0 ]; then
    echo "✅ 测试执行成功！"
    
    echo "3. 生成Allure测试报告..."
    allure generate ./reports/allure-results -o ./reports/allure-report --clean
    
    if [ $? -eq 0 ]; then
        echo "✅ 报告生成成功！"
        
        echo "4. 启动Allure服务..."
        echo "🚀 正在启动Allure服务，请在浏览器中查看测试报告..."
        allure serve ./reports/allure-results
    else
        echo "❌ 报告生成失败！"
        exit 1
    fi
else
    echo "❌ 测试执行失败！"
    exit 1
fi