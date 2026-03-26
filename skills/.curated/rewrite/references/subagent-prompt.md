# Subagent Prompt Template for Long Articles

When rewriting long articles (over 4000 words), use this template to create a shared context prompt for worker subagents.

```markdown
# WeChat Article Rewriting - Shared Context

## Original Source
- URL: {{original_url}}
- Title: {{original_title}}
- Total words: {{total_words}}
- This is chunk {{chunk_number}} of {{total_chunks}}

## Configuration
- Target audience: {{target_audience}}
- Tone: {{tone}}
- WeChat formatting enabled: {{wechat_formatting}}

## Key Principles to Follow

1. **Preserve all key information** - don't omit important facts or arguments
2. **Rewrite in the specified tone** - adjust language to fit the audience
3. **Split long paragraphs** into 1-3 sentence chunks for mobile
4. **Keep Markdown formatting simple** - WeChat supports basic Markdown well
5. **Maintain the original order** of sections and arguments
6. **Keep headings descriptive** but concise for WeChat

## This Chunk

Chunk heading: {{chunk_heading}}
Chunk word count: approx {{chunk_word_count}}

---

BEGIN ORIGINAL CONTENT:

{{chunk_content}}

END ORIGINAL CONTENT

---

Rewrite this chunk according to the specifications above. Preserve all meaning and key information while adapting it for WeChat Official Account publication.
```

## Chunking Strategy

- Split into chunks at natural section boundaries
- Keep each chunk under 2000 words
- Each chunk should be a self-contained unit that can be rewritten independently
- Maintain section hierarchy across chunks
- When merging back, combine chunks in original order and add images at the planned positions
