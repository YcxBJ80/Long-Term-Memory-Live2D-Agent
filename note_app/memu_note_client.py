"""
memU 笔记客户端
用于将笔记直接存储到 memU 记忆库中
"""

import httpx
from typing import Optional, List, Dict, Any
from datetime import datetime
import json


class MemuNoteClient:
    """memU 笔记客户端，用于存储和管理笔记"""

    def __init__(
        self,
        base_url: str = "http://127.0.0.1:8000",
        user_id: str = "note_user",
        user_name: str = "笔记用户",
        agent_id: str = "note_agent",
        agent_name: str = "笔记助手",
        timeout: float = 30.0,
    ):
        """
        初始化 memU 笔记客户端

        Args:
            base_url: memU API 的基础 URL
            user_id: 用户标识
            user_name: 用户名称
            agent_id: 智能体标识
            agent_name: 智能体名称
            timeout: 请求超时时间（秒）
        """
        self.base_url = base_url.rstrip("/")
        self.user_id = user_id
        self.user_name = user_name
        self.agent_id = agent_id
        self.agent_name = agent_name
        self.timeout = timeout

    def save_note(
        self,
        title: str,
        content: str,
        tags: Optional[List[str]] = None,
        category: str = "note",
    ) -> Dict[str, Any]:
        """
        保存笔记到 memU

        Args:
            title: 笔记标题
            content: 笔记内容
            tags: 标签列表
            category: 笔记分类

        Returns:
            API 响应结果
        """
        # 构建对话格式的笔记
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # 构建笔记消息
        note_message = f"[笔记] {title}\n\n{content}"
        if tags:
            note_message += f"\n\n标签: {', '.join(tags)}"
        note_message += f"\n\n记录时间: {timestamp}"

        # 构建对话数据
        conversation_data = {
            "user_id": self.user_id,
            "user_name": self.user_name,
            "agent_id": self.agent_id,
            "agent_name": self.agent_name,
            "conversation": [
                {
                    "role": "user",
                    "content": note_message,
                }
            ],
            "metadata": {
                "type": "note",
                "title": title,
                "category": category,
                "tags": tags or [],
                "timestamp": timestamp,
            },
        }

        # 发送到 memU
        try:
            with httpx.Client(base_url=self.base_url, timeout=self.timeout) as client:
                response = client.post(
                    "/api/v1/memory/memorize",
                    json=conversation_data,
                )
                response.raise_for_status()
                result = response.json()
                print(f"✅ 笔记已保存到 memU: {title}")
                return result
        except httpx.HTTPError as e:
            print(f"❌ 保存笔记失败: {e}")
            raise

    def search_notes(
        self,
        query: str,
        top_k: int = 10,
        min_similarity: float = 0.3,
    ) -> List[Dict[str, Any]]:
        """
        搜索笔记

        Args:
            query: 搜索查询
            top_k: 返回结果数量
            min_similarity: 最小相似度阈值

        Returns:
            搜索结果列表
        """
        search_data = {
            "user_id": self.user_id,
            "agent_id": self.agent_id,
            "query": query,
            "top_k": top_k,
            "min_similarity": min_similarity,
        }

        try:
            with httpx.Client(base_url=self.base_url, timeout=self.timeout) as client:
                response = client.post(
                    "/api/v1/memory/retrieve/related-memory-items",
                    json=search_data,
                )
                response.raise_for_status()
                result = response.json()
                
                memories = result.get("related_memories", [])
                notes = []
                
                for item in memories:
                    memory = item.get("memory", {})
                    similarity = item.get("similarity_score", 0.0)
                    
                    notes.append({
                        "memory_id": memory.get("memory_id"),
                        "category": memory.get("category"),
                        "content": memory.get("content"),
                        "similarity_score": similarity,
                        "metadata": memory.get("metadata", {}),
                    })
                
                print(f"🔍 找到 {len(notes)} 条相关笔记")
                return notes
                
        except httpx.HTTPError as e:
            print(f"❌ 搜索笔记失败: {e}")
            raise

    def list_all_memories(self) -> List[Dict[str, Any]]:
        """
        列出所有记忆（笔记）

        Returns:
            所有记忆列表
        """
        # 使用空查询和低相似度阈值来获取所有记忆
        return self.search_notes("", top_k=100, min_similarity=0.0)


def main():
    """命令行测试"""
    client = MemuNoteClient()
    
    # 测试保存笔记
    print("\n📝 测试保存笔记...")
    client.save_note(
        title="Python 学习笔记",
        content="今天学习了 Python 的装饰器。装饰器是一种设计模式，可以在不修改原函数的情况下增加额外功能。",
        tags=["Python", "编程", "学习"],
        category="技术笔记",
    )
    
    # 测试搜索笔记
    print("\n🔍 测试搜索笔记...")
    results = client.search_notes("Python 装饰器")
    
    for i, note in enumerate(results, 1):
        print(f"\n--- 笔记 {i} ---")
        print(f"相似度: {note['similarity_score']:.2f}")
        print(f"分类: {note['category']}")
        print(f"内容: {note['content'][:100]}...")


if __name__ == "__main__":
    main()
