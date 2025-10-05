#!/usr/bin/env python3
"""
memU 笔记 Web 应用 - 后端服务
使用 FastAPI 提供 REST API
"""

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, FileResponse
from pydantic import BaseModel
from typing import List, Optional
import uvicorn
from memu_note_client import MemuNoteClient
import os

# 创建 FastAPI 应用
app = FastAPI(title="memU 笔记应用", description="基于 memU 的智能笔记系统")

# 初始化 memU 客户端
memu_client = MemuNoteClient(
    base_url="http://127.0.0.1:8000",
    user_id="note_user",
    user_name="笔记用户",
    agent_id="note_agent",
    agent_name="笔记助手",
)


# 请求模型
class NoteCreate(BaseModel):
    """创建笔记请求"""
    title: str
    content: str
    tags: Optional[List[str]] = []
    category: Optional[str] = "note"


class NoteSearch(BaseModel):
    """搜索笔记请求"""
    query: str
    top_k: Optional[int] = 10
    min_similarity: Optional[float] = 0.3


# 响应模型
class NoteResponse(BaseModel):
    """笔记响应"""
    success: bool
    message: str
    data: Optional[dict] = None


class SearchResult(BaseModel):
    """搜索结果"""
    memory_id: str
    category: str
    content: str
    similarity_score: float


# API 路由
@app.get("/", response_class=HTMLResponse)
async def root():
    """返回主页"""
    html_file = os.path.join(os.path.dirname(__file__), "web", "index.html")
    if os.path.exists(html_file):
        with open(html_file, "r", encoding="utf-8") as f:
            return f.read()
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <title>memU 笔记应用</title>
    </head>
    <body>
        <h1>memU 笔记应用</h1>
        <p>Web 界面文件未找到。请确保 web/index.html 存在。</p>
    </body>
    </html>
    """


@app.get("/api/health")
async def health_check():
    """健康检查"""
    return {"status": "ok", "message": "memU 笔记应用运行正常"}


@app.post("/api/notes", response_model=NoteResponse)
async def create_note(note: NoteCreate):
    """创建新笔记"""
    try:
        # 检查是否需要自动生成标签
        auto_generated_tags = None
        tags_to_use = note.tags
        
        if not tags_to_use or len(tags_to_use) == 0:
            # 自动生成标签
            auto_generated_tags = memu_client._generate_tags_with_llm(note.title, note.content)
            tags_to_use = auto_generated_tags
        
        result = memu_client.save_note(
            title=note.title,
            content=note.content,
            tags=tags_to_use,
            category=note.category,
            auto_tags=False,  # 我们已经在这里处理了自动标签
        )
        
        response_data = {
            "success": True,
            "message": f"笔记 '{note.title}' 已保存",
            "data": result,
        }
        
        # 如果使用了自动生成的标签，添加到响应中
        if auto_generated_tags:
            response_data["auto_tags"] = auto_generated_tags
        
        return response_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"保存笔记失败: {str(e)}")


@app.post("/api/notes/search")
async def search_notes(search: NoteSearch):
    """搜索笔记"""
    try:
        results = memu_client.search_notes(
            query=search.query,
            top_k=search.top_k,
            min_similarity=search.min_similarity,
        )
        return {
            "success": True,
            "count": len(results),
            "results": results,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"搜索失败: {str(e)}")


@app.get("/api/notes")
async def list_notes():
    """列出所有笔记"""
    try:
        results = memu_client.search_notes(
            query="笔记",
            top_k=100,
            min_similarity=0.1,
        )
        return {
            "success": True,
            "count": len(results),
            "results": results,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取笔记列表失败: {str(e)}")


# 挂载静态文件
web_dir = os.path.join(os.path.dirname(__file__), "web")
if os.path.exists(web_dir):
    app.mount("/static", StaticFiles(directory=web_dir), name="static")


def main():
    """启动服务器"""
    print("🚀 启动 memU 笔记 Web 应用...")
    print("📝 访问地址: http://localhost:8080")
    print("📖 API 文档: http://localhost:8080/docs")
    print("")
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8080,
        log_level="info",
    )


if __name__ == "__main__":
    main()
