# 📝 memU 笔记软件 - 快速开始

## 🚀 快速启动

### 1. 确保 memU 服务正在运行

```bash
# 检查 memU 是否运行
lsof -i :8000

# 如果未运行，启动 memU
cd ../memU
python3.12 -m memu.server.cli start
```

### 2. 使用启动脚本

```bash
./start_note_app.sh
```

选择你想要的模式：
- **1** - 命令行模式（查看帮助）
- **2** - 图形界面模式
- **3** - 交互模式

## 📖 使用示例

### 命令行模式

```bash
# 清除代理（重要！）
unset http_proxy https_proxy HTTP_PROXY HTTPS_PROXY all_proxy ALL_PROXY

# 添加笔记
python3 note_cli.py add \
  -t "Python 学习笔记" \
  -c "今天学习了 Python 的装饰器。装饰器是一种设计模式，可以在不修改原函数的情况下增加额外功能。" \
  --tags "Python,编程,学习" \
  --category "技术笔记"

# 搜索笔记
python3 note_cli.py search "Python 装饰器"

# 列出所有笔记
python3 note_cli.py list
```

### 交互模式

```bash
# 清除代理
unset http_proxy https_proxy HTTP_PROXY HTTPS_PROXY all_proxy ALL_PROXY

# 启动交互模式
python3 note_cli.py interactive
```

在交互模式中：
- 输入 `add` 添加新笔记
- 输入 `search` 搜索笔记
- 输入 `list` 列出所有笔记
- 输入 `quit` 退出

### 图形界面模式

```bash
# 清除代理
unset http_proxy https_proxy HTTP_PROXY HTTPS_PROXY all_proxy ALL_PROXY

# 启动图形界面
python3 note_gui.py
```

## ⚠️ 重要提示

### 代理问题

如果遇到代理错误，请在运行命令前清除代理环境变量：

```bash
unset http_proxy https_proxy HTTP_PROXY HTTPS_PROXY all_proxy ALL_PROXY
```

### 搜索超时

如果搜索超时，可能是因为：
1. memU 的嵌入模型正在初始化（首次运行需要下载模型）
2. 增加超时时间：修改 `memu_note_client.py` 中的 `timeout` 参数

### memU 连接失败

确保：
1. memU 服务正在运行（端口 8000）
2. 使用正确的 API 地址（默认：`http://127.0.0.1:8000`）

## 💡 快速测试

```bash
# 清除代理
unset http_proxy https_proxy HTTP_PROXY HTTPS_PROXY all_proxy ALL_PROXY

# 添加测试笔记
python3 note_cli.py add \
  -t "测试笔记" \
  -c "这是一条测试笔记，用于验证 memU 笔记软件的功能。" \
  --tags "测试" \
  --category "测试"

# 列出笔记（不需要嵌入模型）
python3 note_cli.py list
```

## 📚 更多信息

查看完整文档：[README.md](README.md)
