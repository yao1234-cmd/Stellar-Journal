# 星迹开发指南 🌟

## 环境准备

### 前置要求
- Node.js 18+ 
- Python 3.11+
- PostgreSQL 14+
- Redis 7+

### 安装数据库

#### PostgreSQL (Windows)
```powershell
# 使用 Chocolatey
choco install postgresql14

# 或下载安装包
# https://www.postgresql.org/download/windows/
```

#### Redis (Windows)
```powershell
# 使用 Chocolatey
choco install redis-64

# 或使用 WSL2 安装 Redis
wsl --install
wsl
sudo apt update
sudo apt install redis-server
```

## 后端设置

### 1. 创建虚拟环境
```bash
cd backend
python -m venv venv

# Windows
.\venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 2. 安装依赖
```bash
pip install -r requirements.txt
```

### 3. 配置环境变量
复制 `.env.example` 为 `.env` 并填写配置：

```bash
cp .env.example .env
```

重要配置项：
- `DATABASE_URL`: PostgreSQL 连接字符串
- `REDIS_URL`: Redis 连接字符串
- `OPENAI_API_KEY`: OpenAI API 密钥（必需）

### 4. 创建数据库
```sql
-- 在 PostgreSQL 中执行
CREATE DATABASE stellar_journal;
```

### 5. 运行数据库迁移
```bash
# 初始化 Alembic
alembic revision --autogenerate -m "Initial migration"

# 执行迁移
alembic upgrade head
```

### 6. 启动后端服务
```bash
# 开发模式（热重载）
uvicorn app.main:app --reload

# 或使用 Python 直接运行
python -m app.main
```

后端将运行在 http://localhost:8000

API 文档：
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 前端设置

### 1. 安装依赖
```bash
cd frontend
npm install
```

### 2. 配置环境变量
```bash
# 复制示例文件
cp .env.local.example .env.local

# 编辑 .env.local
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
```

### 3. 启动开发服务器
```bash
npm run dev
```

前端将运行在 http://localhost:3000

## 开发工作流

### 1. 启动所有服务

**终端 1 - Redis**
```bash
redis-server
# 或 Windows: redis-server.exe
```

**终端 2 - PostgreSQL**
```bash
# 确保 PostgreSQL 服务正在运行
# Windows: 检查服务管理器
# Linux: sudo systemctl start postgresql
```

**终端 3 - 后端**
```bash
cd backend
.\venv\Scripts\activate  # Windows
uvicorn app.main:app --reload
```

**终端 4 - 前端**
```bash
cd frontend
npm run dev
```

### 2. 测试 API

使用 curl 或 Postman 测试：

```bash
# 健康检查
curl http://localhost:8000/health

# 创建心情记录
curl -X POST http://localhost:8000/api/v1/records/ \
  -H "Content-Type: application/json" \
  -d '{
    "type": "mood",
    "content": "今天很开心！"
  }'

# 获取星球状态
curl http://localhost:8000/api/v1/planet/state
```

### 3. 代码规范

**Python (后端)**
```bash
# 格式化代码
black app/

# 检查代码风格
flake8 app/

# 运行测试
pytest
```

**TypeScript (前端)**
```bash
# 类型检查
npm run type-check

# Lint 检查
npm run lint

# 格式化（如果配置了 Prettier）
npm run format
```

## 常见问题

### Q: OpenAI API 调用失败
A: 检查：
1. `.env` 文件中的 `OPENAI_API_KEY` 是否正确
2. 网络连接是否正常
3. API 额度是否充足

### Q: 数据库连接失败
A: 检查：
1. PostgreSQL 服务是否运行
2. 数据库 `stellar_journal` 是否创建
3. `.env` 中的 `DATABASE_URL` 是否正确

### Q: 前端无法连接后端
A: 检查：
1. 后端是否正常运行在 8000 端口
2. `.env.local` 中的 API URL 是否正确
3. 浏览器控制台是否有 CORS 错误

### Q: 3D 场景渲染问题
A: 检查：
1. 浏览器是否支持 WebGL
2. 显卡驱动是否更新
3. 浏览器控制台是否有 Three.js 错误

## 调试技巧

### 后端调试
```python
# 在代码中添加断点
import pdb; pdb.set_trace()

# 或使用 IDE 调试器（VSCode / PyCharm）
```

### 前端调试
- 使用 React Developer Tools
- 使用 Chrome DevTools
- 检查 Network 标签查看 API 请求

## 部署相关

### 生产环境配置

**后端**
```bash
# 使用 Gunicorn
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker
```

**前端**
```bash
# 构建生产版本
npm run build

# 启动生产服务器
npm start
```

## 资源链接

- [FastAPI 文档](https://fastapi.tiangolo.com/)
- [Next.js 文档](https://nextjs.org/docs)
- [React Three Fiber](https://docs.pmnd.rs/react-three-fiber)
- [Tailwind CSS](https://tailwindcss.com/docs)
- [OpenAI API](https://platform.openai.com/docs)

## 获取帮助

遇到问题？
1. 查看错误日志
2. 搜索已知问题
3. 创建 Issue

---

Happy Coding! 🚀✨
