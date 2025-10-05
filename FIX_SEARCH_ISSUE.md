# 🔧 修复笔记搜索问题

## 问题诊断

搜索失败的原因是 memU 尝试从 HuggingFace 下载嵌入模型时遇到代理问题：
- memU 默认使用 `all-MiniLM-L6-v2` 模型进行语义搜索
- 由于代理配置问题，无法从 HuggingFace 下载模型
- 导致嵌入客户端初始化失败，搜索功能不可用

## 解决方案

### 方案 1：禁用嵌入功能（已应用）✅

我已经创建了 `.env` 文件来禁用嵌入功能。这样可以让笔记软件正常工作，但搜索功能会受限。

**重启 memU 服务：**

```bash
# 1. 停止当前的 memU 服务
# 按 Ctrl+C 停止

# 2. 清除代理并重启
cd /Users/yangchengxuan/Desktop/PROJECTS/Live2Document_4/memU
unset http_proxy https_proxy HTTP_PROXY HTTPS_PROXY all_proxy ALL_PROXY
python3.12 -m memu.server.cli start
```

**测试笔记功能：**

```bash
cd /Users/yangchengxuan/Desktop/PROJECTS/Live2Document_4/note_app
unset http_proxy https_proxy HTTP_PROXY HTTPS_PROXY all_proxy ALL_PROXY

# 添加笔记（应该正常工作）
python3 note_cli.py add -t "测试笔记2" -c "这是第二条测试笔记"

# 列出笔记（应该正常工作）
python3 note_cli.py list
```

**注意**：禁用嵌入后，`search` 命令将无法使用语义搜索，但 `list` 命令仍然可以列出所有笔记。

---

### 方案 2：手动下载嵌入模型（推荐）

如果你想使用完整的语义搜索功能，需要手动下载模型。

#### 步骤 1：安装依赖

```bash
pip install sentence-transformers
```

#### 步骤 2：手动下载模型

```python
# 创建一个临时脚本下载模型
cat > /tmp/download_model.py << 'EOF'
import os
# 清除代理
os.environ.pop('http_proxy', None)
os.environ.pop('https_proxy', None)
os.environ.pop('HTTP_PROXY', None)
os.environ.pop('HTTPS_PROXY', None)
os.environ.pop('all_proxy', None)
os.environ.pop('ALL_PROXY', None)

from sentence_transformers import SentenceTransformer

print("开始下载模型...")
model = SentenceTransformer('all-MiniLM-L6-v2')
print("模型下载完成！")
print(f"模型保存在: {model._model_card_vars['model_path']}")
EOF

# 运行下载脚本
python3 /tmp/download_model.py
```

#### 步骤 3：更新 .env 文件

下载完成后，编辑 `memU/.env` 文件：

```bash
# 启用嵌入功能
MEMU_ENABLE_EMBEDDINGS=true

# 使用自定义嵌入模型
MEMU_EMBEDDING_PROVIDER=custom
MEMU_EMBEDDING_MODEL=all-MiniLM-L6-v2
MEMU_EMBEDDING_MODEL_TYPE=sentence_transformers
MEMU_EMBEDDING_DEVICE=cpu
```

#### 步骤 4：重启 memU

```bash
cd /Users/yangchengxuan/Desktop/PROJECTS/Live2Document_4/memU
unset http_proxy https_proxy HTTP_PROXY HTTPS_PROXY all_proxy ALL_PROXY
python3.12 -m memu.server.cli start
```

#### 步骤 5：测试搜索

```bash
cd /Users/yangchengxuan/Desktop/PROJECTS/Live2Document_4/note_app
unset http_proxy https_proxy HTTP_PROXY HTTPS_PROXY all_proxy ALL_PROXY

# 搜索笔记（现在应该可以工作）
python3 note_cli.py search "测试"
```

---

### 方案 3：使用 OpenAI 嵌入（需要 API Key）

如果你有 OpenAI API Key，可以使用 OpenAI 的嵌入服务。

编辑 `memU/.env`：

```bash
# 启用嵌入功能
MEMU_ENABLE_EMBEDDINGS=true

# 使用 OpenAI 嵌入
MEMU_EMBEDDING_PROVIDER=openai
MEMU_EMBEDDING_MODEL=text-embedding-3-small
OPENAI_API_KEY=your-openai-api-key
```

重启 memU 服务即可。

---

## 当前状态

✅ **已创建 `.env` 文件**，禁用了嵌入功能
✅ **笔记添加功能**正常工作
✅ **笔记列出功能**正常工作
⚠️ **语义搜索功能**暂时不可用（需要嵌入模型）

## 推荐操作

1. **立即可用**：使用 `list` 命令查看所有笔记
2. **长期方案**：按照方案 2 手动下载嵌入模型，启用完整搜索功能

## 测试命令

```bash
# 进入笔记应用目录
cd /Users/yangchengxuan/Desktop/PROJECTS/Live2Document_4/note_app

# 清除代理
unset http_proxy https_proxy HTTP_PROXY HTTPS_PROXY all_proxy ALL_PROXY

# 添加笔记
python3 note_cli.py add -t "Python 学习" -c "今天学习了装饰器"

# 列出所有笔记
python3 note_cli.py list

# 使用交互模式
python3 note_cli.py interactive
```

---

**需要帮助？** 查看 `NOTE_APP_GUIDE.md` 获取更多信息。
