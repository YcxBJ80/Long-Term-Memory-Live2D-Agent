# Open-LLM-VTuber + memU Integration Setup Guide

## 📋 Prerequisites

1. **LMStudio**
   - Download and install LMStudio: https://lmstudio.ai/
   - Load model: `qwen3-30b-a3b-2507`
   - Start local server, listening on `http://127.0.0.1:1234`
   - Ensure OpenAI compatible API is enabled in LMStudio settings

2. **Python Environment**
   - Open-LLM-VTuber: Python 3.10+ (currently using 3.9.23, upgrade recommended)
   - memU: Python 3.12+ (configured)

## 🚀 Quick Start

### Method 1: Using Startup Script (Recommended)

```bash
cd /Users/yangchengxuan/Desktop/PROJECTS/Live2Document_4
./start_services.sh
```

### Method 2: Manual Startup

1. **Start LMStudio**
   - Open LMStudio application
   - Load `qwen3-30b-a3b-2507` model
   - Click "Start Server"

2. **Start memU Server**
   ```bash
   cd /Users/yangchengxuan/Desktop/PROJECTS/Live2Document_4/memU
   python3.12 -m memu.server.cli start
   ```
   - memU will run on `http://127.0.0.1:8000`
   - Data stored in `memU/memory_data/` directory

3. **Start Open-LLM-VTuber**
   ```bash
   cd /Users/yangchengxuan/Desktop/PROJECTS/Live2Document_4/Open-LLM-VTuber
   uv run python run_server.py
   ```
   - Service will run on `http://localhost:12393`
   - Open this address in browser to use

## 🔧 Configuration

### memU Configuration (`memU/.env`)

```env
# Server configuration
MEMU_HOST=127.0.0.1
MEMU_PORT=8000

# Memory storage
MEMU_MEMORY_STORE_TYPE=file
MEMU_MEMORY_STORE_PATH=./memory_data

# LLM configuration (using LMStudio)
MEMU_LLM_PROVIDER=openai
MEMU_LLM_MODEL=qwen3-30b-a3b-2507
MEMU_LLM_BASE_URL=http://127.0.0.1:1234/v1
MEMU_LLM_API_KEY=not-needed

# Embedding model (local)
MEMU_ENABLE_EMBEDDINGS=true
MEMU_EMBEDDING_PROVIDER=sentence_transformers
MEMU_EMBEDDING_MODEL=all-MiniLM-L6-v2
MEMU_EMBEDDING_DEVICE=cpu
```

### Open-LLM-VTuber Configuration (`Open-LLM-VTuber/conf.yaml`)

Key configuration items:

```yaml
# memU integration configuration
memu:
  enabled: true                          # Enable memU
  base_url: 'http://127.0.0.1:8000'     # memU API address
  user_id: 'default_user'                # User ID
  agent_id: 'default_agent'              # Agent ID
  top_k: 5                               # Number of memories returned per retrieval
  min_similarity: 0.3                    # Similarity threshold

# LLM configuration
llm:
  provider: 'lmstudio_llm'       # Use LMStudio
  # ... other configurations
```

## 📊 Workflow

1. **User Input** → Open-LLM-VTuber receives voice/text
2. **Memory Retrieval** → Automatically calls memU API to query related memories
3. **Context Enhancement** → Appends retrieved memories to user input
4. **LLM Processing** → LMStudio processes enhanced input
5. **Response Generation** → Generates voice/text response back to user

## 🔍 Test API

### Test memU API

```bash
# Clear proxy (if any)
unset http_proxy https_proxy

# Test memory retrieval
curl -X POST http://127.0.0.1:8000/api/agents/default_agent/memories/search \
  -H "Content-Type: application/json" \
  -d '{
    "query": "machine learning",
    "user_id": "default_user",
    "top_k": 5,
    "min_similarity": 0.3
  }'
```

### Test LMStudio API

```bash
curl http://127.0.0.1:1234/v1/models
```

## 📝 Log Locations

- **memU logs**: `memU/memu.log`
- **Open-LLM-VTuber logs**: Console output
- **memU data**: `memU/memory_data/`

## ⚠️ Common Issues

### 1. memU startup failure
- Check if Python version is 3.12+
- Check if port 8000 is occupied: `lsof -i :8000`
- View logs: `cat memU/memu.log`

### 2. LMStudio connection failure
- Ensure LMStudio application is running
- Ensure model is loaded
- Ensure server is started (click "Start Server" in LMStudio)
- Test connection: `curl http://127.0.0.1:1234/v1/models`

### 3. Open-LLM-VTuber cannot start
- Check if port 12393 is occupied
- Ensure `conf.yaml` configuration is correct
- Run `uv sync` to ensure dependencies are installed

### 4. Memory retrieval not working
- Check if `memu.enabled` in `conf.yaml` is `true`
- Check if memU service is running normally
- Look for memU-related errors in Open-LLM-VTuber logs

## 🛠️ Advanced Configuration

### Adjust memory retrieval parameters

In `conf.yaml`:

```yaml
memu:
  top_k: 10              # Increase number of returned memories
  min_similarity: 0.5    # Increase similarity threshold (stricter)
```

### Use different embedding model

In `memU/.env`:

```env
# Use larger model (more accurate but slower)
MEMU_EMBEDDING_MODEL=all-mpnet-base-v2

# Use multilingual model
MEMU_EMBEDDING_MODEL=paraphrase-multilingual-MiniLM-L12-v2
```

### Switch to GPU acceleration

In `memU/.env`:

```env
MEMU_EMBEDDING_DEVICE=cuda  # or mps (macOS)
```

## 📚 More Information

- **Open-LLM-VTuber Documentation**: https://github.com/t41372/Open-LLM-VTuber
- **memU Documentation**: https://github.com/NevaMind-AI/MemU
- **LMStudio Documentation**: https://lmstudio.ai/docs

## 🎉 Get Started

1. Ensure LMStudio is running and model is loaded
2. Run `./start_services.sh`
3. Open `http://localhost:12393` in browser
4. Start chatting with your AI VTuber!

The system will automatically remember your conversations and use these memories to provide more personalized responses in future conversations.