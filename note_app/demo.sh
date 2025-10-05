#!/bin/bash

# memU 笔记软件演示脚本

echo "🎬 memU 笔记软件演示"
echo "===================="
echo ""

# 清除代理
unset http_proxy https_proxy HTTP_PROXY HTTPS_PROXY all_proxy ALL_PROXY

# 检查 memU
if ! lsof -i :8000 > /dev/null 2>&1; then
    echo "❌ 请先启动 memU 服务"
    exit 1
fi

echo "✅ memU 服务已就绪"
echo ""

# 演示 1: 添加笔记
echo "📝 演示 1: 添加笔记"
echo "-------------------"
echo ""

python3 note_cli.py add \
  -t "Python 装饰器学习" \
  -c "装饰器是 Python 中的一种设计模式，用于在不修改原函数代码的情况下增加额外功能。使用 @decorator 语法。常见用途包括日志记录、性能测试、事务处理等。" \
  --tags "Python,编程,学习" \
  --category "技术笔记"

echo ""
sleep 2

python3 note_cli.py add \
  -t "机器学习基础" \
  -c "监督学习：从标注数据中学习，包括分类和回归。无监督学习：从未标注数据中发现模式，包括聚类和降维。强化学习：通过与环境交互学习最优策略。" \
  --tags "机器学习,AI,学习" \
  --category "技术笔记"

echo ""
sleep 2

python3 note_cli.py add \
  -t "今日工作总结" \
  -c "完成了 memU 笔记软件的开发，实现了命令行和图形界面两个版本。测试了与 memU 的集成，功能正常。明天计划添加更多功能。" \
  --tags "工作,日志" \
  --category "工作日志"

echo ""
echo "✅ 已添加 3 条笔记"
echo ""
sleep 2

# 演示 2: 列出笔记
echo "📚 演示 2: 列出所有笔记"
echo "----------------------"
echo ""

python3 note_cli.py list

echo ""
sleep 3

# 演示 3: 搜索笔记
echo "🔍 演示 3: 搜索笔记"
echo "------------------"
echo ""
echo "搜索关键词: Python"
echo ""

python3 note_cli.py search "Python" -l 5 -s 0.3

echo ""
echo "✅ 演示完成！"
echo ""
echo "💡 提示："
echo "  - 使用 './start_note_app.sh' 启动应用"
echo "  - 查看 'QUICKSTART.md' 了解更多用法"
echo "  - 查看 'README.md' 了解完整文档"
