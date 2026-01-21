# ⚡ 星迹 PWA 快速开始（15 分钟）

## 第一步：本地测试 PWA

```powershell
# 1. 确保后端和前端都在运行
.\start-dev.ps1

# 2. 在浏览器打开
# http://localhost:3000

# 3. 在 Chrome 开发者工具测试 PWA
# F12 → Application → Manifest（检查是否正常）
# F12 → Application → Service Workers（检查是否注册）
```

---

## 第二步：准备部署

### 1. 推送到 GitHub

```powershell
# 初始化 Git（如果还没有）
git init
git add .
git commit -m "Add PWA support"

# 在 GitHub 创建新仓库，然后：
git remote add origin https://github.com/你的用户名/stellar-journal.git
git branch -M main
git push -u origin main
```

### 2. 获取 OpenAI API Key

1. 访问：https://platform.openai.com/api-keys
2. 登录或注册
3. 创建新的 API Key
4. **保存好**，下一步会用

---

## 第三步：部署后端（Railway）

### 选项 A：网页部署（最简单）

1. **访问** https://railway.app
2. **登录** GitHub 账号
3. **点击** "New Project" → "Deploy from GitHub repo"
4. **选择** 你的 stellar-journal 仓库
5. **配置** Root Directory: `backend`
6. **添加数据库**：
   - 点击 "New" → "Database" → "PostgreSQL"
7. **添加环境变量**（在 Variables 标签）：
   ```
   OPENAI_API_KEY=sk-your-key-here
   SECRET_KEY=<运行下面命令生成>
   ```
   
   生成 SECRET_KEY：
   ```powershell
   python -c "import secrets; print(secrets.token_urlsafe(32))"
   ```

8. **等待部署**（约 2-3 分钟）
9. **复制 URL**：如 `https://stellar-backend-xxx.railway.app`

### 选项 B：命令行部署

```powershell
# 1. 安装 CLI
npm install -g @railway/cli

# 2. 登录
railway login

# 3. 部署
cd backend
railway init
railway up

# 4. 添加数据库
railway add postgresql

# 5. 配置环境变量
railway variables set OPENAI_API_KEY=sk-your-key
railway variables set SECRET_KEY=$(python -c "import secrets; print(secrets.token_urlsafe(32))")

# 6. 查看 URL
railway status
```

---

## 第四步：部署前端（Vercel）

### 1. 配置后端地址

在项目根目录创建 `.env.production`：

```bash
NEXT_PUBLIC_API_URL=https://你的railway地址.railway.app/api/v1
```

**重要：替换成你的 Railway URL！**

### 2. 提交更新

```powershell
git add .env.production
git commit -m "Add production config"
git push
```

### 3. 部署到 Vercel

#### 选项 A：网页部署（推荐）

1. **访问** https://vercel.com
2. **登录** GitHub 账号
3. **点击** "Add New" → "Project"
4. **选择** stellar-journal 仓库
5. **配置**：
   - Framework Preset: **Next.js**
   - Root Directory: **frontend**
   - Build Command: `npm run build`
   - Output Directory: `.next`
6. **添加环境变量**：
   - Name: `NEXT_PUBLIC_API_URL`
   - Value: `https://你的railway地址.railway.app/api/v1`
7. **点击** "Deploy"
8. **等待** 1-2 分钟
9. **访问** 提供的网址（如 `https://stellar-journal.vercel.app`）

#### 选项 B：命令行部署

```powershell
# 1. 安装 CLI
npm install -g vercel

# 2. 进入前端目录
cd frontend

# 3. 登录
vercel login

# 4. 部署
vercel --prod

# 5. 按提示操作
# - Scope: 选择你的账号
# - Link to existing project: No
# - Project name: stellar-journal
# - Directory: ./（当前目录）
# - Override settings: No

# 完成！会显示部署的 URL
```

---

## 第五步：在手机上安装

### iPhone/iPad

1. 用 **Safari** 打开你的网址
2. 点击底部 **分享** 按钮（方框+箭头）
3. 向下滚动，选择 **"添加到主屏幕"**
4. 命名为 **"星迹"**
5. 点击 **"添加"**
6. 完成！在桌面找到星迹图标

### Android

1. 用 **Chrome** 打开你的网址
2. 浏览器会自动弹出 **"安装 App"** 提示
3. 点击 **"安装"**
4. 或：点击右上角 **⋮** → **"添加到主屏幕"**
5. 完成！

### 电脑（Windows/Mac）

1. 用 **Chrome** 或 **Edge** 打开你的网址
2. 地址栏右侧会出现 **📥 安装** 图标
3. 点击安装
4. 完成！

---

## 验证清单

### ✅ 后端检查

访问 `https://你的railway地址.railway.app/docs`

- [ ] 能看到 API 文档
- [ ] 创建记录接口能正常调用

### ✅ 前端检查

访问 `https://你的vercel地址.vercel.app`

- [ ] 页面能正常加载
- [ ] 能看到 3D 星球
- [ ] 能创建记录
- [ ] 能看到时光轴

### ✅ PWA 检查

在 Chrome 按 F12：

- [ ] Application → Manifest 显示正常
- [ ] Application → Service Workers 已注册
- [ ] 地址栏有安装图标

---

## 故障排查

### 问题：部署后 API 调用失败

**检查：**
```powershell
# 1. 查看后端日志
railway logs

# 2. 检查环境变量是否正确
railway variables
```

**解决：**
- 确保 `NEXT_PUBLIC_API_URL` 正确
- 确保后端 CORS 配置允许你的 Vercel 域名

### 问题：PWA 没有安装提示

**检查：**
- 是否使用 HTTPS（Railway/Vercel 自动提供）
- 是否在支持的浏览器（Safari/Chrome）
- F12 → Console 是否有错误

**解决：**
```powershell
# 本地测试 PWA
cd frontend
npm run build
npm run start
# 访问 http://localhost:3000
```

### 问题：Service Worker 没有注册

**检查：**
```javascript
// F12 → Console 输入：
navigator.serviceWorker.getRegistrations()
```

**解决：**
- 清除浏览器缓存
- 在 next.config.js 中确认 `disable: false`

---

## 下一步

### 🎨 自定义图标

1. 创建 512x512 的图标（PNG）
2. 使用工具生成各种尺寸：https://realfavicongenerator.net
3. 替换 `frontend/public/icon-*.png`
4. 提交并重新部署

### 📊 添加分析

Vercel 免费提供：
- 访问统计
- 性能监控
- Web Vitals

在项目设置中启用即可。

### 🔒 添加用户系统

目前使用临时用户 ID，后续可以添加：
- 邮箱登录
- Google 登录
- 多设备同步

### 🌍 自定义域名

1. 购买域名（如 Namecheap、Cloudflare）
2. 在 Vercel 项目设置中添加域名
3. 按提示配置 DNS
4. 完成！

---

## 成本估算

| 服务 | 免费额度 | 预计使用 | 实际成本 |
|------|---------|---------|---------|
| Railway | $5/月 | ~$2-3/月 | $0（在额度内）|
| Vercel | 无限制 | 任意 | $0 |
| 域名（可选）| - | - | ~$10/年 |
| **总计** | | | **$0/月** |

---

## 🎉 完成！

现在你有了：
- ✅ 可以在手机桌面打开的 App
- ✅ 支持离线使用
- ✅ 全球 CDN 加速
- ✅ 自动 HTTPS
- ✅ 完全免费

**分享给朋友：** 发送你的 Vercel 网址即可！

---

**需要帮助？** 查看 [完整部署指南](DEPLOY.md)
