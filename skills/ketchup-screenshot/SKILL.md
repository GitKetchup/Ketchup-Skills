---
name: ketchup-screenshot
description: Intelligent screenshot capture using Browser-Use for Ketchup video generation
version: 1.0.0
---

# Ketchup Screenshot Skill 📸

Intelligent, AI-powered screenshot capture for Ketchup video generation. This skill uses [Browser-Use](https://github.com/browser-use/browser-use) to navigate websites, handle logins, and capture feature-specific context.

## Capabilities

- 🧠 **Context-Aware Navigation**: Uses LLMs (Claude/GPT-4) to understand feature descriptions and navigate to the relevant UI.
- 🔒 **Authenticated Capture**: Handles logins seamlessly using provided credentials.
- 🕵️ **Stealth Mode**: Optional cloud browser support to bypass Cloudflare and severe bot protections.
- 🖼️ **Smart Framing**: Captures the exact UI element or viewport relevant to the feature.

## Usage

This skill is designed to be called programmatically by the Ketchup Narrative Engine, but can also be tested via CLI.

```bash
# Test capture via CLI
python scripts/capture.py \
  --url "https://app.ketchup.sh" \
  --username "demo@ketchup.sh" \
  --password "secret" \
  --features "New Analytics Dashboard, User Profile Settings"
```

## Hybrid Strategy

This skill implements a **Local First** strategy:
1. **Default**: Uses local Chromium (fast, free).
2. **Cloud Fallback**: If `BROWSER_USE_API_KEY` is set, switches to cloud browser for stealth capabilities.

## Requirements

> [!IMPORTANT]
> **Bring Your Own Key (BYOK)**: This skill requires an LLM to navigate websites intelligently.  
> You must provide **EITHER** an Anthropic API Key (recommended for best performance) **OR** an OpenAI API Key.

### Environment Variables
You must set one of the following before running the script:
- `OPENROUTER_API_KEY` (**Recommended** - access all models with one key)
- `ANTHROPIC_API_KEY` (Direct: `claude-3-5-sonnet` is used)
- `OPENAI_API_KEY` (Fallback: `gpt-4o` is used)

### Model Selection
Use `--model` flag to override defaults:
```bash
# Use a specific OpenRouter model
python scripts/capture.py --model "google/gemini-pro-1.5" ...

# Use a specific Anthropic model
python scripts/capture.py --model "claude-3-opus-20240229" ...
```

### Dependencies
- Python 3.11+
- `browser-use` package
- `playwright`
- `langchain-anthropic` or `langchain-openai`
