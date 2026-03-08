# Animate Artifact Ritual

## Quest Objective

Weave magical image panels from a panel archive into a single animated scroll (GIF) that captures chronomantic essence. This incantation combines multiple sequential panels into a unified animated artifact with precise temporal power, configurable incantation bindings, and optional dimensional harmonization for consistent frame sizing.

## Context

This ritual is useful for:
- Creating game sprite animations from sequential frame renders
- Generating UI animation loops for interface feedback and loading states
- Building demonstration GIFs for tutorials and documentation
- Previewing game asset animations during development
- Creating animated icons and indicators
- Converting sprite sheet frames into standalone animated artifacts

## Required Reagents

### Panel Archive (Input Directory)
- **Path**: Path to directory containing magical image panels
- **Format**: Any image format supported by the Arcane Arts (PNG, JPEG, WEBP, BMP, TIFF)
- **Minimum panels**: 2 or more image files
- **Maximum total size**: 500MB for all panels combined
- **Frame ordering**: Alphabetical by filename (use numbered prefixes for control)
- **Requirements**: Valid magical images that can be read by the Arcane Pillar (PIL)

### Treasure Options
- **Animated scroll path**: Path to save the animated scroll (default: `<dirname>_animated.gif`)
- **Temporal power**: Duration per panel in milliseconds (10-5000ms, default: 100ms)
- **Incantation binding**: Eternal loop (0) or finite cycle count (default: 0 = eternal)
- **Arcane compression**: Optimize file size (default: True)
- **Dimensional harmonization**: Resize all panels to consistent dimensions

## Spells to Cast

### spells/animate_artifact.py
Weave magical image panels into an animated scroll.

**Reagents:**
- `--input`: Path to panel archive directory (required)
- `--output`: Path to animated scroll (optional)
- `--duration`: Temporal power per panel in milliseconds (short: -d, default: 100)
- `--loop`: Eternal binding (0) or finite incantation count (default: 0)
- `--optimize`: Apply arcane compression (default: True)
- `--no-optimize`: Disable arcane compression
- `--width`: Target width for dimensional harmonization (short: -w)
- `--height`: Target height for dimensional harmonization
- `--no-maintain-aspect`: Don't preserve aspect ratio during harmonization

**Incantation:**
```bash
# Basic animation with default settings (10fps, infinite loop)
python spells/animate_artifact.py --input frames/

# Custom frame rate (20fps = 50ms per frame)
python spells/animate_artifact.py --input sprite_frames/ --duration 50

# Finite loop (play 3 times then stop)
python spells/animate_artifact.py --input frames/ --loop 3

# Resize during animation to 256x256
python spells/animate_artifact.py --input frames/ --width 256 --height 256

# Disable optimization for faster processing
python spells/animate_artifact.py --input frames/ --no-optimize

# Custom output path
python spells/animate_artifact.py --input frames/ --output animations/my_animation.gif

# Slow animation (5fps = 200ms per frame)
python spells/animate_artifact.py --input frames/ --duration 200

# Fast animation (20fps = 50ms per frame)
python spells/animate_artifact.py --input frames/ --duration 50
```

**Treasure:**
- `<dirname>_animated.gif` - Animated scroll with chronomantic essence
- `<dirname>_animated_metadata.json` - Arcane knowledge of ritual parameters and animation metrics

## Expected Magical Treasures

### Animated Scroll Artifact
- **File**: GIF format animated image
- **Content**: All panels woven into sequential animation
- **Frame rate**: Controlled by temporal power setting
- **Loop behavior**: Eternal or finite as specified
- **Optimization**: Compression applied for efficient file size

### Arcane Knowledge
- **File**: JSON format ritual record
- **Contents**:
  - Input panel archive path
  - Output animated scroll path
  - Temporal power (duration per panel)
  - Incantation binding (loop count)
  - Frame count and dimensions
  - Frame rate and total duration
  - File sizes and compression ratio
  - Ritual duration and performance metrics

