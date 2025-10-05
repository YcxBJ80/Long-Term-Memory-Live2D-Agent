#!/usr/bin/env python3
"""
memU 笔记软件 - 命令行版本
将笔记直接存储到 memU 记忆库中
"""

import argparse
import sys
from typing import Optional
from memu_note_client import MemuNoteClient


def add_note(client: MemuNoteClient, args):
    """添加新笔记"""
    title = args.title
    content = args.content
    tags = args.tags.split(",") if args.tags else []
    category = args.category or "note"
    
    try:
        client.save_note(
            title=title,
            content=content,
            tags=tags,
            category=category,
        )
        print(f"\n✅ 笔记 '{title}' 已成功保存到 memU！")
    except Exception as e:
        print(f"\n❌ 保存失败: {e}")
        sys.exit(1)


def search_notes(client: MemuNoteClient, args):
    """搜索笔记"""
    query = args.query
    top_k = args.limit or 10
    min_similarity = args.min_similarity or 0.3
    
    try:
        results = client.search_notes(
            query=query,
            top_k=top_k,
            min_similarity=min_similarity,
        )
        
        if not results:
            print("\n📭 没有找到相关笔记")
            return
        
        print(f"\n🔍 找到 {len(results)} 条相关笔记:\n")
        print("=" * 80)
        
        for i, note in enumerate(results, 1):
            print(f"\n📝 笔记 {i}")
            print(f"   相似度: {note['similarity_score']:.2%}")
            print(f"   分类: {note['category']}")
            print(f"   内容预览:")
            
            # 显示内容预览
            content = note['content']
            lines = content.split('\n')
            for line in lines[:5]:  # 只显示前5行
                print(f"      {line}")
            
            if len(lines) > 5:
                print(f"      ... (还有 {len(lines) - 5} 行)")
            
            print("-" * 80)
            
    except Exception as e:
        print(f"\n❌ 搜索失败: {e}")
        sys.exit(1)


def list_notes(client: MemuNoteClient, args):
    """列出所有笔记"""
    try:
        results = client.list_all_memories()
        
        if not results:
            print("\n📭 还没有任何笔记")
            return
        
        print(f"\n📚 共有 {len(results)} 条笔记:\n")
        print("=" * 80)
        
        for i, note in enumerate(results, 1):
            print(f"\n{i}. {note.get('category', 'note')}")
            
            # 尝试从内容中提取标题
            content = note['content']
            first_line = content.split('\n')[0]
            if first_line.startswith('[笔记]'):
                title = first_line.replace('[笔记]', '').strip()
                print(f"   标题: {title}")
            
            # 显示内容预览
            preview = content[:100].replace('\n', ' ')
            print(f"   预览: {preview}...")
            print("-" * 80)
            
    except Exception as e:
        print(f"\n❌ 列出笔记失败: {e}")
        sys.exit(1)


