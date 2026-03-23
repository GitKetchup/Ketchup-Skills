---
name: ketchup-classify
description: Classify git commits by type and discover features/updates from your codebase using rule-based analysis or your own AI subscription (BYOK).
version: 1.0.0
---

# Ketchup Classify 🏷️

**Commit Intelligence** — Know what your team actually shipped.

Turn a wall of git commits into classified updates, feature clusters, and PR summaries — locally, privately, and instantly.

## Capabilities

- 🏷️ **Commit Classification**: `feature`, `fix`, `refactor`, `chore`, `docs`, `test`, `style`, `ci`, `build`, `perf`
- ✨ **Feature Discovery**: Groups related commits into named feature clusters
- 📋 **PR Extraction**: Parses merge commits + optional GitHub API for PR metadata
- ⚡ **Risk Assessment**: Flags high-risk changes (auth, payments, migrations)
- 💥 **Breaking Change Detection**: Identifies breaking changes from commit messages
- 🤖 **BYOK LLM**: Use your Claude/GPT/Ollama subscription for enhanced accuracy

## Usage

### Rule-Based (No API Key Required!)

Works out of the box. Parses Conventional Commits and uses keyword heuristics.

```bash
# Classify commits in a repo
python scripts/classify.py --repo /path/to/repo --days 30

# Output as JSON
python scripts/classify.py --repo /path/to/repo --json --output results.json

# Include feature discovery
python scripts/classify.py --repo /path/to/repo --features

# Include PR extraction
python scripts/classify.py --repo /path/to/repo --prs
```

### With AI Assistant (BYOK)

Let Claude/Cursor/Antigravity do the classification using your existing subscription:

```
You: "Classify the last 30 days of commits in this repo using the ketchup-classify skill"

Agent: 
1. Reads SKILL.md to understand taxonomy
2. Runs `classify.py --repo . --days 30 --json`
3. Reviews low-confidence results
4. Reclassifies ambiguous commits using its own intelligence
```

### MCP Integration

```bash
# Via Ketchup CLI
ketchup mcp

# Tools exposed:
# - classify_commits(repo_path, days)
# - discover_features(repo_path, days)
# - extract_prs(repo_path, days)
```

## Options

| Flag | Description | Default |
|------|-------------|---------|
| `--repo` | Path to git repository | `.` |
| `--days` | Days of history to analyze | `30` |
| `--features` | Enable feature discovery | `false` |
| `--prs` | Extract PR metadata | `false` |
| `--json` | Output as JSON | `false` |
| `--output` | Output file path | stdout |
| `--min-confidence` | Min confidence threshold | `0.0` |

## Classification Taxonomy

| Type | Pattern | Example |
|------|---------|---------|
| `feature` | `feat:`, "add", "implement" | `feat(auth): add OAuth login` |
| `fix` | `fix:`, "bug", "patch" | `fix: resolve race condition` |
| `refactor` | `refactor:`, "restructure" | `refactor: extract utils` |
| `docs` | `docs:`, "readme" | `docs: update API guide` |
| `test` | `test:`, "coverage" | `test: add auth unit tests` |
| `chore` | `chore:`, "bump", "merge" | `chore: update deps` |
| `style` | `style:`, "format", "lint" | `style: run prettier` |
| `ci` | `ci:`, "pipeline" | `ci: add staging deploy` |
| `build` | `build:`, "webpack" | `build: optimize bundle` |
| `perf` | `perf:`, "optimize" | `perf: lazy load images` |

## Example Output

```json
{
  "classified_commits": [
    {
      "sha": "abc123",
      "type": "feature",
      "scope": "auth",
      "description": "add OAuth login with Google",
      "risk_level": "high",
      "is_breaking": false,
      "confidence": 0.95
    }
  ],
  "discovered_features": [
    {
      "name": "Auth",
      "description": "OAuth login with Google; session management",
      "type": "feature",
      "commit_count": 3,
      "significance": 0.8
    }
  ],
  "pull_requests": [
    {
      "number": 42,
      "title": "Add OAuth login",
      "author": "dashon",
      "merged_at": "2024-01-15T10:00:00Z",
      "commit_count": 3
    }
  ]
}
```

## Requirements

### No API Keys Required! 🎉
Rule-based classification runs entirely locally.

### Optional: BYOK for Enhanced Accuracy
- `OPENROUTER_API_KEY` (recommended)
- `ANTHROPIC_API_KEY`
- `OPENAI_API_KEY`
- Or any local LLM via Ollama/LM Studio

### Dependencies
- Python 3.9+
- `GitPython` (for repo access)

---

*Part of the [Ketchup Skills](https://github.com/GitKetchup/ketchup-skills) ecosystem.*
*Catch up on your code.*
