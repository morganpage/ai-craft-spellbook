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

## Split Artifact Examples

### Basic Split
```
User: Split landscape.png into two halves
Claude: I'll split landscape.png into two equal halves based on orientation.
[Executes: python spells/split_artifact.py --input landscape.png]
Output: Artifact split successfully!
Original size: 1024x512
Split direction: horizontal
Left half: dungeon_cache/landscape_left.png (512x512)
Right half: dungeon_cache/landscape_right.png (512x512)
```

### Vertical Split
```
User: Divide portrait.jpg into top and bottom
Claude: I'll split portrait.jpg vertically into top and bottom halves.
[Executes: python spells/split_artifact.py --input portrait.jpg]
Output: Artifact split successfully!
Original size: 512x1024
Split direction: vertical
Top half: dungeon_cache/portrait_top.png (512x512)
Bottom half: dungeon_cache/portrait_bottom.png (512x512)
```

### Custom Output Directory
```
User: Split sprite.png and save to parts/ folder
Claude: I'll split sprite.png and save the halves to parts/.
[Executes: python spells/split_artifact.py --input sprite.png --output-dir parts/]
Output: Artifact split successfully!
Left half: parts/sprite_left.png (256x256)
Right half: parts/sprite_right.png (256x256)
```

### Different Format
```
User: Split image and save as JPEG
Claude: I'll split the image and save halves as JPEG format.
[Executes: python spells/split_artifact.py --input image.png --format jpg]
Output: Artifact split successfully!
Format: JPEG
Left half: dungeon_cache/image_left.jpg
Right half: dungeon_cache/image_right.jpg
```

### Square Image
```
User: Split square.png into halves
Claude: I'll split square.png horizontally (default for square images).
[Executes: python spells/split_artifact.py --input square.png]
Output: Artifact split successfully!
Original size: 512x512 (square)
Split direction: horizontal
Left half: dungeon_cache/square_left.png (256x512)
Right half: dungeon_cache/square_right.png (256x512)
```

## Resize Artifact Examples

### Basic Resize
```
User: Resize character.png to 512x512
Claude: I'll transmute character.png to 512x512 dimensions.
[Executes: python spells/resize_artifact.py --input character.png --width 512 --height 512]
Output: Transmutation completed successfully!
Original dimensions: 1024x1024
New dimensions: 512x512
Method: fit
Artifact: dungeon_cache/character_resized.png
```

### Scale by Percentage
```
User: Scale down sprite.png by 50%
Claude: I'll reduce sprite.png to 50% of its original size.
[Executes: python spells/resize_artifact.py --input sprite.png --scale 50]
Output: Transmutation completed successfully!
Original dimensions: 256x256
New dimensions: 128x128
Method: scale
Scale factor: 50.0%
```

### Fit Within Bounds
```
User: Resize landscape.jpg to fit within 1920x1080
Claude: I'll resize landscape.jpg to fit within 1920x1080 while maintaining aspect ratio.
[Executes: python spells/resize_artifact.py --input landscape.jpg --width 1920 --height 1080 --fit]
Output: Transmutation completed successfully!
Original dimensions: 3840x2160
New dimensions: 1920x1080
Method: fit
Artifact: dungeon_cache/landscape_resized.jpg
```

### Create Thumbnail
```
User: Create 150x150 thumbnail from photo.png
Claude: I'll create a 150x150 thumbnail from photo.png using fast resampling.
[Executes: python spells/resize_artifact.py --input photo.png --width 150 --height 150 --fit --resampling bilinear]
Output: Transmutation completed successfully!
Original dimensions: 2400x1600
New dimensions: 150x100
Method: fit
Artifact: dungeon_cache/photo_resized.png
```

### Resize Width Only
```
User: Resize icon.png to width 256
Claude: I'll resize icon.png to width 256, calculating height to maintain aspect ratio.
[Executes: python spells/resize_artifact.py --input icon.png --width 256]
Output: Transmutation completed successfully!
Original dimensions: 512x512
New dimensions: 256x256
Method: width
```

### Cover Exact Bounds (May Crop)
```
User: Resize photo.jpg to cover 800x600 exactly
Claude: I'll resize photo.jpg to cover 800x600 exactly, cropping if necessary.
[Executes: python spells/resize_artifact.py --input photo.jpg --width 800 --height 600 --cover]
Output: Transmutation completed successfully!
Original dimensions: 1920x1080
New dimensions: 800x600
Method: cover (center cropped)
Artifact: dungeon_cache/photo_resized.jpg
```

## Image Obscuration Examples

### Basic Blur
```
User: Blur photo.jpg
Claude: I'll obscure photo.jpg with a Gaussian blur ritual.
[Executes: python spells/obscure_artifact.py --input photo.jpg]
Output: Obscuration ritual completed successfully!
Artifact: dungeon_cache/photo_obscured.jpg
Ritual: gaussian
Obscuration power: 5.0
Iterations: 1
```

### Heavy Blur
```
User: Apply heavy blur to sensitive.png
Claude: I'll apply strong obscuration to sensitive.png for privacy.
[Executes: python spells/obscure_artifact.py --input sensitive.png --radius 20]
Output: Obscuration ritual completed successfully!
Artifact: dungeon_cache/sensitive_obscured.png
Obscuration power: 20.0
Ritual: gaussian
```

### Subtle Blur
```
User: Add subtle blur to portrait.png
Claude: I'll apply a soft blur effect to portrait.png.
[Executes: python spells/obscure_artifact.py --input portrait.png --radius 2]
Output: Obscuration ritual completed successfully!
Artifact: dungeon_cache/portrait_obscured.png
Obscuration power: 2.0
Effect: Subtle softening
```

