# opencode-skills

这是一个面向 OpenCode 的自定义 skills 仓库，提供可直接安装和使用的实用 skills。本文档面向想要使用这套 skills 的读者，重点说明如何安装、更新、调用，以及当前已包含 skill 的核心能力和处理流程。

## 快速开始

OpenCode 支持安装单个 skill：

```
skill install https://github.com/<your-username>/opencode-skills/tree/main/skills/.curated/translate
```

安装完成后，重启 OpenCode。

默认情况下，skills 会被安装到：

```bash
~/.agents/skills/
```

## 安装说明

这个仓库把可安装 skill 放在 `skills/.curated/<skill-name>/` 下。这是官方 skills 仓库常见的组织方式，安装器会把它识别为单个 skill。

如果你只想安装某个单个 skill，直接指向具体目录安装。例如安装 `translate`：

```
skill install https://github.com/<your-username>/opencode-skills/tree/main/skills/.curated/translate
```

## 更新说明

需要同步 GitHub 仓库中的新版本时，直接再次运行同一条安装命令即可。

如果你只安装了某个单独的 skill，继续使用对应目录 URL 重新安装，例如：

```
skill install https://github.com/<your-username>/opencode-skills/tree/main/skills/.curated/translate
```

如果你的本地 OpenCode 提示同名 skill 已存在，按提示处理后重新执行对应命令。

## 如何使用

安装并重启 OpenCode 后，可以直接在提示词中显式调用：

```
$translate 把这篇 Markdown 文章翻译成中文
```

也可以自然语言触发，OpenCode 通常可以根据任务内容自动选用合适的 skill。

例如：

- 翻译这篇 README，保留链接和代码块
- 把这篇英文博客精翻成中文
- 把这个 URL 的文章翻译成自然中文

## 当前已包含的 skill

### `wechat-article-writer`

`wechat-article-writer` 是一个面向公众号文章写作的自动化 skill，适合以下场景：

- 写公众号长文、自媒体文章、爆款内容
- 需要搜索资料 + 撰写 + 排版的一站式流程
- 需要质量检查（引用出处、配图、标题优化）

它的核心能力是 5 步闭环写作流程：

1. **搜索资料** — 并行搜索官方数据、行业报告、权威媒体，提取关键数据和案例
2. **撰写文章** — 1000-1500 字，故事化开头，中国语境案例，效果展示 → 问题 → 教学 → 升华结构
3. **生成标题** — 5 个爆款标题候选，覆盖痛点、数字、悬念、情绪等类型
4. **排版优化** — 段落控制、配图位置、金句突出、互动引导
5. **质量检查** — 每条数据标注出处、外链带描述嵌入、Unsplash 配图选图与追踪

### `distill-docs`

`distill-docs` 是一个规划文档归档 skill，适合以下场景：

- 清理执行计划、分析报告、方案评审等临时文档
- 从临时文档中提炼值得长期保留的业务知识
- 确保项目文档只沉淀"代码无法推导的信息"

它的核心流程：

1. **读取与分析** — 并行读取待归档文件，了解已有文档覆盖范围，检查断链
2. **分类提取** — 逐段判断：设计约束/跨文件全貌/生产配置 → 沉淀；调用链/论证过程/git 可查信息 → 丢弃
3. **对齐确认** — 报告沉淀/丢弃计划，等待用户确认后执行
4. **执行变更** — 写入目标文档，删除原文件，修复断链
5. **验证** — 用核心原则自检，确保只保留了不可从代码推导的信息

### `team`

`team` 是一个多 Agent 协作团队创建器，通过 `/team [N] [任务描述]` 调用：

- 创建 N 个 teammate（1-10，默认 5）与你组成协作团队
- 把复杂任务拆分为独立子任务并行执行
- 你作为 lead 统筹，teammate 各自负责子任务

适合需要并行开发、多视角分析或任务可明确拆分的场景。

### `translate`

`translate` 是一个面向长文本和 Markdown 内容的翻译与本地化 skill，适合以下场景：

- 翻译文章、博客、README、普通文档
- 本地化 Markdown 内容，并保留标题层级、链接和代码块
- 处理长文，尤其是需要术语统一和稳定输出目录的情况
- 根据要求输出快翻、常规翻译或精翻版本

