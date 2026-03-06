# Quick Reference Guide

Concise reference for the AI Craft Spellbook spells and commands.

> **New user?** See [START_HERE.md](START_HERE.md) to get started in 3 steps!

## 🎤 Natural Language Examples

Just speak naturally to Claude Code:

| Phrase | Spell Executed |
|---------|---------------|
| "Cleanse podcast.mp3" | audio_cleanse with default settings |
| "Cleanse audio with heavy noise reduction" | audio_cleanse --noise-strength heavy |
| "Remove background from sprite.png" | dispel_background with u2net model |
| "Dispel background from portrait.png with human model" | dispel_background --model u2net_human_seg |
| "Purify video and remove silence" | audio_cleanse with all steps enabled |

## 🔮 How Claude Code Understands You

When you type a natural command, Claude Code:
1. **Analyzes intent** - Understands what transformation you want
2. **Matches spell** - Finds the right spell in `spells/`
3. **Extracts parameters** - Gets file paths and settings from your request
4. **Reads quest** - Checks `quests/` for proper invocation
5. **Executes** - Runs the spell with correct Python syntax
6. **Reports results** - Shows you the magical treasure produced

All you need to do is say what you want!

## 🚀 Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# List all spells
ls spells/

# List all quests
ls quests/

# Read a quest
cat quests/audio_cleanse.md
```

## 📜 Spell Commands

### Audio Cleansing Ritual

**Basic:**
```bash
python spells/audio_cleanse.py --input podcast.mp3
```

**With output:**
```bash
python spells/audio_cleanse.py --input recording.mp4 --output clean.mp4
```

**Custom settings:**
```bash
python spells/audio_cleanse.py --input podcast.mp3 \
  --loudness -16 \
  --noise-strength medium
```

**Key parameters:**
- `--input` (required): Path to audio/video file
- `--output`: Output path (default: `<name>_purified.<ext>`)
- `--loudness`: Target LUFS (-23 broadcast, -16 podcast, -14 YouTube/Spotify)
- `--noise-strength`: light, medium, heavy
- `--silence-threshold`: dB threshold (default: -40)
- `--no-silence-removal`: Skip void banishment
- `--no-normalize`: Skip energy balancing
- `--no-noise-reduction`: Skip purification

### Dispel Background Hex

**Basic:**
```bash
python spells/dispel_background.py --input character.png
```

**With output:**
```bash
python spells/dispel_background.py --input image.png --output clean.png
```

**Custom model:**
```bash
python spells/dispel_background.py --input portrait.png \
  --model u2net_human_seg
```

**Key parameters:**
- `--input` (required): Path to image file
- `--output`: Output path (default: `<name>_dispelled.png`)
- `--model`: u2net, u2netp, u2net_human_seg, u2net_cloth_seg, silueta

## 📋 Spell Comparison

| Spell | Input | Output | Best For |
|-------|--------|---------|----------|
| audio_cleanse | MP3, MP4 | MP3, MP4 | Podcasts, videos, noisy audio |
| dispel_background | PNG, JPG, WEBP | PNG | Sprites, assets, UI elements |

## 🎯 Common Use Cases

### Clean a podcast:
```bash
python spells/audio_cleanse.py --input podcast.mp3 --loudness -16
```

### Clean a video:
```bash
python spells/audio_cleanse.py --input video.mp4 --output clean.mp4
```

### Remove background from sprite:
```bash
python spells/dispel_background.py --input sprite.png
```

### Process portrait with better edges:
```bash
python spells/dispel_background.py --input portrait.png \
  --model u2net_human_seg
```

## 📚 Quest Guides

Full documentation for each spell:
- [quests/audio_cleanse.md](quests/audio_cleanse.md)
- [quests/dispel_background.md](quests/dispel_background.md)

## 🆘 Help

```bash
# Get help for any spell
python spells/audio_cleanse.py --help
python spells/dispel_background.py --help
```

## 🔧 Troubleshooting

**Spell not found:**
```bash
# Check spell exists
ls spells/audio_cleanse.py
```

**Permission denied:**
```bash
# Make executable
chmod +x spells/audio_cleanse.py
```

**Dependencies missing:**
```bash
# Install all requirements
pip install -r requirements.txt
```

## 📖 More Documentation

- [README.md](README.md) - Complete user guide
- [AI_CRAFT_SPELLBOOK.md](AI_CRAFT_SPELLBOOK.md) - Agent instructions
