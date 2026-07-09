# 创建新 Skill

本指南说明如何向 opencode-skills 仓库添加新 skill。

## 仓库结构

每个 skill 是一个独立目录，位于 `skills/<name>/` 下。

```
skills/<name>/
├── SKILL.md        # 【必需】核心指令文件（YAML frontmatter + Markdown 正文）
├── LICENSE.txt     # 【推荐】MIT 许可
├── scripts/        # 【可选】辅助脚本
├── references/     # 【可选】参考文档
├── prompts/        # 【可选】提示词模板
├── assets/         # 【可选】静态资源
└── templates/      # 【可选】模板文件
```

## SKILL.md 文件格式

### Frontmatter

```yaml
---
name: <name>
description: >-
  功能描述（最长 1024 字符）
  包含：核心功能 + 触发条件
version: <semver>
metadata:
  author: Fisher Yu
---
```

### 正文结构

- 使用 `##` 级别的标题组织内容
- 包含触发条件、工作流程、验证标准
- 使用 `## When to use` 或 `## 适用场景` 描述触发条件
- 使用 `## Workflow` 或 `## 流程` 描述执行步骤
- 使用 `## Validation` 或 `## 验证` 描述完成标准

### 自包含原则

- SKILL.md 及其 `references/` 不得引用 skill 目录之外的任何文件
- 共享约定必须**内联**在 SKILL.md 中，而非链接外部文档
- `docs/` 目录是作者端参考，SKILL.md 不得引用

## 注册

1. 在 `.claude-plugin/marketplace.json` 中注册新 skill 路径
2. 提交到 GitHub

## 安装

```bash
skill install https://github.com/yuff100/opencode-skills/tree/main/skills/<name>
```