它的核心能力主要集中在四个方面。

第一是偏好与术语管理。skill 会优先查找 `EXTEND.md`，读取目标语言、模式、受众、文风、分块阈值以及用户自定义术语表，并将这些配置与内置 glossary、外部 glossary 文件合并，尽量保持术语统一。

第二是长文分块处理。对于达到阈值的 Markdown 内容，skill 会先整理术语，再调用 `scripts/main.ts` 做自动分块，把内容拆成多个 chunk，减少长文翻译时的上下文漂移。它优先使用 `bun`，如果系统没有 `bun` 但有 `npx`，则退回到 `npx -y bun`。

第三是多模式翻译。它支持 `quick`、`normal`、`refined` 三种模式，分别对应直接翻译、带分析的翻译，以及带批判审阅和润色的精翻流程。

第四是稳定输出。skill 会把所有中间文件和最终结果写入固定命名的输出目录，避免覆盖旧结果，并在结束后补做一次轻量的图片语言检查。

## `translate` 的处理步骤

`translate` 的工作流比较稳定，整体顺序如下：

1. 读取偏好配置和 glossary。
2. 判断输入来源是文件、URL 还是内联文本。
3. 将 URL 或内联文本物化为本地 Markdown 文件。
4. 在源文件旁边创建输出目录，目录名格式为 `{source-basename}-{target-lang}`。
5. 根据用户要求或默认配置选择 `quick`、`normal`、`refined` 模式。
6. 判断内容长度。短文直接处理，长文先抽取术语再分块。
7. 对每个 chunk 依次翻译，并按顺序合并。
8. 输出中间文件和最终 `translation.md`。
9. 复查 Markdown 结构、术语一致性、链接和代码块，并提示可能仍含源语言文字的图片。

不同输入类型会按固定方式处理：

- 文件：直接使用原文件
- URL：先抓取内容，再保存为 `translate/{slug}.md`
- 内联文本：保存为 `translate/{slug}.md`

输出目录会创建在源文件同级目录下，例如：

```
posts/article.md -> posts/article-zh/
translate/ai-future.md -> translate/ai-future-zh/
```

如果输出目录已经存在，旧结果不会被覆盖，而是先被重命名为带时间戳的备份目录。

## `translate` 的输出文件

不同模式下，输出文件略有不同。

`quick` 模式只输出：

```
translation.md
```

`normal` 模式输出：

```
01-analysis.md
02-prompt.md
translation.md
```

`refined` 模式输出：

```
01-analysis.md
02-prompt.md
03-draft.md
04-critique.md
05-revision.md
translation.md
```

这意味着你不仅能拿到最终译文，还能看到它的分析、提示词、初稿、批判审阅和修订过程。

## Credits

`translate` 基于 [muyi-translate](https://github.com/ohmuyi/muyi-codex-skills) 改造而成，上游项目是 [ohmuyi/muyi-codex-skills](https://github.com/ohmuyi/muyi-codex-skills)，原始上游是 [JimLiu/baoyu-skills](https://github.com/JimLiu/baoyu-skills)。

本仓库在保留原有思路的基础上，针对 OpenCode 的使用场景做了适配。上游项目都使用 MIT 许可。

## 仓库结构

本仓库当前结构如下：

```
opencode-skills/
  skills/
    .curated/
      distill-docs/
      team/
      translate/
      wechat-article-writer/
  _templates/
    skill/
```

`skills/.curated/` 用于存放实际可安装的 skills。每个 skill 都是一个独立目录，至少包含 `SKILL.md`，通常还会包含 `LICENSE.txt`、`references/` 和 `scripts/`。

`_templates/skill/` 是新建 skill 时可复用的模板目录，不会作为实际 skill 安装。

## 如何添加新 skill

1. 复制 `_templates/skill/` 到 `skills/.curated/<your-skill-name>/`
2. 编辑 `SKILL.md` 添加 skill 描述和工作流
3. 添加 `LICENSE.txt`（推荐 MIT）
4. 添加 `references/` 放参考文档
5. 添加 `scripts/` 放辅助脚本
6. 提交到 GitHub 即可分享
