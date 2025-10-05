# 📝 memU 笔记软件使用指南

## 🎉 简介

这是一个将笔记直接存储到 memU 记忆库的笔记应用。所有笔记都会自动保存到 memU 中，并可以通过语义搜索快速找到相关内容。

## 📦 文件结构

```
note_app/
├── memu_note_client.py    # memU 客户端封装
├── note_cli.py             # 命令行版本
├── note_gui.py             # 图形界面版本
├── start_note_app.sh       # 启动脚本
├── demo.sh                 # 演示脚本
├── requirements.txt        # Python 依赖
├── README.md               # 完整文档
└── QUICKSTART.md           # 快速开始指南
```

## 🚀 快速开始

### 1. 安装依赖

```bash
cd note_app
pip install -r requirements.txt
```

### 2. 确保 memU 服务运行

```bash
# 检查 memU 是否运行
lsof -i :8000

# 如果未运行，启动 memU
cd ../memU
python3.12 -m memu.server.cli start
```

### 3. 运行笔记软件

#### 方式 1: 使用启动脚本（推荐）

```bash
cd note_app
./start_note_app.sh
```

#### 方式 2: 直接运行

```bash
# 清除代理（重要！）
unset http_proxy https_proxy HTTP_PROXY HTTPS_PROXY all_proxy ALL_PROXY

# 命令行模式
python3 note_cli.py add -t "标题" -c "内容"

# 交互模式
python3 note_cli.py interactive

# 图形界面
python3 note_gui.py
```

## 💡 使用示例

### 添加笔记

```bash
python3 note_cli.py add \
  -t "Python 学习笔记" \
  -c "今天学习了装饰器的使用方法" \
  --tags "Python,学习" \
  --category "技术笔记"
```

### 搜索笔记

```bash
python3 note_cli.py search "Python 装饰器"
```

### 列出所有笔记

```bash
python3 note_cli.py list
```

### 交互模式

```bash
python3 note_cli.py interactive
```

## 🎨 功能特性

### ✅ 核心功能

- **直接存储到 memU**: 所有笔记自动保存到 memU 记忆库
- **语义搜索**: 使用 memU 的语义搜索功能查找相关笔记
- **标签和分类**: 支持为笔记添加标签和分类
- **时间戳**: 自动记录笔记创建时间
- **多种界面**: 命令行、交互式、图形界面三种模式

### 📊 数据格式

笔记在 memU 中的存储格式：

```
[笔记] 标题

内容

标签: tag1, tag2

记录时间: 2025-10-04 18:00:00
```

### 🔍 搜索参数

- `top_k`: 返回结果数量（默认: 10）
- `min_similarity`: 最小相似度阈值（默认: 0.3）

## ⚙️ 配置

### 默认配置

```python
base_url = "http://127.0.0.1:8000"  # memU API 地址
user_id = "note_user"                # 用户 ID
user_name = "笔记用户"               # 用户名称
agent_id = "note_agent"              # 智能体 ID
agent_name = "笔记助手"              # 智能体名称
timeout = 30.0                       # 超时时间（秒）
```

### 自定义配置

```bash
python3 note_cli.py \
  --base-url http://localhost:8000 \
  --user-id my_user \
  --agent-id my_agent \
  add -t "标题" -c "内容"
```

## 🐛 常见问题

### 1. 代理错误

**错误**: `Using SOCKS proxy, but the 'socksio' package is not installed`

**解决**: 清除代理环境变量

```bash
unset http_proxy https_proxy HTTP_PROXY HTTPS_PROXY all_proxy ALL_PROXY
```

### 2. 搜索超时

**错误**: `timed out`

**原因**: memU 的嵌入模型正在初始化（首次运行需要下载模型）

**解决**: 
- 等待模型下载完成
- 增加超时时间：修改 `memu_note_client.py` 中的 `timeout` 参数

### 3. memU 连接失败

**错误**: `Connection refused`

**解决**: 确保 memU 服务正在运行

```bash
lsof -i :8000
```

### 4. 图形界面无法启动

**错误**: `No module named 'tkinter'`

**解决**: 安装 tkinter

```bash
# macOS
brew install python-tk

# Ubuntu/Debian
sudo apt-get install python3-tk
```

## 📖 完整文档

- **README.md**: 完整的功能文档和 API 参考
- **QUICKSTART.md**: 快速开始指南
- **demo.sh**: 运行演示脚本查看功能

## 🎬 运行演示

```bash
cd note_app
./demo.sh
```

演示脚本会：
1. 添加 3 条示例笔记
2. 列出所有笔记
3. 搜索笔记

## 🌟 使用技巧

### 1. 标签策略

为笔记添加有意义的标签：

```bash
# 技术笔记
--tags "Python,编程,学习"

# 工作日志
--tags "工作,日志,项目名"

# 想法记录
--tags "创意,产品,想法"
```

### 2. 分类管理

使用清晰的分类：

- `技术笔记`: 编程、技术学习
- `工作日志`: 工作记录、项目进展
- `生活`: 生活琐事、个人想法
- `学习`: 学习笔记、读书笔记

### 3. 搜索优化

- 使用具体的关键词
- 可以搜索标题、内容、标签
- 调整 `min_similarity` 控制结果精度

### 4. 内容组织

- 标题简洁明了
- 内容结构清晰
- 使用换行分段

## 🔗 集成说明

### 与 Open-LLM-VTuber 集成

笔记软件使用的 memU 记忆库与 Open-LLM-VTuber 共享。这意味着：

1. **笔记可被 VTuber 访问**: VTuber 可以在对话中引用你的笔记
2. **对话可被笔记搜索**: 你可以搜索 VTuber 的对话记录
3. **统一的记忆系统**: 笔记和对话存储在同一个记忆库中

### 数据隔离

如果需要隔离笔记和 VTuber 的数据，使用不同的 `user_id` 和 `agent_id`：

```bash
# 笔记专用
python3 note_cli.py --user-id note_user --agent-id note_agent

# VTuber 专用（在 conf.yaml 中配置）
memu:
  user_id: vtuber_user
  agent_id: vtuber_agent
```

## 📊 性能说明

- **添加笔记**: 通常 < 1 秒
- **搜索笔记**: 取决于记忆库大小和嵌入模型
  - 小型库（< 100 条）: 1-3 秒
  - 中型库（100-1000 条）: 3-10 秒
  - 大型库（> 1000 条）: 10+ 秒

## 🎯 下一步

1. **运行演示**: `./demo.sh`
2. **添加你的第一条笔记**: 使用交互模式
3. **探索图形界面**: `python3 note_gui.py`
4. **查看完整文档**: 阅读 `README.md`

## 💬 反馈

如有问题或建议，欢迎反馈！

---

**祝你使用愉快！📝✨**
