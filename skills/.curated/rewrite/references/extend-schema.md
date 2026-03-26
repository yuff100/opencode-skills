# EXTEND.md Configuration Schema

This document defines the available configuration fields for `EXTEND.md` preference files.

## Top-level Fields

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `target_audience` | enum | No | `general` | Target audience for the article. Options: `general` (broad audience), `technical` (technical readers), `business` (business professionals), `student` (students) |
| `tone` | enum | No | `conversational` | Writing tone to use. Options: `conversational` (friendly, engaging), `formal` (professional, academic), `story-telling` (narrative, engaging), `inspirational` (motivational) |
| `image_source` | enum | No | `web` | Where to get images from. Options: `web` (search web for images), `ai` (generate prompts for AI), `none` (no images) |
| `image_frequency` | number | No | `2` | Number of images per 1000 words. Range: 1-5 |
| `max_word_count` | number | No | `null` | Maximum word count after rewriting. `null` means no limit |
| `add_frontmatter` | boolean | No | `true` | Whether to add YAML frontmatter with metadata (title, original source, date) |
| `include_original_source` | boolean | No | `true` | Whether to include a link back to the original article at the end |
| `wechat_formatting` | boolean | No | `true` | Apply WeChat-specific formatting rules |
| `add_divider` | boolean | No | `true` | Add horizontal dividers between major sections |
| `avoid_keywords` | string | No | `""` | Comma-separated list of keywords to avoid in image search |
| `preferred_image_aspect` | string | No | `"16:9"` | Preferred image aspect ratio. Common: `16:9`, `4:3`, `1:1` |

## Example EXTEND.md

```markdown
# My WeChat Rewrite Preferences

target_audience: general
tone: conversational
image_source: web
image_frequency: 2
max_word_count: 4000
add_frontmatter: true
include_original_source: true
wechat_formatting: true
add_divider: true
avoid_keywords: portrait, people, face
preferred_image_aspect: 16:9
```

## First-time Setup Template

When creating a new `EXTEND.md`, use this template:

```markdown
# Rewrite Configuration for WeChat Official Accounts

# Who is your audience?
# Options: general, technical, business, student
target_audience: general

# What writing tone do you prefer?
# Options: conversational, formal, story-telling, inspirational
tone: conversational

# Where should images come from?
# Options: web (search web), ai (generate prompts), none (no images)
image_source: web

# How many images per 1000 words? (1-5)
image_frequency: 2

# Maximum word count after rewriting (uncomment to enable)
# max_word_count: 4000

# Add YAML frontmatter with metadata?
add_frontmatter: true

# Include link back to original source?
include_original_source: true

# Apply WeChat-specific formatting (short paragraphs, spacing)?
wechat_formatting: true

# Add dividers between major sections?
add_divider: true

# Keywords to avoid in image search (comma separated)
# avoid_keywords: bad, keyword1, keyword2

# Preferred image aspect ratio
preferred_image_aspect: 16:9
```
