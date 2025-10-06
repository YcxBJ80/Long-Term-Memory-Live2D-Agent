# 🚀 快速开始指南

## 📋 系统概览

这个项目包含三个主要组件：

1. **memU** - 本地记忆管理系统（使用 SQLite + 语义检索）
2. **笔记应用** - 用于添加和管理笔记（CLI + GUI + Web）
3. **Open-LLM-VTuber** - AI 虚拟主播，集成了 memU 记忆检索

## 🎯 工作流程

```
添加笔记 → 存储到 memU → Open-LLM-VTuber 自动检索 → AI 基于记忆回答
```

## 🚀 快速启动（3 步）

### 步骤 1: 启动 memU 服务

```bash
cd /Users/yangchengxuan/Desktop/PROJECTS/Live2Document_4/memU
env -u http_proxy -u https_proxy -u HTTP_PROXY -u HTTPS_PROXY -u all_proxy -u ALL_PROXY \
  uv run python -m memu.server.cli
```

**验证**: 访问 http://127.0.0.1:8000/docs 应该能看到 API 文档

### 步骤 2: 启动 Open-LLM-VTuber

```bash
cd /Users/yangchengxuan/Desktop/PROJECTS/Live2Document_4/Open-LLM-VTuber
env -u http_proxy -u https_proxy -u HTTP_PROXY -u HTTPS_PROXY -u all_proxy -u ALL_PROXY \
  uv run python run_server.py
```

**验证**: 访问 http://localhost:12393 应该能看到 VTuber 界面

### 步骤 3: 开始使用！

现在你可以：
- 通过笔记应用添加笔记
- 与 Open-LLM-VTuber 对话，AI 会自动检索相关记忆

## 📝 添加笔记的 3 种方式

### 方式 1: 命令行（CLI）

```bash
cd /Users/yangchengxuan/Desktop/PROJECTS/Live2Document_4/note_app
env -u http_proxy -u https_proxy -u HTTP_PROXY -u HTTPS_PROXY -u all_proxy -u ALL_PROXY \
  python3 note_cli.py add "机器学习基础" "机器学习是人工智能的一个分支..."
```

### 方式 2: 图形界面（GUI）

```bash
cd /Users/yangchengxuan/Desktop/PROJECTS/Live2Document_4/note_app
env -u http_proxy -u https_proxy -u HTTP_PROXY -u HTTPS_PROXY -u all_proxy -u ALL_PROXY \
  python3 note_gui.py
```

### 方式 3: Web 界面（推荐）

```bash
cd /Users/yangchengxuan/Desktop/PROJECTS/Live2Document_4/note_app
env -u http_proxy -u https_proxy -u HTTP_PROXY -u HTTPS_PROXY -u all_proxy -u ALL_PROXY \
  python3 web_server.py
```

然后访问: http://localhost:8080

## 💡 使用示例

### 示例 1: 添加学习笔记

**使用 CLI:**
```bash
python3 note_cli.py add "深度学习入门" \
  "深度学习是机器学习的子集，使用多层神经网络。主要框架：TensorFlow、PyTorch、Keras。应用领域：计算机视觉、自然语言处理、语音识别。"
```

**使用 Web 界面:**
1. 打开 http://localhost:8080
2. 填写标题和内容
3. 标签留空（AI 会自动生成）
4. 点击"保存笔记"

### 示例 2: 与 AI 对话

1. 打开 http://localhost:12393
2. 输入问题："What did I learn about deep learning?"
3. AI 会自动检索相关笔记并基于记忆回答

### 示例 3: 搜索笔记

**使用 CLI:**
```bash
python3 note_cli.py search "深度学习"
```

**使用 Web 界面:**
1. 打开 http://localhost:8080
2. 在搜索框输入"深度学习"
3. 点击"搜索笔记"

## 🔧 常见问题

### Q1: memU 服务启动失败
**解决方案:**
```bash
# 检查端口是否被占用
lsof -i :8000

# 如果被占用，杀掉进程
lsof -ti :8000 | xargs kill -9

# 重新启动
cd /Users/yangchengxuan/Desktop/PROJECTS/Live2Document_4/memU
env -u http_proxy -u https_proxy -u HTTP_PROXY -u HTTPS_PROXY -u all_proxy -u ALL_PROXY \
  uv run python -m memu.server.cli
```

