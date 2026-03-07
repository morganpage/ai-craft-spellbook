# Spell Invocation Guide for AI Assistants
*Generated: 2026-03-07 12:27:16*

This guide helps AI assistants recognize when to invoke spells in the AI Craft Spellbook framework.
## Quick Reference Table
| Spell | Primary Keywords | Supported Formats | Command Pattern |
|-------|-----------------|-------------------|----------------|
| audio_cleanse | cleanse, purify, clean... | mp3, wav, m4a, aac... | `python spells/audio_cleanse.py --input <file> [options]` |
| dispel_background | remove background, dispel background, remove bg... | jpg, jpeg, png, webp... | `python spells/dispel_background.py --input <file> [options]` |
| split_artifact | split, divide, separate... | png, jpg, jpeg, webp... | `python spells/split_artifact.py --input <file> [options]` |

## Decision Tree: When to Use Spells vs Bash Commands
```
User Request
    │
    ├── Contains spell keyword?
    │   ├── Yes → Check file type matches spell support?
    │   │   ├── Yes → Check if quest exists in quests/?
    │   │   │   ├── Yes → INVOKE THE SPELL
    │   │   │   └── No  → Use bash commands
    │   │   └── No  → Use bash commands
    │
    ├── File operation (copy, move, list)?
    │   └── Yes → Use Bash tool
    │
    ├── Git operation?
    │   └── Yes → Use Bash tool
    │
    └── Other operation?
        └── Use appropriate tool (Read, Glob, Grep, Bash)
```

## Keyword Detection Rules
### Primary Keywords (Must Match)
| Spell | Keywords |
|-------|----------|
| audio_cleanse | `cleanse`, `purify`, `clean`, `purify audio`, `audio cleansing` |
| dispel_background | `remove background`, `dispel background`, `remove bg`, `transparent background`, `background removal` |
| split_artifact | `split`, `divide`, `separate`, `halves` |

## Spell-by-Spell Invocation Guide

### audio_cleanse

**Description:** Purify audio artifacts by removing impurities, banishing void moments, and balancing magical loudness

**Primary Keywords:** cleanse, purify, clean, purify audio, audio cleansing

**Secondary Keywords:**
- *content_type:* podcast, youtube, spotify, broadcast, video
- *noise_level:* noisy, heavy noise, light noise, aggressive
- *feature_toggles:* don't remove silence, keep pauses, skip noise reduction, only normalize

**Supported Formats:** mp3, wav, m4a, aac, ogg, flac, wma, mp4, avi, mov, mkv, webm, flv, wmv

**Common Use Cases:**
- Podcast recordings and episodes
- Video audio tracks and content
- Content distribution preparation
- Noisy environments and background noise
- Broadcast quality audio production

**Natural Language Examples:**
- "cleanse audio in podcast.mp3"
- "purify my video.mp4"
- "clean audio with heavy noise reduction"
- "cleanse podcast with loudness -16"
- "purify youtube video audio"
- "cleanse without removing silence"

**CLI Pattern:** `python spells/audio_cleanse.py --input <file> [options]`

**CLI Parameters:**
- `--input`: Path to magical media artifact (required)
- `--output`: Path to purified artifact (optional)
- `--silence-threshold`: dB threshold for void detection (default: -40)
- `--silence-duration`: Minimum void duration in seconds to banish (default: 0.5)
- `--loudness`: Target magical loudness in LUFS (default: -14)
- `--no-silence-removal`: Skip void banishment
- `--no-normalize`: Skip magical energy balancing
- `--no-noise-reduction`: Skip purification magic (enabled by default)
- `--noise-strength`: Purification strength: light, medium, heavy (default: light)
- `--fade-duration`: Magical fade in/out duration at segment boundaries (default: 0.01)
- `--silence-padding`: Magical buffer to add at segment boundaries (default: 0.3)
- `--keep-temp`: Keep intermediate segment artifacts for debugging
- `--log-level`: Logging level: DEBUG, INFO, WARNING, ERROR (default: INFO)
- `--log-file`: Path to log file (optional)

**Output Naming:** `<name>_purified.<ext>`

---

### dispel_background

**Description:** Remove backgrounds from images using arcane vision and machine learning

**Primary Keywords:** remove background, dispel background, remove bg, transparent background, background removal

**Secondary Keywords:**
- *model_type:* human model, portrait, human seg, clothing, fashion, fast, quick, lightweight, silhouette, icon
- *quality:* cleaner edges, better edges, high quality, alpha matting
- *processing:* batch, batch process, multiple files

**Supported Formats:** jpg, jpeg, png, webp, bmp, tiff, gif

**Common Use Cases:**
- Character portraits and sprites
- Product photography and ecommerce
- Icon and logo design
- Fashion and clothing images
- Social media content creation

**Natural Language Examples:**
- "remove background from character.png"
- "dispel background on sprite.png with human model"
- "remove bg from photo.jpg quickly"
- "dispel background with cleaner edges"
- "batch process all images in sprites/"
- "use human model for portrait.png"

**CLI Pattern:** `python spells/dispel_background.py --input <file> [options]`

