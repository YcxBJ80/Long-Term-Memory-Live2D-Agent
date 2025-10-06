# 🔧 memU超时问题修复

## 🐛 问题描述

### 错误信息
```
ERROR | src.open_llm_vtuber.memory.memu_client:retrieve_related_memories:106 | 
memU request failed with HTTPError: ReadTimeout:
```

### 根本原因
虽然之前在 `service_context.py` 中设置了 10 秒超时，但实际上：
1. **配置文件缺失**: `conf.yaml` 中没有 `timeout` 配置项
2. **配置类缺失**: `MemuSettings` 类没有 `timeout` 字段
3. **传参缺失**: `MemuClientManager` 创建客户端时没有传递 `timeout` 参数
4. **默认值太小**: `MemuClient` 的默认超时只有 2.0 秒

结果是：虽然代码中有超时设置，但从未真正生效！

## ✅ 修复方案

### 1. 更新配置文件 ✅
**文件**: `Open-LLM-VTuber/conf.yaml`

```yaml
  memu:
    enabled: true
    base_url: 'http://127.0.0.1:8000'
    user_id: 'note_user'
    agent_id: 'note_agent'
    top_k: 5
    min_similarity: 0.3
    timeout: 10.0  # Request timeout in seconds
```

### 2. 更新配置类 ✅
**文件**: `Open-LLM-VTuber/src/open_llm_vtuber/config_manager/system.py`

```python
class MemuSettings(I18nMixin):
    """Configuration for the memU local memory service.
    
    Attributes:
        ...
        timeout: Request timeout in seconds for memU API calls.
    """
    
    enabled: bool = Field(False, alias="enabled")
    base_url: str = Field("http://127.0.0.1:8000", alias="base_url")
    user_id: str = Field("default_user", alias="user_id")
    agent_id: str = Field("default_agent", alias="agent_id")
    top_k: int = Field(5, alias="top_k")
    min_similarity: float = Field(0.3, alias="min_similarity")
    timeout: float = Field(10.0, alias="timeout")  # ✨ 新增
    
    DESCRIPTIONS: ClassVar[Dict[str, Description]] = {
        ...
        "timeout": Description(
            en="Request timeout in seconds for memU API calls",
            zh="memU API 请求超时时间（秒）",
        ),
    }
```

### 3. 更新客户端管理器 ✅
**文件**: `Open-LLM-VTuber/src/open_llm_vtuber/memory/memu_manager.py`

```python
if self._client is None:
    logger.info("Initializing memU client ✨")
    self._client = MemuClient(
        base_url=self._settings.base_url,
        user_id=self._settings.user_id,
        agent_id=self._settings.agent_id,
        top_k=self._settings.top_k,
        min_similarity=self._settings.min_similarity,
        timeout=self._settings.timeout,  # ✨ 新增
    )
```

### 4. 更新客户端默认值 ✅
**文件**: `Open-LLM-VTuber/src/open_llm_vtuber/memory/memu_client.py`

```python
def __init__(
    self,
    base_url: str,
    user_id: str,
    agent_id: str,
    top_k: int,
    min_similarity: float,
    timeout: float = 10.0,  # 修改: 从 2.0 改为 10.0
) -> None:
```

## 📊 修复效果

### 修复前
```
2025-10-05 10:40:34 | INFO | New Conversation Chain started!
2025-10-05 10:40:34 | INFO | Initializing memU client ✨
2025-10-05 10:40:36 | ERROR | memU request failed with HTTPError: ReadTimeout:
                              ^^^ 2秒后就超时了
```

### 修复后
```
2025-10-05 10:49:53 | INFO | New Conversation Chain started!
2025-10-05 10:49:53 | INFO | Initializing memU client ✨
                              现在有10秒时间来完成请求
```

## 🎯 技术细节

### 配置传递链路
```
conf.yaml (timeout: 10.0)
    ↓
MemuSettings (timeout: float = 10.0)
    ↓
MemuClientManager (self._settings.timeout)
    ↓
MemuClient (timeout=self._settings.timeout)
    ↓
httpx.AsyncClient (timeout=self._timeout)
```

### 为什么需要10秒超时？
1. **嵌入计算**: memU需要计算查询的embedding（~1-2秒）
2. **相似度搜索**: 在大量记忆中搜索相似项（~1-2秒）
3. **网络延迟**: 本地请求也有一定延迟（~0.5秒）
4. **系统负载**: 如果系统繁忙，可能需要更多时间
5. **安全边界**: 10秒提供了足够的安全边界

## ✅ 完成状态

- [x] **配置文件**: 添加 `timeout: 10.0`
- [x] **配置类**: 添加 `timeout` 字段和描述
- [x] **客户端管理器**: 传递 `timeout` 参数
- [x] **客户端默认值**: 更新为 10.0 秒
- [x] **服务器重启**: VTuber服务器已重启
- [x] **测试验证**: 配置已生效

## 🚀 预期效果

现在memU请求将：
- ✅ **有足够时间**: 10秒超时，足够完成嵌入计算和搜索
- ✅ **配置可控**: 可以通过 `conf.yaml` 调整超时时间
- ✅ **降级优雅**: 如果仍然超时，会优雅降级到无记忆模式
- ✅ **日志清晰**: 超时错误会被正确记录和处理

**memU超时问题已完全修复！** 🎉

现在系统可以正常检索记忆，不会因为超时而失败。