### Arcane Knowledge Example
```json
{
  "spell_name": "animate_artifact",
  "version": "1.0.0",
  "cast_at": "2024-02-19T12:00:00.000Z",
  "input_dir": "frames/",
  "output_path": "frames_animated.gif",
  "settings": {
    "duration": 100,
    "loop": 0,
    "optimize": true,
    "width": null,
    "height": null,
    "maintain_aspect": true
  },
  "animation": {
    "frame_count": 24,
    "original_dimensions": {
      "width": 512,
      "height": 512
    },
    "final_dimensions": {
      "width": 512,
      "height": 512
    },
    "frame_rate_fps": 10.0,
    "duration_seconds": 2.4,
    "is_infinite_loop": true,
    "loop_count": "infinite"
  },
  "panels": {
    "count": 24,
    "files": ["frame_001.png", "frame_002.png", "..."]
  },
  "input_info": {
    "total_size_bytes": 12582912,
    "panel_count": 24
  },
  "output_info": {
    "size_bytes": 2097152,
    "format": ".gif"
  },
  "performance": {
    "spell_name": "animate_artifact",
    "duration_seconds": 3.45,
    "input_size_bytes": 12582912,
    "output_size_bytes": 2097152
  }
}
```

## Chronomantic Ritual Details

### Temporal Power (Frame Duration)

The temporal power setting controls how long each panel displays in the animated scroll:

| Duration (ms) | Frame Rate | Best For |
|---------------|------------|----------|
| 50ms | 20 fps | Fast motion, game sprites |
| 100ms | 10 fps | Standard animation (default) |
| 167ms | 6 fps | Slower pacing |
| 200ms | 5 fps | Slow demonstrations |
| 500ms | 2 fps | Very slow transitions |

**Formula**: `Frame Rate (fps) = 1000 / Duration (ms)`

### Incantation Binding (Loop Control)

Control how many times the animated scroll plays:

- **0 (default)**: Eternal binding - animation loops forever
- **1**: Single playback - animation plays once and stops
- **3+**: Finite cycles - animation plays specified number of times

### Arcane Compression (Optimization)

Optimization reduces file size by analyzing frame differences and compressing efficiently:

- **Enabled (default)**: Smaller file size, slower processing
- **Disabled**: Larger file size, faster processing

Recommendation: Keep enabled for most use cases. Disable only if processing is too slow.

### Dimensional Harmonization (Resizing)

When panels have varying dimensions or specific target dimensions are needed:

- **Width only**: Height calculated to maintain aspect ratio
- **Height only**: Width calculated to maintain aspect ratio
- **Both width and height**: By default, fits within bounds maintaining aspect ratio
- **Both with --no-maintain-aspect**: Exact dimensions, may distort panels

## Ritual Examples

### Example 1: Basic Game Sprite Animation

```bash
# Animate character walk cycle frames (24 frames at 12fps)
python spells/animate_artifact.py \
  --input game_assets/walk_cycle_frames/ \
  --duration 83
```

**Result**: `game_assets/walk_cycle_frames_animated.gif` - 2-second walk cycle at 12fps, eternal loop

### Example 2: Loading Indicator Animation

```bash
# Create fast loading spinner (8 frames at 20fps)
python spells/animate_artifact.py \
  --input ui_elements/loading_spinner/ \
  --duration 50 \
  --width 64 \
  --height 64
```

**Result**: `ui_elements/loading_spinner_animated.gif` - 0.4-second loading animation at 20fps, 64x64 pixels

### Example 3: Tutorial Demonstration GIF

```bash
# Create demonstration that plays 3 times then stops
python spells/animate_artifact.py \
  --input tutorial_screenshots/ \
  --duration 500 \
  --loop 3 \
  --width 800 \
  --height 600
```

**Result**: `tutorial_screenshots_animated.gif` - Slower demonstration (2fps) that plays 3 times, resized to 800x600

### Example 4: Preview Animation (No Optimization)

```bash
# Quick preview during development (faster processing)
python spells/animate_artifact.py \
  --input rendered_frames/ \
  --duration 100 \
  --no-optimize
```

**Result**: `rendered_frames_animated.gif` - Quick preview with larger file size but faster processing

### Example 5: Character Animation with Custom Output

```bash
# Animate attack animation and save to specific location
python spells/animate_artifact.py \
  --input character_frames/attack_01/ \
  --duration 67 \
  --output animations/attack_attack_01.gif
```

**Result**: `animations/attack_attack_01.gif` - Character attack animation at 15fps in custom location

### Example 6: Variable Dimension Panels

```bash
# Harmonize panels from different sources to consistent size
python spells/animate_artifact.py \
  --input mixed_size_panels/ \
  --width 256 \
  --height 256 \
  --duration 100
```

