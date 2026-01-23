---
name: ketchup-code-viz
description: Generate beautiful, syntax-highlighted code images from git diffs
version: 1.0.0
---

# Ketchup Code Viz 🥑

**Code Guacamole** - Turn raw git diffs into beautiful, shareable code images.

Perfect for backend features that have no UI to screenshot. Make your code changes *cinematic*.

## Capabilities

- 🎨 **Syntax Highlighting**: 100+ language support via Shiki
- 📸 **Carbon-Style Output**: Beautiful dark-mode code images
- 📊 **Diff Visualization**: Red/green highlighting for changes
- 🖼️ **Multiple Formats**: PNG, SVG, or HTML output
- 🚀 **Zero API Keys**: Runs entirely locally (no BYOK needed!)

## Usage

### CLI
```bash
python scripts/render.py \
  --repo "/path/to/repo" \
  --commit "abc123" \
  --file "src/auth.ts" \
  --output "auth-changes.png"
```

### From Diff Text
```bash
python scripts/render.py \
  --diff "$(git diff HEAD~1)" \
  --language "typescript" \
  --output "latest-changes.png"
```

### Options
| Flag | Description | Default |
|------|-------------|---------|
| `--theme` | Color theme | `github-dark` |
| `--font-size` | Font size in pixels | `14` |
| `--padding` | Image padding | `32` |
| `--max-lines` | Max lines to show | `30` |
| `--show-line-numbers` | Display line numbers | `true` |

## Themes

Supported themes include:
- `github-dark` (default)
- `github-light`
- `dracula`
- `nord`
- `one-dark-pro`
- `monokai`

## Example Output

```
┌─────────────────────────────────────────────┐
│ src/auth.ts                            1:23 │
├─────────────────────────────────────────────┤
│  1 │ - import { jwt } from 'jsonwebtoken'   │
│  2 │ + import { session } from 'redis'      │
│  3 │                                        │
│  4 │   export async function verify(token) {│
│  5 │ -   return jwt.verify(token, SECRET)   │
│  6 │ +   return session.get(token)          │
│  7 │   }                                    │
└─────────────────────────────────────────────┘
```

## Requirements

### Dependencies
- Python 3.11+
- `Pillow` (image generation)
- `pygments` (syntax highlighting)
- `GitPython` (optional, for repo access)

### No API Keys Required! 🎉
This skill runs entirely locally. No BYOK needed.

## Integration

This skill is designed to complement `ketchup-screenshot`:
- **Screenshot**: Captures UI features
- **Code Viz**: Captures backend/code features

Together, they provide complete visual coverage for any changelog.

---

*Part of the [Ketchup Skills](https://github.com/GitKetchup/ketchup-skills) ecosystem.*
*Catch up on your code.*
