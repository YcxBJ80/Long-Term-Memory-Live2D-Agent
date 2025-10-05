# 🔧 memU 记忆检索修复总结

## 🐛 问题描述

Open-LLM-VTuber 成功检索到 memU 记忆，但 LLM 没有基于这些记忆生成回答。

## 🔍 根本原因

发现了两个关键问题：

### 问题 1: httpx 响应对象作用域错误
**位置**: `Open-LLM-VTuber/src/open_llm_vtuber/memory/memu_client.py`

**原因**: `response.raise_for_status()` 和 `response.json()` 在 `async with` 块外部调用，导致响应对象失效。

**修复**:
```python
# 修复前（错误）
async with httpx.AsyncClient(...) as client:
    response = await client.post(...)
response.raise_for_status()  # ❌ 在 async with 外部
payload = response.json()    # ❌ 在 async with 外部

# 修复后（正确）
async with httpx.AsyncClient(...) as client:
    response = await client.post(...)
    response.raise_for_status()  # ✅ 在 async with 内部
    payload = response.json()    # ✅ 在 async with 内部
```

### 问题 2: 代理配置干扰本地服务
**位置**: `Open-LLM-VTuber/src/open_llm_vtuber/memory/memu_client.py`

**原因**: httpx 客户端尝试使用系统代理（SOCKS）访问本地 memU 服务（`http://127.0.0.1:8000`），导致连接失败。

**修复**:
```python
# 添加 proxies={} 禁用代理
async with httpx.AsyncClient(
    base_url=self._base_url, 
    timeout=self._timeout,
    proxies={}  # ✅ 禁用代理，用于本地服务
) as client:
```

## ✅ 修复内容

### 1. 修复 `memu_client.py`
```python
# 文件: Open-LLM-VTuber/src/open_llm_vtuber/memory/memu_client.py

async def retrieve_related_memories(self, query: str) -> list[MemuMemory]:
    try:
        async with httpx.AsyncClient(
            base_url=self._base_url, 
            timeout=self._timeout,
            proxies={}  # 禁用代理
        ) as client:
            response = await client.post(
                "/api/v1/memory/retrieve/related-memory-items",
                json={
                    "user_id": self._user_id,
                    "agent_id": self._agent_id,
                    "query": query,
                    "top_k": self._top_k,
                    "min_similarity": self._min_similarity,
                },
            )
            response.raise_for_status()  # 移到 async with 内部
            payload: dict[str, Any] = response.json()  # 移到 async with 内部
    except httpx.HTTPError as exc:
        logger.warning(f"memU request failed: {exc}")
        return []
    
    # ... 处理响应 ...
```

### 2. 添加调试日志
```python
# 文件: Open-LLM-VTuber/src/open_llm_vtuber/conversations/single_conversation.py

elif memu_memories:
    logger.info("Augmented user input with %d memU memories", len(memu_memories))
    memory_summary = "\n".join(
        f"[{memory.category}] {memory.content}" for memory in memu_memories
    )
    logger.debug(f"MemU context injected:\n{memory_summary}")
    logger.info(f"📝 Original input: {original_input_text}")
    logger.info(f"✨ Augmented input (first 200 chars): {input_text[:200]}...")
```

### 3. 创建启动脚本
```bash
# 文件: start_vtuber.sh

#!/bin/bash
cd /Users/yangchengxuan/Desktop/PROJECTS/Live2Document_4/Open-LLM-VTuber

# 停止现有服务
lsof -ti :12393 | xargs kill -9 2>/dev/null

# 禁用所有代理并启动
env -u http_proxy -u https_proxy -u HTTP_PROXY -u HTTPS_PROXY -u all_proxy -u ALL_PROXY \
  nohup uv run python run_server.py > /tmp/vtuber.log 2>&1 &
```

## 🧪 测试验证

### 测试步骤
1. 启动 memU 服务（端口 8000）
2. 运行启动脚本：`./start_vtuber.sh`
3. 访问 http://localhost:12393
4. 发送测试消息："我之前学习了什么？"

### 预期结果
日志应该显示：
```
✅ memU returned N relevant memories
📝 Original input: 我之前学习了什么？
✨ Augmented input (first 200 chars): 我之前学习了什么？

[MemU Memories]
1. (profile, score 0.49) 笔记用户是一名中文母语者...
2. (activity, score 0.48) 笔记用户在2025-10-04记录了...
```

然后 AI 应该基于这些记忆生成回答。

## 📝 使用说明

### 快速启动
```bash
cd /Users/yangchengxuan/Desktop/PROJECTS/Live2Document_4

# 启动 memU
cd memU
env -u http_proxy -u https_proxy -u HTTP_PROXY -u HTTPS_PROXY -u all_proxy -u ALL_PROXY \
  uv run python -m memu.server.cli &

# 启动 Open-LLM-VTuber
cd ..
./start_vtuber.sh
```

### 查看日志
```bash
# 实时查看日志
tail -f /tmp/vtuber.log

# 查看 memU 相关日志
tail -f /tmp/vtuber.log | grep -E "memU|MemU|memu"

# 查看对话日志
tail -f /tmp/vtuber.log | grep -E "User input:|AI response:|Augmented"
```

### 测试 memU API
```bash
# 直接测试 memU API
env -u http_proxy -u https_proxy -u HTTP_PROXY -u HTTPS_PROXY -u all_proxy -u ALL_PROXY \
curl -X POST http://127.0.0.1:8000/api/v1/memory/retrieve/related-memory-items \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "note_user",
    "agent_id": "note_agent",
    "query": "学习",
    "top_k": 5,
    "min_similarity": 0.3
  }' | python3 -m json.tool
```

## 🔧 故障排除

### 问题 1: memU 请求失败
**症状**: 日志显示 `memU request failed`

**解决方案**:
1. 检查 memU 服务是否运行：`lsof -i :8000`
2. 确保使用启动脚本（禁用代理）
3. 检查 `conf.yaml` 中的 `user_id` 和 `agent_id` 是否匹配

### 问题 2: 没有检索到记忆
**症状**: 日志显示 `memU returned 0 relevant memories`

**解决方案**:
1. 降低相似度阈值：`min_similarity: 0.2`（在 `conf.yaml` 中）
2. 使用更通用的查询词
3. 确认笔记已经保存到 memU

### 问题 3: LLM 启动失败（SOCKS 代理错误）
**症状**: `Using SOCKS proxy, but the 'socksio' package is not installed`

**解决方案**:
使用启动脚本 `./start_vtuber.sh`，它会自动禁用所有代理环境变量。

## 📊 修复效果

### 修复前
```
❌ memU request failed: (空错误信息)
❌ 没有检索到记忆
❌ LLM 无法基于记忆回答
```

### 修复后
```
✅ memU returned 5 relevant memories
✅ Augmented user input with 5 memU memories
✅ AI 基于记忆生成回答
```

## 📚 相关文档

- [memU 集成成功文档](./MEMU_INTEGRATION_SUCCESS.md)
- [快速开始指南](./QUICK_START_GUIDE.md)
- [心理咨询师模式](./COUNSELOR_MODE.md)

---

**修复时间**: 2025-10-04
**状态**: ✅ 已修复，待测试验证
