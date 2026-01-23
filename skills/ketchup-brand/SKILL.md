---
name: ketchup-brand
description: Extract brand assets (logos, colors, fonts) from any website
version: 1.0.0
---

# Ketchup Brand 🎨

**Auto-Branding** - Harvest brand identity from any landing page.

No more manual color picking. Let the robot do it.

## Capabilities

- 🎨 **Color Extraction**: Primary, secondary, and accent colors
- 🖼️ **Logo Detection**: Finds and downloads logo assets
- 🔤 **Font Discovery**: Identifies web fonts in use
- 📊 **Palette Generation**: Creates complementary color schemes
- 📦 **JSON Export**: Machine-readable brand tokens

## Usage

### CLI
```bash
python scripts/extract.py \
  --url "https://stripe.com" \
  --output "stripe-brand.json"
```

### Options
| Flag | Description | Default |
|------|-------------|---------|
| `--format` | Output format (json, css, tailwind) | `json` |
| `--download-assets` | Download logos locally | `false` |
| `--include-fonts` | Extract font information | `true` |

## Example Output

```json
{
  "brand": {
    "name": "Stripe",
    "url": "https://stripe.com"
  },
  "colors": {
    "primary": "#635BFF",
    "secondary": "#0A2540",
    "accent": "#00D4FF",
    "background": "#F6F9FC",
    "text": "#425466"
  },
  "logo": {
    "url": "https://stripe.com/img/v3/home/social.png",
    "local_path": "./assets/stripe-logo.png"
  },
  "fonts": {
    "heading": "Söhne, system-ui, sans-serif",
    "body": "Söhne, system-ui, sans-serif"
  },
  "palette": ["#635BFF", "#0A2540", "#00D4FF", "#F6F9FC", "#425466"]
}
```

## Requirements

### No API Keys Required! 🎉
This skill runs entirely locally using Playwright.

### Dependencies
- Python 3.11+
- `playwright`
- `colorthief` (for color extraction)
- `Pillow`

---

*Part of the [Ketchup Skills](https://github.com/GitKetchup/ketchup-skills) ecosystem.*
*Catch up on your code.*
