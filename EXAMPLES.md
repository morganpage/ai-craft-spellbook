# Natural Language Command Examples

Complete examples of natural language requests and what they do.

> **Start here:** [START_HERE.md](START_HERE.md) shows you how to begin in 3 steps!

## Audio Cleansing Examples

### Basic Cleansing
```
User: Cleanse audio in podcast.mp3
Claude: I'll cleanse the audio in podcast.mp3 for you.
[Executes: python spells/audio_cleanse.py --input podcast.mp3]
Output: Ritual completed successfully!
Artifact: dungeon_cache/podcast_purified.mp3
Metadata: dungeon_cache/podcast_purification_metadata.json
```

### Custom Settings
```
User: Cleanse audio with medium noise reduction and -16 LUFS
Claude: I'll cleanse with medium purification and podcast loudness settings.
[Executes: python spells/audio_cleanse.py --input podcast.mp3 --noise-strength medium --loudness -16]
Output: Ritual completed successfully!
Artifact: dungeon_cache/podcast_purified.mp3
Noise reduction: medium
Loudness target: -16 LUFS
```

### Video Files
```
User: Purify the audio in my_video.mp4
Claude: I'll cleanse the audio in my_video.mp4.
[Executes: python spells/audio_cleanse.py --input my_video.mp4]
Output: Ritual completed successfully!
Artifact: dungeon_cache/my_video_purified.mp4
Video stream: Preserved
Audio stream: Cleansed
```

### Without Silence Removal
```
User: Cleanse the audio but don't remove silence
Claude: I'll cleanse the audio while preserving all moments.
[Executes: python spells/audio_cleanse.py --input interview.mp3 --no-silence-removal]
Output: Ritual completed successfully!
Silence removal: Skipped
Noise reduction: Applied
Normalization: Applied
```

## Background Dispel Examples

### Basic Removal
```
User: Remove background from character.png
Claude: I'll dispel the background from character.png.
[Executes: python spells/dispel_background.py --input character.png]
Output: Background dispelled successfully!
Artifact: dungeon_cache/character_dispelled.png
Metadata: dungeon_cache/character_dispel_metadata.json
```

### Specific Model
```
User: Use the human model to dispel background from portrait.png
Claude: I'll use the u2net_human_seg crystal for portrait.png.
[Executes: python spells/dispel_background.py --input portrait.png --model u2net_human_seg]
Output: Background dispelled successfully!
Model: u2net_human_seg (specialized for human subjects)
```

### Custom Output
```
User: Dispel background from sprite.png and save as sprite_clean.png
Claude: I'll dispel the background and save to sprite_clean.png.
[Executes: python spells/dispel_background.py --input sprite.png --output sprite_clean.png]
Output: Background dispelled successfully!
Artifact: sprite_clean.png
```

### Fast Processing
```
User: Remove background quickly from icon.png
Claude: I'll use the lightweight u2netp crystal for fast processing.
[Executes: python spells/dispel_background.py --input icon.png --model u2netp]
Output: Background dispelled successfully!
Model: u2netp (lightweight, faster)
```

## Complex Requests

### Multi-Step Processing
```
User: I want to process all images in my sprites/ folder and remove their backgrounds
Claude: I'll cast the dispel background hex on all images in sprites/.
[Executes multiple spells]
Processing: sprites/warrior_1.png...
Processing: sprites/warrior_2.png...
Processing: sprites/warrior_3.png...
Output: Processed 12 sprites successfully!
Artifacts: sprites/warrior_*_dispelled.png
```

### Specific Settings Combination
```
User: Cleanse the interview recording, remove silence aggressively, and use heavy noise reduction
Claude: I'll cleanse with aggressive silence removal and heavy purification.
[Executes: python spells/audio_cleanse.py --input interview.mp3 --silence-threshold -30 --silence-duration 0.3 --noise-strength heavy]
Output: Ritual completed successfully!
Silence threshold: -30 dB
Silence duration: 0.3s
Noise reduction: heavy
```

### Batch with Custom Output
```
User: Remove backgrounds from all PNGs in assets/ and save to cleaned/
Claude: I'll dispel backgrounds from assets/*.png and save to cleaned/.
[Executes batch processing]
Processing: assets/character.png → cleaned/character_dispelled.png
Processing: assets/monster.png → cleaned/monster_dispelled.png
Processing: assets/weapon.png → cleaned/weapon_dispelled.png
Output: Processed 5 artifacts successfully!
```

## What Claude Code Does Behind the Scenes

1. **Parses your request** - Identifies the spell and parameters needed
2. **Validates** - Checks that files exist and parameters are correct
3. **Explains** - Tells you what it's about to do before executing
4. **Executes** - Runs the Python spell with the proper arguments
5. **Reports** - Shows you success or any spell fumbles
6. **Saves results** - Tells you exactly where your treasures are located

## Common Patterns

### File References
- "Cleanse podcast.mp3" → `--input podcast.mp3`
- "Remove background from images/character.png" → `--input images/character.png`

### Settings Requests
- "with heavy noise reduction" → `--noise-strength heavy`
- "use -16 LUFS" → `--loudness -16`
- "with human model" → `--model u2net_human_seg`

### Output Requests
- "save as clean.mp3" → `--output clean.mp3`
- "output to results/" → `--output results/purified.mp3`

### Modifiers
- "don't remove silence" → `--no-silence-removal`
- "skip noise reduction" → `--no-noise-reduction`
- "only normalize" → `--no-silence-removal --no-noise-reduction`

## Tips for Best Results

1. **Be specific with file paths** - Include full path if file isn't in current directory
2. **Mention settings clearly** - "medium noise reduction" is better than "better quality"
3. **Refer to models by name** - "human model" or "u2net_human_seg" both work
4. **Let Claude explain** - Claude will show you the exact command before running
5. **Check the output** - Claude will tell you where results are saved

## Example Session

```
[User starts Claude Code]
User: I have a noisy podcast recording that needs cleaning
Claude: I can help with that! What's the file name?
User: It's called my_podcast.mp3
Claude: I'll cleanse the audio in my_podcast.mp3 for you.
[Executes: python spells/audio_cleanse.py --input my_podcast.mp3]
Output: Ritual completed successfully!
Artifact: dungeon_cache/my_podcast_purified.mp3
Duration reduced by: 8.3 minutes (12.4%)
Noise reduction: light
User: Great! Now can you remove the background from this portrait.png?
Claude: I'll dispel the background from portrait.png.
[Executes: python spells/dispel_background.py --input portrait.png --model u2net_human_seg]
Output: Background dispelled successfully!
Artifact: dungeon_cache/portrait_dispelled.png
Model: u2net_human_seg
User: Perfect!
```

See [README.md](README.md) for getting started and [QUICKSTART.md](QUICKSTART.md) for command reference.
