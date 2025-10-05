#!/usr/bin/env python3
"""测试 Open-LLM-VTuber 的 memU 集成"""

import asyncio
import websockets
import json

async def test_vtuber():
    uri = "ws://localhost:12393/client-ws"
    
    print("🔌 连接到 Open-LLM-VTuber...")
    async with websockets.connect(uri) as websocket:
        print("✅ 已连接")
        
        # 发送测试消息
        test_message = "我之前学习了什么？"
        print(f"📤 发送消息: {test_message}")
        
        message = {
            "type": "text-input",
            "text": test_message
        }
        
        await websocket.send(json.dumps(message))
        print("✅ 消息已发送")
        
        # 接收响应
        print("📥 等待响应...")
        response_count = 0
        while True:  # 持续接收响应
            try:
                response = await asyncio.wait_for(websocket.recv(), timeout=60.0)
                data = json.loads(response)
                response_count += 1
                print(f"📨 收到响应 {response_count}: {data.get('type', 'unknown')}")
                if data.get('type') == 'full-text':
                    print(f"   内容: {data.get('text', '')[:200]}...")
                elif data.get('type') == 'control':
                    print(f"   控制: {data.get('text', '')}")
                
                # 如果收到 conversation-chain-end，结束
                if data.get('type') == 'conversation-chain-end':
                    print("✅ 对话结束")
                    break
            except asyncio.TimeoutError:
                print("⏱️  等待超时")
                break
            except Exception as e:
                print(f"❌ 错误: {e}")
                break

if __name__ == "__main__":
    asyncio.run(test_vtuber())
