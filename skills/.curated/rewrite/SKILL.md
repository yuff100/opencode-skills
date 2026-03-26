---
name: "rewrite"
description: "Rewrites web content for WeChat Official Accounts publication with automatic image insertion and formatting adjustments. Takes a URL input, extracts content, restructures for mobile reading, and generates optimized titles."
---

# Rewrite

Use when you need to rewrite web content for WeChat Official Accounts publication, with automatic image insertion and formatting adjustments. Takes a URL input, fetches content, rewrites tone and structure, automatically inserts relevant images (AI-generated or from web search), and generates 5 optional headlines with a one-sentence summary.

## When to use

- User provides a URL and asks to prepare it for WeChat Official Account publication
- Need to rewrite articles for better readability on mobile WeChat
- Want automatic image insertion to make the article more engaging
- Need to convert technical/academic content into a more accessible format for general audience
- Repurposing content from other platforms for WeChat

## Core Features

1. **URL Content Extraction** - Cleans and extracts main article content from any URL
2. **Tone & Structure Adaptation** - Restructures for mobile reading with shorter paragraphs
3. **WeChat Formatting** - Follows WeChat publishing best practices
4. **Automatic Image Insertion** - Finds or generates relevant images at natural breakpoints
5. **Title & Summary Generation** - Creates 5 optional headlines and a summary

## Resource map

- `references/extend-schema.md`: EXTEND.md configuration schema and documentation
- `references/first-time-setup.md`: First-run setup instructions
- `references/subagent-prompt.md`: Subagent prompt template for content rewriting
- `references/wechat-guidelines.md`: WeChat Official Account formatting best practices
- `references/workflow.md`: Detailed step-by-step workflow documentation
- `scripts/fetch-url.js`: Helper script for URL content extraction

## Configuration Preferences

The skill supports `EXTEND.md` configuration for persistent preferences. The skill checks for configuration in this order (first found is used):

1. `.rewrite/EXTEND.md` (project local)
2. `${XDG_CONFIG_HOME:-$HOME/.config}/rewrite/EXTEND.md` (user config)
3. `$HOME/.rewrite/EXTEND.md` (legacy fallback)

See `references/extend-schema.md` for the complete configuration schema, available options, default settings, and an example template.

## Workflow Summary

1. **Input** - Receive URL and optional preferences
2. **Configuration** - Load preferences from `EXTEND.md` or use defaults
3. **Extraction** - Fetch and clean main content from URL
4. **Analysis** - Analyze structure and plan image positions
5. **Rewriting** - Restructure and reformat according to WeChat guidelines
6. **Images** - Acquire and insert images at planned positions
7. **Assembly** - Combine into final publication-ready Markdown
8. **Completion** - Generate optional titles and summary

See `references/workflow.md` for the complete step-by-step workflow.

## Examples

### Basic Usage
```
Rewrite this URL for WeChat Official Account: https://example.com/article.html
```

Follows default settings: general audience, conversational tone, web images.

### Customized Usage
```
Rewrite this URL for WeChat, target audience is technical professionals, formal tone, don't add images:
https://example.com/technical-article
```

Will apply your custom preferences for this run.

## Validation

Before completion, always verify:
- All original main content is preserved
- Markdown formatting is correct and WeChat-compatible
- Images are correctly linked
- All image attributions are included where required
- Tone matches the requested audience preference
- Paragraphs are appropriately short for mobile reading
- 5 optional headlines and one-sentence introduction have been generated

## Dependencies

- `webfetch` for URL content fetching (built-in)
- `websearch_web_search_exa` for image search (built-in)
- `bun` or `node` optional for helper scripts (not required)

## Author

Created based on the OpenCode skill framework.

## License

MIT
