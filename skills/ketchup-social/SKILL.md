---
name: ketchup-social
description: Generate viral launch threads for Twitter/LinkedIn from changelogs
version: 1.0.0
---

# Ketchup Social 📱

**Social Salsa** - Turn your releases into viral launch threads.

You built it. Now let the world know.

## Capabilities

- 🐦 **Twitter Threads**: Hook-optimized tweet sequences
- 💼 **LinkedIn Posts**: Professional announcement format
- 🎯 **Engagement Hooks**: First-line optimization
- #️⃣ **Hashtag Generation**: Relevant, trending tags
- 🔗 **Link Formatting**: Smart URL shortening suggestions

## Usage

### CLI
```bash
python scripts/generate.py \
  --changelog "v2.0.0.md" \
  --platform twitter \
  --output "launch-thread.txt"
```

### From Text
```bash
python scripts/generate.py \
  --content "We just shipped dark mode!" \
  --platform linkedin \
  --output "announcement.txt"
```

### Options
| Flag | Description | Default |
|------|-------------|---------|
| `--platform` | Target platform | `twitter` |
| `--style` | Tone (hype, professional, casual) | `hype` |
| `--thread-length` | Number of tweets | `5` |
| `--include-cta` | Add call-to-action | `true` |

## Example Output (Twitter)

```
🚀 We just shipped Auth 2.0 — and it changes everything.

Here's what's new (thread 🧵)

---

1/ We rebuilt authentication from the ground up.

JWT → Sessions. 
Why? Security + performance.

Here's the before/after performance chart 📊

---

2/ Session-based auth means:
- Instant revocation
- No JWT decode overhead  
- Server-side session management

Result: 40% faster auth checks ⚡

---

3/ But the REAL unlock?

We added Redis for session storage.

That means horizontal scaling with zero complexity.

---

4/ Migration path?

We've got you covered:
- Automatic token conversion
- 30-day grace period
- Zero downtime upgrade

Docs: [link]

---

5/ Try Auth 2.0 today:

npm install @yourapp/auth@latest

Star us on GitHub ⭐
[link]

#opensource #devtools #authentication
```

## Requirements

> [!IMPORTANT]
> **BYOK Required**: This skill uses an LLM for content generation.

### Environment Variables
- `OPENROUTER_API_KEY` (**Recommended** - access all models)
- `ANTHROPIC_API_KEY` (Direct)
- `OPENAI_API_KEY` (Fallback)

### Model Selection
```bash
# Use a cheaper model for drafts
python generate.py --model "anthropic/claude-3-haiku" --content "..."

# Use GPT-4 for premium quality
python generate.py --model "openai/gpt-4-turbo" --content "..."
```

### Dependencies
- Python 3.11+
- `langchain-anthropic` or `langchain-openai`

---

*Part of the [Ketchup Skills](https://github.com/GitKetchup/ketchup-skills) ecosystem.*
*Catch up on your code.*
