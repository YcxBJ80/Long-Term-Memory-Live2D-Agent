# 🌐 memU 笔记 Web 应用使用指南

## 🎉 简介

memU 笔记 Web 应用是一个基于浏览器的智能笔记系统，使用语义搜索技术，让你可以轻松管理和查找笔记。

## 🚀 快速开始

### 1. 确保服务运行

#### memU 服务（必需）

```bash
# 检查 memU 是否运行
lsof -i :8000

# 如果未运行，启动 memU
cd memU
unset http_proxy https_proxy HTTP_PROXY HTTPS_PROXY all_proxy ALL_PROXY
python3.12 -m memu.server.cli start
```

#### Web 服务器

```bash
# 方式 1：使用启动脚本（推荐）
cd note_app
./start_web.sh

# 方式 2：手动启动
cd note_app
unset http_proxy https_proxy HTTP_PROXY HTTPS_PROXY all_proxy ALL_PROXY
python3 web_server.py
```

### 2. 访问应用

打开浏览器，访问：

```
http://localhost:8080
```

## 📊 功能特性

### ✏️ 新建笔记

1. **标题**：输入笔记标题（必填）
2. **内容**：输入笔记内容（必填）
3. **标签**：用逗号分隔，例如：`Python,学习,技术`
4. **分类**：笔记分类，默认为 `note`

点击"保存笔记"按钮即可保存。

### 🔍 搜索笔记

1. 在搜索框中输入关键词
2. 点击"搜索"按钮或按回车键
3. 查看搜索结果

**搜索特性**：
- **语义理解**：搜索"AI"能找到"人工智能"相关笔记
- **相似度评分**：每个结果显示相似度百分比
- **智能排序**：按相似度从高到低排序

### 📊 笔记统计

页面底部显示当前笔记总数。

## 🎨 界面说明

### 主界面布局

```
┌─────────────────────────────────────┐
│         📝 memU 智能笔记            │
│   基于语义搜索的智能笔记系统         │
├──────────────┬──────────────────────┤
│              │                      │
│  ✏️ 新建笔记  │    🔍 搜索笔记        │
│              │                      │
│  [表单]      │    [搜索框]          │
│              │    [搜索结果]        │
│              │                      │
├──────────────┴──────────────────────┤
│         📊 笔记统计                  │
│            5 条笔记                 │
└─────────────────────────────────────┘
```

### 颜色说明

- **紫色渐变**：主题色，用于标题和按钮
- **蓝色标签**：相似度标签
- **紫色标签**：分类标签
- **绿色提示**：成功消息
- **红色提示**：错误消息

## 💡 使用技巧

### 1. 添加笔记

**最佳实践**：
- 使用清晰简洁的标题
- 内容详细具体
- 添加相关标签便于分类
- 选择合适的分类

**示例**：

```
标题：Python 装饰器学习
内容：装饰器是 Python 的一个强大特性，可以在不修改原函数的情况下增加额外功能。
      常见用途：日志记录、性能测试、权限验证等。
标签：Python,编程,学习
分类：技术笔记
```

### 2. 搜索笔记

**搜索策略**：
- 使用关键概念词（如"机器学习"而不是"学习"）
- 尝试不同的关键词组合
- 利用语义理解（搜索"AI"能找到"人工智能"）

**搜索示例**：

| 搜索词 | 能找到的笔记 |
|--------|------------|
| 机器学习 | 机器学习基础、深度学习、神经网络 |
| Python | Python 装饰器、Python 异步编程 |
| AI | 人工智能、机器学习、深度学习 |

### 3. 管理笔记

- **定期回顾**：使用搜索功能回顾旧笔记
- **标签系统**：建立统一的标签体系
- **分类管理**：使用有意义的分类名称

## 🔧 API 文档

Web 应用提供以下 REST API：

### 健康检查

```bash
GET /api/health

响应：
{
  "status": "ok",
  "message": "memU 笔记应用运行正常"
}
```

### 创建笔记

```bash
POST /api/notes
Content-Type: application/json

请求体：
{
  "title": "笔记标题",
  "content": "笔记内容",
  "tags": ["标签1", "标签2"],
  "category": "分类"
}

响应：
{
  "success": true,
  "message": "笔记 '笔记标题' 已保存",
  "data": {...}
}
```

### 搜索笔记

