#!/usr/bin/env python3
"""
memU Note Software - GUI Version
Create a simple graphical interface using tkinter
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
from typing import Optional
from memu_note_client import MemuNoteClient
import threading


class NoteApp:
    """memU Note Application GUI"""

    def __init__(self, root):
        self.root = root
        self.root.title("📝 memU Note Software")
        self.root.geometry("900x700")
        
        # Initialize memU client
        self.client = MemuNoteClient()
        
        # Create interface
        self.create_widgets()
        
    def create_widgets(self):
        """Create interface components"""
        # Create notebook (tabs)
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Add note tab
        self.add_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.add_frame, text="✏️ New Note")
        self.create_add_tab()
        
        # Search notes tab
        self.search_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.search_frame, text="🔍 Search Notes")
        self.create_search_tab()
        
        # Status bar
        self.status_bar = ttk.Label(
            self.root,
            text="Ready",
            relief=tk.SUNKEN,
            anchor=tk.W,
        )
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
    def create_add_tab(self):
        """Create add note tab"""
        # Title
        title_frame = ttk.Frame(self.add_frame)
        title_frame.pack(fill=tk.X, padx=20, pady=10)
        
        ttk.Label(title_frame, text="Title:", font=("Arial", 12)).pack(side=tk.LEFT)
        self.title_entry = ttk.Entry(title_frame, font=("Arial", 12))
        self.title_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=10)
        
        # Category
        category_frame = ttk.Frame(self.add_frame)
        category_frame.pack(fill=tk.X, padx=20, pady=5)
        
        ttk.Label(category_frame, text="Category:").pack(side=tk.LEFT)
        self.category_entry = ttk.Entry(category_frame)
        self.category_entry.insert(0, "note")
        self.category_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=10)
        
        # Tags
        tags_frame = ttk.Frame(self.add_frame)
        tags_frame.pack(fill=tk.X, padx=20, pady=5)
        
        ttk.Label(tags_frame, text="Tags:").pack(side=tk.LEFT)
        self.tags_entry = ttk.Entry(tags_frame)
        self.tags_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=10)
        ttk.Label(tags_frame, text="(comma separated)", font=("Arial", 9)).pack(side=tk.LEFT)
        
        # Content
        content_frame = ttk.Frame(self.add_frame)
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        ttk.Label(content_frame, text="Content:", font=("Arial", 12)).pack(anchor=tk.W)
        self.content_text = scrolledtext.ScrolledText(
            content_frame,
            font=("Arial", 11),
            wrap=tk.WORD,
        )
        self.content_text.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Buttons
        button_frame = ttk.Frame(self.add_frame)
        button_frame.pack(fill=tk.X, padx=20, pady=10)
        
        ttk.Button(
            button_frame,
            text="💾 Save Note",
            command=self.save_note,
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            button_frame,
            text="🗑️ Clear",
            command=self.clear_form,
        ).pack(side=tk.LEFT, padx=5)
        
    def create_search_tab(self):
        """Create search notes tab"""
        # Search box
        search_frame = ttk.Frame(self.search_frame)
        search_frame.pack(fill=tk.X, padx=20, pady=10)
        
        ttk.Label(search_frame, text="Search:", font=("Arial", 12)).pack(side=tk.LEFT)
        self.search_entry = ttk.Entry(search_frame, font=("Arial", 12))
        self.search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=10)
        self.search_entry.bind("<Return>", lambda e: self.search_notes())
        
        ttk.Button(
            search_frame,
            text="🔍 Search",
            command=self.search_notes,
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            search_frame,
            text="📚 Show All",
            command=self.list_all_notes,
        ).pack(side=tk.LEFT, padx=5)
        
        # Result display
        result_frame = ttk.Frame(self.search_frame)
        result_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        ttk.Label(result_frame, text="Search Results:", font=("Arial", 12)).pack(anchor=tk.W)
        
        # Create tree view
        self.result_tree = ttk.Treeview(
            result_frame,
            columns=("similarity", "category", "preview"),
            show="tree headings",
            height=15,
        )
        
        self.result_tree.heading("#0", text="No.")
        self.result_tree.heading("similarity", text="Similarity")
        self.result_tree.heading("category", text="Category")
        self.result_tree.heading("preview", text="Content Preview")
        
        self.result_tree.column("#0", width=50)
        self.result_tree.column("similarity", width=80)
        self.result_tree.column("category", width=100)
        self.result_tree.column("preview", width=500)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(result_frame, orient=tk.VERTICAL, command=self.result_tree.yview)
        self.result_tree.configure(yscrollcommand=scrollbar.set)
        
        self.result_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Double-click to view details
        self.result_tree.bind("<Double-1>", self.show_note_detail)
        
        # Detail display
        detail_frame = ttk.Frame(self.search_frame)
        detail_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        ttk.Label(detail_frame, text="Note Details:", font=("Arial", 12)).pack(anchor=tk.W)
        self.detail_text = scrolledtext.ScrolledText(
            detail_frame,
            font=("Arial", 10),
            wrap=tk.WORD,
            height=10,
        )
        self.detail_text.pack(fill=tk.BOTH, expand=True, pady=5)
        
    def save_note(self):
        """Save note"""
        title = self.title_entry.get().strip()
        content = self.content_text.get("1.0", tk.END).strip()
        category = self.category_entry.get().strip() or "note"
        tags_str = self.tags_entry.get().strip()
        tags = [t.strip() for t in tags_str.split(",")] if tags_str else []
        
        if not title:
            messagebox.showwarning("Warning", "Please enter note title")
            return
        
        if not content:
            messagebox.showwarning("Warning", "Please enter note content")
            return
        
        # Save in background thread
        self.status_bar.config(text="Saving note...")
        
        def save_thread():
            try:
                self.client.save_note(
                    title=title,
                    content=content,
                    tags=tags,
                    category=category,
                )
                self.root.after(0, lambda: self.status_bar.config(text=f"✅ Note '{title}' saved"))
                self.root.after(0, lambda: messagebox.showinfo("Success", f"Note '{title}' saved to memU!"))
                self.root.after(0, self.clear_form)
            except Exception as e:
                self.root.after(0, lambda: self.status_bar.config(text=f"❌ Save failed: {e}"))
                self.root.after(0, lambda: messagebox.showerror("Error", f"Save failed: {e}"))
        
        threading.Thread(target=save_thread, daemon=True).start()
        
    def clear_form(self):
        """Clear form"""
        self.title_entry.delete(0, tk.END)
        self.content_text.delete("1.0", tk.END)
        self.tags_entry.delete(0, tk.END)
        self.category_entry.delete(0, tk.END)
        self.category_entry.insert(0, "note")
        
    def search_notes(self):
        """Search notes"""
        query = self.search_entry.get().strip()
        
        if not query:
            messagebox.showwarning("Warning", "Please enter search keywords")
            return
        
        # Clear results
        for item in self.result_tree.get_children():
            self.result_tree.delete(item)
        
        self.detail_text.delete("1.0", tk.END)
        self.status_bar.config(text=f"Searching for '{query}'...")
        
        def search_thread():
            try:
                results = self.client.search_notes(query)
                self.root.after(0, lambda: self.display_results(results))
                self.root.after(0, lambda: self.status_bar.config(text=f"Found {len(results)} notes"))
            except Exception as e:
                self.root.after(0, lambda: self.status_bar.config(text=f"❌ Search failed: {e}"))
                self.root.after(0, lambda: messagebox.showerror("Error", f"Search failed: {e}"))
        
        threading.Thread(target=search_thread, daemon=True).start()
        
    def list_all_notes(self):
        """List all notes"""
        # Clear results
        for item in self.result_tree.get_children():
            self.result_tree.delete(item)
        
        self.detail_text.delete("1.0", tk.END)
        self.status_bar.config(text="Loading all notes...")
        
        def list_thread():
            try:
                results = self.client.list_all_memories()
                self.root.after(0, lambda: self.display_results(results))
                self.root.after(0, lambda: self.status_bar.config(text=f"Total {len(results)} notes"))
            except Exception as e:
                self.root.after(0, lambda: self.status_bar.config(text=f"❌ Load failed: {e}"))
                self.root.after(0, lambda: messagebox.showerror("Error", f"Load failed: {e}"))
        
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
    """Main function"""
    root = tk.Tk()
    app = NoteApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
