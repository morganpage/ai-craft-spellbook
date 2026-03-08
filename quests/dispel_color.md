# Dispel Color (Chroma Key Spell)

## Quest Objective
Remove pixels from an image that match a specific sampled color using chroma key magic. This spell is essential for green screen effects, removing solid color backgrounds, or creating transparent backgrounds from images with uniform colored backgrounds.

## When to Cast This Spell
- You have a photo with a green screen background that needs removal
- An image has a solid color background you want to make transparent
- You need to key out a specific color from an image
- You have a color palette/swatch and want to remove matching colors

## Required Spell Components
- Python 3.8+
- Pillow (PIL) image manipulation library
- Input image with background to remove
- Color source image OR hex color code

## Spell to Cast
```bash
# Using a color palette/swatch image with coordinates
python spells/dispel_color.py --input <image> --color-source <palette> --color-x <x> --color-y <y>

# Using a direct hex color code
python spells/dispel_color.py --input <image> --color <#RRGGBB>

# With custom tolerance
python spells/dispel_color.py --input <image> --color-source <palette> --color-x <x> --color-y <y> --tolerance 50
```

## Required Reagents
| Reagent | Description | Example |
|----------|-------------|---------|
| `--input` | Path to the image to process | `photo.png` |
| `--color-source` | Path to image containing color to sample | `palette.png` |
| `--color-x` | X coordinate to sample (pixels from left) | `100` |
| `--color-y` | Y coordinate to sample (pixels from top) | `50` |
| `--color` | Direct hex color (alternative to color-source) | `#00FF00` |

## Optional Spell Parameters
| Parameter | Description | Default | Range |
|-----------|-------------|---------|-------|
| `--tolerance` | Color matching sensitivity | `30` | `0-100` |
| `--output` | Output file path | `<input>_dispelled.png` | Any valid path |

**Tolerance Guide:**
- **0-20**: Very exact color matching (only near-exact matches removed)
- **30-50**: Balanced matching (good for solid backgrounds with slight variation)
- **60-100**: Aggressive matching (removes wider color range, may affect subject)

## Ritual Steps

### Step 1: Identify the Background Color
**Method A - Sample from Palette Image:**
- Identify a color palette or swatch image showing the background color
- Note the X,Y coordinates where the color appears
- Example: If the background color is at position (100, 50) in the palette

**Method B - Direct Hex Color:**
- Use an image editor to identify the RGB/hex value of the background
- Common green screen: `#00FF00`
- Common blue screen: `#0000FF`
- Pure white: `#FFFFFF`
- Pure black: `#000000`

### Step 2: Cast the Spell

**Using palette sampling:**
```bash
python spells/dispel_color.py \
  --input "Character Design Sheet.png" \
  --color-source "color_palette.png" \
  --color-x 150 \
  --color-y 50
```

**Using direct hex color:**
```bash
python spells/dispel_color.py \
  --input "photo.png" \
  --color "#00FF00" \
  --tolerance 40
```

### Step 3: Adjust Tolerance if Needed
If the background isn't fully removed:
- Increase tolerance (try 40, 50, 60)

If parts of your subject are being removed:
- Decrease tolerance (try 20, 15, 10)

### Step 4: Verify Results
- Check the output image for clean edges
- Ensure the subject remains intact
- Verify background is fully transparent

## Expected Magical Treasures
- **Output image**: PNG file with transparent background where matching colors were removed
- **Metadata file**: JSON file containing processing details and statistics
- **Console output**: Processing summary with dimensions, colors, and pixel counts

## Spell Fumble Recovery

| Error | Cause | Solution |
|-------|-------|----------|
| "Artifact not found" | Input image path is incorrect | Check file path and extension |
| "Color source image not found" | Palette image path is incorrect | Verify palette image exists |
| "Invalid hex color" | Hex color format is wrong | Use format `#RRGGBB` or `RRGGBB` (6 hex digits) |
| "--tolerance must be between 0 and 100" | Tolerance value out of range | Use value between 0-100 |
| Too much of subject removed | Tolerance too high | Decrease tolerance value |
| Background not fully removed | Tolerance too low | Increase tolerance value |

## Arcane Notes

**Color Distance Calculation:**
- The spell uses Euclidean distance in RGB color space
- Maximum possible distance between colors: ~441.67 (black to white)
- Tolerance of 30 = ~30% of max distance (~132 units)
- Tolerance of 100 = entire color space removed

**Choosing Coordinates:**
- X is measured from the left edge (0 = leftmost pixel)
- Y is measured from the top edge (0 = topmost pixel)
- Use any image viewer to find pixel coordinates
- Many tools show coordinates when hovering over images

**Common Use Cases:**
1. **Green Screen**: Tolerance 30-50, sample from pure green area
2. **White Background**: Tolerance 15-30, white reflects light creating variation
3. **Black Background**: Tolerance 10-25, easier to match exactly
4. **Blue Screen**: Tolerance 30-50, similar to green screen

**Output Format:**
- Always outputs as PNG to preserve transparency
- PNG with alpha channel (RGBA) for proper transparency
- Optimized PNG for smaller file size

**Performance:**
- Processes pixel-by-pixel, so large images take longer
- Typical 1920x1080 image: 1-3 seconds
- No external AI models required (faster than dispel_background for solid colors)

**Advanced Tips:**
- For complex backgrounds, use `dispel_background` (AI-based) instead
- For semi-transparent backgrounds, try multiple passes with different tolerances
- Combine with other spells: dispel_color → resize_artifact → obscure_artifact
