# 星迹 (Stellar Journal) 🌟

<div align="center">

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.11+-blue.svg)
![Node](https://img.shields.io/badge/node-18+-green.svg)
![Status](https://img.shields.io/badge/status-MVP-orange.svg)

**让每一次内心波动，都成为构建独特宇宙的星辰**

[快速开始](#-快速开始) • [功能特性](#-核心功能) • [技术架构](#-技术架构) • [文档](#-文档) • [贡献](#-贡献)

</div>

---

## 📖 项目简介

**星迹 (Stellar Journal)** 是一款融合情感计算与3D数据可视化的治愈系记录应用。

通过AI解析你记录的文字或语音，动态生成并演化一个独一无二的3D星球：
- 💗 **心情** → 决定星球大气层颜色
- ✨ **灵感** → 化为环绕的星辰
- 🌳 **思考** → 沉淀为地表植被

每一次记录，都让你的专属宇宙更加独特和美丽。

### ✨ 核心亮点

- 🎨 **情感可视化**: AI实时分析情绪并映射为色彩
- 🌍 **3D交互星球**: 流畅的Three.js渲染，支持旋转缩放
- 🤖 **智能分析**: OpenAI GPT-4o mini 驱动的情感分析
- 📊 **数据洞察**: 时光轴回顾情绪变化趋势
- 🎭 **治愈系设计**: 玻璃态UI + 流畅动画

## 🎯 核心功能

| 功能 | 描述 | 视觉效果 |
|------|------|----------|
| 💗 心情记录 | 记录日常情绪，AI分析情感倾向 | 影响星球大气层颜色 |
| ✨ 灵感捕捉 | 快速记录灵光一闪的想法 | 生成环绕星球的星星 |
| 🌳 思考沉淀 | 深度思考记录与主题聚类 | 星球表面长出树木 |
| 📅 时光轴 | 查看历史记录和情绪趋势 | 颜色光谱展示 |
| 📊 统计面板 | 记录数量和活跃天数统计 | 实时数据展示 |

## 🚀 快速开始

### 一键启动（Windows 推荐）

```powershell
# 在项目根目录执行
.\start-dev.ps1
```

启动脚本会自动：
- ✓ 检查环境依赖
- ✓ 安装必要的包
- ✓ 启动 Redis 和数据库
- ✓ 启动前后端服务

然后访问：
- 🌟 应用: http://localhost:3000
- 🔌 API: http://localhost:8000
- 📚 文档: http://localhost:8000/docs

### 手动启动

#### 1. 环境准备

**必需软件：**
- [Node.js 18+](https://nodejs.org/)
- [Python 3.11+](https://www.python.org/)
- [PostgreSQL 14+](https://www.postgresql.org/)
- [Redis 7+](https://redis.io/)

**安装方法 (Windows):**
```powershell
# 使用 Chocolatey
choco install nodejs python postgresql redis-64
```

#### 2. 数据库设置

```sql
-- 创建数据库
CREATE DATABASE stellar_journal;
```

#### 3. 配置环境变量

**后端** (`backend/.env`):
```env
DATABASE_URL=postgresql://postgres:password@localhost:5432/stellar_journal
REDIS_URL=redis://localhost:6379/0
OPENAI_API_KEY=sk-your-api-key-here
```

**前端** (`frontend/.env.local`):
```env
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
```

#### 4. 安装依赖并启动

**后端:**
```bash
cd backend
python -m venv venv
.\venv\Scripts\Activate  # Windows
source venv/bin/activate  # Linux/Mac
pip install -r requirements.txt
alembic upgrade head
uvicorn app.main:app --reload
```

**前端:**
```bash
cd frontend
npm install
npm run dev
```

📖 详细教程请查看 [快速开始指南](docs/QUICKSTART.md)

## 🏗️ 技术架构

### 技术栈

**前端 (Frontend)**
```
Next.js 14 + TypeScript
├── React Three Fiber  # 3D 渲染
├── Drei               # Three.js 辅助库
├── Tailwind CSS       # 样式
├── Framer Motion      # 动画
└── Zustand            # 状态管理
```

**后端 (Backend)**
```
Python 3.11+ FastAPI
├── SQLAlchemy         # ORM
├── PostgreSQL         # 数据库
├── Redis              # 缓存
├── Alembic            # 迁移
└── OpenAI API
    ├── GPT-4o mini    # 情感分析
    └── Whisper        # 语音转文字
```

### 系统架构

```
┌─────────────┐
│  用户界面   │  Next.js + React Three Fiber
└──────┬──────┘
       │ HTTP/REST
┌──────▼──────┐
│  API 网关   │  FastAPI
└──────┬──────┘
       │
┌──────▼──────┐
│ 业务逻辑层  │  Services (AI + 计算)
└──────┬──────┘
       │
┌──────▼──────┐
│  数据层     │  PostgreSQL + Redis
└─────────────┘
       │
┌──────▼──────┐
│  AI 服务    │  OpenAI API
└─────────────┘
```

## 📁 项目结构

```
stellar-journal/
├── backend/                    # 后端服务
│   ├── app/
│   │   ├── api/v1/            # API 路由
│   │   ├── core/              # 核心配置
│   │   ├── models/            # 数据模型
│   │   ├── schemas/           # Pydantic 模式
│   │   ├── services/          # 业务逻辑
│   │   └── main.py            # 入口文件
│   └── requirements.txt
│
├── frontend/                  # 前端应用
│   ├── src/
│   │   ├── app/              # Next.js 页面
│   │   ├── components/       # React 组件
│   │   │   ├── planet/       # 3D 星球组件
│   │   │   └── ui/           # UI 组件
│   │   ├── lib/              # 工具函数
│   │   └── stores/           # 状态管理
│   └── package.json
│
├── docs/                     # 文档
│   ├── QUICKSTART.md         # 快速开始
│   ├── DEVELOPMENT.md        # 开发指南
│   ├── PROJECT_OVERVIEW.md   # 项目概览
│   ├── API_REFERENCE.md      # API 文档
│   └── USER_GUIDE.md         # 使用指南
│
├── start-dev.ps1             # Windows 启动脚本
├── README.md                 # 本文档
└── CONTRIBUTING.md           # 贡献指南
```

## 📚 文档

| 文档 | 描述 |
|------|------|
| [快速开始](docs/QUICKSTART.md) | 5分钟快速上手 |
| [开发指南](docs/DEVELOPMENT.md) | 详细的开发教程 |
| [项目概览](docs/PROJECT_OVERVIEW.md) | 完整的技术文档 |
| [API 文档](docs/API_REFERENCE.md) | API 接口说明 |
| [使用指南](docs/USER_GUIDE.md) | 用户使用手册 |
| [贡献指南](CONTRIBUTING.md) | 如何参与贡献 |

## 🎨 界面预览

### 主界面
- 🌍 中央3D星球场景（支持交互）
- 📝 底部记录输入面板
- 📊 顶部统计信息栏
- 📅 右侧时光轴面板

### 交互体验
- 🖱️ 流畅的3D旋转和缩放
- ✨ 实时的情感色彩反馈
- 🎭 治愈系玻璃态设计
- 🎬 丝滑的动画过渡

## 🔬 核心算法

### 情感分析流程

1. **文本输入** → 用户记录内容
2. **AI 分析** → GPT-4o mini 提取情感特征
3. **二维模型** → 映射到 (效价, 唤起度) 坐标
4. **色彩计算** → HSL 色彩空间转换
5. **视觉呈现** → 更新星球大气层颜色

### 色彩映射原理

```
情绪维度:
├── 效价 (Valence): 消极 ←──────→ 积极
└── 唤起度 (Arousal): 平静 ←──────→ 激动

色彩映射:
├── 色相 (Hue): 由效价决定
│   ├── 积极 → 暖色系 (黄、橙)
│   └── 消极 → 冷色系 (蓝、紫)
├── 饱和度: 由唤起度决定
└── 亮度: 由两者组合决定
```

## 📋 开发路线图

### ✅ Phase 1: MVP (已完成)
- [x] 项目架构搭建
- [x] 后端 API 开发
- [x] 前端 UI 实现
- [x] 3D 星球渲染
- [x] AI 情感分析集成
- [x] 记录系统（心情/灵感/思考）
- [x] 时光轴功能

### 🚧 Phase 2: 生态构建 (进行中)
- [ ] 完整的语音输入支持
- [ ] 更智能的思考聚类
- [ ] 环境音效系统
- [ ] 星球快照分享
- [ ] 用户认证系统

### 🔮 Phase 3: 洞察与陪伴 (规划中)
- [ ] 情绪趋势报告
- [ ] AI 生成的月度摘要
- [ ] 多种星球主题皮肤
- [ ] 移动端适配 (iOS/Android)
- [ ] 数据导出功能

## 🤝 贡献

我们欢迎任何形式的贡献！

### 贡献方式
- 🐛 报告 Bug
- 💡 提出新功能建议
- 📝 改进文档
- 🔧 提交代码

### 贡献流程
1. Fork 项目
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交变更 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建 Pull Request

详细信息请查看 [贡献指南](CONTRIBUTING.md)

## 🐛 问题反馈

遇到问题？
1. 查看 [文档](docs/)
2. 搜索 [已知问题](https://github.com/yourusername/stellar-journal/issues)
3. 创建新 Issue

## 📄 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件

## 💖 致谢

- [OpenAI](https://openai.com/) - AI 能力支持
- [Three.js](https://threejs.org/) - 3D 渲染引擎
- [Next.js](https://nextjs.org/) - React 框架
- [FastAPI](https://fastapi.tiangolo.com/) - 现代 Python Web 框架

## 🌟 Star History

如果这个项目对你有帮助，请给我们一个 ⭐️ Star！

---

<div align="center">

**让每一次内心波动，都成为构建独特宇宙的星辰** ✨

Made with 💜 by Stellar Journal Team

[立即体验](http://localhost:3000) • [查看文档](docs/) • [参与贡献](CONTRIBUTING.md)

</div>

