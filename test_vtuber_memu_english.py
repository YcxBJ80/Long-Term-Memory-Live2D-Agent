#!/usr/bin/env python3
"""Test Open-LLM-VTuber memU integration (English query)"""

import asyncio
import websockets
import json

async def test_vtuber():
    uri = "ws://localhost:12393/client-ws"
    
    print("🔌 Connecting to Open-LLM-VTuber...")
    async with websockets.connect(uri) as websocket:
        print("✅ Connected")
        
        # Send test message (English)
        test_message = "What did I learn about machine learning?"
        print(f"📤 Sending message: {test_message}")
        
        message = {
            "type": "text-input",
            "text": test_message
        }
        
        await websocket.send(json.dumps(message))
        print("✅ Message sent")
        
        # Receive response
        print("📥 Waiting for response...")
        response_count = 0
        while True:
            try:
                response = await asyncio.wait_for(websocket.recv(), timeout=60.0)
                data = json.loads(response)
                response_count += 1
                print(f"📨 Received response {response_count}: {data.get('type', 'unknown')}")
                if data.get('type') == 'full-text':
                    content = data.get('text', '')
                    print(f"   Content: {content[:300]}...")
                elif data.get('type') == 'control':
                    print(f"   Control: {data.get('text', '')}")
                
                # End if received conversation-chain-end
                if data.get('type') == 'conversation-chain-end':
                    print("✅ Conversation ended")
                    break
            except asyncio.TimeoutError:
                print("⏱️  Timeout waiting")
                break
            except Exception as e:
                print(f"❌ Error: {e}")
                break

if __name__ == "__main__":
    asyncio.run(test_vtuber())
