---
name: ketchup-diff-analyzer
description: Intelligent git diff summarization using LLMs
version: 1.0.0
---

# Ketchup Diff Analyzer 🔍

**Diff to English** - Stop reading diffs. Start understanding changes.

Let AI explain *what* changed and *why* it matters.

## Capabilities

- 🧠 **Smart Summarization**: LLM-powered diff analysis
- 📝 **Markdown Output**: Clean, readable summaries
- 🏷️ **Change Classification**: Categorizes changes (refactor, feature, fix, etc.)
- ⚠️ **Breaking Change Detection**: Flags API/schema changes
- 📊 **Impact Assessment**: Estimates scope and risk

## Usage

### CLI
```bash
python scripts/analyze.py \
  --repo "/path/to/repo" \
  --from "v1.0.0" \
  --to "v1.1.0" \
  --output "summary.md"
```

### From Diff Text
```bash
git diff HEAD~5 | python scripts/analyze.py --stdin --output summary.md
```

### Options
| Flag | Description | Default |
|------|-------------|---------|
| `--format` | Output format (md, json, text) | `md` |
| `--detail` | Detail level (brief, normal, verbose) | `normal` |
| `--focus` | Focus area (all, breaking, features) | `all` |

## Example Output

```markdown
## Summary: Authentication Refactor

### 🎯 TL;DR
Migrated from JWT to session-based authentication for improved security.

### 📦 Changes
- **src/auth.ts**: Replaced JWT verification with Redis session lookup
- **src/middleware.ts**: Added session hydration middleware
- **package.json**: Added `ioredis` dependency

### ⚠️ Breaking Changes
- `auth.verify()` is now async
- Token format changed (old tokens invalidated)

### 🏷️ Classification
Type: Refactor | Risk: Medium | Files: 3
```

## Requirements

> [!IMPORTANT]
> **BYOK Required**: This skill uses an LLM for intelligent summarization.

### Environment Variables
- `OPENROUTER_API_KEY` (**Recommended** - access all models)
- `ANTHROPIC_API_KEY` (Direct)
- `OPENAI_API_KEY` (Fallback)

### Model Selection
```bash
# Use Gemini via OpenRouter
python analyze.py --model "google/gemini-pro-1.5" --repo . --from v1.0

# Use GPT-4
python analyze.py --model "gpt-4-turbo" --repo . --from v1.0
```

### Dependencies
- Python 3.11+
- `GitPython`
- `langchain-anthropic` or `langchain-openai`

---

*Part of the [Ketchup Skills](https://github.com/GitKetchup/ketchup-skills) ecosystem.*
*Catch up on your code.*
