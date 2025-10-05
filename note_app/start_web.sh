#!/bin/bash

# memU 笔记 Web 应用启动脚本

echo "🚀 启动 memU 笔记 Web 应用"
echo "=========================="
echo ""

# 检查 memU 服务
if ! lsof -i :8000 > /dev/null 2>&1; then
    echo "❌ memU 服务未运行"
    echo "请先启动 memU 服务："
    echo "  cd ../memU"
    echo "  python3.12 -m memu.server.cli start"
    exit 1
fi

echo "✅ memU 服务正在运行"
echo ""

# 清除代理
unset http_proxy https_proxy HTTP_PROXY HTTPS_PROXY all_proxy ALL_PROXY

# 检查端口 8080 是否被占用
if lsof -i :8080 > /dev/null 2>&1; then
    echo "⚠️  端口 8080 已被占用"
    echo "正在停止旧服务..."
    lsof -ti :8080 | xargs kill -9 2>/dev/null
    sleep 2
fi

# 启动 Web 服务器
echo "🌐 启动 Web 服务器..."
echo ""
echo "📝 访问地址: http://localhost:8080"
echo "📖 API 文档: http://localhost:8080/docs"
echo ""
echo "按 Ctrl+C 停止服务"
echo ""

python3 web_server.py
