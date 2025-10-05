#!/bin/bash

# 启动优化后的 VTuber 服务（使用 Python 3.12）

echo "🚀 启动 Live2Document 服务..."
echo ""

# 清除代理设置（避免干扰本地服务连接）
echo "🧹 清除代理设置..."
unset http_proxy https_proxy HTTP_PROXY HTTPS_PROXY all_proxy ALL_PROXY
echo "✅ 代理设置已清除"

echo ""
echo "⚠️  请确保以下服务正在运行："
echo "  1. LM Studio (http://127.0.0.1:1234)"
echo "  2. memU API (http://localhost:8000)"
echo ""
echo "💡 如果LM Studio未运行，请先启动它："
echo "   - 打开LM Studio应用"
echo "   - 加载模型: qwen3-30b-a3b-2507"
echo "   - 启动本地服务器"
echo ""

# 检查LM Studio状态
echo "🔍 检查LM Studio状态..."
if curl --noproxy 127.0.0.1 -s http://127.0.0.1:1234/v1/models > /dev/null 2>&1; then
    echo "✅ LM Studio运行正常"
else
    echo "⚠️  LM Studio未运行或未正确启动"
    echo ""
    echo "请按以下步骤启动LM Studio："
    echo "1. 打开LM Studio应用程序"
    echo "2. 在左侧栏搜索并下载模型: qwen3-30b-a3b-2507"
    echo "3. 点击'启动聊天'或'启动服务器'"
    echo "4. 确保服务器运行在 http://127.0.0.1:1234"
    echo ""
    echo "启动脚本将继续，但VTuber可能无法正常工作。"
    echo "请启动LM Studio后重新运行此脚本。"
    echo ""
    echo "或者，您可以："
    echo "1. 先启动LM Studio"
    echo "2. 然后重新运行此脚本"
    echo ""
    read -p "按Enter键继续启动其他服务，或Ctrl+C退出..."
fi

echo ""

# 检查 Python 版本
PYTHON_CMD=""
if command -v python3.12 &> /dev/null; then
    PYTHON_CMD="python3.12"
elif command -v python3.11 &> /dev/null; then
    PYTHON_CMD="python3.11"
elif command -v python3.10 &> /dev/null; then
    PYTHON_CMD="python3.10"
else
    echo "❌ 错误: 需要 Python 3.10 或更高版本"
    echo "当前 Python 版本: $(python --version)"
    echo ""
    echo "请安装 Python 3.10+ 或使用以下命令："
    echo "  brew install python@3.12  # macOS"
    exit 1
fi

echo "✅ 使用 Python: $PYTHON_CMD ($(${PYTHON_CMD} --version))"
echo ""

# 启动 memU 服务器
echo "📚 启动 memU 服务器..."
cd memU
${PYTHON_CMD} -m memu.server.cli start > ../logs/memu.log 2>&1 &
MEMU_PID=$!
echo "   PID: $MEMU_PID"
echo "   日志: logs/memu.log"
cd ..

# 等待 memU 启动
echo ""
echo "⏳ 等待 memU 服务器启动..."
sleep 3

# 检查 memU 是否启动成功
if curl --noproxy localhost -s http://localhost:8000/health > /dev/null 2>&1; then
    echo "✅ memU 服务器启动成功！"
else
    echo "⚠️  memU 服务器可能还在启动中..."
fi

# 启动 VTuber 服务器
echo ""
echo "🎤 启动 VTuber 服务器..."
cd Open-LLM-VTuber
${PYTHON_CMD} run_server.py > ../logs/vtuber.log 2>&1 &
VTUBER_PID=$!
echo "   PID: $VTUBER_PID"
echo "   日志: logs/vtuber.log"
cd ..

# 等待 VTuber 启动
echo ""
echo "⏳ 等待 VTuber 服务器启动..."
sleep 5

# 检查 VTuber 是否启动成功
if curl --noproxy localhost -s http://localhost:12393 > /dev/null 2>&1; then
    echo "✅ VTuber 服务器启动成功！"
else
    echo "⚠️  VTuber 服务器可能还在启动中..."
fi

# 启动笔记 Web 服务器
echo ""
echo "📝 启动笔记 Web 服务器..."
cd note_app
${PYTHON_CMD} web_server.py > ../logs/note_web.log 2>&1 &
NOTE_PID=$!
echo "   PID: $NOTE_PID"
echo "   日志: logs/note_web.log"
cd ..

# 等待笔记服务启动
echo ""
echo "⏳ 等待笔记服务器启动..."
sleep 3

# 检查笔记服务是否启动成功
if curl --noproxy localhost -s http://localhost:8080 > /dev/null 2>&1; then
    echo "✅ 笔记服务器启动成功！"
else
    echo "⚠️  笔记服务器可能还在启动中..."
fi

echo ""
echo "================================"
echo "🎉 服务启动完成！"
echo "================================"
echo ""
echo "📊 服务状态:"
echo "  - memU:   http://localhost:8000"
echo "  - VTuber: http://localhost:12393"
echo "  - 笔记:   http://localhost:8080"
echo ""
echo "📝 查看日志:"
echo "  - memU:   tail -f logs/memu.log"
echo "  - VTuber: tail -f logs/vtuber.log"
echo "  - 笔记:   tail -f logs/note_web.log"
echo ""
echo "🛑 停止服务:"
echo "  - kill $MEMU_PID $VTUBER_PID $NOTE_PID"
echo ""
echo "💡 完整功能已启用:"
echo "  ✅ memU 查询缓存（英文记忆）"
echo "  ✅ NumPy 向量加速"
echo "  ✅ 异步非阻塞查询（10秒超时）"
echo "  ✅ 智能降级策略"
echo "  ✅ 全英文界面和记忆"
echo ""
echo "预期性能: 对答延迟 2-3 秒（优化前 4-5 秒）"
echo ""
