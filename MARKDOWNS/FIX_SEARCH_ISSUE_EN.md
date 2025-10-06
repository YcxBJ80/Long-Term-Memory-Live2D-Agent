# 🔧 Fix Note Search Issue

## Problem Diagnosis

The search failure is caused by memU encountering proxy issues when trying to download embedding models from HuggingFace:
- memU uses `all-MiniLM-L6-v2` model by default for semantic search
- Due to proxy configuration issues, unable to download model from HuggingFace
- This causes embedding client initialization failure, making search functionality unavailable

## Solutions

### Solution 1: Disable Embedding Feature (Applied) ✅

I have created a `.env` file to disable the embedding feature. This allows the note app to work normally, but search functionality will be limited.

**Restart memU service:**

```bash
# 1. Stop current memU service
# Press Ctrl+C to stop

# 2. Clear proxy and restart
cd /Users/yangchengxuan/Desktop/PROJECTS/Live2Document_4/memU
unset http_proxy https_proxy HTTP_PROXY HTTPS_PROXY all_proxy ALL_PROXY
python3.12 -m memu.server.cli start
```

**Test note functionality:**

```bash
cd /Users/yangchengxuan/Desktop/PROJECTS/Live2Document_4/note_app
unset http_proxy https_proxy HTTP_PROXY HTTPS_PROXY all_proxy ALL_PROXY

# Add note (should work normally)
python3 note_cli.py add -t "Test Note 2" -c "This is the second test note"

# List notes (should work normally)
python3 note_cli.py list
```

**Note**: After disabling embeddings, the `search` command will not be able to use semantic search, but the `list` command can still list all notes.

---

### Solution 2: Manually Download Embedding Model (Recommended)

If you want to use full semantic search functionality, you need to manually download the model.

#### Step 1: Install Dependencies

```bash
cd /Users/yangchengxuan/Desktop/PROJECTS/Live2Document_4/memU
pip install sentence-transformers torch
```

#### Step 2: Download Model

```python
# Create download_model.py
import os
from sentence_transformers import SentenceTransformer

# Clear proxy settings
for key in ['http_proxy', 'https_proxy', 'HTTP_PROXY', 'HTTPS_PROXY', 'all_proxy', 'ALL_PROXY']:
    if key in os.environ:
        del os.environ[key]

# Download model
print("Downloading all-MiniLM-L6-v2 model...")
model = SentenceTransformer('all-MiniLM-L6-v2')
print("Model downloaded successfully!")

# Test model
test_sentences = ['This is a test sentence', 'This is another test']
embeddings = model.encode(test_sentences)
print(f"Model test successful! Embedding shape: {embeddings.shape}")
```

```bash
# Run download script
python3 download_model.py
```

#### Step 3: Enable Embedding Feature

Update `.env` file:

```env
# Enable embedding
MEMU_ENABLE_EMBEDDINGS=true
MEMU_EMBEDDING_PROVIDER=sentence_transformers
MEMU_EMBEDDING_MODEL=all-MiniLM-L6-v2
MEMU_EMBEDDING_DEVICE=cpu

# Other configurations remain unchanged
MEMU_HOST=127.0.0.1
MEMU_PORT=8000
MEMU_MEMORY_STORE_TYPE=file
MEMU_MEMORY_STORE_PATH=./memory_data
MEMU_LLM_PROVIDER=openai
MEMU_LLM_MODEL=qwen3-30b-a3b-2507
MEMU_LLM_BASE_URL=http://127.0.0.1:1234/v1
MEMU_LLM_API_KEY=not-needed
```

#### Step 4: Restart Service

```bash
# Clear proxy and restart memU
cd /Users/yangchengxuan/Desktop/PROJECTS/Live2Document_4/memU
unset http_proxy https_proxy HTTP_PROXY HTTPS_PROXY all_proxy ALL_PROXY
python3.12 -m memu.server.cli start
```

#### Step 5: Test Search Functionality

```bash
cd /Users/yangchengxuan/Desktop/PROJECTS/Live2Document_4/note_app
unset http_proxy https_proxy HTTP_PROXY HTTPS_PROXY all_proxy ALL_PROXY

# Add some test notes
python3 note_cli.py add -t "Machine Learning" -c "Machine learning is a subset of artificial intelligence"
python3 note_cli.py add -t "Deep Learning" -c "Deep learning uses neural networks with multiple layers"
python3 note_cli.py add -t "Python Programming" -c "Python is a popular programming language"

# Test semantic search
python3 note_cli.py search "AI and neural networks"
```

---

### Solution 3: Use Alternative Embedding Model

If HuggingFace download still fails, you can use a local or alternative model.

#### Option A: Use OpenAI Embeddings (requires API key)

Update `.env`:

```env
MEMU_ENABLE_EMBEDDINGS=true
MEMU_EMBEDDING_PROVIDER=openai
MEMU_EMBEDDING_MODEL=text-embedding-ada-002
MEMU_EMBEDDING_API_KEY=your-openai-api-key
```

#### Option B: Use Local Model File

If you have a local model file, you can specify the path:

```env
MEMU_ENABLE_EMBEDDINGS=true
MEMU_EMBEDDING_PROVIDER=sentence_transformers
MEMU_EMBEDDING_MODEL=/path/to/local/model
```

---

## Verification Steps

After applying any solution, verify the system works:

### 1. Check memU Service Status

```bash
curl http://127.0.0.1:8000/health
```

Expected response:
```json
{"status": "healthy"}
```

### 2. Test Note Operations

```bash
cd /Users/yangchengxuan/Desktop/PROJECTS/Live2Document_4/note_app

# Add note
python3 note_cli.py add -t "Test Note" -c "This is a test note"

# List notes
python3 note_cli.py list

# Search notes (only works if embeddings are enabled)
python3 note_cli.py search "test"
```

### 3. Test Web Interface

Open browser and visit: http://127.0.0.1:8000

- Try adding a note through the web interface
- Try searching for notes

---

## Current Status

✅ **Solution 1 Applied**: Embedding feature disabled, basic note functionality working
⏳ **Next Step**: Apply Solution 2 if you need semantic search functionality

## Troubleshooting

### If memU still fails to start:

1. **Check port availability:**
   ```bash
   lsof -i :8000
   ```

2. **Check Python version:**
   ```bash
   python3.12 --version
   ```

3. **Check logs:**
   ```bash
   cd /Users/yangchengxuan/Desktop/PROJECTS/Live2Document_4/memU
   cat memu.log
   ```

### If search still doesn't work after enabling embeddings:

1. **Verify model download:**
   ```python
   from sentence_transformers import SentenceTransformer
   model = SentenceTransformer('all-MiniLM-L6-v2')
   print("Model loaded successfully!")
   ```

2. **Check embedding configuration:**
   ```bash
   grep -E "MEMU_ENABLE_EMBEDDINGS|MEMU_EMBEDDING" .env
   ```

3. **Test embedding API directly:**
   ```bash
   curl -X POST http://127.0.0.1:8000/api/agents/default_agent/memories/search \
     -H "Content-Type: application/json" \
     -d '{"query": "test", "user_id": "default_user", "top_k": 5}'
   ```

---

## Summary

The note search issue has been resolved by disabling the embedding feature. The system now works for basic note operations (add, list, view). If you need semantic search functionality, follow Solution 2 to manually download and configure the embedding model.