#!/bin/bash
# 启动 Open-LLM-VTuber（禁用代理）

cd /Users/yangchengxuan/Desktop/PROJECTS/Live2Document_4/Open-LLM-VTuber

# 停止现有服务
echo "🛑 停止现有服务..."
lsof -ti :12393 | xargs kill -9 2>/dev/null

# 禁用所有代理并启动
echo "🚀 启动 Open-LLM-VTuber..."
env -u http_proxy -u https_proxy -u HTTP_PROXY -u HTTPS_PROXY -u all_proxy -u ALL_PROXY \
  nohup uv run python run_server.py > /tmp/vtuber.log 2>&1 &

sleep 3

# 检查是否启动成功
if lsof -i :12393 > /dev/null 2>&1; then
    echo "✅ Open-LLM-VTuber 已成功启动！"
    echo "📱 访问: http://localhost:12393"
    echo "📋 日志: tail -f /tmp/vtuber.log"
else
    echo "❌ 启动失败，请查看日志: tail -f /tmp/vtuber.log"
    exit 1
fi