```bash
POST /api/notes/search
Content-Type: application/json

请求体：
{
  "query": "搜索关键词",
  "top_k": 10,
  "min_similarity": 0.3
}

响应：
{
  "success": true,
  "count": 5,
  "results": [
    {
      "memory_id": "abc123",
      "category": "activity",
      "content": "笔记内容...",
      "similarity_score": 0.85
    }
  ]
}
```

### 列出笔记

```bash
GET /api/notes

响应：
{
  "success": true,
  "count": 10,
  "results": [...]
}
```

## 🐛 故障排除

### 问题 1：无法访问 Web 应用

**症状**：浏览器显示"无法连接"

**解决方案**：
1. 检查 Web 服务器是否运行：
   ```bash
   lsof -i :8080
   ```
2. 如果未运行，启动服务器：
   ```bash
   cd note_app
   ./start_web.sh
   ```

### 问题 2：保存笔记失败

**症状**：点击保存后显示错误

**解决方案**：
1. 检查 memU 服务是否运行：
   ```bash
   lsof -i :8000
   ```
2. 查看浏览器控制台错误信息
3. 检查 Web 服务器日志：
   ```bash
   tail -f /tmp/note_web.log
   ```

### 问题 3：搜索无结果

**症状**：搜索后显示"没有找到相关笔记"

**可能原因**：
- 笔记还未生成嵌入向量（需要等待几秒）
- 搜索关键词不匹配
- 相似度阈值过高

**解决方案**：
- 等待几秒后再次搜索
- 尝试不同的关键词
- 降低相似度阈值（修改代码中的 `min_similarity`）

### 问题 4：代理错误

**症状**：502 Bad Gateway

**解决方案**：
清除代理环境变量后重启：
```bash
lsof -ti :8080 | xargs kill -9
cd note_app
unset http_proxy https_proxy HTTP_PROXY HTTPS_PROXY all_proxy ALL_PROXY
python3 web_server.py
```

## 📁 文件结构

```
note_app/
├── web_server.py          # FastAPI 后端服务
├── memu_note_client.py    # memU 客户端
├── start_web.sh           # 启动脚本
├── web/
│   └── index.html         # Web 前端界面
├── note_cli.py            # 命令行版本
├── note_gui.py            # 图形界面版本
└── requirements.txt       # Python 依赖
```

## 🚀 高级功能

### 自定义端口

编辑 `web_server.py`，修改端口号：

```python
uvicorn.run(
    app,
    host="0.0.0.0",
    port=8888,  # 修改为你想要的端口
    log_level="info",
)
```

### 自定义搜索参数

编辑 `web/index.html`，修改搜索参数：

```javascript
body: JSON.stringify({
    query,
    top_k: 20,           // 返回结果数量
    min_similarity: 0.1, // 最小相似度
}),
```

### 启用 HTTPS

使用 nginx 或其他反向代理配置 HTTPS。

## 📊 性能优化

### 提高搜索速度

1. **降低 top_k**：减少返回结果数量
2. **提高 min_similarity**：只返回高相关度结果
3. **使用更快的嵌入模型**：在 memU 配置中选择更小的模型

### 减少内存占用

1. **定期清理旧笔记**
2. **使用更小的嵌入模型**
3. **限制笔记内容长度**

## 🎯 使用场景

### 1. 学习笔记

- 记录课程内容
- 整理学习资料
- 复习知识点

### 2. 工作日志

- 记录每日工作
- 项目进展跟踪
- 问题解决方案

### 3. 想法收集

- 记录灵感
- 项目创意
- 产品想法

### 4. 知识管理

- 技术文档
- 最佳实践
- 经验总结

## 📖 相关文档

- **嵌入功能指南**：`EMBEDDING_ENABLED_SUCCESS.md`
- **使用指南**：`NOTE_APP_GUIDE.md`
- **命令行版本**：`note_app/README.md`

## 🎉 总结

### 优势

✅ **浏览器访问**：无需安装，随时随地使用
✅ **语义搜索**：智能理解搜索意图
✅ **美观界面**：现代化设计，使用体验好
✅ **实时更新**：即时保存，即时搜索
✅ **跨平台**：支持所有现代浏览器

### 下一步

1. **打开浏览器**：访问 http://localhost:8080
2. **添加第一条笔记**：尝试新建功能
3. **测试搜索**：体验语义搜索
4. **探索功能**：发现更多可能

---

**开始使用 memU 笔记 Web 应用，享受智能笔记的便利！** 🚀