def interactive_mode(client: MemuNoteClient):
    """交互式模式"""
    print("\n" + "=" * 80)
    print("📝 memU 笔记软件 - 交互模式")
    print("=" * 80)
    print("\n命令:")
    print("  add    - 添加新笔记")
    print("  search - 搜索笔记")
    print("  list   - 列出所有笔记")
    print("  quit   - 退出")
    print()
    
    while True:
        try:
            command = input("\n> ").strip().lower()
            
            if command == "quit" or command == "exit":
                print("\n👋 再见！")
                break
            
            elif command == "add":
                print("\n--- 添加新笔记 ---")
                title = input("标题: ").strip()
                if not title:
                    print("❌ 标题不能为空")
                    continue
                
                print("内容 (输入 'END' 结束):")
                content_lines = []
                while True:
                    line = input()
                    if line.strip() == "END":
                        break
                    content_lines.append(line)
                content = "\n".join(content_lines)
                
                if not content:
                    print("❌ 内容不能为空")
                    continue
                
                tags_input = input("标签 (用逗号分隔，可选): ").strip()
                tags = [t.strip() for t in tags_input.split(",")] if tags_input else []
                
                category = input("分类 (可选，默认为 'note'): ").strip() or "note"
                
                try:
                    client.save_note(
                        title=title,
                        content=content,
                        tags=tags,
                        category=category,
                    )
                    print(f"\n✅ 笔记 '{title}' 已保存！")
                except Exception as e:
                    print(f"\n❌ 保存失败: {e}")
            
            elif command == "search":
                query = input("\n搜索关键词: ").strip()
                if not query:
                    print("❌ 搜索关键词不能为空")
                    continue
                
                try:
                    results = client.search_notes(query)
                    
                    if not results:
                        print("\n📭 没有找到相关笔记")
                        continue
                    
                    print(f"\n🔍 找到 {len(results)} 条相关笔记:\n")
                    
                    for i, note in enumerate(results, 1):
                        print(f"\n📝 笔记 {i}")
                        print(f"   相似度: {note['similarity_score']:.2%}")
                        print(f"   分类: {note['category']}")
                        
                        # 显示内容
                        content = note['content']
                        lines = content.split('\n')
                        print(f"   内容:")
                        for line in lines[:3]:
                            print(f"      {line}")
                        if len(lines) > 3:
                            print(f"      ... (还有 {len(lines) - 3} 行)")
                        print("-" * 60)
                        
                except Exception as e:
                    print(f"\n❌ 搜索失败: {e}")
            
            elif command == "list":
                try:
                    results = client.list_all_memories()
                    
                    if not results:
                        print("\n📭 还没有任何笔记")
                        continue
                    
                    print(f"\n📚 共有 {len(results)} 条笔记:\n")
                    
                    for i, note in enumerate(results, 1):
                        content = note['content']
                        first_line = content.split('\n')[0]
                        
                        # 提取标题
                        if first_line.startswith('[笔记]'):
                            title = first_line.replace('[笔记]', '').strip()
                        else:
                            title = first_line[:50]
                        
                        print(f"{i}. {title}")
                        print(f"   分类: {note.get('category', 'note')}")
                        print()
                        
                except Exception as e:
                    print(f"\n❌ 列出笔记失败: {e}")
            
            else:
                print("❌ 未知命令。请使用 add, search, list 或 quit")
        
        except KeyboardInterrupt:
            print("\n\n👋 再见！")
            break
        except EOFError:
            print("\n\n👋 再见！")
            break


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description="memU 笔记软件 - 将笔记直接存储到 memU 记忆库",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 添加笔记
  %(prog)s add -t "Python 学习" -c "今天学习了装饰器" --tags "Python,学习"
  
  # 搜索笔记
  %(prog)s search "Python 装饰器"
  
  # 列出所有笔记
  %(prog)s list
  
  # 交互模式
  %(prog)s interactive
        """,
    )
    
    parser.add_argument(
        "--base-url",
        default="http://127.0.0.1:8000",
        help="memU API 地址 (默认: http://127.0.0.1:8000)",
    )
    parser.add_argument(
        "--user-id",
        default="note_user",
        help="用户 ID (默认: note_user)",
    )
    parser.add_argument(
        "--agent-id",
        default="note_agent",
        help="智能体 ID (默认: note_agent)",
    )
    
    subparsers = parser.add_subparsers(dest="command", help="可用命令")
    
    # add 命令
    add_parser = subparsers.add_parser("add", help="添加新笔记")
    add_parser.add_argument("-t", "--title", required=True, help="笔记标题")
    add_parser.add_argument("-c", "--content", required=True, help="笔记内容")
    add_parser.add_argument("--tags", help="标签，用逗号分隔")
    add_parser.add_argument("--category", help="笔记分类")
    
    # search 命令
    search_parser = subparsers.add_parser("search", help="搜索笔记")
    search_parser.add_argument("query", help="搜索关键词")
    search_parser.add_argument("-l", "--limit", type=int, help="返回结果数量 (默认: 10)")
    search_parser.add_argument(
        "-s", "--min-similarity", type=float, help="最小相似度 (默认: 0.3)"
    )
    
    # list 命令
    list_parser = subparsers.add_parser("list", help="列出所有笔记")
    
    # interactive 命令
    interactive_parser = subparsers.add_parser("interactive", help="交互模式")
    
    args = parser.parse_args()
    
    # 创建客户端
    client = MemuNoteClient(
        base_url=args.base_url,
        user_id=args.user_id,
        agent_id=args.agent_id,
    )
    
    # 执行命令
    if args.command == "add":
        add_note(client, args)
    elif args.command == "search":
        search_notes(client, args)
    elif args.command == "list":
        list_notes(client, args)
    elif args.command == "interactive":
        interactive_mode(client)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
