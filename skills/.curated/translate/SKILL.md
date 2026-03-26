---
name: "translate"
description: "Translates and localizes articles, documents, URLs, and Markdown content between languages with terminology consistency management, automatic chunking for long documents, and multiple quality modes."
---

# Translate

Use when the user asks to translate or localize an article, document, URL, Markdown file, or inline text between languages, especially when terminology consistency, long-document chunking, or publication-quality refinement matters. Supports quick, normal, and refined modes plus EXTEND.md preferences and glossary loading.

Ported from muyi-codex-skills by shuimuyi (https://github.com/ohmuyi).

## When to use

- Translate articles, documents, blog posts, README files, URLs, or inline text.
- Localize Markdown content while preserving structure, links, and code blocks.
- Handle long documents where chunking and terminology consistency matter.
- Produce either a fast draft or a refined publication-quality translation.

## Resource map

- `references/config/extend-schema.md`: EXTEND.md fields and glossary schema
- `references/config/first-time-setup.md`: first-run question set and EXTEND.md template
- `references/workflow-mechanics.md`: source materialization, output directory, conflict handling
- `references/refined-workflow.md`: analysis, critique, revision, and polish guidance
- `references/subagent-prompt-template.md`: shared-context template for chunked translation
- `references/glossary-en-zh.md`: built-in EN -> ZH glossary

## Runtime

- Prefer `bun` for the chunking script.
- If `bun` is unavailable but `npx` exists, use `npx -y bun`.
- If neither is available, explain that automated chunking is unavailable and either install Bun or chunk manually.

## Preference lookup

Check for `EXTEND.md` in standard location order (project local → user config → legacy fallback). If found, load and apply. If no configuration exists and this is the first run, ask for user preferences and create `EXTEND.md`. If user skips setup, use built-in defaults.

## Defaults

- `target_language`: `zh-CN`
- `default_mode`: `normal`
- `audience`: `general`
- `style`: `storytelling`
- `chunk_threshold`: `4000`
- `chunk_max_words`: `5000`

See `references/config/extend-schema.md` for complete configuration documentation.

## Workflow Summary

1. **Load Preferences** - Merge configuration and glossary from all sources
2. **Materialize Source** - Save URL/inline text to file, create output directory (see `references/workflow-mechanics.md`)
3. **Select Mode** - Quick (direct), Normal (analyze + translate), or Refined (full critique-revision polish)
4. **Assess Length** - Chunk long documents at or above threshold using `scripts/main.ts` with bun/npx
5. **Translate** - Translate chunks sequentially, merge results, preserve structure
6. **Apply Principles** - Preserve meaning, keep terminology consistent, maintain Markdown structure
7. **Save Outputs** - Stable filenames based on mode (quick: `translation.md`, full mode: multiple step files)
8. **Final Check** - Lightweight check for source-language text in images

Detailed mechanics for each step are in the reference documents.

## Mode details

### Quick

Translate directly to `translation.md`. Use this for short or disposable content.

### Normal

Create `01-analysis.md` and `02-prompt.md`, then write `translation.md`.

If the user later asks to continue polishing, rename the current `translation.md` to `03-draft.md` and continue with critique, revision, and polish using `references/refined-workflow.md`.

### Refined

Follow the review loop in `references/refined-workflow.md`.

Use the main agent for critique, revision, and polish even if the initial draft was chunked.

## Validation

- Ensure the final output preserves Markdown structure and stable file naming.
- Re-read the translation for terminology drift, broken links, code block corruption, and inconsistent annotation depth.
- **Completeness Check (MANDATORY)**: After translation completes, **verify against the source material**:
  - Count the number of top-level sections/headings in source and translation
  - Compare that all paragraphs, lists, code blocks, and concluding sections are present
  - Verify no content was truncated due to context window limits
  - If the source was truncated, explicitly fetch the remaining content and translate it before completing
  - Flag any missing content to the user instead of silently omitting it
- **File Existence Check (MANDATORY)**: After saving the output, **verify the file actually exists** on the filesystem before reporting completion. If the file does not exist, re-save it and verify again. Do not report "saved" when the file cannot be accessed.
- If `EXTEND.md` creation or chunk automation was skipped because tooling was missing, state that explicitly.

## Post-Translation Tasks for Publication

If the translated article is intended for Chinese tech blog or WeChat public account publication:

1. **Generate 5 WeChat public account titles**: Suggest 5 catchy, clickable titles in Chinese that fit WeChat reading habits
2. **Write 1-2 sentence summary**: Provide a concise introduction that summarizes the core value of the article for readers

Both are for the author's reference when preparing to publish.

## Author

shuimuyi (https://github.com/ohmuyi)

## License

MIT
