#!/bin/bash

# 启动 memU 和 Open-LLM-VTuber 的脚本

echo "🚀 启动服务..."
echo ""

# 检查 LMStudio 是否在运行
echo "📋 检查 LMStudio 服务..."
if curl -s http://127.0.0.1:1234/v1/models >/dev/null 2>&1; then
    echo "✅ LMStudio 服务正常运行"
else
    echo "❌ 警告: LMStudio 服务未运行！"
    echo "   请先启动 LMStudio 并加载模型: openai/gpt-oss-20b"
    echo "   LMStudio 应该监听在 http://127.0.0.1:1234"
    echo ""
fi

# 检查 memU 是否在运行
echo "📋 检查 memU 服务..."
if lsof -i :8000 >/dev/null 2>&1; then
    echo "✅ memU 服务已在运行 (端口 8000)"
else
    echo "🔧 启动 memU 服务..."
    cd /Users/yangchengxuan/Desktop/PROJECTS/Live2Document_4/memU
    nohup python3.12 -m memu.server.cli start > memu.log 2>&1 &
    echo "   memU 日志: memU/memu.log"
    sleep 3
    if lsof -i :8000 >/dev/null 2>&1; then
        echo "✅ memU 服务启动成功"
    else
        echo "❌ memU 服务启动失败，请查看日志"
    fi
fi

echo ""
echo "🎭 启动 Open-LLM-VTuber..."
cd /Users/yangchengxuan/Desktop/PROJECTS/Live2Document_4/Open-LLM-VTuber
echo "   访问地址: http://localhost:12393"
echo ""
echo "按 Ctrl+C 停止服务"
echo "================================"
echo ""

uv run python run_server.py
