# First-time Setup for Rewrite Skill

When using the rewrite skill for the first time, you'll be asked a few questions to create your personalized configuration. This saves your preferences so you don't need to specify them every time.

## Questions you'll be asked

1. **Target audience**: Who reads your WeChat Official Account?
   - `general` - General audience (default)
   - `technical` - Technical professionals
   - `business` - Business readers
   - `student` - Students/younger audience

2. **Preferred tone**: What writing style fits your account?
   - `conversational` - Friendly and engaging (default)
   - `formal` - Professional/academic
   - `story-telling` - Narrative approach
   - `inspirational` - Motivational

3. **Image source**: Where should images come from?
   - `web` - Search web for free-to-use images (default)
   - `ai` - Generate prompts for AI image generation
   - `none` - Don't include images

4. **Image frequency**: How many images per 1000 words?
   - Default: 2 images per 1000 words (one every ~500 words)
   - Range: 1-5 images

5. **Save location**: Where to save the `EXTEND.md` config?
   - Default: `~/.config/rewrite/EXTEND.md`

## After setup

Once your `EXTEND.md` is created, the skill will automatically load it for every future use. You can edit the file at any time to change your preferences.

## Creating a project-specific config

If you have different preferences for different projects, you can create a `.rewrite/EXTEND.md` file in your project directory. This will override the global configuration for that project.

## Resetting configuration

To change your preferences after setup, simply edit the `EXTEND.md` file or delete it and you'll be asked the setup questions again next time.
