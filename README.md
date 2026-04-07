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

### ⚡ Quick Start
| Skill | Description | API Key? | Status |
|-------|-------------|----------|--------|
| **[`ketchup-recap`](/skills/ketchup-recap)** | **Quick Recap**. Generate video recaps from git commits in < 3 min. | ❌ None needed | ✅ Live |
| **[`ketchup-classify`](/skills/ketchup-classify)** | **Commit Intelligence**. Classifies commits, discovers features, extracts PRs. | ❌ None needed | ✅ Live |

### 🔍 Analysis & Visualization
| Skill | Description | API Key? | Status |
|-------|-------------|----------|--------|
| **[`ketchup-changelog`](/skills/ketchup-changelog)** | **Git to Story**. Complexity, security, momentum, process analysis via MCP. | Optional (cloud) | ✅ Live |
| **[`ketchup-diff-analyzer`](/skills/ketchup-diff-analyzer)** | **Diff to English**. LLM-powered code change explanations. | ✅ BYOK | ✅ Live |
| **[`ketchup-code-viz`](/skills/ketchup-code-viz)** | **Code Images**. Syntax-highlighted diff screenshots. | ❌ None needed | ✅ Live |

---

## 🍳 Installation

### Via Ketchup CLI (Recommended)
```bash
# Install the CLI (skills are built-in)
npm install -g @gitketchup/cli

# Generate a recap video
ketchup cloud recap

# Or use the MCP server for AI assistant integration
ketchup mcp
```

### Via Skills.sh
```bash
npx skills add gitketchup/ketchup-skills --skill ketchup-recap
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

> "Generate a recap of what I built this week using the ketchup-recap skill"

The agent will:
1. Read `SKILL.md` to understand the workflow
2. Extract commits via `git log`
3. Cluster commits into features using AI
4. Call the Ketchup API to generate a video

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
