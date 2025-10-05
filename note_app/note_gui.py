#!/usr/bin/env python3
"""
memU 笔记软件 - 图形界面版本
使用 tkinter 创建简单的图形界面
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
from typing import Optional
from memu_note_client import MemuNoteClient
import threading


class NoteApp:
    """memU 笔记应用图形界面"""

    def __init__(self, root):
        self.root = root
        self.root.title("📝 memU 笔记软件")
        self.root.geometry("900x700")
        
        # 初始化 memU 客户端
        self.client = MemuNoteClient()
        
        # 创建界面
        self.create_widgets()
        
    def create_widgets(self):
        """创建界面组件"""
        # 创建笔记本（标签页）
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 添加笔记标签页
        self.add_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.add_frame, text="✏️ 新建笔记")
        self.create_add_tab()
        
        # 搜索笔记标签页
        self.search_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.search_frame, text="🔍 搜索笔记")
        self.create_search_tab()
        
        # 状态栏
        self.status_bar = ttk.Label(
            self.root,
            text="就绪",
            relief=tk.SUNKEN,
            anchor=tk.W,
        )
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
    def create_add_tab(self):
        """创建添加笔记标签页"""
        # 标题
        title_frame = ttk.Frame(self.add_frame)
        title_frame.pack(fill=tk.X, padx=20, pady=10)
        
        ttk.Label(title_frame, text="标题:", font=("Arial", 12)).pack(side=tk.LEFT)
        self.title_entry = ttk.Entry(title_frame, font=("Arial", 12))
        self.title_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=10)
        
        # 分类
        category_frame = ttk.Frame(self.add_frame)
        category_frame.pack(fill=tk.X, padx=20, pady=5)
        
        ttk.Label(category_frame, text="分类:").pack(side=tk.LEFT)
        self.category_entry = ttk.Entry(category_frame)
        self.category_entry.insert(0, "note")
        self.category_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=10)
        
        # 标签
        tags_frame = ttk.Frame(self.add_frame)
        tags_frame.pack(fill=tk.X, padx=20, pady=5)
        
        ttk.Label(tags_frame, text="标签:").pack(side=tk.LEFT)
        self.tags_entry = ttk.Entry(tags_frame)
        self.tags_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=10)
        ttk.Label(tags_frame, text="(用逗号分隔)", font=("Arial", 9)).pack(side=tk.LEFT)
        
        # 内容
        content_frame = ttk.Frame(self.add_frame)
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        ttk.Label(content_frame, text="内容:", font=("Arial", 12)).pack(anchor=tk.W)
        self.content_text = scrolledtext.ScrolledText(
            content_frame,
            font=("Arial", 11),
            wrap=tk.WORD,
        )
        self.content_text.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # 按钮
        button_frame = ttk.Frame(self.add_frame)
        button_frame.pack(fill=tk.X, padx=20, pady=10)
        
        ttk.Button(
            button_frame,
            text="💾 保存笔记",
            command=self.save_note,
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            button_frame,
            text="🗑️ 清空",
            command=self.clear_form,
        ).pack(side=tk.LEFT, padx=5)
        
    def create_search_tab(self):
        """创建搜索笔记标签页"""
        # 搜索框
        search_frame = ttk.Frame(self.search_frame)
        search_frame.pack(fill=tk.X, padx=20, pady=10)
        
        ttk.Label(search_frame, text="搜索:", font=("Arial", 12)).pack(side=tk.LEFT)
        self.search_entry = ttk.Entry(search_frame, font=("Arial", 12))
        self.search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=10)
        self.search_entry.bind("<Return>", lambda e: self.search_notes())
        
        ttk.Button(
            search_frame,
            text="🔍 搜索",
            command=self.search_notes,
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            search_frame,
            text="📚 显示全部",
            command=self.list_all_notes,
        ).pack(side=tk.LEFT, padx=5)
        
        # 结果显示
        result_frame = ttk.Frame(self.search_frame)
        result_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        ttk.Label(result_frame, text="搜索结果:", font=("Arial", 12)).pack(anchor=tk.W)
        
        # 创建树形视图
        self.result_tree = ttk.Treeview(
            result_frame,
            columns=("similarity", "category", "preview"),
            show="tree headings",
            height=15,
        )
        
        self.result_tree.heading("#0", text="序号")
        self.result_tree.heading("similarity", text="相似度")
        self.result_tree.heading("category", text="分类")
        self.result_tree.heading("preview", text="内容预览")
        
        self.result_tree.column("#0", width=50)
        self.result_tree.column("similarity", width=80)
        self.result_tree.column("category", width=100)
        self.result_tree.column("preview", width=500)
        
        # 滚动条
        scrollbar = ttk.Scrollbar(result_frame, orient=tk.VERTICAL, command=self.result_tree.yview)
        self.result_tree.configure(yscrollcommand=scrollbar.set)
        
        self.result_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # 双击查看详情
        self.result_tree.bind("<Double-1>", self.show_note_detail)
        
        # 详情显示
        detail_frame = ttk.Frame(self.search_frame)
        detail_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        ttk.Label(detail_frame, text="笔记详情:", font=("Arial", 12)).pack(anchor=tk.W)
        self.detail_text = scrolledtext.ScrolledText(
            detail_frame,
            font=("Arial", 10),
            wrap=tk.WORD,
            height=10,
        )
        self.detail_text.pack(fill=tk.BOTH, expand=True, pady=5)
        
    def save_note(self):
        """保存笔记"""
        title = self.title_entry.get().strip()
        content = self.content_text.get("1.0", tk.END).strip()
        category = self.category_entry.get().strip() or "note"
        tags_str = self.tags_entry.get().strip()
        tags = [t.strip() for t in tags_str.split(",")] if tags_str else []
        
        if not title:
            messagebox.showwarning("警告", "请输入笔记标题")
            return
        
        if not content:
            messagebox.showwarning("警告", "请输入笔记内容")
            return
        
        # 在后台线程中保存
        self.status_bar.config(text="正在保存笔记...")
        
        def save_thread():
            try:
                self.client.save_note(
                    title=title,
                    content=content,
                    tags=tags,
                    category=category,
                )
                self.root.after(0, lambda: self.status_bar.config(text=f"✅ 笔记 '{title}' 已保存"))
                self.root.after(0, lambda: messagebox.showinfo("成功", f"笔记 '{title}' 已保存到 memU！"))
                self.root.after(0, self.clear_form)
            except Exception as e:
                self.root.after(0, lambda: self.status_bar.config(text=f"❌ 保存失败: {e}"))
                self.root.after(0, lambda: messagebox.showerror("错误", f"保存失败: {e}"))
        
        threading.Thread(target=save_thread, daemon=True).start()
        
    def clear_form(self):
        """清空表单"""
        self.title_entry.delete(0, tk.END)
        self.content_text.delete("1.0", tk.END)
        self.tags_entry.delete(0, tk.END)
        self.category_entry.delete(0, tk.END)
        self.category_entry.insert(0, "note")
        
    def search_notes(self):
        """搜索笔记"""
        query = self.search_entry.get().strip()
        
        if not query:
            messagebox.showwarning("警告", "请输入搜索关键词")
            return
        
        # 清空结果
        for item in self.result_tree.get_children():
            self.result_tree.delete(item)
        
        self.detail_text.delete("1.0", tk.END)
        self.status_bar.config(text=f"正在搜索 '{query}'...")
        
        def search_thread():
            try:
                results = self.client.search_notes(query)
                self.root.after(0, lambda: self.display_results(results))
                self.root.after(0, lambda: self.status_bar.config(text=f"找到 {len(results)} 条笔记"))
            except Exception as e:
                self.root.after(0, lambda: self.status_bar.config(text=f"❌ 搜索失败: {e}"))
                self.root.after(0, lambda: messagebox.showerror("错误", f"搜索失败: {e}"))
        
        threading.Thread(target=search_thread, daemon=True).start()
        
    def list_all_notes(self):
        """列出所有笔记"""
        # 清空结果
        for item in self.result_tree.get_children():
            self.result_tree.delete(item)
        
        self.detail_text.delete("1.0", tk.END)
        self.status_bar.config(text="正在加载所有笔记...")
        
        def list_thread():
            try:
                results = self.client.list_all_memories()
                self.root.after(0, lambda: self.display_results(results))
                self.root.after(0, lambda: self.status_bar.config(text=f"共有 {len(results)} 条笔记"))
            except Exception as e:
                self.root.after(0, lambda: self.status_bar.config(text=f"❌ 加载失败: {e}"))
                self.root.after(0, lambda: messagebox.showerror("错误", f"加载失败: {e}"))
        
        threading.Thread(target=list_thread, daemon=True).start()
        
    def display_results(self, results):
        """显示搜索结果"""
        for i, note in enumerate(results, 1):
            similarity = f"{note['similarity_score']:.1%}"
            category = note.get('category', 'note')
            content = note['content']
            
            # 提取预览
            preview = content.split('\n')[0][:60]
            if len(content) > 60:
                preview += "..."
            
            # 插入到树形视图
            self.result_tree.insert(
                "",
                tk.END,
                text=str(i),
                values=(similarity, category, preview),
                tags=(str(i),),
            )
            
            # 存储完整内容
            self.result_tree.set(self.result_tree.get_children()[-1], "full_content", content)
        
    def show_note_detail(self, event):
        """显示笔记详情"""
        selection = self.result_tree.selection()
        if not selection:
            return
        
        item = selection[0]
        content = self.result_tree.set(item, "full_content")
        
        self.detail_text.delete("1.0", tk.END)
        self.detail_text.insert("1.0", content)


def main():
    """主函数"""
    root = tk.Tk()
    app = NoteApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
