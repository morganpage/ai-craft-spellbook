# Resize Artifact Transmutation

## Quest Objective

Transmute the size of magical image artifacts while preserving their essence. This powerful ritual allows you to resize images to exact dimensions, scale by percentage, or fit within bounds while maintaining aspect ratio—perfect for game asset preparation, thumbnail generation, and creating optimized versions for different display sizes.

## When to Cast This Spell

- Preparing game assets at multiple resolution versions
- Creating thumbnails for previews and web distribution
- Scaling sprite sheets for different device sizes (mobile, tablet, desktop)
- Optimizing images for specific display dimensions
- Batch resizing image collections
- Preparing assets for retina/high-DPI displays

## Required Spell Components

- Arcane Image Manipulation Grimoire (Pillow library)
- Input magical artifact: PNG, JPG, WEBP, BMP, TIFF, or GIF image

## Spell to Cast

```bash
python spells/resize_artifact.py --input <artifact> [resize options]
```

## Required Reagents

| Input | Description | Example |
|-------|-------------|---------|
| `--input` | Path to magical image artifact | `character.png` |

## Optional Spell Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| `--output` | `<name>_resized.<ext>` | Path to transmuted artifact |
| `--width` | None | Target width in pixels |
| `--height` | None | Target height in pixels |
| `--scale` | None | Scale percentage (e.g., 50 for half size) |
| `--fit` | false | Fit within bounds (maintains aspect ratio) |
| `--cover` | false | Cover bounds exactly (may crop, maintains aspect ratio) |
| `--exact` | false | Exact dimensions (may distort) |
| `--no-maintain-aspect` | false | Don't maintain aspect ratio |
| `--quality` | 95 | Output quality for lossy formats (1-100) |
| `--resampling` | lanczos | Resampling filter: nearest, bilinear, bicubic, lanczos |

## Ritual Steps

### Dimension Calculation

The transmutation ritual intelligently calculates new dimensions based on your intent:

1. **Scale Mode**: When `--scale` is specified, both dimensions are multiplied by the scale percentage
   - Example: `--scale 50` creates an image at 50% of original size

2. **Exact Mode**: When `--exact` is specified with both width and height, dimensions are set exactly (may distort)
   - Example: `--width 200 --height 300 --exact` forces exact 200x300 dimensions

3. **Fit Mode**: When `--fit` is specified, image fits entirely within bounds while maintaining aspect ratio
   - Example: `--width 1920 --height 1080 --fit` ensures image is no larger than 1920x1080

4. **Cover Mode**: When `--cover` is specified, image covers bounds exactly while maintaining aspect ratio (may crop)
   - Example: `--width 800 --height 600 --cover` fills 800x600 exactly, cropping excess

5. **Default Mode**: When width or height is specified alone, the other dimension is calculated to maintain aspect ratio
   - Example: `--width 512` calculates height automatically

### Resampling Filters

The ritual uses different alchemical filters for resizing:

- **nearest**: Fastest, preserves hard edges (good for pixel art)
- **bilinear**: Fast, smooth results (good for quick previews)
- **bicubic**: Balanced quality and speed (good for general use)
- **lanczos**: Highest quality, slower (best for final assets)

### Color Mode Handling

- PNG with transparency (RGBA) is preserved when outputting to PNG
- When outputting to JPEG, RGBA is converted to RGB with white background
- Other color modes are preserved appropriately

## Ritual Examples

### Resize to exact dimensions (maintains aspect ratio)
```bash
python spells/resize_artifact.py --input character.png --width 512 --height 512
```

### Scale to 50% of original size
```bash
python spells/resize_artifact.py --input sprite.png --scale 50
```

### Fit within maximum bounds
```bash
python spells/resize_artifact.py --input landscape.jpg --width 1920 --height 1080 --fit
```

### Cover exact bounds (may crop)
```bash
python spells/resize_artifact.py --input photo.png --width 800 --height 600 --cover
```

