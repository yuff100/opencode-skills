# opencode-skills

OpenCode 自定义 skills 仓库。每个 skill 是一个独立的指令文件（SKILL.md），可通过 `skill install` 直接安装。

## 安装

```bash
skill install https://github.com/yuff100/opencode-skills/tree/main/skills/<name>
```

安装完成后重启 OpenCode。skills 默认安装到 `~/.agents/skills/`。

## Skills

| Skill | 描述 |
|-------|------|
| `anti-sycophancy` | 批判性思维伙伴。默认 constructive disagreement，帮你识别思维盲区 |
| `distill-docs` | `/distill-docs` — 归档规划文档，提取业务规则沉淀到项目文档 |
| `rewrite` | Rewrite web content for WeChat Official Accounts publication |
| `team` | `/team [N]` — 创建多 Agent 协作团队，并行执行子任务 |
| `translate` | 三模式翻译（quick/normal/refined），术语管理，长文自动分块 |
| `wechat-article-writer` | 公众号文章 5 步自动化写作：搜索 → 撰写 → 标题 → 排版 → 检查 |

### 详细说明

#### `wechat-article-writer`

公众号文章自动化写作，5 步闭环流程：

1. **搜索资料** — 并行搜索官方数据、行业报告、权威媒体，提取关键数据和案例
2. **撰写文章** — 1000-1500 字，故事化开头，中国语境案例
3. **生成标题** — 5 个爆款标题候选
4. **排版优化** — 段落控制、配图位置、金句突出
5. **质量检查** — 每条数据标注出处、外链带描述嵌入

#### `distill-docs`

规划文档归档 skill，从临时文档中提炼业务知识沉淀到项目文档：

1. **读取与分析** — 并行读取待归档文件，检查断链
2. **分类提取** — 判断保留/丢弃
3. **对齐确认** — 报告计划，等待用户确认
4. **执行变更** — 写入目标文档，删除原文件
5. **验证** — 用核心原则自检

#### `team`

多 Agent 协作团队创建器，通过 `/team [N] [任务描述]` 调用：

- 创建 N 个 teammate（1-10，默认 5）
- 把复杂任务拆分为独立子任务并行执行

#### `translate`

三模式翻译，支持长文自动分块和术语管理。

- 模式：quick（直接翻译）、normal（分析+翻译）、refined（批判审阅+润色）
- 长文超过阈值自动分块
- 支持 EXTEND.md 用户偏好配置
- 稳定输出目录，同名目录自动备份

#### `rewrite`

将网页内容改写为微信公众号风格，自动插入配图，生成标题候选。

#### `anti-sycophancy`

批判性思维伙伴。默认 constructive disagreement，在同意之前先找假设，先反驳再认同。

## 仓库结构

```
opencode-skills/
├── skills/                   # 所有 skill，每个独立目录
│   ├── <name>/               # 命名规范: 小写 kebab-case
│   │   ├── SKILL.md          # 核心指令文件
│   │   ├── scripts/          # 辅助脚本
│   │   ├── references/       # 参考文档
│   │   └── ...
│   └── ...
├── docs/                     # 作者端参考文档
│   └── creating-skills.md    # 新增 skill 指南
├── .claude-plugin/           # 插件注册
│   └── marketplace.json
├── CLAUDE.md                 # 项目级 AI 指南
└── package.json              # 根 workspace
```

## 新增 Skill

参见 [docs/creating-skills.md](docs/creating-skills.md)。

## License

MIT
