# Live2Document

一个综合性的AI驱动笔记和对话系统，集成了memU记忆数据库和Open-LLM-VTuber，实现智能的记忆增强交互。

## 概述

本项目结合了三个强大的组件：
- **memU**：用于存储和检索上下文信息的高级记忆数据库系统
- **Open-LLM-VTuber**：由大型语言模型驱动的虚拟YouTuber系统
- **笔记应用**：具有Web、CLI和GUI界面的多接口笔记系统

## 功能特性

### 核心功能
- 智能笔记存储与语义搜索
- 记忆增强的AI对话
- 多模态界面（Web、CLI、GUI）
- 实时记忆检索和上下文增强
- 自动标签和分类
- 跨平台兼容性

### 技术特性
- RESTful API集成
- 基于嵌入的相似度搜索
- 缓存和性能优化
- 异步处理
- 全面的日志记录和监控

## 架构

```
Live2Document_4/
├── memU/                    # 记忆数据库系统
├── Open-LLM-VTuber/        # 虚拟YouTuber AI系统
├── note_app/               # 笔记应用程序
│   ├── web/               # Web界面
│   ├── note_cli.py        # 命令行界面
│   ├── note_gui.py        # 桌面GUI界面
│   └── memu_note_client.py # memU集成客户端
└── logs/                   # 系统日志
```

## 快速开始

### 前置要求
- Python 3.10+（memU推荐Python 3.12+）
- 带有兼容语言模型的LMStudio
- Git用于克隆子模块

### 安装

1. 克隆包含子模块的仓库：
```bash
git clone --recursive https://github.com/your-username/Live2Document_4.git
cd Live2Document_4
```

2. 安装依赖：
```bash
./install_deps.sh
```

3. 启动所有服务：
```bash
./start_services.sh
```

### 使用方法

#### Web界面
访问笔记Web界面：`http://localhost:8080`

#### 命令行
```bash
cd note_app
python note_cli.py add -t "标题" -c "内容" --tags "标签1,标签2"
python note_cli.py search "关键词"
python note_cli.py list
```

#### 桌面GUI
```bash
cd note_app
python note_gui.py
```

#### VTuber界面
访问AI对话界面：`http://localhost:12393`

## 配置

### memU配置
编辑`memU/.env`来配置：
- 服务器设置
- 嵌入模型
- LLM集成
- 存储路径

### Open-LLM-VTuber配置
编辑`Open-LLM-VTuber/conf.yaml`来配置：
- memU集成设置
- LLM提供商设置
- 语音和头像设置

## API文档

### memU API
- `POST /api/v1/memory/memorize` - 存储新记忆
- `POST /api/v1/memory/retrieve/related-memory-items` - 检索相关记忆

### 笔记应用API
- `GET /api/notes` - 列出所有笔记
- `POST /api/notes` - 创建新笔记
- `GET /api/notes/search` - 搜索笔记

## 开发

### 项目结构
- `memU/` - 记忆数据库系统（子模块）
- `Open-LLM-VTuber/` - VTuber系统（子模块）
- `note_app/` - 笔记应用程序
- `logs/` - 应用程序日志
- `MARKDOWNS/` - 文档和指南

### 贡献
1. Fork仓库
2. 创建功能分支
3. 进行更改
4. 如适用，添加测试
5. 提交拉取请求

## 故障排除

### 常见问题
1. **端口冲突**：确保端口8000、8080和12393可用
2. **Python版本**：memU使用Python 3.12+，其他组件使用Python 3.10+
3. **依赖项**：运行`./install_deps.sh`安装所有必需的包
4. **LMStudio**：确保LMStudio正在运行并加载了模型

### 日志
检查以下日志文件进行调试：
- `logs/memu.log` - memU服务日志
- `logs/note_web.log` - Web界面日志
- `logs/vtuber.log` - VTuber系统日志

## 性能优化

系统包含多项性能优化：
- 嵌入缓存和预加载
- NumPy加速的向量运算
- 查询结果的LRU缓存
- 异步非阻塞查询
- 智能超时处理

## 许可证

本项目集成了具有不同许可证的多个组件：
- memU：查看memU仓库了解许可证详情
- Open-LLM-VTuber：查看Open-LLM-VTuber仓库了解许可证详情
- 笔记应用：MIT许可证

## 致谢

- [memU](https://github.com/NevaMind-AI/MemU) - 高级记忆数据库系统
- [Open-LLM-VTuber](https://github.com/t41372/Open-LLM-VTuber) - 虚拟YouTuber AI系统
- LMStudio - 本地语言模型托管