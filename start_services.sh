#!/bin/bash

# Script to start memU and Open-LLM-VTuber services

echo "🚀 Starting services..."

# Check if LMStudio is running
echo "📋 Checking LMStudio service..."
if curl -s http://127.0.0.1:1234/v1/models > /dev/null 2>&1; then
    echo "✅ LMStudio service is running normally"
else
    echo "❌ Warning: LMStudio service is not running!"
    echo "   Please start LMStudio first and load model: qwen3-30b-a3b-2507"
    echo "   LMStudio should listen on http://127.0.0.1:1234"
fi

# Check if memU is running
echo "📋 Checking memU service..."
if curl -s http://127.0.0.1:8000/api/health > /dev/null 2>&1; then
    echo "✅ memU service is already running (port 8000)"
else
    echo "🔧 Starting memU service..."
    cd memU
    nohup python3.12 -m memu.server.main > memu.log 2>&1 &
    echo "   memU log: memU/memu.log"
    sleep 3
    if curl -s http://127.0.0.1:8000/api/health > /dev/null 2>&1; then
        echo "✅ memU service started successfully"
    else
        echo "❌ memU service failed to start, please check logs"
    fi
    cd ..
fi

echo "🎭 Starting Open-LLM-VTuber..."
cd Open-LLM-VTuber
echo "   Access URL: http://localhost:12393"
python3.12 run_server.py
echo "Press Ctrl+C to stop services"
