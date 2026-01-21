# 🌟 星迹 - 启动指南

## 第一步：安装必需软件

### 1. 安装 Node.js
- 访问：https://nodejs.org/
- 下载并安装 LTS 版本（18 或更高）
- 验证安装：
```powershell
node --version
npm --version
```

### 2. 安装 Python
- 访问：https://www.python.org/downloads/
- 下载并安装 Python 3.11 或更高版本
- ⚠️ 安装时勾选 "Add Python to PATH"
- 验证安装：
```powershell
python --version
pip --version
```

### 3. 安装 PostgreSQL
- 访问：https://www.postgresql.org/download/windows/
- 下载并安装
- 记住你设置的密码（默认用户名是 postgres）
- 验证安装：
```powershell
psql --version
```

### 4. 安装 Redis
- 访问：https://github.com/microsoftarchive/redis/releases
- 下载 Redis-x64-xxx.msi
- 安装并启动服务
- 或使用 WSL2：
```powershell
wsl --install
wsl
sudo apt install redis-server
redis-server
```

---

## 第二步：配置数据库

### 1. 创建数据库

打开 PowerShell 或命令提示符：

```powershell
# 连接到 PostgreSQL
psql -U postgres

# 在 psql 中执行（输入你的密码）
CREATE DATABASE stellar_journal;

# 退出
\q
```

---

## 第三步：配置项目

### 1. 配置后端

在 `backend` 目录下创建 `.env` 文件：

```powershell
cd backend
```

创建 `.env` 文件，内容如下：

```env
# 应用配置
APP_NAME=Stellar Journal
DEBUG=True
ENVIRONMENT=development

# 数据库配置（修改密码为你的实际密码）
DATABASE_URL=postgresql://postgres:你的密码@localhost:5432/stellar_journal

# Redis配置
REDIS_URL=redis://localhost:6379/0

# OpenAI API（必需！）
OPENAI_API_KEY=sk-你的OpenAI密钥

# 安全配置
SECRET_KEY=your-secret-key-here-change-in-production
```

⚠️ **重要**：你需要有一个 OpenAI API Key
- 访问：https://platform.openai.com/api-keys
- 登录并创建 API Key
- 复制并粘贴到 `.env` 文件中

### 2. 配置前端

在 `frontend` 目录下创建 `.env.local` 文件：

```powershell
cd ..\frontend
```

创建 `.env.local` 文件，内容如下：

```env
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
```

---

## 第四步：安装依赖

### 1. 安装后端依赖

```powershell
# 进入后端目录
cd ..\backend

# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
.\venv\Scripts\Activate

# 安装依赖
pip install -r requirements.txt
```

### 2. 初始化数据库

```powershell
# 确保在 backend 目录，并且虚拟环境已激活
alembic revision --autogenerate -m "Initial migration"
alembic upgrade head
```

### 3. 安装前端依赖

打开**新的** PowerShell 窗口：

```powershell
# 进入前端目录
cd frontend

# 安装依赖
npm install
```

---

## 第五步：启动项目 🚀

你需要打开 **3 个终端窗口**：

### 终端 1 - Redis（如果没有自动运行）

```powershell
redis-server
```

### 终端 2 - 后端服务

```powershell
cd backend
.\venv\Scripts\Activate
uvicorn app.main:app --reload
```

你应该看到：
```
INFO:     Uvicorn running on http://127.0.0.1:8000
```

### 终端 3 - 前端服务

```powershell
cd frontend
npm run dev
```

你应该看到：
```
▲ Next.js 14.x.x
- Local:        http://localhost:3000
```

---

## 第六步：访问应用 ✨

打开浏览器，访问：

- 🌟 **星迹应用**: http://localhost:3000
- 🔌 **API 服务**: http://localhost:8000
- 📚 **API 文档**: http://localhost:8000/docs

---

## 🎮 测试功能

### 1. 创建第一条心情记录

1. 打开 http://localhost:3000
2. 在底部输入框中，确保选中 "心情" 标签
3. 输入：`今天天气很好，心情不错！`
4. 点击发送按钮（或按 Enter）
5. 观察星球的颜色变化 ✨

### 2. 添加灵感

1. 切换到 "灵感" 标签
2. 输入：`做一个自动整理照片的工具`
3. 发送后，会在星球周围出现一颗星星 ⭐

### 3. 记录思考

1. 切换到 "思考" 标签
2. 输入：`关于时间管理的思考`
3. 发送后，会在星球表面生成一棵树 🌳

---

## ❓ 常见问题

### Q1: 后端启动失败 - 数据库连接错误

**解决方案：**
1. 检查 PostgreSQL 服务是否运行
2. 检查 `.env` 中的数据库密码是否正确
3. 确认数据库 `stellar_journal` 已创建

### Q2: 前端启动失败 - 依赖安装错误

**解决方案：**
```powershell
# 删除 node_modules 和 package-lock.json
rm -r node_modules
rm package-lock.json

# 重新安装
npm install
```

### Q3: OpenAI API 调用失败

**解决方案：**
1. 确认 API Key 正确
2. 检查 OpenAI 账户是否有额度
3. 检查网络连接

### Q4: Redis 连接失败

**解决方案：**
- Windows: 检查 Redis 服务是否运行
- 可以在任务管理器中查找 redis-server.exe

### Q5: 星球不显示

**解决方案：**
1. 打开浏览器开发者工具（F12）
2. 查看 Console 标签是否有错误
3. 确认后端 API 返回数据正常
4. 检查浏览器是否支持 WebGL

---

## 🎯 快速验证清单

在启动前，确保：

- [ ] Node.js 已安装 (`node --version`)
- [ ] Python 已安装 (`python --version`)
- [ ] PostgreSQL 已安装并运行
- [ ] Redis 已安装并运行
- [ ] 数据库 `stellar_journal` 已创建
- [ ] OpenAI API Key 已配置
- [ ] 后端 `.env` 文件已创建
- [ ] 前端 `.env.local` 文件已创建
- [ ] 后端依赖已安装
- [ ] 前端依赖已安装
- [ ] 数据库迁移已执行

---

## 🆘 需要帮助？

如果遇到问题：

1. **查看终端输出** - 错误信息会告诉你问题所在
2. **检查日志** - 后端和前端都有详细的错误日志
3. **查看文档** - `docs/` 目录有详细文档
4. **查看 API 文档** - http://localhost:8000/docs

---

## 🎉 启动成功！

如果一切正常，你应该能看到：

1. 一个浮动在宇宙中的 3D 星球 🌍
2. 底部有记录输入面板 📝
3. 右侧有时光轴面板 📅
4. 顶部有统计信息 📊

现在开始记录你的情感之旅吧！✨

---

**祝你使用愉快！🌟**
