# GitHub Token权限问题说明

## 问题分析

您提供的GitHub Personal Access Token (PAT) 缺少创建仓库所需的权限。

### 当前状态
- **用户名**: Murray-2026
- **Token权限范围**: 无
- **可访问仓库数**: 2个
- **所属组织**: 0个

### 错误信息
```
403: Resource not accessible by personal access token
```

## 解决方案

### 方案1: 重新生成带有正确权限的Token（推荐）

#### 步骤1: 删除旧Token并创建新Token

1. 访问 GitHub Settings -> Developer settings -> Personal access tokens
2. 点击 "Generate new token (classic)"
3. 填写Token描述，例如: "pharma-equipment-doc-generator"
4. 在权限设置中，勾选以下权限:
   - ✅ **repo** (Full control of private repositories)
     - 勾选此选项将自动包含:
       - repo:status
       - repo:deployment
       - public_repo
       - repo:invite
       - security_events

5. 点击 "Generate token"
6. 复制新生成的Token

#### 步骤2: 使用新Token

创建并运行以下脚本:

```python
from github import Github
import os
import subprocess

# 使用新Token
GITHUB_TOKEN = "ghp_xxxxxxxxxxxx"  # 替换为新Token
REPO_NAME = "pharma-equipment-doc-generator"
LOCAL_REPO_PATH = "/workspace"

def create_and_push():
    g = Github(GITHUB_TOKEN)
    user = g.get_user()
    
    # 创建仓库
    repo = user.create_repo(
        REPO_NAME,
        description="制药设备售前文档生成器",
        private=False
    )
    
    # 配置Git并推送
    os.chdir(LOCAL_REPO_PATH)
    os.system("git init")
    os.system(f"git remote add origin {repo.clone_url}")
    os.system("git add .")
    os.system("git commit -m 'Initial commit'")
    os.system("git branch -M main")
    os.system("git push -u origin main")
    
    print(f"仓库创建成功: {repo.html_url}")

if __name__ == "__main__":
    create_and_push()
```

### 方案2: 手动创建仓库并推送

如果无法获取新Token，可以手动创建仓库:

1. 访问 https://github.com/new
2. 仓库名称输入: `pharma-equipment-doc-generator`
3. 选择 Public
4. 点击 "Create repository"
5. 然后手动推送代码:

```bash
cd /workspace
git init
git remote add origin https://github.com/Murray-2026/pharma-equipment-doc-generator.git
git add .
git commit -m "Initial commit: Pharma Equipment Document Generator"
git branch -M main
git push -u origin main
```

## 验证Token权限

运行以下命令验证Token权限:

```bash
curl -H "Authorization: token YOUR_TOKEN" https://api.github.com/user
```

在响应头中查找 `X-OAuth-Scopes` 字段，应该包含 `repo`。

## 当前已创建的代码文件

所有必要的代码文件已经准备就绪:

✅ app.py - Streamlit主应用
✅ requirements.txt - 依赖列表
✅ README.md - 项目说明
✅ .streamlit/config.toml - Streamlit配置
✅ utils/ - 工具模块
  - config_loader.py
  - template_manager.py
  - document_generator.py
  - __init__.py
✅ templates/ - 模板目录
  - template_info.json

## 下一步

1. 获取具有`repo`权限的新GitHub Token
2. 运行deploy.py脚本创建仓库并推送代码
3. 访问Streamlit Cloud进行部署

## 获取帮助

如果遇到问题，请检查:
- Token是否过期
- Token是否具有repo权限
- Token是否正确配置
