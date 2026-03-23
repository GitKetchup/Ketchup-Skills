<div align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="assets/logo-dark.svg">
    <source media="(prefers-color-scheme: light)" srcset="assets/logo-light.svg">
    <img alt="Ketchup Logo" src="assets/logo-light.svg" width="400">
  </picture>

  # Ketchup Skills
  
  **Open Source AI Agent Skills for Code Intelligence**
  <p><i>Catch up on your code.</i></p>

  [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
  [![Skills.sh](https://img.shields.io/badge/Skills.sh-Compatible-blueviolet)](https://skills.sh)
  [![Powered by MCP](https://img.shields.io/badge/Powered%20by-MCP-green)](https://modelcontextprotocol.io)

</div>

---

## 🍅 What's Here

These skills power Ketchup's code intelligence and work with any AI assistant (Claude, Cursor, Antigravity, Copilot). They run **locally** — your code never leaves your machine.

## 🥑 The Menu

### 🏷️ Core Intelligence
| Skill | Description | API Key? | Status |
|-------|-------------|----------|--------|
| **[`ketchup-classify`](/skills/ketchup-classify)** | **Commit Intelligence**. Classifies commits, discovers features, extracts PRs. | ❌ None needed | ✅ Live |
| **[`ketchup-changelog`](/skills/ketchup-changelog)** | **Git to Story**. Complexity, security, momentum, process analysis via MCP. | Optional (cloud) | ✅ Live |

### 🔍 Analysis Tools
| Skill | Description | API Key? | Status |
|-------|-------------|----------|--------|
| **[`ketchup-diff-analyzer`](/skills/ketchup-diff-analyzer)** | **Diff to English**. LLM-powered code change explanations. | ✅ BYOK | ✅ Live |
| **[`ketchup-code-viz`](/skills/ketchup-code-viz)** | **Code Images**. Syntax-highlighted diff screenshots. | ❌ None needed | ✅ Live |

---

## 🍳 Installation

### Via Ketchup CLI (Recommended)
```bash
# Install the CLI (skills are built-in)
npm install -g @gitketchup/cli

# Classification runs automatically during sync
ketchup sync

# Or use the MCP server for AI assistant integration
ketchup mcp
```

### Standalone (pip)
```bash
# Coming soon
pip install ketchup-skills
```

### Via Skills.sh
```bash
npx skills add gitketchup/ketchup-skills --skill ketchup-classify
```

### Direct (clone)
```bash
git clone https://github.com/gitketchup/ketchup-skills.git
cd ketchup-skills/skills/ketchup-classify
python scripts/classify.py --repo /your/repo --features --json
```

---

## 🤖 Use with AI Assistants

All skills are **MCP-compatible**. Tell your AI:

> "Classify my last 30 days of commits using the ketchup-classify SKILL.md"

The agent will:
1. Read `SKILL.md` to understand the taxonomy
2. Run `classify.py` to get rule-based results
3. Optionally use its own LLM intelligence to reclassify low-confidence commits
4. Group results into feature clusters

### BYOK (Bring Your Own Key)

Skills that use LLMs support any provider:
- `OPENROUTER_API_KEY` (recommended — access all models)
- `ANTHROPIC_API_KEY`
- `OPENAI_API_KEY`
- Or any local LLM via Ollama/LM Studio

---

## 🌶️ Want the Full Experience?

These skills handle the **analysis**. The full Ketchup platform adds:
- 🎬 **Cinematic video generation** from your commits
- 🎨 **Auto-branding** with your colors and logos
- 📸 **Smart screenshots** of your features
- 🎙️ **Professional narration**

👉 **[Try Ketchup](https://gitketchup.com)**

---

## 📄 License

MIT License. See [LICENSE](./LICENSE) for details.
