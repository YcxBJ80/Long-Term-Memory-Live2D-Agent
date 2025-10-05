# Python 版本问题修复

## 问题描述

启动 VTuber 服务器时遇到错误：
```
TypeError: unsupported operand type(s) for |: 'ModelMetaclass' and 'NoneType'
```

## 原因

- **你的 Python 版本**: 3.9.23
- **项目要求**: Python >= 3.10

Python 3.9 不支持 `|` 类型注解语法（如 `str | None`），这是 Python 3.10+ 的特性。

## 解决方案

### ✅ 方案 1: 使用 Python 3.12（推荐）

你的系统已经安装了 Python 3.12，使用它即可：

```bash
cd /Users/yangchengxuan/Desktop/PROJECTS/Live2Document_4

# 使用修复后的启动脚本（自动使用 Python 3.12）
./start_vtuber_fixed.sh
```

### 手动启动（使用 Python 3.12）

```bash
# 启动 memU
cd /Users/yangchengxuan/Desktop/PROJECTS/Live2Document_4/memU
python3.12 -m memu.server.cli start &

# 启动 VTuber
cd /Users/yangchengxuan/Desktop/PROJECTS/Live2Document_4/Open-LLM-VTuber
python3.12 run_server.py
```

### 方案 2: 设置 Python 3.12 为默认（可选）

如果你想让 `python` 命令默认使用 Python 3.12：

```bash
# 使用 pyenv
pyenv global 3.12

# 或者创建别名（添加到 ~/.zshrc）
alias python=python3.12
alias python3=python3.12
```

## 验证

启动后应该看到：

```
✅ 使用 Python: python3.12 (Python 3.12.x)
✅ memU 服务器启动成功！
✅ VTuber 服务器启动成功！
```

## 新的启动脚本

已创建 `start_vtuber_fixed.sh`，它会：
1. ✅ 自动检测并使用 Python 3.10+
2. ✅ 启动 memU 和 VTuber 服务器
3. ✅ 显示详细的启动信息
4. ✅ 记录日志到 `logs/` 目录

使用方法：
```bash
cd /Users/yangchengxuan/Desktop/PROJECTS/Live2Document_4
./start_vtuber_fixed.sh
```

## 查看日志

```bash
# 查看 memU 日志
tail -f logs/memu.log

# 查看 VTuber 日志
tail -f logs/vtuber.log
```

## 停止服务

```bash
# 查看进程
ps aux | grep -E "(memu|run_server)"

# 停止所有服务
pkill -f "memu.server.cli"
pkill -f "run_server.py"
```

---

**问题已解决！** 使用 `./start_vtuber_fixed.sh` 启动即可。
