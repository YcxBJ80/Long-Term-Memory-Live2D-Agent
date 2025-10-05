#!/bin/bash

# memU 笔记软件启动脚本

echo "📝 memU 笔记软件"
echo "================"
echo ""

# 检查 memU 是否运行
if ! lsof -i :8000 > /dev/null 2>&1; then
    echo "❌ memU 服务未运行"
    echo "请先启动 memU 服务："
    echo "  cd ../memU"
    echo "  python3.12 -m memu.server.cli start"
    exit 1
fi

echo "✅ memU 服务正在运行"
echo ""

# 清除代理环境变量
unset http_proxy https_proxy HTTP_PROXY HTTPS_PROXY all_proxy ALL_PROXY

# 选择模式
echo "请选择运行模式："
echo "  1) 命令行模式"
echo "  2) 图形界面模式"
echo "  3) 交互模式"
echo ""
read -p "请输入选项 (1-3): " choice

case $choice in
    1)
        echo ""
        echo "命令行模式帮助："
        python3 note_cli.py --help
        ;;
    2)
        echo ""
        echo "启动图形界面..."
        python3 note_gui.py
        ;;
    3)
        echo ""
        echo "启动交互模式..."
        python3 note_cli.py interactive
        ;;
    *)
        echo "无效选项"
        exit 1
        ;;
esac
