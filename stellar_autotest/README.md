# Stellar-Journal 接口自动化测试框架

## 目录结构

```
stellar_autotest/
├── config/
│   └── config.yaml          # 环境配置（base_url、测试账号等）
├── tests/
│   ├── conftest.py          # pytest 全局 fixture（登录、测试数据）
│   ├── test_auth.py         # 认证模块用例
│   ├── test_records.py      # 记录模块用例
│   └── test_planet.py       # 星球模块用例
├── utils/
│   ├── config_manager.py    # 读取 config.yaml
│   ├── http_client.py       # 请求封装（Session + 重试 + Bearer token）
│   ├── assertion_helper.py  # 断言工具（状态码、字段、类型等）
│   └── logger.py            # 统一日志
├── reports/                 # 运行后自动生成（git 忽略）
├── logs/                    # 运行后自动生成（git 忽略）
├── pytest.ini               # pytest 配置
├── requirements.txt         # Python 依赖
└── run.ps1                  # 一键运行脚本（PowerShell）
```

## 前置条件

1. 后端服务已在本地启动（默认 `http://localhost:8000`）
2. `config/config.yaml` 里的 `test_user` 账号已在系统中注册
3. 已安装 Python 3.11+ 和 pip
4. 如需查看 Allure 报告，需安装 Allure CLI

## 安装依赖

```powershell
cd stellar_autotest
pip install -r requirements.txt
```

## 运行方式

```powershell
# 跑全部用例
./run.ps1

# 只跑冒烟用例
./run.ps1 -Mark smoke

# 只跑认证模块
./run.ps1 -Mark auth

# 跑完后自动生成并打开 Allure 报告
./run.ps1 -Report

# 直接用 pytest（在 stellar_autotest 目录下）
pytest
pytest -m smoke
pytest -m "auth and negative"
pytest tests/test_auth.py -v
```

## 用例标记说明

| 标记 | 含义 |
|---|---|
| `smoke` | 冒烟测试，覆盖核心主流程 |
| `regression` | 回归测试 |
| `positive` | 正向用例（合法输入） |
| `negative` | 负向用例（非法输入、无权限等） |
| `boundary` | 边界用例（超长、空值等极限情况） |
| `auth` | 认证模块 |
| `records` | 记录模块 |
| `planet` | 星球模块 |
