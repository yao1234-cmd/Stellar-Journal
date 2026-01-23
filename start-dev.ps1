# 星迹开发环境启动脚本 (Windows PowerShell)

Write-Host "🌟 启动星迹开发环境..." -ForegroundColor Cyan

# 检查 Node.js
Write-Host "`n检查 Node.js..." -ForegroundColor Yellow
if (Get-Command node -ErrorAction SilentlyContinue) {
    $nodeVersion = node --version
    Write-Host "✓ Node.js $nodeVersion" -ForegroundColor Green
} else {
    Write-Host "✗ 未找到 Node.js，请先安装 Node.js 18+" -ForegroundColor Red
    exit 1
}

# 检查 Python
Write-Host "`n检查 Python..." -ForegroundColor Yellow
if (Get-Command python -ErrorAction SilentlyContinue) {
    $pythonVersion = python --version
    Write-Host "✓ $pythonVersion" -ForegroundColor Green
} else {
    Write-Host "✗ 未找到 Python，请先安装 Python 3.11+" -ForegroundColor Red
    exit 1
}

# 检查 PostgreSQL
Write-Host "`n检查 PostgreSQL..." -ForegroundColor Yellow
if (Get-Service -Name postgresql* -ErrorAction SilentlyContinue) {
    Write-Host "✓ PostgreSQL 服务已安装" -ForegroundColor Green
} else {
    Write-Host "⚠ 未找到 PostgreSQL 服务" -ForegroundColor Yellow
    Write-Host "请确保 PostgreSQL 已安装并运行" -ForegroundColor Yellow
}

# 检查 Redis
Write-Host "`n检查 Redis..." -ForegroundColor Yellow
if (Get-Process redis-server -ErrorAction SilentlyContinue) {
    Write-Host "✓ Redis 正在运行" -ForegroundColor Green
} else {
    Write-Host "⚠ Redis 未运行，尝试启动..." -ForegroundColor Yellow
    Start-Process redis-server -WindowStyle Hidden -ErrorAction SilentlyContinue
    Start-Sleep -Seconds 2
    if (Get-Process redis-server -ErrorAction SilentlyContinue) {
        Write-Host "✓ Redis 已启动" -ForegroundColor Green
    } else {
        Write-Host "⚠ 无法启动 Redis，请手动启动" -ForegroundColor Yellow
    }
}

# 启动后端
Write-Host "`n🔧 启动后端服务..." -ForegroundColor Cyan
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd backend; if (Test-Path venv) { .\venv\Scripts\Activate.ps1 } else { python -m venv venv; .\venv\Scripts\Activate.ps1; pip install -r requirements.txt }; Write-Host '🚀 启动 FastAPI...' -ForegroundColor Green; uvicorn app.main:app --reload"

Start-Sleep -Seconds 3

# 启动前端
Write-Host "`n💻 启动前端服务..." -ForegroundColor Cyan
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd frontend; if (!(Test-Path node_modules)) { Write-Host '📦 安装依赖...' -ForegroundColor Yellow; npm install }; Write-Host '🚀 启动 Next.js...' -ForegroundColor Green; npm run dev"

Write-Host "`n✨ 开发环境启动完成！" -ForegroundColor Green
Write-Host "`n📱 前端: http://localhost:3000" -ForegroundColor Cyan
Write-Host "🔌 后端: http://localhost:8000" -ForegroundColor Cyan
Write-Host "📚 API 文档: http://localhost:8000/docs" -ForegroundColor Cyan
Write-Host "`n按 Ctrl+C 停止服务" -ForegroundColor Yellow
