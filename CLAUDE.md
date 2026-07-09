# opencode-skills 项目指南

## 仓库结构

```
opencode-skills/
├── skills/                 # 所有 skill，每个独立目录
│   ├── opencode-<name>/    # 命名规范: opencode- 前缀
│   │   ├── SKILL.md        # 【必需】核心指令文件
│   │   ├── scripts/        # 【可选】辅助脚本
│   │   ├── references/     # 【可选】参考文档
│   │   ├── prompts/        # 【可选】提示词模板
│   │   ├── assets/         # 【可选】静态资源
│   │   └── templates/      # 【可选】模板文件
│   └── ...
├── docs/                   # 作者端参考文档（SKILL.md 不得引用）
│   └── creating-skills.md  # 新增 skill 的权威指南
├── scripts/                # 仓库级维护脚本
├── .claude-plugin/         # Claude Code 插件注册
│   └── marketplace.json
├── CLAUDE.md               # 本文件
└── package.json            # 根 workspace
```

## Skill 命名规范

- 所有 skill 目录必须以 `opencode-` 前缀开头
- 目录名使用小写字母和连字符（kebab-case）
- 每个 skill 至少包含 `SKILL.md`

## SKILL.md 规范

### Frontmatter

```yaml
---
name: opencode-<name>
description: >-
  功能描述 + 触发条件
version: <semver>
metadata:
  author: Fisher Yu
---
```

### 内容要求

- SKILL.md 及其 `references/` 不得引用 skill 目录之外的任何文件
- `docs/` 目录是作者端参考，只能从本 CLAUDE.md 引用
- 保持自包含，引用内联而非链接外部

## 新增 Skill 流程

1. 在 `skills/` 下创建 `opencode-<name>/` 目录
2. 编写 `SKILL.md`（参考现有 skill 格式）
3. 添加 `LICENSE.txt`（MIT）
4. 可选：添加 `references/`、`scripts/`、`assets/`
5. 在 `.claude-plugin/marketplace.json` 中注册路径
