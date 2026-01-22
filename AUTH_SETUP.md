# 认证系统配置指南

## 📋 概述

本项目已集成完整的用户认证系统，包括：
- ✅ 邮箱注册 + 邮箱验证
- ✅ JWT Token 认证
- ✅ 7 天自动登录
- ✅ Token 自动刷新
- ✅ 数据隔离（每个用户独立数据）

---

## 🔧 后端配置

### 1. 安装新依赖

```bash
cd backend
pip install -r requirements.txt
```

新增依赖：
- `resend==0.7.0` - 邮件服务

### 2. 配置环境变量

在 `backend/.env` 中添加以下配置：

```env
# Security & Authentication
SECRET_KEY=your-super-secret-jwt-key-change-this-in-production
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=10080  # 7 days
REFRESH_TOKEN_EXPIRE_DAYS=30

# Email Service (Resend)
RESEND_API_KEY=re_xxxxxxxxxxxxxxxxxxxxxxxxxxxxx
EMAIL_FROM=noreply@yourdomain.com
EMAIL_FROM_NAME=Stellar Journal
FRONTEND_URL=https://your-frontend-domain.com  # 或 http://localhost:3000

# CORS Origins (添加你的前端域名)
BACKEND_CORS_ORIGINS=http://localhost:3000,https://your-frontend-domain.com
```

### 3. 获取 Resend API Key

1. 访问 [Resend](https://resend.com)
2. 注册账号（免费额度：每月 3000 封邮件）
3. 创建 API Key：https://resend.com/api-keys
4. 复制 API Key 到环境变量 `RESEND_API_KEY`
5. 配置发件域名（免费版可使用 `onboarding@resend.dev`）

> **注意**：免费版只能发送到你注册的邮箱。生产环境需要绑定自己的域名。

### 4. 运行数据库迁移

```bash
cd backend
alembic upgrade head
```

这会添加以下字段到 `users` 表：
- `is_email_verified` - 邮箱是否已验证
- `verification_token` - 验证令牌
- `verification_token_expires` - 令牌过期时间

### 5. 启动后端

```bash
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

---

## 🎨 前端配置

### 1. 安装新依赖

```bash
cd frontend
npm install zustand
```

### 2. 配置环境变量

确保 `frontend/.env.local` 配置正确：

```env
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
```

生产环境：
```env
NEXT_PUBLIC_API_URL=https://your-backend-domain.com/api/v1
```

### 3. 启动前端

```bash
cd frontend
npm run dev
```

---

## 🚀 部署到云端

### 后端 (Railway)

1. **添加环境变量**

在 Railway 项目的 Variables 中添加：

```env
DATABASE_URL=<Railway 自动提供>
REDIS_URL=<Redis 服务 URL>
SECRET_KEY=<生成一个强密码>
RESEND_API_KEY=<你的 Resend API Key>
EMAIL_FROM=noreply@yourdomain.com
EMAIL_FROM_NAME=Stellar Journal
FRONTEND_URL=https://your-vercel-domain.vercel.app
BACKEND_CORS_ORIGINS=https://your-vercel-domain.vercel.app
ZHIPU_API_KEY=<你的智谱AI Key>
AI_PROVIDER=zhipu
ENVIRONMENT=production
DEBUG=False
```

2. **运行迁移**

在 Railway 项目中，运行一次性命令：
```bash
alembic upgrade head
```

### 前端 (Vercel)

1. **配置环境变量**

在 Vercel 项目的 Settings → Environment Variables 中添加：

```
NEXT_PUBLIC_API_URL=https://your-railway-backend.up.railway.app/api/v1
```

2. **重新部署**

```bash
git add .
git commit -m "Add authentication system"
git push
```

---

## 📝 使用流程

### 用户注册流程

1. 用户访问 `/register` 填写信息
2. 后端创建用户（`is_email_verified=False`）
3. 发送验证邮件到用户邮箱
4. 用户点击邮件中的链接（`/verify-email?token=xxx`）
5. 后端验证 token，设置 `is_email_verified=True`
6. 用户可以登录

### 用户登录流程

1. 用户访问 `/login` 输入邮箱和密码
2. 后端验证凭据
3. 检查邮箱是否已验证
4. 返回 `access_token` 和 `refresh_token`
5. 前端保存到 localStorage
6. 跳转到主页 `/`

### Token 管理

- **Access Token**: 7 天有效期
- **Refresh Token**: 30 天有效期
- **自动刷新**: API 返回 401 时自动使用 refresh token 获取新 token
- **自动登出**: refresh token 失效后清除认证状态并跳转登录页

### 数据隔离

所有 API 请求现在都需要认证：
- `/api/v1/records/*` - 记录相关接口
- `/api/v1/planet/*` - 星球状态接口

每个用户只能看到和操作自己的数据。

---

## 🧪 本地测试

### 1. 注册新用户

```bash
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "your-email@example.com",
    "password": "Test1234"
  }'
```

### 2. 检查邮箱并点击验证链接

### 3. 登录

```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "your-email@example.com",
    "password": "Test1234"
  }'
```

返回：
```json
{
  "access_token": "eyJ...",
  "refresh_token": "eyJ...",
  "token_type": "bearer"
}
```

### 4. 使用 Token 访问 API

```bash
curl http://localhost:8000/api/v1/records/ \
  -H "Authorization: Bearer <access_token>"
```

---

## 🎯 新增页面

- `/login` - 登录页（星空背景）
- `/register` - 注册页（星空背景）
- `/verify-email` - 邮箱验证页

---

## 🔒 安全注意事项

1. **SECRET_KEY**: 生产环境必须使用强随机密钥
2. **HTTPS**: 生产环境必须启用 HTTPS
3. **CORS**: 只允许信任的前端域名
4. **密码要求**: 至少 8 位，包含字母和数字
5. **Token 过期**: Access token 7 天，Refresh token 30 天

---

## 🐛 常见问题

### 1. 注册后收不到验证邮件

- 检查 `RESEND_API_KEY` 是否正确
- Resend 免费版只能发送到注册邮箱
- 检查垃圾邮件文件夹

### 2. 登录后提示"请先验证您的邮箱"

- 点击注册时收到的验证邮件
- 或使用 `/api/v1/auth/resend-verification` 重新发送

### 3. 401 Unauthorized

- Token 可能已过期
- 清除浏览器 localStorage 重新登录
- 或等待自动 token 刷新

### 4. CORS 错误

- 检查 `BACKEND_CORS_ORIGINS` 包含前端域名
- 前后端域名协议（http/https）要匹配

---

## 📚 API 文档

访问 `http://localhost:8000/docs` 查看完整的 API 文档（Swagger UI）。

新增认证端点：
- `POST /api/v1/auth/register` - 注册
- `POST /api/v1/auth/verify-email` - 验证邮箱
- `POST /api/v1/auth/login` - 登录
- `POST /api/v1/auth/refresh` - 刷新 Token
- `GET /api/v1/auth/me` - 获取当前用户信息
- `POST /api/v1/auth/resend-verification` - 重新发送验证邮件

---

## ✅ 完成！

认证系统已完全集成。现在每个用户都有独立的情感星球！ 🌍✨