**Result**: `mixed_size_panels_animated.gif` - All panels harmonized to 256x256 with aspect ratio preserved

### Example 7: Icon Animation Loop

```bash
# Create small icon animation that loops 5 times
python spells/animate_artifact.py \
  --input icon_frames/ \
  --duration 200 \
  --width 32 \
  --height 32 \
  --loop 5
```

**Result**: `icon_frames_animated.gif` - 32x32 icon animation at 5fps, plays 5 times

### Example 8: High-Fidelity Animation

```bash
# Smooth high-frame-rate animation for showcase
python spells/animate_artifact.py \
  --input showcase_frames/ \
  --duration 40 \
  --width 1920 \
  --height 1080
```

**Result**: `showcase_frames_animated.gif` - Smooth 25fps animation at 1080p resolution

## Arcane Complications and Constraints

### Minimum Panel Count
- **Minimum**: 2 panels required for animation
- **Spell fumble**: "Animation requires at least 2 magical panels"
- **Recovery**: Add more image files to the panel archive

### Panel Archive Size
- **Maximum**: 500MB total for all panels combined
- **Spell fumble**: "Panel archive too large"
- **Recovery**: Process smaller batches or reduce individual panel file sizes

### Temporal Power Limits
- **Range**: 10ms to 5000ms per panel
- **Spell fumble**: "Temporal power must be between 10ms and 5000ms"
- **Recovery**: Use value within valid range (10-5000)

### Incantation Count Validation
- **Valid values**: 0 (eternal) or positive integers
- **Spell fumble**: "Incantation count must be 0 or positive"
- **Recovery**: Use 0 for eternal loop or positive number for finite cycles

### RGBA to RGB Conversion
- **Issue**: GIF format doesn't properly support alpha channels
- **Handling**: Transparent pixels converted to white background
- **Note**: This is expected behavior, not a spell fumble

### Varying Panel Dimensions
- **Detection**: Panels with different sizes automatically trigger dimensional harmonization
- **Result**: All panels resized to match reference panel or target dimensions
- **Preservation**: Aspect ratio maintained by default

### Frame Ordering
- **Method**: Alphabetical sort by filename
- **Recommendation**: Use numbered prefixes (e.g., `frame_001.png`, `frame_002.png`)
- **Warning**: Random filenames may produce unexpected frame order

### Large Frame Counts
- **Consideration**: More frames = larger file size and longer processing
- **Optimization**: Enable compression (default) for better file size
- **Trade-off**: Compression increases processing time

## Spell Fumble Recovery

### Panel Archive Issues
| Spell Fumble | Recovery |
|--------------|----------|
| Panel archive not found | Check that the directory path is correct and exists |
| Path is not a directory | Provide a path to a directory, not a file |
| No magical panels found | Add supported image files (PNG, JPEG, WEBP, etc.) |
| Insufficient magical panels | Add at least 2 image files to the directory |

### Parameter Validation
| Spell Fumble | Recovery |
|--------------|----------|
| Temporal power out of range | Use value between 10ms (fast) and 5000ms (slow) |
| Invalid incantation count | Use 0 for eternal loop or positive number for finite |
| Invalid target dimensions | Use positive integer values for width/height |

### Processing Issues
| Spell Fumble | Recovery |
|--------------|----------|
| Failed to load magical panel | Check that files are valid images and not corrupted |
| Failed to weave animated scroll | Try reducing frame count, dimensions, or disable optimization |
| Cannot write to output path | Check write permissions and disk space |

### Optimization Issues
| Spell Fumble | Recovery |
|--------------|----------|
| Processing too slow | Disable optimization with --no-optimize flag |
| File size too large | Enable optimization (default) or reduce dimensions |
| Quality too low | Disable optimization or reduce frame count |

## Integration with Existing Quests

### With Resize Artifact
```bash
# 1. Resize all panels to consistent dimensions first
for frame in frames/*.png; do
  python spells/resize_artifact.py --input "$frame" --width 256 --height 256
done

# 2. Animate the resized panels
python spells/animate_artifact.py --input frames/ --duration 100
```

### With Dispel Background
```bash
# 1. Remove backgrounds from all panels
python spells/dispel_background.py --batch \
  --input "character_frames/*.png" \
  --output-dir character_frames_clean/

# 2. Animate the transparent panels
python spells/animate_artifact.py \
  --input character_frames_clean/ \
  --duration 67
```

