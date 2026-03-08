# Obscure Artifact Hex

## Quest Objective

Cast the obscure artifact hex to shroud magical images in mystical haze. This powerful ritual applies blur effects to image artifacts, creating an obscuring mist that can hide sensitive details, soften backgrounds, or create artistic depth-of-field effects. Choose between the Gaussian ritual for smooth results or the Box enchantment for faster processing.

## When to Cast This Spell

- Protecting privacy by blurring sensitive information (faces, documents, locations)
- Softening backgrounds in portraits and product photography
- Creating artistic depth-of-field effects
- Image preprocessing before further processing operations
- Generating placeholder or preview versions of images
- Creating frosted glass or dreamy effects
- Reducing noise in scanned documents

## Required Spell Components

- Arcane Image Manipulation Grimoire (Pillow library)
- Input magical artifact: PNG, JPG, WEBP, BMP, TIFF, or GIF image

## Spell to Cast

```bash
python spells/obscure_artifact.py --input <artifact> [obscuration options]
```

## Required Reagents

| Input | Description | Example |
|-------|-------------|---------|
| `--input` | Path to magical image artifact | `photo.jpg` |

## Optional Spell Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| `--output` | `<name>_obscured.<ext>` | Path to obscured artifact |
| `--radius` | 5.0 | Obscuration power 0.1-100.0 (higher = more blur) |
| `--blur-type` | gaussian | Ritual type: gaussian (smooth), box (fast) |
| `--iterations` | 1 | Number of blur passes 1-10 (more = stronger effect) |
| `--quality` | 95 | Output quality for lossy formats (1-100) |

## Obscuration Ritual Details

### Blur Rituals

The spell supports two distinct obscuration rituals:

**Gaussian Ritual** (`--blur-type gaussian`)
- Creates smooth, natural-looking blur
- Uses Gaussian distribution for pixel averaging
- Best for portraits and realistic effects
- Slightly slower processing
- Recommended for most use cases

**Box Enchantment** (`--blur-type box`)
- Creates uniform blur effect
- Uses simple box filter for pixel averaging
- Faster processing
- Good for previews and batch processing
- Slightly less natural appearance

### Obscuration Power Guide

| Radius | Effect | Use Case |
|--------|--------|----------|
| 0.5 - 2.0 | Subtle softening | Slight background blur, noise reduction |
| 3.0 - 7.0 | Moderate blur | Portrait backgrounds, general softening |
| 8.0 - 15.0 | Heavy blur | Privacy protection, strong background blur |
| 16.0 - 30.0 | Very heavy blur | Complete detail obscuration, frosted glass |
| 31.0 - 100.0 | Extreme blur | Unrecognizable content, abstract effects |

### Iteration Effects

Multiple iterations amplify the blur effect exponentially:
- 1 iteration: Standard blur effect at specified radius
- 2-3 iterations: Significantly stronger blur (recommended for privacy)
- 4-5 iterations: Very heavy blur (details mostly obscured)
- 6-10 iterations: Near-complete abstraction (use sparingly)

**Note:** Each iteration increases processing time. For strong effects, consider increasing radius rather than iterations.

## Ritual Examples

### Basic Blur
```bash
python spells/obscure_artifact.py --input photo.jpg
```

### Subtle Blur
```bash
python spells/obscure_artifact.py --input portrait.png --radius 2
```

### Heavy Blur for Privacy
```bash
python spells/obscure_artifact.py --input sensitive.png --radius 20
```

### Fast Box Blur
```bash
python spells/obscure_artifact.py --input sprite.png --blur-type box --radius 10
```

### Multiple Iterations for Strong Effect
```bash
python spells/obscure_artifact.py --input background.jpg --radius 5 --iterations 3
```

### Custom Output Path
```bash
python spells/obscure_artifact.py --input image.png --output blurred/image.png
```

### Extreme Blur
```bash
python spells/obscure_artifact.py --input document.jpg --radius 50 --iterations 2
```

### Subtle Softening with High Quality
```bash
python spells/obscure_artifact.py --input portrait.png --radius 1.5 --quality 98
```

## Expected Magical Output

```
Obscuration ritual completed successfully!
  Artifact: /path/to/input.png
  Obscured: /path/to/input_obscured.png
  Ritual: gaussian
  Obscuration power: 5.0
  Iterations: 1
  Dimensions: 1024x768
  Size: 2.45 MB → 2.38 MB
  Duration: 0.35s
  Arcane knowledge: /path/to/input_obscure_metadata.json
```

## Spell Fumble Recovery

| Spell Fumble | Cause | Recovery |
|--------------|-------|----------|
| `Artifact not found` | Input path doesn't exist | Verify artifact path is correct |
| `Unsupported artifact format` | File format not supported | Use PNG, JPG, WEBP, BMP, TIFF, or GIF |
| `Obscuration power must be between` | Radius value out of range | Use value between 0.1 and 100.0 |
| `Unknown ritual type` | Invalid blur type specified | Use 'gaussian' or 'box' |
| `Iterations must be between` | Iteration count out of range | Use value between 1 and 10 |
| `Quality must be between 1 and 100` | Invalid quality value | Use value between 1 (lowest) and 100 (highest) |
| `Artifact too large` | File exceeds size limit | Provide smaller file or increase max size |

## Arcane Notes

- **Radius Selection**: Start with lower values and increase gradually. Higher values create stronger effects but may cause complete loss of detail.
- **Gaussian vs Box**: Gaussian produces more natural results; Box is faster but slightly less smooth.
- **Iterations vs Radius**: Increasing radius is usually more efficient than adding iterations for stronger blur.
- **Transparency Preservation**: PNG/WEBP with transparency (RGBA) is preserved when outputting to PNG/WEBP.
- **JPEG Conversion**: When outputting to JPEG, RGBA is converted to RGB with white background.
- **Quality Setting**: Only affects lossy formats (JPEG, WEBP). PNG uses lossless compression.
- **Processing Time**: Gaussian blur is slower than box blur, especially at high radii.
- **Multiple Iterations**: Each iteration compounds the previous blur effect exponentially.
- **Privacy Protection**: For complete privacy, use radius 20+ with 2-3 iterations.
- **Original Artifact**: The original artifact is never modified.

## Common Use Cases

### Privacy Protection
```bash
# Blur faces or sensitive information
python spells/obscure_artifact.py --input photo_with_faces.jpg --radius 25 --iterations 2

# Blur document text
python spells/obscure_artifact.py --input document.jpg --radius 15 --iterations 3
```

### Background Softening
```bash
# Subtle background blur for portraits
python spells/obscure_artifact.py --input portrait.png --radius 3

# Moderate background softening
python spells/obscure_artifact.py --input product_photo.jpg --radius 6
```

### Artistic Effects
```bash
# Dreamy, soft effect
python spells/obscure_artifact.py --input landscape.png --radius 2 --iterations 2

# Frosted glass effect
python spells/obscure_artifact.py --input window.png --radius 8
```

### Image Preprocessing
```bash
# Reduce noise before further processing
python spells/obscure_artifact.py --input noisy_scan.png --radius 1

# Create preview/placeholder
python spells/obscure_artifact.py --input detailed.png --radius 10 --blur-type box
```

## Blur Ritual Comparison

| Ritual | Speed | Quality | Best For |
|--------|-------|---------|----------|
| gaussian | Moderate | Excellent | Portraits, realistic effects, final output |
| box | Fast | Good | Previews, batch processing, placeholders |

## Arcane Discoveries

_This section is updated when spell fumbles are encountered and resolved._

- None yet - will be populated as the spell is used in production