### Resize to exact width (height calculated automatically)
```bash
python spells/resize_artifact.py --input icon.png --width 256
```

### Scale up for high-DPI displays
```bash
python spells/resize_artifact.py --input asset.png --scale 200
```

### Create thumbnail with fast resampling
```bash
python spells/resize_artifact.py --input photo.jpg --width 150 --height 150 --resampling bilinear
```

### Exact dimensions (may distort)
```bash
python spells/resize_artifact.py --input square.png --width 200 --height 300 --exact
```

### Custom output path
```bash
python spells/resize_artifact.py --input sprite.png --width 64 --height 64 --output assets/sprite_icon.png
```

## Expected Magical Output

```
Transmutation completed successfully!
Artifact: /path/to/input.png
Transmuted: /path/to/input_resized.png
Original dimensions: 1024x768
New dimensions: 512x384
Method: width
Scale factor: 50.0%
Size: 2.45 MB → 512.34 KB
Duration: 0.23s
Arcane knowledge: /path/to/input_resize_metadata.json
```

## Spell Fumble Recovery

| Spell Fumble | Cause | Recovery |
|--------------|-------|----------|
| `Artifact not found` | Input path doesn't exist | Verify artifact path |
| `Unsupported artifact format` | File format not supported | Use PNG, JPG, WEBP, BMP, TIFF, or GIF |
| `Must specify at least one of` | No dimensions or scale provided | Provide --width, --height, or --scale |
| `Exact mode requires both` | --exact used with only one dimension | Provide both --width and --height |
| `Invalid resampling filter` | Unknown filter specified | Use: nearest, bilinear, bicubic, or lanczos |
| `Quality must be between 1 and 100` | Invalid quality value | Use value between 1 (lowest) and 100 (highest) |

## Arcane Notes

- **Aspect Ratio**: By default, aspect ratio is maintained to prevent distortion
- **Fit vs Cover**: Use `--fit` to ensure entire image is visible, `--cover` to fill bounds completely
- **Upscaling**: Scaling up (`--scale 200`) works but may reduce quality—consider using dedicated upscaling tools
- **Pixel Art**: Use `--resampling nearest` for pixel art to preserve hard edges
- **Transparency**: PNG transparency is preserved when outputting to PNG, but JPEG requires RGB conversion
- **Quality Setting**: Only affects lossy formats (JPEG, WEBP), PNG uses lossless compression
- **Original Artifact**: The original artifact is never modified
- **Batch Processing**: For multiple images, use shell scripting or Python to iterate over files

## Transmutation Methods

| Method | Description | When to Use |
|--------|-------------|-------------|
| `scale` | Multiply both dimensions by percentage | Quick overall size change |
| `exact` | Force exact dimensions (may distort) | Thumbnails, tiles, grid layouts |
| `fit` | Fit within bounds (maintains aspect) | Max dimension constraints |
| `cover` | Cover bounds exactly (may crop) | Hero images, banners, covers |
| `width` | Set width, calculate height | Fixed-width layouts |
| `height` | Set height, calculate width | Fixed-height layouts |

## Common Use Cases

### Game Assets
```bash
# Create multiple resolution versions
python spells/resize_artifact.py --input character.png --scale 200 --output character_2x.png
python spells/resize_artifact.py --input character.png --scale 100 --output character_1x.png
python spells/resize_artifact.py --input character.png --scale 50 --output character_05x.png
```

### Thumbnail Generation
```bash
# Create fast thumbnail
python spells/resize_artifact.py --input photo.jpg --width 200 --height 200 --fit --resampling bilinear
```

### Web Optimization
```bash
# Scale down for web with optimized quality
python spells/resize_artifact.py --input large.png --width 1920 --quality 85 --output optimized.jpg
```

### Mobile Preparation
```bash
# Create mobile version
python spells/resize_artifact.py --input desktop.png --width 640 --output mobile.png
```

## Arcane Discoveries

_This section is updated when spell fumbles are encountered and resolved._

- None yet - will be populated as the spell is used in production
