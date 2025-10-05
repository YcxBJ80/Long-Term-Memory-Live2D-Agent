# 📝 memU 笔记软件

将笔记直接存储到 memU 记忆库中的笔记应用。

## 🌟 特性

- ✅ 直接将笔记存储到 memU 记忆库
- ✅ 支持标题、内容、标签和分类
- ✅ 语义搜索笔记内容
- ✅ 命令行和图形界面两种模式
- ✅ 自动记录时间戳
- ✅ 支持批量查看和管理

## 📦 安装

### 依赖

```bash
pip install httpx
```

对于图形界面版本，还需要 tkinter（Python 通常自带）。

## 🚀 使用方法

### 1. 命令行版本

#### 基本命令

```bash
# 添加笔记
python note_cli.py add -t "笔记标题" -c "笔记内容" --tags "标签1,标签2"

# 搜索笔记
python note_cli.py search "关键词"

# 列出所有笔记
python note_cli.py list

# 交互模式
python note_cli.py interactive
```

#### 示例

```bash
# 添加一条技术笔记
python note_cli.py add \
  -t "Python 装饰器学习" \
  -c "装饰器是一种设计模式，可以在不修改原函数的情况下增加额外功能。使用 @decorator 语法。" \
  --tags "Python,编程,学习" \
  --category "技术笔记"

# 搜索关于 Python 的笔记
python note_cli.py search "Python 装饰器"

# 搜索并限制结果数量
python note_cli.py search "Python" -l 5 -s 0.5
```

#### 交互模式

```bash
python note_cli.py interactive
```

在交互模式中，你可以：
- 输入 `add` 添加新笔记
- 输入 `search` 搜索笔记
- 输入 `list` 列出所有笔记
- 输入 `quit` 退出

### 2. 图形界面版本

```bash
python note_gui.py
```

图形界面提供：
- **新建笔记**标签页：创建和保存新笔记
- **搜索笔记**标签页：搜索和浏览笔记

#### 操作说明

1. **添加笔记**：
   - 在"新建笔记"标签页填写标题、内容、标签和分类
   - 点击"保存笔记"按钮

2. **搜索笔记**：
   - 在"搜索笔记"标签页输入关键词
   - 点击"搜索"或按回车键
   - 双击结果查看详情

3. **查看所有笔记**：
   - 点击"显示全部"按钮

### 3. Python API

```python
from memu_note_client import MemuNoteClient

# 创建客户端
client = MemuNoteClient(
    base_url="http://127.0.0.1:8000",
    user_id="note_user",
    agent_id="note_agent",
)

# 保存笔记
client.save_note(
    title="我的笔记",
    content="这是笔记内容",
    tags=["标签1", "标签2"],
    category="工作笔记",
)

# 搜索笔记
results = client.search_notes("关键词", top_k=10, min_similarity=0.3)

for note in results:
    print(f"相似度: {note['similarity_score']:.2%}")
    print(f"内容: {note['content']}")
```

## ⚙️ 配置

### memU 服务器配置

默认配置：
- **API 地址**: `http://127.0.0.1:8000`
- **用户 ID**: `note_user`
- **智能体 ID**: `note_agent`

可以通过命令行参数修改：

```bash
python note_cli.py --base-url http://localhost:8000 \
                   --user-id my_user \
                   --agent-id my_agent \
                   add -t "标题" -c "内容"
```

## 📊 数据格式

笔记在 memU 中以对话格式存储：

```json
{
  "user_id": "note_user",
  "agent_id": "note_agent",
  "conversation": [
    {
      "role": "user",
      "content": "[笔记] 标题\n\n内容\n\n标签: tag1, tag2\n\n记录时间: 2025-10-04 18:00:00"
    }
  ],
  "metadata": {
    "type": "note",
    "title": "标题",
    "category": "分类",
    "tags": ["tag1", "tag2"],
    "timestamp": "2025-10-04 18:00:00"
  }
}
```

## 🔍 搜索功能

笔记软件使用 memU 的语义搜索功能：

- **语义理解**：不仅匹配关键词，还理解语义
- **相似度评分**：每个结果都有相似度分数
- **可调参数**：
  - `top_k`：返回结果数量
  - `min_similarity`：最小相似度阈值（0.0-1.0）

## 💡 使用技巧

1. **标签使用**：
   - 为笔记添加相关标签，便于分类和搜索
   - 标签会被包含在搜索内容中

2. **分类管理**：
   - 使用有意义的分类名称（如"工作"、"学习"、"生活"）
   - 分类也会参与语义搜索

3. **搜索优化**：
   - 使用具体的关键词
   - 可以搜索标题、内容、标签中的任何信息
   - 调整 `min_similarity` 参数控制结果精度

4. **内容组织**：
   - 笔记标题应简洁明了
   - 内容可以包含多段文字
   - 使用换行组织内容结构

## 🛠️ 故障排除

### memU 连接失败

确保 memU 服务正在运行：

```bash
# 检查 memU 是否运行
lsof -i :8000

# 如果未运行，启动 memU
cd /path/to/memU
python3.12 -m memu.server.cli start
```

### 搜索返回空结果

1. 检查是否有笔记：
   ```bash
   python note_cli.py list
   ```

2. 降低相似度阈值：
   ```bash
   python note_cli.py search "关键词" -s 0.1
   ```

3. 确保 memU 的嵌入模型已正确初始化

### 图形界面无法启动

确保安装了 tkinter：

```bash
# macOS
brew install python-tk

# Ubuntu/Debian
sudo apt-get install python3-tk

# Windows
# tkinter 通常随 Python 一起安装
```

## 📝 示例场景

### 学习笔记

```bash
python note_cli.py add \
  -t "机器学习基础" \
  -c "监督学习：从标注数据中学习。包括分类和回归。\n无监督学习：从未标注数据中发现模式。包括聚类和降维。" \
  --tags "机器学习,AI,学习" \
  --category "学习笔记"
```

### 工作日志

```bash
python note_cli.py add \
  -t "2025-10-04 工作日志" \
  -c "今天完成了 memU 集成，实现了笔记应用。下一步计划添加更多功能。" \
  --tags "工作,日志" \
  --category "工作"
```

### 想法记录

```bash
python note_cli.py add \
  -t "产品创意" \
  -c "可以开发一个基于 memU 的个人知识管理系统，整合笔记、文档、对话记录。" \
  --tags "创意,产品" \
  --category "想法"
```

## 🔗 相关链接

- [memU 项目](https://github.com/NevaMind-AI/MemU)
- [Open-LLM-VTuber 项目](https://github.com/t41372/Open-LLM-VTuber)

## 📄 许可证

本项目遵循 MIT 许可证。
