# 贡献指南 🤝

感谢你对星迹项目的关注！我们欢迎任何形式的贡献。

## 如何贡献

### 报告 Bug

在 GitHub Issues 中提交 Bug 报告，请包含：

- **标题**: 简短描述问题
- **环境**: 操作系统、浏览器版本等
- **重现步骤**: 详细的步骤
- **预期行为**: 应该发生什么
- **实际行为**: 实际发生了什么
- **截图**: 如果适用

### 功能建议

我们欢迎功能建议！请在 Issues 中提交，包含：

- **功能描述**: 清晰描述建议的功能
- **使用场景**: 为什么需要这个功能
- **期望效果**: 功能应该如何工作

### 代码贡献

1. **Fork 项目**
   ```bash
   # 点击 GitHub 上的 Fork 按钮
   ```

2. **克隆到本地**
   ```bash
   git clone https://github.com/your-username/stellar-journal.git
   cd stellar-journal
   ```

3. **创建功能分支**
   ```bash
   git checkout -b feature/amazing-feature
   ```

4. **开发并测试**
   - 遵循代码规范
   - 编写测试
   - 确保所有测试通过

5. **提交变更**
   ```bash
   git add .
   git commit -m 'Add some amazing feature'
   ```

6. **推送到 GitHub**
   ```bash
   git push origin feature/amazing-feature
   ```

7. **创建 Pull Request**
   - 填写 PR 模板
   - 关联相关 Issue
   - 等待代码审查

## 代码规范

### Python (后端)

- 遵循 PEP 8
- 使用 Black 格式化
- 类型注解（Type Hints）
- 文档字符串（Docstrings）

```python
def analyze_emotion(text: str) -> Dict[str, Any]:
    """
    分析文本情感
    
    Args:
        text: 输入文本
        
    Returns:
        情感分析结果字典
    """
    pass
```

### TypeScript (前端)

- 使用 ESLint
- 明确的类型定义
- 函数式组件
- Hooks 优先

```typescript
interface PlanetProps {
  color: string
  size: number
}

const Planet: React.FC<PlanetProps> = ({ color, size }) => {
  // ...
}
```

### Git Commit 规范

使用语义化提交信息：

```
feat: 新功能
fix: Bug 修复
docs: 文档更新
style: 代码格式（不影响功能）
refactor: 重构
test: 测试
chore: 构建/工具链
```

示例：
```
feat: 添加语音输入功能
fix: 修复星球旋转卡顿问题
docs: 更新 API 文档
```

## 开发流程

### 设置开发环境

参考 [开发指南](docs/DEVELOPMENT.md)

### 运行测试

```bash
# 后端测试
cd backend
pytest

# 前端测试（如果有）
cd frontend
npm test
```

### 代码审查检查清单

- [ ] 代码符合规范
- [ ] 添加了必要的测试
- [ ] 测试全部通过
- [ ] 更新了相关文档
- [ ] 没有遗留的 console.log
- [ ] 没有遗留的 TODO
- [ ] 提交信息清晰

## 项目结构

理解项目结构有助于贡献：

```
stellar-journal/
├── backend/      # Python FastAPI 后端
├── frontend/     # Next.js React 前端
├── docs/         # 文档
└── tests/        # 测试
```

## 优先级任务

当前优先级高的任务：

1. 🔥 **高优先级**
   - [ ] 用户认证系统
   - [ ] 语音输入完整实现
   - [ ] 数据导出功能

2. 🚀 **中优先级**
   - [ ] 性能优化
   - [ ] 移动端适配
   - [ ] 多语言支持

3. 💡 **低优先级**
   - [ ] 主题自定义
   - [ ] 社交分享功能
   - [ ] 统计报告生成

## 社区准则

- 尊重他人
- 建设性反馈
- 友好讨论
- 包容多样性

## 许可证

贡献代码即表示同意以 MIT 许可证开源。

## 问题？

如有疑问，请：
- 查看 [文档](docs/)
- 搜索现有 Issues
- 创建新 Issue
- 加入讨论

---

感谢你让星迹变得更好！✨
