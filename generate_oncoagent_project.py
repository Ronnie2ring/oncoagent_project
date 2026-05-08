#!/usr/bin/env python3
"""
自动生成 OncoAgent 项目所有文件
运行: python generate_oncoagent_project.py
"""

import os


def write_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"✓ 已生成: {path}")


def main():
    base_dir = "oncoagent_project"

    # ==================== 根目录文件 ====================
    write_file(os.path.join(base_dir, "README.md"), '''# OncoAgent

多Agent协作与长链推理的肿瘤精准决策系统（MVP实现）。

## 安装

```bash
pip install -r requirements.txt