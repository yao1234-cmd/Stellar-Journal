# 快速开始 🚀

## 一键启动（Windows）

### 方式 1: 使用启动脚本（推荐）

```powershell
# 在项目根目录执行
.\start-dev.ps1
```

脚本会自动：
- ✓ 检查环境依赖
- ✓ 安装 Python 和 Node.js 依赖
- ✓ 启动 Redis（如果未运行）
- ✓ 启动后端服务（FastAPI）
- ✓ 启动前端服务（Next.js）

### 方式 2: 手动启动

#### 1. 启动 Redis
```powershell
redis-server
```

#### 2. 启动后端
```powershell
cd backend
.\venv\Scripts\Activate
uvicorn app.main:app --reload
```

#### 3. 启动前端
```powershell
cd frontend
npm run dev
```

## 首次运行配置

### 1. 安装数据库

**PostgreSQL**
```powershell
# 使用 Chocolatey
choco install postgresql14

# 创建数据库
psql -U postgres
CREATE DATABASE stellar_journal;
\q
```

**Redis**
```powershell
choco install redis-64
```

### 2. 配置后端环境变量

在 `backend/` 目录下创建 `.env` 文件：

```env
# 数据库配置
DATABASE_URL=postgresql://postgres:你的密码@localhost:5432/stellar_journal

# Redis配置
REDIS_URL=redis://localhost:6379/0

# OpenAI API（必需）
OPENAI_API_KEY=sk-你的API密钥

# 其他配置
DEBUG=True
ENVIRONMENT=development
```

### 3. 配置前端环境变量

在 `frontend/` 目录下创建 `.env.local` 文件：

```env
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
```

### 4. 运行数据库迁移

```powershell
cd backend
.\venv\Scripts\Activate
alembic revision --autogenerate -m "Initial migration"
alembic upgrade head
```

## 访问应用

启动成功后，访问：

- 🌟 **星迹应用**: http://localhost:3000
- 🔌 **API 服务**: http://localhost:8000
- 📚 **API 文档**: http://localhost:8000/docs

## 测试功能

### 1. 创建第一条心情记录

1. 打开 http://localhost:3000
2. 在底部输入框选择"心情"
3. 输入内容，例如："今天天气很好，心情不错！"
4. 点击发送按钮
5. 观察星球颜色变化 ✨

### 2. 添加灵感

1. 切换到"灵感"标签
2. 输入一个灵感点子
3. 发送后会在星球周围出现一颗星星 ⭐

### 3. 记录思考

1. 切换到"思考"标签
2. 输入深度思考内容
3. 发送后会在星球表面生成一棵树 🌳

### 4. 查看时光轴

1. 点击右侧"时光轴"按钮
2. 查看历史记录
3. 点击任意日期切换到那天的星球状态

## 常见问题

### Q: 星球不显示？
**A**: 检查浏览器控制台是否有错误，确保：
- Three.js 加载成功
- WebGL 支持正常
- 后端 API 连接成功

### Q: 创建记录后星球没有变化？
**A**: 检查：
- 后端是否返回了颜色和位置数据
- 浏览器控制台Network标签查看API响应
- 前端状态是否刷新（`usePlanetStore.refreshPlanet()`）

### Q: OpenAI API 调用失败？
**A**: 
- 确认 API Key 正确
- 检查网络连接
- 确认 API 额度充足

### Q: 数据库连接失败？
**A**:
- 确认 PostgreSQL 服务运行中
- 检查数据库名称和连接字符串
- 确认用户名密码正确

## 下一步

- 📖 阅读 [开发文档](./DEVELOPMENT.md)
- 🎨 自定义星球主题
- 🔧 扩展新功能
- 🚀 部署到生产环境

## 获取帮助

- 查看完整文档：`docs/`
- API 文档：http://localhost:8000/docs
- 问题反馈：创建 Issue

---

祝你探索愉快！✨🌟
