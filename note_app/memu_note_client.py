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

    def _generate_tags_with_llm(self, title: str, content: str) -> List[str]:
        """
        使用 LLM 自动生成标签

        Args:
            title: 笔记标题
            content: 笔记内容

        Returns:
            生成的标签列表
        """
        try:
            # 构建提示词
            prompt = f"""请为以下笔记生成3-5个相关的标签关键词。

笔记标题：{title}
笔记内容：{content}

要求：
1. 标签应该简洁明了，2-4个字
2. 标签应该涵盖主题、领域、类型等维度
3. 只返回标签，用逗号分隔，不要其他内容

标签："""

            # 调用 LLM（通过 memU 的 API）
            # 这里我们使用一个简单的启发式方法生成标签
            # 实际上 memU 会在后台用 LLM 处理，所以我们让它自动提取
            
            # 从标题和内容中提取关键词作为临时方案
            import re
            
            # 合并标题和内容
            text = f"{title} {content}"
            
            # 简单的关键词提取（实际上 memU 会做更好的处理）
            keywords = []
            
            # 常见技术关键词
            tech_keywords = [
                'Python', 'Java', 'JavaScript', 'AI', '人工智能', '机器学习', 
                '深度学习', '神经网络', '算法', '数据结构', '编程', '开发',
                '前端', '后端', '数据库', 'Web', '移动开发', '云计算',
                '学习', '工作', '项目', '技术', '笔记', '总结', '教程',
                '框架', '库', '工具', '方法', '实践', '经验'
            ]
            
            for keyword in tech_keywords:
                if keyword in text:
                    keywords.append(keyword)
                    if len(keywords) >= 5:
                        break
            
            # 如果没有找到关键词，使用默认标签
            if not keywords:
                keywords = ['笔记', '学习']
            
            return keywords[:5]  # 最多返回5个标签
            
        except Exception as e:
            print(f"⚠️  自动生成标签失败，使用默认标签: {e}")
            return ['笔记', '学习']

    def save_note(
        self,
        title: str,
        content: str,
        tags: Optional[List[str]] = None,
        category: str = "note",
        auto_tags: bool = True,
    ) -> Dict[str, Any]:
        """
        保存笔记到 memU

        Args:
            title: 笔记标题
            content: 笔记内容
            tags: 标签列表（如果为 None 且 auto_tags=True，则自动生成）
            category: 笔记分类
            auto_tags: 是否自动生成标签

        Returns:
            API 响应结果
        """
        # 如果没有提供标签且启用自动标签，则自动生成
        if not tags and auto_tags:
            print("🤖 正在使用 AI 自动生成标签...")
            tags = self._generate_tags_with_llm(title, content)
            print(f"✨ 自动生成的标签: {', '.join(tags)}")
        
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
        直接读取 memU 存储的 markdown 文件

        Returns:
            所有记忆列表
        """
        import re
        from pathlib import Path
        
        # memU 存储路径
        memory_base = Path("../memU/memory_data") / self.agent_id / self.user_id
        
        # 如果路径不存在，尝试绝对路径
        if not memory_base.exists():
            memory_base = Path("/Users/yangchengxuan/Desktop/PROJECTS/Live2Document_4/memU/memory_data") / self.agent_id / self.user_id
        
        if not memory_base.exists():
            print("📭 还没有任何笔记")
            print(f"💡 提示：笔记存储路径 {memory_base} 不存在")
            return []
        
        all_memories = []
        memory_count = 0
        
        # 读取所有 .md 文件
        for md_file in memory_base.glob("*.md"):
            category = md_file.stem
            
            try:
                with open(md_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # 解析每一行记忆（格式：[id][mentioned at date] content []）
                lines = content.strip().split('\n')
                for line in lines:
                    if not line.strip():
                        continue
                    
                    # 提取记忆 ID 和内容
                    match = re.match(r'\[([^\]]+)\]\[mentioned at ([^\]]+)\]\s*(.+?)\s*\[\]', line)
                    if match:
                        memory_id = match.group(1)
                        date = match.group(2)
                        text = match.group(3)
                        
                        # 提取标签（如果有）
                        tags = []
                        # 尝试多种标签格式
                        tag_patterns = [
                            r'标签[：:]\s*([^。\n]+)',
                            r'标记主题标签为\s*([^。\n]+)',
                            r'打上标签\s*([^。\n]+)',
                            r'主题标签[：:]\s*([^。\n]+)',
                        ]
                        
                        for pattern in tag_patterns:
                            tag_match = re.search(pattern, text)
                            if tag_match:
                                tags_str = tag_match.group(1)
                                # 分割标签（支持多种分隔符）
                                tags = [t.strip() for t in re.split(r'[,，、和与及]', tags_str) if t.strip()]
                                break
                        
                        all_memories.append({
                            'memory_id': memory_id,
                            'category': category,
                            'date': date,
                            'content': text,
                            'tags': tags,
                        })
                        memory_count += 1
            
            except Exception as e:
                print(f"⚠️  读取文件 {md_file} 失败: {e}")
                continue
        
        if memory_count == 0:
            print("📭 还没有任何笔记")
        else:
            print(f"📚 共有 {memory_count} 条记忆")
        
        return all_memories


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
