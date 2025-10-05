#!/bin/bash

# 临时禁用代理安装依赖

echo "🔧 安装缺失的依赖包..."
echo ""

# 保存当前代理设置
OLD_HTTP_PROXY=$http_proxy
OLD_HTTPS_PROXY=$https_proxy
OLD_ALL_PROXY=$all_proxy

# 临时禁用代理
unset http_proxy
unset https_proxy
unset HTTP_PROXY
unset HTTPS_PROXY
unset all_proxy
unset ALL_PROXY

echo "✅ 已临时禁用代理"
echo ""

# 安装依赖
echo "📦 安装 httpx[socks] 和 socksio..."
cd /Users/yangchengxuan/Desktop/PROJECTS/Live2Document_4/Open-LLM-VTuber
python3.12 -m pip install 'httpx[socks]' socksio --user

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ 依赖安装成功！"
else
    echo ""
    echo "❌ 依赖安装失败"
    exit 1
fi

# 恢复代理设置
export http_proxy=$OLD_HTTP_PROXY
export https_proxy=$OLD_HTTPS_PROXY
export all_proxy=$OLD_ALL_PROXY

echo ""
echo "✅ 已恢复代理设置"
echo ""
echo "🎉 完成！现在可以重新启动服务了"
echo ""
echo "运行: ./start_vtuber_fixed.sh"