### Box Blur (Fast)
```
User: Blur sprite.png with box filter
Claude: I'll use the box enchantment for fast processing.
[Executes: python spells/obscure_artifact.py --input sprite.png --blur-type box --radius 10]
Output: Obscuration ritual completed successfully!
Artifact: dungeon_cache/sprite_obscured.png
Ritual: box (fast)
Obscuration power: 10.0
```

### Multiple Iterations
```
User: Blur background.jpg heavily with multiple passes
Claude: I'll apply multiple blur iterations for strong obscuration.
[Executes: python spells/obscure_artifact.py --input background.jpg --radius 5 --iterations 3]
Output: Obscuration ritual completed successfully!
Artifact: dungeon_cache/background_obscured.jpg
Obscuration power: 5.0
Iterations: 3
Effect: Very strong blur
```

## Animate Artifact Examples

### Basic Animation
```
User: Create gif from frames/
Claude: I'll weave those magical panels into an animated scroll.
[Executes: python spells/animate_artifact.py --input frames/]
Output: Animation ritual completed successfully!
Animated scroll: frames_animated.gif
Frame count: 24
Frame rate: 10 fps
Duration: 2.4s
Incantation binding: Eternal
```

### Custom Frame Rate
```
User: Make animation from sprite_frames/ with 200ms duration
Claude: I'll animate sprite_frames/ with 200ms temporal power per panel.
[Executes: python spells/animate_artifact.py --input sprite_frames/ --duration 200]
Output: Animation ritual completed successfully!
Animated scroll: sprite_frames_animated.gif
Frame count: 12
Frame rate: 5 fps
Duration: 2.4s
```

### Finite Loop
```
User: Generate gif from panels/ with 3 loops
Claude: I'll create an animation from panels/ that plays 3 times.
[Executes: python spells/animate_artifact.py --input panels/ --loop 3]
Output: Animation ritual completed successfully!
Animated scroll: panels_animated.gif
Frame count: 8
Frame rate: 10 fps
Incantation binding: 3 times
```

### Resize and Animate
```
User: Animate frames/ and resize to 256x256
Claude: I'll animate frames/ and apply dimensional harmonization to 256x256.
[Executes: python spells/animate_artifact.py --input frames/ --width 256 --height 256]
Output: Animation ritual completed successfully!
Animated scroll: frames_animated.gif
Original dimensions: 512x512
Final dimensions: 256x256
Frame count: 16
```

### Optimized Animation
```
User: Create optimized gif from rendered_frames/
Claude: I'll create an optimized animated scroll from rendered_frames/.
[Executes: python spells/animate_artifact.py --input rendered_frames/ --optimize]
Output: Animation ritual completed successfully!
Animated scroll: rendered_frames_animated.gif
Optimization: Enabled
Compression ratio: 15.2%
Size: 12.5 MB → 1.9 MB
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
- "save as JPEG" → `--format jpg`
- "output to splits/" → `--output-dir splits/`
- "scale by 50%" → `--scale 50`
- "fit within bounds" → `--fit`
- "cover exact bounds" → `--cover`
- "use lanczos filter" → `--resampling lanczos`
- "blur with radius 10" → `--radius 10`
- "heavy blur" → `--radius 20` (or higher)
- "subtle blur" → `--radius 2` (or lower)
- "use box blur" → `--blur-type box`
- "multiple iterations" → `--iterations 3`
- "create gif" → `--input <directory>`
- "make animation" → `--input <directory>`
- "frame rate" → `--duration <milliseconds>`
- "fps" → derived from duration (1000/duration)
- "loop" → `--loop <count>`
- "infinite loop" → `--loop 0` (default)
- "resize animation" → `--width <pixels> --height <pixels>`
- "no optimization" → `--no-optimize`

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
User: Perfect! Now can you split this landscape image into two sprites?
Claude: I'll split the landscape image into two halves based on orientation.
[Executes: python spells/split_artifact.py --input landscape.png]
Output: Artifact split successfully!
Original size: 1024x512
Split direction: horizontal
Left half: dungeon_cache/landscape_left.png (512x512)
Right half: dungeon_cache/landscape_right.png (512x512)
User: Excellent! Now can you resize this character.png to 256x256 for a thumbnail?
Claude: I'll transmute character.png to 256x256 dimensions.
[Executes: python spells/resize_artifact.py --input character.png --width 256 --height 256]
Output: Transmutation completed successfully!
Original dimensions: 1024x1024
New dimensions: 256x256
Method: fit
Artifact: dungeon_cache/character_resized.png
User: Perfect! Now can you blur this background image for privacy?
Claude: I'll obscure the background image with a Gaussian blur ritual.
[Executes: python spells/obscure_artifact.py --input background.jpg --radius 15]
Output: Obscuration ritual completed successfully!
Artifact: dungeon_cache/background_obscured.jpg
Ritual: gaussian
Obscuration power: 15.0
User: Perfect! Now can you create an animated GIF from these frames in walk_cycle/?
Claude: I'll weave those magical panels into an animated scroll.
[Executes: python spells/animate_artifact.py --input walk_cycle/]
Output: Animation ritual completed successfully!
Animated scroll: walk_cycle_animated.gif
Frame count: 24
Frame rate: 10 fps
Duration: 2.4s
Incantation binding: Eternal
User: Excellent, thank you!
```

See [README.md](README.md) for getting started and [QUICKSTART.md](QUICKSTART.md) for command reference.
