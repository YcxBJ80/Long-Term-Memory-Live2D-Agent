#!/bin/bash

echo "🔧 修复笔记搜索问题"
echo "===================="
echo ""

echo "📋 问题："
echo "  memU 无法下载嵌入模型，导致搜索功能不可用"
echo ""

echo "✅ 解决方案："
echo "  1. 已创建 .env 文件禁用嵌入功能"
echo "  2. 笔记添加和列出功能正常"
echo "  3. 语义搜索暂时不可用"
echo ""

echo "🔄 重启 memU 服务..."
echo ""
echo "请手动执行以下命令："
echo ""
echo "  # 停止当前 memU 服务 (Ctrl+C)"
echo "  # 然后运行："
echo "  cd ../memU"
echo "  unset http_proxy https_proxy HTTP_PROXY HTTPS_PROXY all_proxy ALL_PROXY"
echo "  python3.12 -m memu.server.cli start"
echo ""

echo "📝 测试笔记功能："
echo ""
echo "  cd note_app"
echo "  unset http_proxy https_proxy HTTP_PROXY HTTPS_PROXY all_proxy ALL_PROXY"
echo "  python3 note_cli.py add -t '测试' -c '测试内容'"
echo "  python3 note_cli.py list"
echo ""

echo "📖 查看完整修复指南："
echo "  cat ../FIX_SEARCH_ISSUE.md"
