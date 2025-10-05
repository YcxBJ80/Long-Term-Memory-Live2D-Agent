# Open-LLM-VTuber + memU 集成设置指南

## 📋 前置要求

1. **LMStudio**
   - 下载并安装 LMStudio: https://lmstudio.ai/
   - 加载模型: `openai/gpt-oss-20b`
   - 启动本地服务器，监听在 `http://127.0.0.1:1234`
   - 在 LMStudio 设置中确保启用了 OpenAI 兼容 API

2. **Python 环境**
   - Open-LLM-VTuber: Python 3.10+ (当前使用 3.9.23，建议升级)
   - memU: Python 3.12+ (已配置)

## 🚀 快速启动

### 方式一：使用启动脚本（推荐）

```bash
cd /Users/yangchengxuan/Desktop/PROJECTS/Live2Document_4
./start_services.sh
```

### 方式二：手动启动

1. **启动 LMStudio**
   - 打开 LMStudio 应用
   - 加载 `openai/gpt-oss-20b` 模型
   - 点击 "Start Server"

2. **启动 memU 服务器**
   ```bash
   cd /Users/yangchengxuan/Desktop/PROJECTS/Live2Document_4/memU
   python3.12 -m memu.server.cli start
   ```
   - memU 将在 `http://127.0.0.1:8000` 运行
   - 数据存储在 `memU/memory_data/` 目录

3. **启动 Open-LLM-VTuber**
   ```bash
   cd /Users/yangchengxuan/Desktop/PROJECTS/Live2Document_4/Open-LLM-VTuber
   uv run python run_server.py
   ```
   - 服务将在 `http://localhost:12393` 运行
   - 在浏览器中打开此地址即可使用

## 🔧 配置说明

### memU 配置 (`memU/.env`)

```env
# 服务器配置
MEMU_HOST=0.0.0.0
MEMU_PORT=8000

# 内存存储
MEMU_MEMORY_DIR=./memory_data
MEMU_ENABLE_EMBEDDINGS=true

# LLM 配置（使用 LMStudio）
MEMU_LLM_PROVIDER=openai
OPENAI_API_KEY=lm-studio
OPENAI_BASE_URL=http://127.0.0.1:1234/v1
MEMU_OPENAI_MODEL=openai/gpt-oss-20b

# 嵌入模型（本地）
MEMU_EMBEDDING_PROVIDER=custom
MEMU_EMBEDDING_MODEL=all-MiniLM-L6-v2
MEMU_EMBEDDING_MODEL_TYPE=sentence_transformers
MEMU_EMBEDDING_DEVICE=cpu
```

### Open-LLM-VTuber 配置 (`Open-LLM-VTuber/conf.yaml`)

关键配置项：

```yaml
system_config:
  # memU 集成配置
  memu:
    enabled: true                          # 启用 memU
    base_url: 'http://127.0.0.1:8000'     # memU API 地址
    user_id: 'default_user'                # 用户 ID
    agent_id: 'default_agent'              # 智能体 ID
    top_k: 5                               # 每次检索返回的记忆数量
    min_similarity: 0.3                    # 相似度阈值

character_config:
  agent_config:
    agent_settings:
      basic_memory_agent:
        llm_provider: 'lmstudio_llm'       # 使用 LMStudio

  llm_configs:
    lmstudio_llm:
      base_url: 'http://127.0.0.1:1234/v1'
      model: 'openai/gpt-oss-20b'
      temperature: 0.7
```

## 📊 工作流程

1. **用户输入** → Open-LLM-VTuber 接收语音/文本
2. **记忆检索** → 自动调用 memU API 查询相关记忆
3. **上下文增强** → 将检索到的记忆附加到用户输入
4. **LLM 处理** → LMStudio 处理增强后的输入
5. **响应生成** → 生成语音/文本响应返回用户

## 🔍 测试 API

### 测试 memU API

```bash
# 清除代理（如果有）
unset http_proxy https_proxy HTTP_PROXY HTTPS_PROXY all_proxy ALL_PROXY

# 测试记忆检索
curl -X POST http://127.0.0.1:8000/api/v1/memory/retrieve/related-memory-items \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "default_user",
    "agent_id": "default_agent",
    "query": "hello",
    "top_k": 5,
    "min_similarity": 0.3
  }'
```

### 测试 LMStudio API

```bash
curl http://127.0.0.1:1234/v1/models
```

## 📝 日志位置

- **memU 日志**: `memU/memu.log`
- **Open-LLM-VTuber 日志**: 控制台输出
- **memU 数据**: `memU/memory_data/`

## ⚠️ 常见问题

### 1. memU 启动失败
- 检查 Python 版本是否为 3.12+
- 检查端口 8000 是否被占用: `lsof -i :8000`
- 查看日志: `cat memU/memu.log`

### 2. LMStudio 连接失败
- 确保 LMStudio 应用正在运行
- 确保模型已加载
- 确保服务器已启动（在 LMStudio 中点击 "Start Server"）
- 测试连接: `curl http://127.0.0.1:1234/v1/models`

### 3. Open-LLM-VTuber 无法启动
- 检查端口 12393 是否被占用
- 确保 `conf.yaml` 配置正确
- 运行 `uv sync` 确保依赖已安装

### 4. 记忆检索不工作
- 检查 `conf.yaml` 中 `memu.enabled` 是否为 `true`
- 检查 memU 服务是否正常运行
- 查看 Open-LLM-VTuber 日志中是否有 memU 相关错误

## 🛠️ 高级配置

### 调整记忆检索参数

在 `conf.yaml` 中修改：

```yaml
system_config:
  memu:
    top_k: 10              # 增加返回的记忆数量
    min_similarity: 0.5    # 提高相似度阈值（更严格）
```

### 使用不同的嵌入模型

在 `memU/.env` 中修改：

```env
# 使用更大的模型（更准确但更慢）
MEMU_EMBEDDING_MODEL=all-mpnet-base-v2

# 使用多语言模型
MEMU_EMBEDDING_MODEL=paraphrase-multilingual-MiniLM-L12-v2
```

### 切换到 GPU 加速

在 `memU/.env` 中修改：

```env
MEMU_EMBEDDING_DEVICE=cuda  # 或 mps (macOS)
```

## 📚 更多信息

- **Open-LLM-VTuber 文档**: https://github.com/t41372/Open-LLM-VTuber
- **memU 文档**: https://github.com/NevaMind-AI/MemU
- **LMStudio 文档**: https://lmstudio.ai/docs

## 🎉 开始使用

1. 确保 LMStudio 正在运行并加载了模型
2. 运行 `./start_services.sh`
3. 在浏览器中打开 `http://localhost:12393`
4. 开始与你的 AI VTuber 对话！

系统会自动记住你们的对话，并在未来的对话中使用这些记忆来提供更个性化的响应。