### With Split Artifact
```bash
# 1. Split sprite sheet into individual frames
python spells/split_artifact.py \
  --input sprites/walk_cycle_sheet.png \
  --format png

# 2. Organize frames in directory (manual step)
# Move split frames to walk_cycle_frames/

# 3. Animate the frames
python spells/animate_artifact.py \
  --input walk_cycle_frames/ \
  --duration 83
```

### With Obscure Artifact
```bash
# 1. Apply blur to panels for special effect
for frame in frames/*.png; do
  python spells/obscure_artifact.py --input "$frame" --radius 2
done

# 2. Animate the blurred frames
python spells/animate_artifact.py \
  --input frames/ \
  --duration 100
```

## Success Criteria

Animation is successful when:
- Animated scroll file is created
- All panels appear in correct order
- Frame rate matches temporal power setting
- Loop behavior matches specification
- Dimensions are harmonized (if requested)
- RGBA panels converted to RGB without errors
- File size is reasonable (with optimization enabled)
- Animation plays smoothly in image viewers
- Metadata accurately records ritual parameters
- Performance metrics are captured

## Arcane Troubleshooting

### Wrong Frame Order
- **Problem**: Frames appear in unexpected sequence
- **Recovery**: Rename files with numbered prefixes (frame_001.png, frame_002.png, etc.)
- **Prevention**: Use consistent naming convention from start

### Choppy Animation
- **Problem**: Animation doesn't play smoothly
- **Recovery**: Decrease temporal power (duration) for higher frame rate
- **Prevention**: Test different duration values to find smoothness

### Too Large File Size
- **Problem**: Animated scroll file is too large for intended use
- **Recovery**: Enable optimization, reduce dimensions, or decrease frame count
- **Prevention**: Use optimization (default) and consider target file size

### Poor Quality
- **Problem**: Animation has artifacts or color banding
- **Recovery**: Disable optimization or reduce frame count
- **Prevention**: Test with --no-optimize for quality comparison

### Transparent Areas Become White
- **Problem**: RGBA panels have white backgrounds instead of transparent
- **Recovery**: This is expected behavior - GIF format doesn't support proper transparency
- **Prevention**: Use PNG format for individual panels if transparency is needed

### Processing Takes Too Long
- **Problem**: Ritual takes excessive time to complete
- **Recovery**: Disable optimization with --no-optimize flag
- **Prevention**: Use smaller dimensions or fewer frames for faster processing

## Best Practices

1. **Use numbered filenames** - Prefix with frame numbers for correct ordering (001, 002, 003)
2. **Test temporal power** - Experiment with duration values to find ideal frame rate
3. **Enable optimization** - Keep compression enabled for reasonable file sizes
4. **Consider target use** - Web animations need smaller files than local previews
5. **Maintain aspect ratio** - Preserve panel proportions by default
6. **Check panel dimensions** - Verify all panels have consistent size before animating
7. **Use appropriate frame rates** - 10-15fps for standard animation, 20+fps for smooth motion
8. **Test before production** - Create preview with smaller dimensions first
9. **Document settings** - Save metadata for reproducing animations later
10. **Organize panel archives** - Keep frame sets in separate directories by animation

## Quick Reference

```bash
# Basic animation
python spells/animate_artifact.py --input frames/

# Custom frame rate
python spells/animate_artifact.py --input frames/ --duration 50

# Finite loop
python spells/animate_artifact.py --input frames/ --loop 3

# Resize and animate
python spells/animate_artifact.py --input frames/ --width 256 --height 256

# No optimization
python spells/animate_artifact.py --input frames/ --no-optimize
```

## Frame Rate Quick Reference

| Duration | FPS | Use Case |
|----------|-----|----------|
| 40ms | 25 fps | Smooth showcase animation |
| 50ms | 20 fps | Fast game sprites |
| 67ms | 15 fps | Standard character animation |
| 83ms | 12 fps | Walk cycles |
| 100ms | 10 fps | Default animation speed |
| 167ms | 6 fps | Slow transitions |
| 200ms | 5 fps | Very slow demonstrations |
| 500ms | 2 fps | Step-by-step tutorials |

This ritual provides a reliable way to create animated GIFs from directories of image panels!
