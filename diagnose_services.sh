#!/bin/bash

echo "🔍 Live2Document 服务诊断工具"
echo "================================"
echo ""

# 检查代理设置
echo "1. 检查代理设置..."
if env | grep -q proxy; then
    echo "⚠️  发现代理设置，可能干扰本地连接"
    echo "当前代理设置："
    env | grep proxy | head -5
    echo ""
else
    echo "✅ 代理设置正常"
fi

# 检查LM Studio
echo "2. 检查LM Studio状态..."
if curl --noproxy 127.0.0.1 -s http://127.0.0.1:1234/v1/models > /dev/null 2>&1; then
    echo "✅ LM Studio运行正常"
    echo "API地址: http://127.0.0.1:1234/v1"
else
    echo "❌ LM Studio未运行或未正确启动"
    echo ""
    echo "请启动LM Studio："
    echo "1. 打开LM Studio应用"
    echo "2. 加载模型: qwen3-30b-a3b-2507"
    echo "3. 启动本地服务器 (端口1234)"
fi

echo ""

# 检查memU
echo "3. 检查memU状态..."
if curl --noproxy localhost -s http://localhost:8000/health > /dev/null 2>&1; then
    echo "✅ memU运行正常"
    echo "API地址: http://localhost:8000"
else
    echo "❌ memU未运行"
fi

echo ""

# 检查VTuber
echo "4. 检查VTuber状态..."
if curl --noproxy localhost -s http://localhost:12393 > /dev/null 2>&1; then
    echo "✅ VTuber运行正常"
    echo "访问地址: http://localhost:12393"
else
    echo "❌ VTuber未运行"
fi

echo ""

# 检查笔记应用
echo "5. 检查笔记应用状态..."
if curl --noproxy localhost -s http://localhost:8080 > /dev/null 2>&1; then
    echo "✅ 笔记应用运行正常"
    echo "访问地址: http://localhost:8080"
else
    echo "❌ 笔记应用未运行"
fi

echo ""
echo "================================"
echo "📋 服务状态总结："
echo ""
echo "需要运行的服务："
echo "✅ LM Studio (http://127.0.0.1:1234) - 您的LLM服务"
echo "✅ memU API (http://localhost:8000) - 记忆存储"
echo "✅ VTuber (http://localhost:12393) - AI对话界面"
echo "✅ 笔记应用 (http://localhost:8080) - 笔记管理"
echo ""
echo "💡 如果LM Studio未运行，请先启动它"
echo "🚀 然后运行: ./start_vtuber_fixed.sh"
