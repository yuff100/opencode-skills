# Complete Workflow Reference

This document outlines the complete step-by-step workflow that the rewrite skill follows.

## Step 1: Input Processing

1. Receive URL input from user
2. Check for any one-off preferences specified by the user
3. Create a slug from the URL for file naming

## Step 2: Load Configuration

1. Check for `EXTEND.md` in the standard locations (see SKILL.md)
2. If found, load and merge preferences
3. If not found, prompt the user for setup (see first-time-setup.md)
4. Merge user's one-off preferences into the configuration

## Step 3: Create Output Directory

```
rewrite/{slug}/
├── raw-content.md
├── analysis.md
├── images/
└── final-rewrite.md
```

## Step 4: Fetch Content

1. Use `webfetch` to retrieve content from the URL
2. Extract the main article content, removing:
   - Navigation menus
   - Advertisements
   - Sidebars
   - Footers
   - Comment sections
   - Social sharing buttons
3. Clean up HTML/formatting and convert to basic Markdown
4. Save to `raw-content.md`

## Step 5: Content Analysis

1. Read the raw content and understand:
   - Main topic and key points
   - Overall structure
   - Number of words
   - Natural breaking points for images
2. Identify how many images are needed based on word count and `image_frequency` setting
3. For each section, generate 2-3 relevant keywords for image search
4. Write analysis to `analysis.md` including:
   - Original word count
   - Target word count after rewrite
   - Number of images to be inserted
   - List of image search keywords per position
   - Outline of the restructured article

## Step 6: Rewriting Process

Apply these transformation rules according to configuration:

### Tone Adjustment
- **conversational**: Use more first/second person, contractions, conversational language
- **formal**: Keep language professional, avoid contractions, use more formal vocabulary
- **story-telling**: Narrative flow with engaging opening, build-up, conclusion
- **inspirational**: Add motivational elements, focus on takeaways

### Structural Changes
- Split any paragraph longer than 3 lines into shorter paragraphs
- Add descriptive subheadings where missing
- Break up long sections with subheadings every 300-500 words
- Convert bulky lists to bullet points for better mobile scanning
- Add an engaging opening paragraph that hooks the reader

### WeChat Formatting (when enabled)
- Ensure all paragraphs are 1-3 lines maximum
- Leave a blank line between every paragraph
- Use `**bold**` for important points instead of italics
- Avoid complex nested structures
- Add horizontal dividers between major sections when enabled
- Keep line length comfortable for mobile reading

## Step 7: Image Acquisition

### For `image_source: web`
1. For each image position, use `websearch_web_search_exa` to search for relevant images with image keywords
2. Find image URLs from the search results (many search results only describe images, don't directly link)
3. **Do NOT download** - insert the full image URL directly in Markdown
4. WeChat Official Account editor will automatically download and host the image
5. Record the source webpage URL for attribution
6. Insert Markdown image reference with the original URL at the correct position

**Why this approach**:
- Direct downloading often fails due to CORS, hotlinking protection, and anti-crawler measures
- WeChat pulls the image from the original URL when you paste the Markdown
- This avoids the "HTML saved as JPG" problem completely

### For `image_source: ai`
1. Generate a detailed prompt for each image based on the section content
2. Use the built-in multi-modal AI to generate the image directly
3. Save the generated image to `rewrite/{slug}/images/`
4. Insert Markdown image reference in the text at the correct position

### For `image_source: none`
- Skip image insertion completely

## Step 8: Final Assembly

1. Add YAML frontmatter if enabled:
   ```yaml
   ---
   title: [rewritten title]
   original_url: [source URL]
   date: [current date]
   word_count: [final word count]
   images_used: [number]
   ---
   ```
2. Add link back to original source at the end if enabled
3. Add image attribution for web-sourced images
4. Write the final Markdown to `final-rewrite.md`

## Step 9: Validation

Perform these checks before reporting completion:

1. **Completeness**: Verify all main content from original is included
2. **Word Count**: Check if within `max_word_count` limit if set
3. **Formatting**: Ensure Markdown is valid and follows WeChat rules
4. **Images**: 
   - For `image_source: ai`: Verify image files exist and local links are correct
   - For `image_source: web`: Verify image URLs are valid and properly formatted
5. **Tone**: Double-check that tone matches the requested preference
6. **Structure**: Confirm paragraphs are short enough for mobile

## Step 10: Completion

Report back to the user with:
- Path to the final output file
- Summary of changes made
- Word count before/after
- Number of images inserted
- Any next steps they need to take (like generating AI images)
