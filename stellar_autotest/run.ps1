# Stellar-Journal 接口自动化运行脚本（PowerShell）
# 用法：
#   ./run.ps1                   # 跑全部用例
#   ./run.ps1 -Mark smoke       # 只跑冒烟用例
#   ./run.ps1 -Mark auth        # 只跑认证模块
#   ./run.ps1 -Report           # 跑完后自动打开 Allure 报告

param(
    [string]$Mark = "",
    [switch]$Report
)

Set-Location $PSScriptRoot

# 检查依赖
Write-Host ">>> 检查依赖..." -ForegroundColor Cyan
pip install -r requirements.txt -q

# 构建 pytest 命令
$cmd = "pytest"
if ($Mark -ne "") {
    $cmd += " -m $Mark"
    Write-Host ">>> 仅运行标记: $Mark" -ForegroundColor Yellow
} else {
    Write-Host ">>> 运行全部用例" -ForegroundColor Yellow
}

# 执行测试
Write-Host ">>> 开始执行..." -ForegroundColor Cyan
Invoke-Expression $cmd
$exitCode = $LASTEXITCODE

# 生成 Allure 报告
if ($Report) {
    Write-Host ">>> 生成 Allure 报告..." -ForegroundColor Cyan
    allure generate reports/allure-results -o reports/allure-report --clean
    Write-Host ">>> 打开 Allure 报告..." -ForegroundColor Cyan
    allure open reports/allure-report
}

exit $exitCode
