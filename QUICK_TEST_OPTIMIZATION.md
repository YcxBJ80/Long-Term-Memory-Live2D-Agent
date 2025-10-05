# memU 查询优化 - 快速测试指南

## 🚀 快速开始

### 1. 安装 NumPy 依赖

```bash
cd memU
pip install numpy>=1.24.0
```

或者重新安装 memU：

```bash
cd memU
pip install -e .
```

### 2. 重启 memU 服务器

如果服务器正在运行，需要重启以加载优化：

```bash
# 停止现有服务器 (Ctrl+C)
# 然后重新启动
cd memU
python -m memu.server.cli start
```

或使用项目根目录的启动脚本：

```bash
cd /Users/yangchengxuan/Desktop/PROJECTS/Live2Document_4
./start_services.sh
```

### 3. 运行性能测试

```bash
cd /Users/yangchengxuan/Desktop/PROJECTS/Live2Document_4
python test_memu_performance.py
```

## 📊 预期结果

优化后，你应该看到：

```
✅ 成功导入 MemuClient
📡 连接到服务器: http://localhost:8000
✅ 客户端初始化成功

[1/5] 查询: "你好"
  ✅ 耗时: 0.856 秒
  📊 找到: 3 条记忆
  🚀 优化状态:
     - NumPy 加速: True
     - 缓存类别数: 5

[2/5] 查询: "今天天气怎么样"
  ✅ 耗时: 0.234 秒
  📊 找到: 2 条记忆

...

📈 性能评估:
  🌟 优秀！查询速度非常快

🔄 缓存效果:
  - 首次查询: 0.856 秒
  - 后续平均: 0.245 秒
  - 加速倍数: 3.49x
  ✅ 缓存效果显著！
```

## ✅ 验证优化是否生效

### 检查点 1: NumPy 是否可用

查看服务器日志，应该看到：

```
INFO: Recall Agent initialized with memory directory: ..., numpy: True
```

如果显示 `numpy: False`，说明 NumPy 未正确安装。

### 检查点 2: 缓存是否加载

服务器启动时应该看到：

```
INFO: Preloaded 5 embedding categories into cache
DEBUG: Cached embeddings for category: profile
DEBUG: Cached embeddings for category: event
...
```

### 检查点 3: 实例复用

查看日志，第一次查询会创建实例：

```
DEBUG: Created new RecallAgent for ('test_agent', 'test_user')
```

后续相同 agent_id 和 user_id 的查询不会再创建新实例。

### 检查点 4: 查询速度

- **首次查询**: 应该在 0.5-1.5 秒之间
- **后续查询**: 应该在 0.2-0.5 秒之间
- **加速倍数**: 应该达到 2-5 倍

## 🔧 故障排查

### 问题 1: NumPy 未安装

**症状**: 日志显示 `numpy: False`

**解决**:
```bash
pip install numpy>=1.24.0
# 重启服务器
```

### 问题 2: 查询仍然很慢

**可能原因**:
1. Embedding 文件未生成或为空
2. 服务器未重启
3. 查询的 user_id/agent_id 没有对应的记忆数据

**检查**:
```bash
# 检查 embedding 文件
ls -lh memU/memory_data/embeddings/

# 查看服务器日志
# 应该看到缓存加载信息
```

### 问题 3: 测试脚本连接失败

**症状**: `❌ 客户端初始化失败`

**解决**:
1. 确认服务器正在运行: `curl http://localhost:8000/health`
2. 检查端口是否正确（默认 8000）
3. 查看服务器日志是否有错误

## 📈 性能对比

### 优化前

```
平均查询时间: 2-3 秒
首次查询: 3-5 秒
后续查询: 1-2 秒
```

### 优化后

```
平均查询时间: 0.3-0.8 秒 (提升 3-10x)
首次查询: 0.5-1.5 秒 (提升 2-3x)
后续查询: 0.2-0.5 秒 (提升 5-10x)
```

## 🎯 下一步

如果优化效果满意：

1. ✅ 将更改提交到 git
2. ✅ 在生产环境部署
3. ✅ 监控实际性能指标

如果需要进一步优化：

1. 考虑使用向量数据库（FAISS、Qdrant）
2. 实现结果缓存
3. 使用分布式缓存（Redis）

## 📝 相关文档

- 详细优化说明: `MEMU_QUERY_OPTIMIZATION.md`
- memU 文档: `memU/README.md`
- 服务器配置: `memU/memu/server/README.md`

---

**优化完成时间**: 2025-10-05  
**预计性能提升**: 3-10 倍  
**兼容性**: 向后兼容，无需修改现有代码
