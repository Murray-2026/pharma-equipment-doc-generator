#!/bin/bash

# ============================================================
# 制药设备售前文档生成器 - 一键部署脚本
# ============================================================

echo "============================================================"
echo "🏭 制药设备售前文档生成器 - 部署工具"
echo "============================================================"
echo ""

# 检查Python环境
if ! command -v python3 &> /dev/null; then
    echo "❌ 错误: Python3未安装"
    exit 1
fi

echo "✅ Python3已安装"
echo ""

# 检查Git
if ! command -v git &> /dev/null; then
    echo "❌ 错误: Git未安装"
    exit 1
fi

echo "✅ Git已安装"
echo ""

# 检查PyGithub
if ! python3 -c "import github" &> /dev/null; then
    echo "📦 正在安装PyGithub..."
    pip install PyGithub==2.1.1 -q
    echo "✅ PyGithub安装完成"
else
    echo "✅ PyGithub已安装"
fi

echo ""

# 运行部署脚本
echo "🚀 开始部署..."
echo ""

python3 deploy_to_github.py

echo ""
echo "============================================================"
echo "📝 后续步骤"
echo "============================================================"
echo ""
echo "1. 如果部署成功，GitHub仓库已创建"
echo "2. 访问 https://share.streamlit.io 进行Streamlit Cloud部署"
echo "3. 详细说明请查看 DEPLOYMENT_GUIDE.md"
echo ""
echo "============================================================"
