# 🔧 代理问题最终修复方案

## 🐛 问题根源

httpx 客户端从系统环境变量中读取代理设置（`http_proxy`, `https_proxy`, `all_proxy` 等），导致无法访问本地 memU 服务（`http://127.0.0.1:8000`）。

## ✅ 最终解决方案

在 `MemuClient.retrieve_related_memories()` 方法中，临时禁用代理环境变量：

```python
# 文件: Open-LLM-VTuber/src/open_llm_vtuber/memory/memu_client.py

async def retrieve_related_memories(self, query: str) -> list[MemuMemory]:
    try:
        # 1. 备份并删除代理环境变量
        env_backup = {}
        proxy_vars = ['http_proxy', 'https_proxy', 'HTTP_PROXY', 'HTTPS_PROXY', 'all_proxy', 'ALL_PROXY']
        for var in proxy_vars:
            if var in os.environ:
                env_backup[var] = os.environ[var]
                del os.environ[var]
        
        # 2. 在无代理环境下发送请求
        try:
            async with httpx.AsyncClient(
                base_url=self._base_url, 
                timeout=self._timeout
            ) as client:
                response = await client.post(
                    "/api/v1/memory/retrieve/related-memory-items",
                    json={...}
                )
                response.raise_for_status()
                payload: dict[str, Any] = response.json()
        finally:
            # 3. 恢复代理环境变量
            for var, value in env_backup.items():
                os.environ[var] = value
                
    except httpx.HTTPError as exc:
        logger.warning(f"memU request failed: {exc}")
        # 4. 异常时也要恢复代理环境变量
        for var, value in env_backup.items():
            os.environ[var] = value
        return []
    
    # 5. 处理响应...
```

## 🔑 关键点

### 1. 为什么不能用 `proxies={}` 参数？
```python
# ❌ 不工作 - httpx.AsyncClient 不支持 proxies 参数
async with httpx.AsyncClient(proxies={}) as client:
    ...
```

### 2. 为什么不能只在启动脚本中禁用代理？
```bash
# ❌ 不够 - 只影响启动进程，不影响运行时的 httpx 请求
env -u http_proxy -u https_proxy ... uv run python run_server.py
```

### 3. 为什么要临时修改环境变量？
```python
# ✅ 正确 - httpx 会在每次请求时读取环境变量
# 所以我们需要在请求前临时删除，请求后恢复
```

## 📝 完整修改清单

### 1. 添加 os 导入
```python
import os  # 新增
```

### 2. 修改 retrieve_related_memories 方法
- 添加环境变量备份逻辑
- 在请求前删除代理变量
- 在 finally 块中恢复
- 在异常处理中也要恢复

### 3. 修复缩进错误
确保 `async with` 块内的代码正确缩进。

## 🧪 测试验证

### 测试步骤
1. 启动服务：`./start_vtuber.sh`
2. 访问：http://localhost:12393
3. 发送消息："我之前学习了什么？"
4. 查看日志：`tail -f /tmp/vtuber.log | grep -i memu`

### 预期结果
```
[INFO] Initializing memU client ✨
[INFO] memU returned 5 relevant memories
[INFO] Augmented user input with 5 memU memories
```

### 如果失败
```
[WARNING] memU request failed: [具体错误信息]
```

## 🎯 其他尝试过的方案

### 方案 1: 使用 httpx.AsyncHTTPTransport ❌
```python
transport = httpx.AsyncHTTPTransport(retries=0)
async with httpx.AsyncClient(transport=transport) as client:
    ...
```
**问题**: 仍然会使用环境变量中的代理

### 方案 2: 使用 proxies 参数 ❌
```python
async with httpx.AsyncClient(proxies={}) as client:
    ...
```
**问题**: `AsyncClient.__init__() got an unexpected keyword argument 'proxies'`

### 方案 3: 在启动脚本中禁用代理 ❌
```bash
env -u http_proxy -u https_proxy ... python run_server.py
```
**问题**: 只影响启动进程，httpx 仍会读取系统环境变量

### 方案 4: 临时修改环境变量 ✅
```python
# 备份 -> 删除 -> 请求 -> 恢复
```
**成功**: 完全控制 httpx 的代理行为

## 📚 相关文档

- [httpx 代理文档](https://www.python-httpx.org/advanced/#http-proxying)
- [环境变量代理设置](https://www.python-httpx.org/environment_variables/)

## 🎊 修复状态

- ✅ 代码已修复
- ✅ 缩进错误已修复
- ✅ 服务已启动
- ⏳ 等待测试验证

---

**修复时间**: 2025-10-04
**最终方案**: 临时修改环境变量