**CLI Parameters:**
- `--input`: Path to magical image artifact (required)
- `--output`: Path to dispelled artifact (optional)
- `--output-dir`: Directory for dispelled artifacts in batch mode
- `--model`: Arcane crystal to use (u2net, u2netp, u2net_human_seg, u2net_cloth_seg, silueta)
- `--alpha-matting`: Apply alpha matting for cleaner edges (slower)
- `--alpha-matting-foreground-threshold`: Foreground threshold for alpha matting (default: 240)
- `--alpha-matting-background-threshold`: Background threshold for alpha matting (default: 10)
- `--alpha-matting-erode-size`: Erosion size for alpha matting (default: 10)
- `--batch`: Batch process multiple files using glob pattern
- `--log-level`: Logging level: DEBUG, INFO, WARNING, ERROR (default: INFO)
- `--log-file`: Path to log file (optional)

**Output Naming:** `<name>_dispelled.png`

---

### split_artifact

**Description:** Divide images into two equal halves based on orientation

**Primary Keywords:** split, divide, separate, halves

**Secondary Keywords:**
- *orientation:* landscape, wide, portrait, tall, vertical, square
- *direction:* left and right, top and bottom
- *output_format:* JPEG, JPG, PNG, WEBP
- *location:* save to, output to, folder

**Supported Formats:** png, jpg, jpeg, webp, gif, bmp, tiff

**Common Use Cases:**
- Separating wide sprite sheets into distinct pieces
- Splitting character portraits into top/bottom sections
- Dividing large UI elements into manageable components
- Preparing assets for game engine import
- Creating dual-frame sprites from single source

**Natural Language Examples:**
- "split landscape.png"
- "divide portrait.jpg into top and bottom"
- "separate sprite.png into two halves"
- "split square_512.png"
- "divide wide image into left and right"
- "split and save as JPEG"

**CLI Pattern:** `python spells/split_artifact.py --input <file> [options]`

**CLI Parameters:**
- `--input`: Magical image artifact path (required)
- `--output-dir`: Sanctum for split artifacts (optional, default: same as input)
- `--format`: Magical format for output: png, jpg, webp, gif, bmp, tiff (default: png)
- `--log-level`: Logging level: DEBUG, INFO, WARNING, ERROR (default: INFO)
- `--log-file`: Path to log file (optional)

**Output Naming:** `<name>_left/right/top/bottom.<ext>`

---

## Natural Language to CLI Parameter Extraction

### audio_cleanse

| Natural Language | CLI Flag |
|------------------|----------|
| `with heavy noise reduction` | `--noise-strength heavy` |
| `for podcast` | `--loudness -16` |
| `for YouTube` | `--loudness -14` |
| `for broadcast` | `--loudness -23` |
| `don't remove silence` | `--no-silence-removal` |
| `keep pauses` | `--no-silence-removal` |
| `skip noise reduction` | `--no-noise-reduction` |
| `only normalize` | `--no-silence-removal --no-noise-reduction` |

### dispel_background

| Natural Language | CLI Flag |
|------------------|----------|
| `human model` / `portrait` | `--model u2net_human_seg` |
| `clothing` / `fashion` | `--model u2net_cloth_seg` |
| `fast` / `quick` / `lightweight` | `--model u2netp` |
| `silhouette` / `icon` | `--model silueta` |
| `cleaner edges` / `better edges` | `--alpha-matting` |
| `high quality` | `use u2net (default)` |
| `batch process` | `--batch --input "*.png"` |

### split_artifact

| Natural Language | CLI Flag |
|------------------|----------|
| `JPEG` / `JPG` | `--format jpg` |
| `PNG` | `--format png (default)` |
| `WEBP` | `--format webp` |
| `save to folder/` | `--output-dir folder/` |
| `landscape` / `wide` | `horizontal split (auto)` |
| `portrait` / `tall` | `vertical split (auto)` |

## File Type Validation Matrix

| Spell | Supported Extensions |
|-------|-------------------|
| audio_cleanse | .mp3, .wav, .m4a, .aac, .ogg, .flac, .wma, .mp4, .avi, .mov, .mkv, .webm, .flv, .wmv |
| dispel_background | .jpg, .jpeg, .png, .webp, .bmp, .tiff, .gif |
| split_artifact | .png, .jpg, .jpeg, .webp, .gif, .bmp, .tiff |

## Output Naming Conventions

All spells follow consistent output naming:

| Spell | Output Pattern | Example |
|-------|---------------|---------|
| audio_cleanse | `<name>_purified.<ext>` | `artifact_purified.png` |
| dispel_background | `<name>_dispelled.png` | `artifact_dispelled.png` |
| split_artifact | `<name>_left/right/top/bottom.<ext>` | `artifact_left/right/top/bottom.png` |

## Troubleshooting Spell Invocation

| Issue | Diagnosis | Solution |
|-------|------------|----------|
| Spell not recognized | Check spelling and verify spell exists in spells/ directory | Refer to Quick Reference Table |
| Metadata missing | Add SPELL_METADATA dict to spell file | See templates/new_spell.py.template |
| Wrong spell invoked | Verify primary keyword matches spell intent | Check file type against supported formats |
| File type not supported | Use different format or bash commands | Check File Type Validation Matrix |
| Parameters not extracted | Use explicit CLI flags | Spell keywords may not match natural language |

---
*This guide is automatically generated from SPELL_METADATA in each spell. Run `python tools/update_spell_docs.py` to update.*