### Q2: Open-LLM-VTuber 启动失败
**解决方案:**
```bash
# 检查端口是否被占用
lsof -i :12393

# 如果被占用，杀掉进程
lsof -ti :12393 | xargs kill -9

# 重新启动
cd /Users/yangchengxuan/Desktop/PROJECTS/Live2Document_4/Open-LLM-VTuber
env -u http_proxy -u https_proxy -u HTTP_PROXY -u HTTPS_PROXY -u all_proxy -u ALL_PROXY \
  uv run python run_server.py
```

### Q3: AI 没有检索到记忆
**可能原因:**
1. memU 服务没有运行
2. user_id/agent_id 配置不匹配
3. 相似度阈值太高

**解决方案:**
```bash
# 1. 检查 memU 服务
lsof -i :8000

# 2. 检查配置
grep -A 6 "memu:" /Users/yangchengxuan/Desktop/PROJECTS/Live2Document_4/Open-LLM-VTuber/conf.yaml

# 应该显示:
#   user_id: 'note_user'
#   agent_id: 'note_agent'

# 3. 降低相似度阈值（如果需要）
# 编辑 conf.yaml，将 min_similarity 从 0.3 改为 0.2
```

### Q4: 笔记应用超时
**解决方案:**
```bash
# 确保没有设置代理
env | grep -i proxy

# 如果有代理，使用以下命令清除
unset http_proxy https_proxy HTTP_PROXY HTTPS_PROXY all_proxy ALL_PROXY

# 或者在命令前加上 env -u ...
```

## 📊 系统架构

```
┌─────────────────┐
│   笔记应用      │
│ (CLI/GUI/Web)   │
└────────┬────────┘
         │ POST /api/v1/memory/memorize
         ↓
┌─────────────────┐
│   memU 服务     │
│  (Port 8000)    │
│                 │
│ ┌─────────────┐ │
│ │   SQLite    │ │
│ └─────────────┘ │
│ ┌─────────────┐ │
│ │  Embeddings │ │
│ └─────────────┘ │
└────────┬────────┘
         │ POST /api/v1/memory/retrieve/related-memory-items
         ↓
┌─────────────────┐
│ Open-LLM-VTuber │
│  (Port 12393)   │
│                 │
│ ┌─────────────┐ │
│ │MemuClient   │ │
│ └─────────────┘ │
│ ┌─────────────┐ │
│ │ LLM Agent   │ │
│ └─────────────┘ │
└─────────────────┘
```

## 🎯 最佳实践

### 1. 笔记标题要清晰
✅ 好的标题: "机器学习基础 - 监督学习"
❌ 不好的标题: "笔记1"

### 2. 笔记内容要结构化
```
主题：机器学习基础

定义：
机器学习是人工智能的一个分支...

主要类别：
1. 监督学习（分类、回归）
2. 无监督学习（聚类、降维）
3. 强化学习

常用算法：
- 决策树
- 随机森林
- 神经网络
```

### 3. 使用自动标签
- 标签留空，让 AI 自动生成
- AI 会根据标题和内容提取关键词

### 4. 定期搜索和整理
```bash
# 列出所有笔记
python3 note_cli.py list

# 搜索特定主题
python3 note_cli.py search "机器学习"
```

## 📚 更多文档

- [memU 集成成功文档](./MEMU_INTEGRATION_SUCCESS.md) - 详细的集成说明
- [笔记应用指南](./WEB_APP_GUIDE.md) - Web 应用使用指南
- [自动标签功能](./AUTO_TAGS_FEATURE.md) - AI 自动标签说明

## 🎉 开始使用

现在你已经准备好了！按照上面的步骤启动服务，然后开始添加笔记和与 AI 对话吧！

**提示**: 第一次使用时，建议先添加几条笔记，然后与 AI 对话测试记忆检索功能。

---

**最后更新**: 2025-10-04
**状态**: ✅ 所有功能正常工作
