# Live2Document

A comprehensive AI-powered note-taking and conversation system that integrates memU memory database with Open-LLM-VTuber for intelligent, memory-enhanced interactions.

## Overview

This project combines three powerful components:
- **memU**: An advanced memory database system for storing and retrieving contextual information
- **Open-LLM-VTuber**: A virtual YouTuber system powered by large language models
- **Note Application**: A multi-interface note-taking system with web, CLI, and GUI interfaces

## Features

### Core Capabilities
- Intelligent note storage with semantic search
- Memory-enhanced AI conversations
- Multi-modal interfaces (Web, CLI, GUI)
- Real-time memory retrieval and context augmentation
- Automatic tagging and categorization
- Cross-platform compatibility

### Technical Features
- RESTful API integration
- Embedding-based similarity search
- Caching and performance optimization
- Asynchronous processing
- Comprehensive logging and monitoring

## Architecture

```
Live2Document_4/
├── memU/                    # Memory database system
├── Open-LLM-VTuber/        # Virtual YouTuber AI system
├── note_app/               # Note-taking applications
│   ├── web/               # Web interface
│   ├── note_cli.py        # Command-line interface
│   ├── note_gui.py        # Desktop GUI interface
│   └── memu_note_client.py # memU integration client
└── logs/                   # System logs
```

## Quick Start

### Prerequisites
- Python 3.10+ (Python 3.12+ recommended for memU)
- LMStudio with a compatible language model
- Git for cloning submodules

### Installation

1. Clone the repository with submodules:
```bash
git clone --recursive https://github.com/your-username/Live2Document_4.git
cd Live2Document_4
```

2. Install dependencies:
```bash
./install_deps.sh
```

3. Start all services:
```bash
./start_services.sh
```

### Usage

#### Web Interface
Access the note-taking web interface at `http://localhost:8080`

#### Command Line
```bash
cd note_app
python note_cli.py add -t "Title" -c "Content" --tags "tag1,tag2"
python note_cli.py search "keyword"
python note_cli.py list
```

#### Desktop GUI
```bash
cd note_app
python note_gui.py
```

#### VTuber Interface
Access the AI conversation interface at `http://localhost:12393`

## Configuration

### memU Configuration
Edit `memU/.env` to configure:
- Server settings
- Embedding models
- LLM integration
- Storage paths

### Open-LLM-VTuber Configuration
Edit `Open-LLM-VTuber/conf.yaml` to configure:
- memU integration settings
- LLM provider settings
- Voice and avatar settings

## API Documentation

### memU API
- `POST /api/v1/memory/memorize` - Store new memories
- `POST /api/v1/memory/retrieve/related-memory-items` - Retrieve related memories

### Note Application API
- `GET /api/notes` - List all notes
- `POST /api/notes` - Create new note
- `GET /api/notes/search` - Search notes

## Development

### Project Structure
- `memU/` - Memory database system (submodule)
- `Open-LLM-VTuber/` - VTuber system (submodule)
- `note_app/` - Note applications
- `logs/` - Application logs
- `MARKDOWNS/` - Documentation and guides

### Contributing
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## Troubleshooting

### Common Issues
1. **Port conflicts**: Ensure ports 8000, 8080, and 12393 are available
2. **Python version**: Use Python 3.12+ for memU, 3.10+ for other components
3. **Dependencies**: Run `./install_deps.sh` to install all required packages
4. **LMStudio**: Ensure LMStudio is running with a loaded model

### Logs
Check the following log files for debugging:
- `logs/memu.log` - memU service logs
- `logs/note_web.log` - Web interface logs
- `logs/vtuber.log` - VTuber system logs

## Performance Optimization

The system includes several performance optimizations:
- Embedding caching and preloading
- NumPy-accelerated vector operations
- LRU caching for query results
- Asynchronous non-blocking queries
- Intelligent timeout handling

## License

This project integrates multiple components with different licenses:
- memU: Check memU repository for license details
- Open-LLM-VTuber: Check Open-LLM-VTuber repository for license details
- Note Application: MIT License

## Acknowledgments

- [memU](https://github.com/NevaMind-AI/MemU) - Advanced memory database system
- [Open-LLM-VTuber](https://github.com/t41372/Open-LLM-VTuber) - Virtual YouTuber AI system
- LMStudio - Local language model hosting

---

**中文文档**: [README.CN.md](README.CN.md)