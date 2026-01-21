# 🚀 星迹 PWA 部署指南

本指南将帮助你在 **15 分钟内** 将星迹部署为 PWA，完全免费！

---

## 📱 PWA 是什么？

PWA (Progressive Web App) = **网站 + App 的优点**

用户体验：
- ✅ 在手机桌面有独立图标（像普通 App）
- ✅ 全屏运行，没有浏览器地址栏
- ✅ 支持离线使用
- ✅ 加载速度快（有缓存）
- ✅ 保留所有 3D 效果

安装方式：
1. 用户打开你的网址
2. 浏览器提示"添加到主屏幕"
3. 点击添加，完成！

---

## 第一步：部署后端到 Railway（5 分钟）

### 1. 创建 Railway 账号
- 访问：https://railway.app
- 用 GitHub 账号登录（免费）
- 免费额度：$5/月，足够测试使用

### 2. 部署后端

**方式 A：通过网页部署（推荐）**

1. 进入 Railway 控制台
2. 点击 "New Project" → "Deploy from GitHub repo"
3. 选择你的项目仓库（需要先推送到 GitHub）
4. Railway 会自动检测到 Python 项目

**方式 B：通过命令行部署**

```powershell
# 1. 安装 Railway CLI
npm install -g @railway/cli

# 2. 登录（会打开浏览器）
railway login

# 3. 进入后端目录
cd backend

# 4. 初始化项目
railway init

# 5. 部署
railway up
```

### 3. 添加数据库

```powershell
# 在后端目录
railway add postgresql
```

或在网页上：
1. 点击 "New" → "Database" → "PostgreSQL"
2. Railway 会自动连接

### 4. 配置环境变量

在 Railway 网页控制台 → Variables，添加：

```
DATABASE_URL=<Railway自动提供>
REDIS_URL=<暂时可以不配置>
OPENAI_API_KEY=你的OpenAI密钥
SECRET_KEY=随机生成一个长字符串
```

生成 SECRET_KEY：
```powershell
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

### 5. 获取后端 URL

部署完成后，Railway 会提供一个 URL，类似：
```
https://your-app-name.railway.app
```

**记下这个 URL**，下一步会用到！

---

## 第二步：部署前端到 Vercel（5 分钟）

### 1. 创建 Vercel 账号
- 访问：https://vercel.com
- 用 GitHub 账号登录（免费）
- 完全免费，没有限制

### 2. 配置环境变量

在项目根目录创建 `.env.production`：

```bash
NEXT_PUBLIC_API_URL=https://your-app-name.railway.app/api/v1
```

**重要：** 把 `your-app-name` 替换为你的 Railway 地址！

### 3. 推送代码到 GitHub

```powershell
# 如果还没有 Git 仓库
git init
git add .
git commit -m "Initial commit"

# 创建 GitHub 仓库并推送
# 在 GitHub 上创建新仓库后：
git remote add origin https://github.com/你的用户名/stellar-journal.git
git push -u origin main
```

### 4. 在 Vercel 部署

**方式 A：网页部署（推荐）**

1. 登录 Vercel
2. 点击 "Add New" → "Project"
3. 选择你的 GitHub 仓库
4. 配置：
   - Framework Preset: Next.js
   - Root Directory: `frontend`
   - Build Command: `npm run build`
   - Output Directory: `.next`
5. 添加环境变量：
   - `NEXT_PUBLIC_API_URL` = `https://your-app-name.railway.app/api/v1`
6. 点击 "Deploy"

**方式 B：命令行部署**

```powershell
# 安装 Vercel CLI
npm install -g vercel

# 进入前端目录
cd frontend

# 登录
vercel login

# 部署
vercel --prod
```

### 5. 获取网址

部署完成后，Vercel 会提供一个网址，类似：
```
https://stellar-journal.vercel.app
```

或者你可以绑定自己的域名（可选）。

---

## 第三步：测试 PWA（2 分钟）

### 在手机上测试

1. **iPhone/iPad (Safari)**
   - 打开你的 Vercel 网址
   - 点击底部的"分享"按钮
   - 选择"添加到主屏幕"
   - 命名为"星迹"
   - 完成！

2. **Android (Chrome)**
   - 打开你的 Vercel 网址
   - 浏览器会自动弹出"安装 App"提示
   - 或点击菜单 → "添加到主屏幕"
   - 完成！

### 在电脑上测试

1. **Chrome/Edge**
   - 打开你的 Vercel 网址
   - 地址栏右侧会出现"安装"图标
   - 点击安装
   - 完成！

---

## 第四步：优化（可选）

### 1. 生成真实图标

当前使用的是 SVG 临时图标，你可以：

1. 使用设计工具创建 512x512 的图标
2. 使用在线工具生成各种尺寸：
   - https://realfavicongenerator.net
   - https://www.pwabuilder.com/imageGenerator

3. 替换文件：
   ```
   frontend/public/icon-192.png
   frontend/public/icon-512.png
   ```

### 2. 添加启动画面

在 `manifest.json` 中已配置，浏览器会自动生成。

### 3. 开启 HTTPS

Railway 和 Vercel 都默认提供 HTTPS，无需额外配置。

### 4. 性能优化

已自动配置：
- ✅ 静态资源缓存
- ✅ API 响应缓存
- ✅ 离线支持
- ✅ Service Worker

---

## 常见问题

### Q: 为什么在浏览器中没有"安装"提示？

A: 需要满足以下条件：
- ✅ 使用 HTTPS（Vercel 自动提供）
- ✅ 有 manifest.json（已配置）
- ✅ 有 Service Worker（已自动生成）
- ✅ 在手机上使用 Safari/Chrome

### Q: 如何更新 PWA？

A: 
1. 修改代码后推送到 GitHub
2. Vercel 会自动重新部署
3. 用户下次打开时自动更新

### Q: PWA 能使用相机和麦克风吗？

A: 能！PWA 支持：
- ✅ 相机拍照
- ✅ 麦克风录音
- ✅ 地理位置
- ✅ 通知（需要用户授权）

### Q: 离线时能用吗？

A: 部分功能可以：
- ✅ 查看已缓存的星球和记录
- ✅ 创建新记录（会在联网后自动同步）
- ❌ AI 分析需要联网

### Q: 如何查看安装了多少用户？

A: 在 Vercel Analytics 中可以看到访问统计。

### Q: 成本是多少？

A: 
- Railway: $5/月免费额度（足够测试）
- Vercel: 完全免费
- 域名: 可选，约 $10/年
- **总计：前期完全免费！**

---

## 下一步

### 分享给朋友

发送你的 Vercel 网址：
```
https://your-app.vercel.app
```

告诉他们：
1. 用手机浏览器打开
2. 点击"添加到主屏幕"
3. 开始使用星迹！

### 绑定自定义域名（可选）

1. 购买域名（如 `stellarjournal.com`）
2. 在 Vercel 项目设置中添加域名
3. 按提示配置 DNS
4. 完成！

### 监控和分析

Vercel 提供：
- 访问统计
- 性能监控
- 错误日志

Railway 提供：
- 服务器日志
- 数据库监控
- 资源使用情况

---

## 需要帮助？

遇到问题可以：
1. 查看 Railway 日志：`railway logs`
2. 查看 Vercel 日志：在网页控制台
3. 检查浏览器控制台是否有错误

---

**恭喜！🎉 你的星迹 PWA 已经上线了！**

现在任何人都可以访问你的网址并安装 App 了！
