# 🏭 制药设备售前文档生成器 - GitHub部署指南

## 📋 项目概述

这是一个基于Streamlit的制药设备售前文档自动生成工具，帮助销售人员快速生成专业的技术文档、产品介绍和招标参数。

## ✅ 已完成的工作

### 1. 项目文件结构创建

所有必要的代码文件已经创建完成:

```
/workspace/
├── app.py                          # Streamlit主应用
├── requirements.txt                # Python依赖列表
├── README.md                       # 项目说明文档
├── deploy_to_github.py             # GitHub部署脚本
├── TOKEN_PERMISSION_GUIDE.md        # Token权限配置指南
├── .streamlit/
│   └── config.toml                 # Streamlit配置
├── utils/
│   ├── __init__.py                 # 包初始化
│   ├── config_loader.py            # 配置加载器
│   ├── template_manager.py          # 模板管理器
│   └── document_generator.py       # 文档生成器
└── templates/
    └── template_info.json          # 模板配置
```

### 2. 功能特性

- ✅ 支持多种制药设备类型（粉碎机、混合机、制粒机、压片机、包装机）
- ✅ 支持多种文档类型（技术方案书、产品介绍、招标参数、报价单）
- ✅ 自动生成专业的Word文档
- ✅ 符合行业标准的技术参数模板
- ✅ 支持GMP、CE、FDA等认证要求

## ⚠️ 当前问题

### GitHub Token权限不足

**错误信息:**
```
403: Resource not accessible by personal access token
```

**问题原因:**
- 您提供的GitHub Personal Access Token缺少创建仓库所需的 `repo` 权限
- 当前Token权限范围显示为"无"

## 🔧 解决方案

### 方案1: 重新生成具有正确权限的GitHub Token（推荐）

#### 步骤1: 生成新的GitHub Token

1. 访问 GitHub Settings: https://github.com/settings/tokens
2. 点击 "Generate new token (classic)"
3. 填写Token描述: `pharma-equipment-doc-generator`
4. 在权限设置中，**必须勾选** `repo` 权限:
   - ✅ 勾选 `repo` (Full control of private repositories)
5. 点击 "Generate token"
6. **重要**: 立即复制并保存新Token（Token只显示一次）

#### 步骤2: 更新部署脚本

编辑 `/workspace/deploy_to_github.py` 文件，将第15行的Token替换为新生成的:

```python
# 第15行
GITHUB_TOKEN = "ghp_xxxxxxxxxxxxxxxxxxxx"  # 替换为您的新Token
```

#### 步骤3: 运行部署脚本

```bash
cd /workspace
python deploy_to_github.py
```

脚本将自动:
- ✅ 创建GitHub仓库
- ✅ 初始化Git仓库
- ✅ 推送所有代码文件
- ✅ 显示部署摘要

### 方案2: 手动创建仓库并推送

如果您无法获取新Token，可以手动操作:

#### 步骤1: 手动创建GitHub仓库

1. 访问 https://github.com/new
2. 仓库名称: `pharma-equipment-doc-generator`
3. 选择: Public
4. 勾选: Add a README file（可选）
5. 点击 "Create repository"

#### 步骤2: 推送代码

在终端中运行:

```bash
cd /workspace

# 初始化Git仓库
git init

# 配置用户信息
git config user.email "noreply@github.com"
git config user.name "Your Name"

# 添加远程仓库（替换YOUR_USERNAME为您的GitHub用户名）
git remote add origin https://github.com/Murray-2026/pharma-equipment-doc-generator.git

# 添加所有文件
git add .

# 提交
git commit -m "Initial commit: Pharma Equipment Document Generator

- Streamlit-based web application
- Support for multiple pharmaceutical equipment types
- Multiple document type generation
- Professional Word document output"

# 推送
git branch -M main
git push -u origin main
```

## 🚀 Streamlit Cloud部署步骤

无论您使用哪种方案创建GitHub仓库，之后都需要在Streamlit Cloud上部署应用:

### 步骤1: 访问Streamlit Cloud

访问: https://share.streamlit.io

### 步骤2: 登录

使用您的GitHub账号登录Streamlit Cloud

### 步骤3: 创建新应用

点击 "New app" 按钮

### 步骤4: 配置应用

在配置页面填写:
- **Repository**: `Murray-2026/pharma-equipment-doc-generator`
- **Branch**: `main`
- **Main file path**: `app.py`
- **App URL**: (可选) 自定义应用URL，例如 `pharma-equipment-generator`

### 步骤5: 部署

点击 "Deploy!" 按钮

### 步骤6: 等待部署完成

Streamlit Cloud将自动:
- 克隆GitHub仓库
- 安装依赖（从requirements.txt）
- 启动应用

部署完成后，您将获得一个类似以下的URL:
```
https://share.streamlit.io/YOUR_USERNAME/pharma-equipment-doc-generator
```

## 📱 部署后的应用访问

部署成功后，您可以通过以下方式访问应用:

### 访问URL格式
```
https://share.streamlit.io/[用户名]/pharma-equipment-doc-generator
```

### 实际示例
假设您成功部署，应用URL将是:
```
https://share.streamlit.io/Murray-2026/pharma-equipment-doc-generator
```

## 🔍 验证部署

### 检查1: GitHub仓库

访问您创建的GitHub仓库，确认以下文件存在:
- ✅ app.py
- ✅ requirements.txt
- ✅ README.md
- ✅ .streamlit/config.toml
- ✅ utils/ 目录
- ✅ templates/ 目录

### 检查2: Streamlit应用

1. 访问您部署的Streamlit应用URL
2. 确认页面正常加载
3. 测试基本功能:
   - 选择设备类型
   - 填写项目信息
   - 点击"生成文档"
   - 确认可以下载Word文档

## 🐛 常见问题

### Q1: Token创建失败

**问题**: 无法创建GitHub Token
**解决方案**: 
- 确保您已验证邮箱
- 检查是否达到了Token数量限制
- 尝试删除旧的未使用的Token

### Q2: 推送失败

**问题**: Git推送被拒绝
**解决方案**:
- 检查Token是否有效
- 确保Token具有repo权限
- 尝试使用HTTPS而非SSH

### Q3: Streamlit Cloud部署失败

**问题**: 部署到Streamlit Cloud时报错
**解决方案**:
- 检查requirements.txt中的依赖是否正确
- 确保Python版本兼容（推荐Python 3.8-3.11）
- 查看部署日志，定位具体错误

### Q4: 应用无法访问

**问题**: 部署成功但无法访问
**解决方案**:
- 等待2-3分钟让应用完全启动
- 检查应用状态（Running/Stopped）
- 尝试刷新浏览器缓存

## 📞 技术支持

如果遇到其他问题，请提供:
1. 完整的错误信息
2. 您尝试的操作步骤
3. 相关的截图或日志

## 🎯 预期结果

完成所有步骤后，您将拥有:

1. ✅ GitHub仓库: `https://github.com/Murray-2026/pharma-equipment-doc-generator`
2. ✅ 已部署的Streamlit应用: `https://share.streamlit.io/Murray-2026/pharma-equipment-doc-generator`
3. ✅ 所有源代码和文档文件

## 📝 下一步

1. ✅ 按照本指南获取新的GitHub Token（如果尚未获取）
2. ✅ 运行 `python deploy_to_github.py` 创建GitHub仓库并推送代码
3. ✅ 访问Streamlit Cloud完成应用部署
4. ✅ 测试应用功能
5. ✅ 开始使用文档生成器!

---

**祝您部署顺利！🚀**
