# memU Note Application

A note-taking application that stores notes directly into the memU memory database, providing intelligent storage and retrieval capabilities.

## Features

- Direct integration with memU memory database
- Support for titles, content, tags, and categories
- Semantic search functionality
- Multiple interfaces: Web, CLI, and GUI
- Automatic timestamp recording
- Batch viewing and management capabilities
- Real-time memory retrieval and context enhancement

## Installation

### Dependencies

```bash
pip install httpx
```

For the GUI version, tkinter is also required (usually included with Python).

## Usage

### 1. Web Interface

Start the web server:
```bash
python web_server.py
```

Access the web interface at `http://localhost:8080`

### 2. Command Line Interface

#### Basic Commands

```bash
# Add a note
python note_cli.py add -t "Note Title" -c "Note Content" --tags "tag1,tag2"

# Search notes
python note_cli.py search "keyword"

# List all notes
python note_cli.py list

# Interactive mode
python note_cli.py interactive
```

#### Examples

```bash
# Add a technical note
python note_cli.py add \
  -t "Python Decorators Learning" \
  -c "Decorators are a design pattern that can add extra functionality without modifying the original function. Use @decorator syntax." \
  --tags "Python,Programming,Learning" \
  --category "Technical Notes"

# Search for Python-related notes
python note_cli.py search "Python decorators"

# Search with result limits
python note_cli.py search "Python" -l 5 -s 0.5
```

#### Interactive Mode

```bash
python note_cli.py interactive
```

In interactive mode, you can:
- Type `add` to add new notes
- Type `search` to search notes
- Type `list` to list all notes
- Type `quit` to exit

### 3. Desktop GUI Interface

```bash
python note_gui.py
```

The GUI provides:
- **New Note** tab: Create and save new notes
- **Search Notes** tab: Search and browse notes

#### Operation Instructions

1. **Adding Notes**:
   - Fill in title, content, tags, and category in the "New Note" tab
   - Click the "Save Note" button

2. **Searching Notes**:
   - Enter keywords in the "Search Notes" tab
   - Click "Search" or press Enter
   - Double-click results to view details

3. **View All Notes**:
   - Click the "Show All" button

### 4. Python API

```python
from memu_note_client import MemuNoteClient

# Create client
client = MemuNoteClient(
    base_url="http://127.0.0.1:8000",
    user_id="note_user",
    agent_id="note_agent",
)

# Save note
client.save_note(
    title="My Note",
    content="This is the note content",
    tags=["tag1", "tag2"],
    category="Work Notes",
)

# Search notes
results = client.search_notes("keyword", top_k=10, min_similarity=0.3)

for note in results:
    print(f"Similarity: {note['similarity_score']:.2%}")
    print(f"Content: {note['content']}")
```

## Configuration

### memU Server Configuration

Default settings:
- **API URL**: `http://127.0.0.1:8000`
- **User ID**: `note_user`
- **Agent ID**: `note_agent`

You can modify these via command line arguments:

```bash
python note_cli.py --base-url http://localhost:8000 \
                   --user-id my_user \
                   --agent-id my_agent \
                   add -t "Title" -c "Content"
```

## Data Format

Notes are stored in memU in conversation format:

```json
{
  "user_id": "note_user",
  "agent_id": "note_agent",
  "conversation": [
    {
      "role": "user",
      "content": "[Note] Title\n\nContent\n\nTags: tag1, tag2\n\nTimestamp: 2025-10-04 18:00:00"
    }
  ],
  "metadata": {
    "type": "note",
    "title": "Title",
    "category": "Category",
    "tags": ["tag1", "tag2"],
    "timestamp": "2025-10-04 18:00:00"
  }
}
```

## Search Features

The note application uses memU's semantic search capabilities:

- **Semantic Understanding**: Matches not only keywords but also semantic meaning
- **Similarity Scoring**: Each result includes a similarity score
- **Adjustable Parameters**:
  - `top_k`: Number of results to return
  - `min_similarity`: Minimum similarity threshold (0.0-1.0)

## Usage Tips

1. **Tag Usage**:
   - Add relevant tags to notes for better categorization and search
   - Tags are included in search content

2. **Category Management**:
   - Use meaningful category names (e.g., "Work", "Study", "Personal")
   - Categories also participate in semantic search

3. **Search Optimization**:
   - Use specific keywords
   - Search across titles, content, and tags
   - Adjust `min_similarity` parameter to control result precision

4. **Content Organization**:
   - Keep note titles concise and clear
   - Content can include multiple paragraphs
   - Use line breaks to organize content structure

## Troubleshooting

### memU Connection Failed

Ensure memU service is running:

```bash
# Check if memU is running
lsof -i :8000

# If not running, start memU
cd /path/to/memU
python3.12 -m memu.server.cli start
```

### Search Returns Empty Results

1. Check if there are any notes:
   ```bash
   python note_cli.py list
   ```

2. Lower the similarity threshold:
   ```bash
   python note_cli.py search "keyword" -s 0.1
   ```

3. Ensure memU's embedding model is properly initialized

### GUI Cannot Start

Ensure tkinter is installed:

```bash
# macOS
brew install python-tk

# Ubuntu/Debian
sudo apt-get install python3-tk

# Windows
# tkinter is usually installed with Python
```

## Example Scenarios

### Study Notes

```bash
python note_cli.py add \
  -t "Machine Learning Basics" \
  -c "Supervised Learning: Learn from labeled data. Includes classification and regression.\nUnsupervised Learning: Discover patterns from unlabeled data. Includes clustering and dimensionality reduction." \
  --tags "machine-learning,AI,study" \
  --category "Study Notes"
```

### Work Log

```bash
python note_cli.py add \
  -t "2025-10-04 Work Log" \
  -c "Completed memU integration today, implemented note application. Next step is to add more features." \
  --tags "work,log" \
  --category "Work"
```

### Ideas

```bash
python note_cli.py add \
  -t "Product Idea" \
  -c "Could develop a personal knowledge management system based on memU, integrating notes, documents, and conversation records." \
  --tags "idea,product" \
  --category "Ideas"
```

## Related Links

- [memU Project](https://github.com/NevaMind-AI/MemU)
- [Open-LLM-VTuber Project](https://github.com/t41372/Open-LLM-VTuber)

## License

This project is licensed under the MIT License.
