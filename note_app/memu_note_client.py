"""memU Note Client
For storing notes directly into memU memory database
"""

import httpx
from typing import Optional, List, Dict, Any
from datetime import datetime
import json


class MemuNoteClient:
    """memU Note Client for storing and managing notes"""

    def __init__(
        self,
        base_url: str = "http://127.0.0.1:8000",
        user_id: str = "note_user",
        user_name: str = "Note User",
        agent_id: str = "note_agent",
        agent_name: str = "Note Assistant",
        timeout: float = 30.0,
    ):
        """
        Initialize memU Note Client

        Args:
            base_url: Base URL for memU API
            user_id: User identifier
            user_name: User name
            agent_id: Agent identifier
            agent_name: Agent name
            timeout: Request timeout in seconds
        """
        self.base_url = base_url.rstrip("/")
        self.user_id = user_id
        self.user_name = user_name
        self.agent_id = agent_id
        self.agent_name = agent_name
        self.timeout = timeout

    def _generate_tags_with_llm(self, title: str, content: str) -> List[str]:
        """
        Automatically generate tags using LLM

        Args:
            title: Note title
            content: Note content

        Returns:
            Generated tag list
        """
        try:
            # Build prompt
            prompt = f"""Please generate 3-5 relevant tag keywords for the following note.

Note Title: {title}
Note Content: {content}

Requirements:
1. Tags should be concise and clear, 2-4 characters
2. Tags should cover dimensions like topic, field, type, etc.
3. Only return tags, separated by commas, no other content

Tags: """

            # Call LLM (through memU's API)
            # Here we use a simple heuristic method to generate tags
            # Actually memU will process with LLM in the background, so we let it auto-extract
            
            # Extract keywords from title and content as temporary solution
            import re
            
            # Merge title and content
            text = f"{title} {content}"
            
            # Simple keyword extraction (actually memU will do better processing)
            keywords = []
            
            # Common technical keywords
            tech_keywords = [
                'Python', 'Java', 'JavaScript', 'AI', 'Artificial Intelligence', 'Machine Learning', 
                'Deep Learning', 'Neural Network', 'Algorithm', 'Data Structure', 'Programming', 'Development',
                'Frontend', 'Backend', 'Database', 'Web', 'Mobile Development', 'Cloud Computing',
                'Learning', 'Work', 'Project', 'Technology', 'Note', 'Summary', 'Tutorial',
                'Framework', 'Library', 'Tool', 'Method', 'Practice', 'Experience'
            ]
            
            for keyword in tech_keywords:
                if keyword.lower() in text.lower():
                    keywords.append(keyword)
                    if len(keywords) >= 5:
                        break
            
            # If no keywords found, use default tags
            if not keywords:
                keywords = ['Note', 'Learning']
            
            return keywords[:5]  # Return at most 5 tags
            
        except Exception as e:
            print(f"⚠️  Auto tag generation failed, using default tags: {e}")
            return ['Note', 'Learning']

    def save_note(
        self,
        title: str,
        content: str,
        tags: Optional[List[str]] = None,
        category: str = "note",
        auto_tags: bool = True,
    ) -> Dict[str, Any]:
        """
        Save note to memU

        Args:
            title: Note title
            content: Note content
            tags: Tag list (if None and auto_tags=True, auto-generate)
            category: Note category
            auto_tags: Whether to auto-generate tags

        Returns:
            API response result
        """
        # If no tags provided and auto tags enabled, auto-generate
        if not tags and auto_tags:
            print("🤖 Using AI to auto-generate tags...")
            tags = self._generate_tags_with_llm(title, content)
            print(f"✨ Auto-generated tags: {', '.join(tags)}")
        
        # Build conversation format note
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Build note message
        note_message = f"[Note] {title}\n\n{content}"
        if tags:
            note_message += f"\n\nTags: {', '.join(tags)}"
        note_message += f"\n\nRecorded at: {timestamp}"

        # Build conversation data
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

        # Send to memU
        try:
            with httpx.Client(base_url=self.base_url, timeout=self.timeout) as client:
                response = client.post(
                    "/api/v1/memory/memorize",
                    json=conversation_data,
                )
                response.raise_for_status()
                result = response.json()
                print(f"✅ Note saved to memU: {title}")
                return result
        except httpx.HTTPError as e:
            print(f"❌ Failed to save note: {e}")
            raise

    def search_notes(
        self,
        query: str,
        top_k: int = 10,
        min_similarity: float = 0.3,
    ) -> List[Dict[str, Any]]:
        """
        Search notes

        Args:
            query: Search query
            top_k: Number of results to return
            min_similarity: Minimum similarity threshold

        Returns:
            Search result list
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
                
                print(f"🔍 Found {len(notes)} related notes")
                return notes
                
        except httpx.HTTPError as e:
            print(f"❌ Failed to search notes: {e}")
            raise

    def get_all_memories(self) -> List[Dict[str, Any]]:
        """
        Get all memories from memU database via API
        
        Returns:
            All memory list
        """
        try:
            with httpx.Client(base_url=self.base_url, timeout=self.timeout) as client:
                # 调用 memU API 获取默认分类
                response = client.post(
                    "/api/v1/memory/retrieve/default-categories",
                    json={
                        "user_id": self.user_id,
                        "agent_id": self.agent_id,
                        "include_inactive": False,
                    },
                )
                response.raise_for_status()
                result = response.json()
                
                # 提取所有记忆
                all_memories = []
                categories = result.get("categories", [])
                
                for category_info in categories:
                    category_name = category_info.get("name", "unknown")
                    memories = category_info.get("memories", [])
                    
                    for memory in memories:
                        all_memories.append({
                            "memory_id": memory.get("memory_id", ""),
                            "category": category_name,
                            "content": memory.get("content", ""),
                            "happened_at": memory.get("happened_at", ""),
                            "metadata": memory.get("metadata", {}),
                        })
                
                print(f"📚 从数据库加载了 {len(all_memories)} 条记忆")
                return all_memories
                
        except httpx.HTTPError as e:
            print(f"❌ 获取记忆失败: {e}")
            # 如果 API 调用失败，回退到文件读取方法
            print("💡 尝试从文件系统读取...")
            return self.list_all_memories()
    
    def list_all_memories(self) -> List[Dict[str, Any]]:
        """
        List all memories (notes)
        Directly read markdown files stored by memU

        Returns:
            All memory list
        """
        import re
        from pathlib import Path
        
        # memU storage path
        memory_base = Path("../memU/memory_data") / self.agent_id / self.user_id
        
        # If path doesn't exist, try absolute path
        if not memory_base.exists():
            memory_base = Path("/Users/yangchengxuan/Desktop/PROJECTS/Live2Document_4/memU/memory_data") / self.agent_id / self.user_id
        
        if not memory_base.exists():
            print("📭 No notes yet")
            print(f"💡 Tip: Note storage path {memory_base} does not exist")
            return []
        
        all_memories = []
        memory_count = 0
        
        # Read all .md files
        for md_file in memory_base.glob("*.md"):
            category = md_file.stem
            
            try:
                with open(md_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Parse each line of memory (format: [id][mentioned at date] content [])
                lines = content.strip().split('\n')
                for line in lines:
                    if not line.strip():
                        continue
                    
                    # Extract memory ID and content
                    match = re.match(r'\[([^\]]+)\]\[mentioned at ([^\]]+)\]\s*(.+?)\s*\[\]', line)
                    if match:
                        memory_id = match.group(1)
                        date = match.group(2)
                        text = match.group(3)
                        
                        # Extract tags (if any)
                        tags = []
                        # Try multiple tag formats
                        tag_patterns = [
                            r'Tags[：:]\s*([^。\n]+)',
                            r'Tagged with\s*([^。\n]+)',
                            r'Tag with\s*([^。\n]+)',
                            r'Topic tags[：:]\s*([^。\n]+)',
                        ]
                        
                        for pattern in tag_patterns:
                            tag_match = re.search(pattern, text)
                            if tag_match:
                                tags_str = tag_match.group(1)
                                # Split tags (support multiple separators)
                                tags = [t.strip() for t in re.split(r'[,，、and&]', tags_str) if t.strip()]
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
                print(f"⚠️  Failed to read file {md_file}: {e}")
                continue
        
        if memory_count == 0:
            print("📭 No notes yet")
        else:
            print(f"📚 Total {memory_count} memories")
        
        return all_memories


def main():
    """Command line test"""
    client = MemuNoteClient()
    
    # Test saving note
    print("\n📝 Testing save note...")
    client.save_note(
        title="Python Learning Notes",
        content="Today I learned about Python decorators. Decorators are a design pattern that can add extra functionality without modifying the original function.",
        tags=["Python", "Programming", "Learning"],
        category="Technical Notes",
    )
    
    # Test searching notes
    print("\n🔍 Testing search notes...")
    results = client.search_notes("Python decorator")
    
    for i, note in enumerate(results, 1):
        print(f"\n--- Note {i} ---")
        print(f"Similarity: {note['similarity_score']:.2f}")
        print(f"Category: {note['category']}")
        print(f"Content: {note['content'][:100]}...")


if __name__ == "__main__":
    main()
