#!/usr/bin/env python3
"""
memU Note App - Command Line Version
Store notes directly into memU memory database
"""

import argparse
import sys
from typing import Optional
from memu_note_client import MemuNoteClient


def add_note(client: MemuNoteClient, args):
    """Add new note"""
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
        print(f"\n✅ Note '{title}' successfully saved to memU!")
    except Exception as e:
        print(f"\n❌ Save failed: {e}")
        sys.exit(1)


def search_notes(client: MemuNoteClient, args):
    """Search notes"""
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
            print("\n📭 No related notes found")
            return
        
        print(f"\n🔍 Found {len(results)} related notes:\n")
        print("=" * 80)
        
        for i, note in enumerate(results, 1):
            print(f"\n📝 Note {i}")
            print(f"   Similarity: {note['similarity_score']:.2%}")
            print(f"   Category: {note['category']}")
            print(f"   Content preview:")
            
            # Show content preview
            content = note['content']
            lines = content.split('\n')
            for line in lines[:5]:  # Show only first 5 lines
                print(f"      {line}")
            
            if len(lines) > 5:
                print(f"      ... ({len(lines) - 5} more lines)")
            
            print("-" * 80)
            
    except Exception as e:
        print(f"\n❌ Search failed: {e}")
        sys.exit(1)


def list_notes(client: MemuNoteClient, args):
    """List all notes"""
    try:
        results = client.list_all_memories()
        
        if not results:
            return
        
        print(f"\n📚 Total {len(results)} memories:\n")
        print("=" * 100)
        print(f"{'No.':<6} {'Category':<12} {'Date':<12} {'Tags':<30} {'Content Preview'}")
        print("=" * 100)
        
        for i, note in enumerate(results, 1):
            category = note.get('category', 'unknown')
            date = note.get('date', 'unknown')
            tags = note.get('tags', [])
            content = note.get('content', '')
            
            # Tags display
            tags_str = ', '.join(tags[:3]) if tags else '-'
            if len(tags) > 3:
                tags_str += f' (+{len(tags)-3})'
            
            # Content preview (remove extra spaces and newlines)
            preview = content[:50].replace('\n', ' ').strip()
            if len(content) > 50:
                preview += '...'
            
            print(f"{i:<6} {category:<12} {date:<12} {tags_str:<30} {preview}")
        
        print("=" * 100)
        print(f"\n💡 Tip: Use search command to search for specific content")
            
    except Exception as e:
        print(f"\n❌ List notes failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


def interactive_mode(client: MemuNoteClient):
    """Interactive mode"""
    print("\n" + "=" * 80)
    print("📝 memU Note App - Interactive Mode")
    print("=" * 80)
    print("\nCommands:")
    print("  add    - Add new note")
    print("  search - Search notes")
    print("  list   - List all notes")
    print("  quit   - Exit")
    print()
    
    while True:
        try:
            command = input("\n> ").strip().lower()
            
            if command == "quit" or command == "exit":
                print("\n👋 Goodbye!")
                break
            
            elif command == "add":
                print("\n--- Add New Note ---")
                title = input("Title: ").strip()
                if not title:
                    print("❌ Title cannot be empty")
                    continue
                
                print("Content (type 'END' to finish):")
                content_lines = []
                while True:
                    line = input()
                    if line.strip() == "END":
                        break
                    content_lines.append(line)
                content = "\n".join(content_lines)
                
                if not content:
                    print("❌ Content cannot be empty")
                    continue
                
                tags_input = input("Tags (comma-separated, optional): ").strip()
                tags = [t.strip() for t in tags_input.split(",")] if tags_input else []
                
                category = input("Category (optional, default 'note'): ").strip() or "note"
                
                try:
                    client.save_note(
                        title=title,
                        content=content,
                        tags=tags,
                        category=category,
                    )
                    print(f"\n✅ Note '{title}' saved!")
                except Exception as e:
                    print(f"\n❌ Save failed: {e}")
            
            elif command == "search":
                query = input("\nSearch keywords: ").strip()
                if not query:
                    print("❌ Search keywords cannot be empty")
                    continue
                
                try:
                    results = client.search_notes(query)
                    
                    if not results:
                        print("\n📭 No related notes found")
                        continue
                    
                    print(f"\n🔍 Found {len(results)} related notes:\n")
                    
                    for i, note in enumerate(results, 1):
                        print(f"\n📝 Note {i}")
                        print(f"   Similarity: {note['similarity_score']:.2%}")
                        print(f"   Category: {note['category']}")
                        
                        # Show content
                        content = note['content']
                        lines = content.split('\n')
                        print(f"   Content:")
                        for line in lines[:3]:
                            print(f"      {line}")
                        if len(lines) > 3:
                            print(f"      ... ({len(lines) - 3} more lines)")
                        print("-" * 60)
                        
                except Exception as e:
                    print(f"\n❌ Search failed: {e}")
            
            elif command == "list":
                try:
                    results = client.list_all_memories()
                    
                    if not results:
                        print("\n📭 No notes yet")
                        continue
                    
                    print(f"\n📚 Total {len(results)} notes:\n")
                    
                    for i, note in enumerate(results, 1):
                        content = note['content']
                        first_line = content.split('\n')[0]
                        
                        # Extract title
                        if first_line.startswith('[Note]'):
                            title = first_line.replace('[Note]', '').strip()
                        else:
                            title = first_line[:50]
                        
                        print(f"{i}. {title}")
                        print(f"   Category: {note.get('category', 'note')}")
                        print()
                        
                except Exception as e:
                    print(f"\n❌ List notes failed: {e}")
            
            else:
                print("❌ Unknown command. Please use add, search, list or quit")
        
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            break
        except EOFError:
            print("\n\n👋 Goodbye!")
            break


def main():
    """Main function"""
    parser = argparse.ArgumentParser(
        description="memU Note App - Store notes directly into memU memory database",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Add note
  %(prog)s add -t "Python Learning" -c "Learned about decorators today" --tags "Python,learning"
  
  # Search notes
  %(prog)s search "Python decorators"
  
  # List all notes
  %(prog)s list
  
  # Interactive mode
  %(prog)s interactive
        """,
    )
    
    parser.add_argument(
        "--base-url",
        default="http://127.0.0.1:8000",
        help="memU API address (default: http://127.0.0.1:8000)",
    )
    parser.add_argument(
        "--user-id",
        default="note_user",
        help="User ID (default: note_user)",
    )
    parser.add_argument(
        "--agent-id",
        default="note_agent",
        help="Agent ID (default: note_agent)",
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # add command
    add_parser = subparsers.add_parser("add", help="Add new note")
    add_parser.add_argument("-t", "--title", required=True, help="Note title")
    add_parser.add_argument("-c", "--content", required=True, help="Note content")
    add_parser.add_argument("--tags", help="Tags, comma-separated")
    add_parser.add_argument("--category", help="Note category")
    
    # search command
    search_parser = subparsers.add_parser("search", help="Search notes")
    search_parser.add_argument("query", help="Search keywords")
    search_parser.add_argument("-l", "--limit", type=int, help="Number of results to return (default: 10)")
    search_parser.add_argument(
        "-s", "--min-similarity", type=float, help="Minimum similarity (default: 0.3)"
    )
    
    # list command
    list_parser = subparsers.add_parser("list", help="List all notes")
    
    # interactive command
    interactive_parser = subparsers.add_parser("interactive", help="Interactive mode")
    
    args = parser.parse_args()
    
    # Create client
    client = MemuNoteClient(
        base_url=args.base_url,
        user_id=args.user_id,
        agent_id=args.agent_id,
    )
    
    # Execute command
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
