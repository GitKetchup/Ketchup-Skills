---
name: ketchup-voice
description: Generate professional voiceovers using ElevenLabs AI voices
version: 1.0.0
---

# Ketchup Voice 🎙️

**Pro Narrator** - Studio-quality voiceovers for your changelog videos.

TTS is bland. Voice Design is spicy. 🌶️

## Capabilities

- 🎤 **Pro Voices**: Access to ElevenLabs' premium voice library
- 🎭 **Emotion Control**: Adjust tone, pace, and emphasis
- 📝 **SSML Support**: Fine-grained control with Speech Synthesis Markup
- 🔊 **Multi-Format**: MP3, WAV, or OGG output
- 🚀 **Batch Processing**: Generate multiple segments in one call

## Usage

### CLI
```bash
python scripts/generate.py \
  --script "We just shipped Auth 2.0. Here's what's new." \
  --voice "storyteller" \
  --output "narration.mp3"
```

### From File
```bash
python scripts/generate.py \
  --file "script.txt" \
  --voice "professional" \
  --output "narration.mp3"
```

### Options
| Flag | Description | Default |
|------|-------------|---------|
| `--voice` | Voice preset | `storyteller` |
| `--speed` | Playback speed (0.5-2.0) | `1.0` |
| `--stability` | Voice consistency (0-1) | `0.5` |
| `--clarity` | Clarity enhancement (0-1) | `0.75` |
| `--format` | Output format | `mp3` |

## Voice Presets

| Preset | Best For | Vibe |
|--------|----------|------|
| `storyteller` | Changelogs, demos | Warm, engaging |
| `professional` | Enterprise content | Clear, authoritative |
| `hype` | Launch videos | Energetic, exciting |
| `calm` | Tutorials | Soothing, patient |
| `documentary` | Deep dives | Thoughtful, measured |

## Requirements

> [!IMPORTANT]
> **BYOK Required**: This skill requires an ElevenLabs API key.
> Get yours at [elevenlabs.io](https://elevenlabs.io)

### Environment Variables
```bash
export ELEVENLABS_API_KEY="your-key-here"
```

### Dependencies
- Python 3.11+
- `elevenlabs` package
- `pydub` (for audio processing)

## Integration

This skill is designed to work with `ketchup-changelog`:
1. **Changelog** generates the story script
2. **Voice** converts it to professional narration
3. **Ketchup Platform** syncs it to your video

---

*Part of the [Ketchup Skills](https://github.com/GitKetchup/ketchup-skills) ecosystem.*
*Catch up on your code.*
