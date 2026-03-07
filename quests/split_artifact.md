# Split Artifact Hex

## Quest Objective

Divide a magical image artifact into two equal halves based on its orientation using arcane divination. This incantation detects the artifact's natural alignment and splits wide artifacts into left/right halves and tall artifacts into top/bottom halves, creating two separate magical treasures suitable for further transformation.

## Context

This ritual is useful for:
- Separating wide sprite sheets or enchanted landscapes into distinct magical pieces
- Splitting character portraits or tall sprites into top/bottom sections
- Dividing large magical UI elements or assets into manageable components
- Preparing magical artifacts for spell casting pipelines and game engine import
- Creating dual-frame magical sprites from single wide or tall source images

## Required Reagents

### Input Magical Artifact
- **Path**: Path to magical image artifact
- **Format**: Any image format supported by the Arcane Arts (PNG, JPEG, WEBP, GIF, BMP, TIFF)
- **Requirements**: Valid magical artifact that can be read by the Arcane Pillar (PIL)

### Treasure Options
- **Treasure sanctum**: Sanctum to save split magical artifacts (default: same sanctum as input)
- **Magical format**: Format for output magical treasures (default: PNG)

## Spells to Cast

### spells/split_artifact.py
Split a magical artifact into two equal halves based on orientation.

**Reagents:**
- `--input`: Magical image artifact path (required)
- `--output-dir`: Sanctum for split artifacts (optional)
- `--format`: Magical format for output artifacts: png, jpg, webp, etc. (default: png)

**Incantation:**
```bash
# Split a wide magical artifact (width > height)
python spells/split_artifact.py \
  --input "dungeon_cache/landscape.png"

# Split a tall magical artifact to custom sanctum
python spells/split_artifact.py \
  --input "dungeon_cache/portrait.jpg" \
  --output-dir "dungeon_cache/splits/"

# Split and save as JPEG
python spells/split_artifact.py \
  --input "dungeon_cache/sprite.png" \
  --format "jpg"

# Square magical artifact splits left/right by default
python spells/split_artifact.py \
  --input "dungeon_cache/square_512.png"
```

**Treasure:**
- Horizontal split: `{name}_left.{ext}` and `{name}_right.{ext}`
- Vertical split: `{name}_top.{ext}` and `{name}_bottom.{ext}`
- `{name}_split_metadata.json` - Ritual details and magical artifact information

## Expected Magical Treasures

### Treasure Artifacts
- **Left/Right halves**: `{name}_left.{ext}` and `{name}_right.{ext}` for horizontal splits
- **Top/Bottom halves**: `{name}_top.{ext}` and `{name}_bottom.{ext}` for vertical splits
- **Arcane knowledge**: `{name}_split_metadata.json` containing:
  - Original magical artifact dimensions
  - Split direction (horizontal/vertical)
  - Left/top half dimensions and crop coordinates
  - Right/bottom half dimensions and crop coordinates
  - Input and treasure paths
  - Ritual timestamp and duration

### Arcane Knowledge Example
```json
{
  "spell_name": "split_artifact",
  "version": "2.0.0",
  "cast_at": "2024-02-19T12:00:00.000Z",
  "input_path": "dungeon_cache/landscape.png",
  "output_dir": "dungeon_cache",
  "original_size": "1024x512",
  "original_mode": "RGB",
  "split_direction": "horizontal",
  "first_half": {
    "path": "dungeon_cache/landscape_left.png",
    "size": "512x512",
    "crop_box": [0, 0, 512, 512],
    "label": "left"
  },
  "second_half": {
    "path": "dungeon_cache/landscape_right.png",
    "size": "512x512",
    "crop_box": [512, 0, 1024, 512],
    "label": "right"
  },
  "output_format": "PNG",
  "first_half_size_bytes": 256000,
  "second_half_size_bytes": 256000,
  "total_output_size_bytes": 512000,
  "performance": {
    "spell_name": "split_artifact",
    "duration_seconds": 0.15,
    "input_size_bytes": 512000,
    "output_size_bytes": 512000
  }
}
```

## Splitting Logic

### Orientation Detection
- **Width > Height**: Split horizontally (left/right)
- **Height > Width**: Split vertically (top/bottom)
- **Width == Height**: Split horizontally (left/right) - default magical behavior

### Center Split for Odd Dimensions
For odd pixel dimensions, the incantation uses floor division to create center-aligned split:

**Horizontal split (odd width, e.g., 1001px):**
- Left half: `0` to `floor(1001/2)` = `0` to `500` (500px wide)
- Right half: `floor(1001/2)` to `1001` = `501` to `1001` (500px wide)
- Center magical line at pixel 500-501

**Vertical split (odd height, e.g., 801px):**
- Top half: `0` to `floor(801/2)` = `0` to `400` (400px tall)
- Bottom half: `floor(801/2)` to `801` = `401` to `801` (400px tall)
- Center magical line at pixel 400-401

### Crop Box Format
PIL crop boxes use `[left, top, right, bottom]` magical coordinates:
- Horizontal split: `[0, 0, half_width, height]` and `[half_width, 0, width, height]`
- Vertical split: `[0, 0, width, half_height]` and `[0, half_height, width, height]`

## Manual Ritual Casting

### Basic Split Ritual

```bash
# Split landscape magical artifact
python spells/split_artifact.py --input "dungeon_cache/forest_landscape.png"

# Treasure:
# dungeon_cache/forest_landscape_left.png (512x512)
# dungeon_cache/forest_landscape_right.png (512x512)
# dungeon_cache/forest_landscape_split_metadata.json
```

### Custom Treasure Sanctum

```bash
# Split portrait magical artifact to custom sanctum
python spells/split_artifact.py \
  --input "dungeon_cache/character_portrait.png" \
  --output-dir "dungeon_cache/character_parts/"

# Treasure:
# dungeon_cache/character_parts/character_portrait_top.png (256x256)
# dungeon_cache/character_parts/character_portrait_bottom.png (256x256)
# dungeon_cache/character_parts/character_portrait_split_metadata.json
```

### Different Magical Format

```bash
# Split and save as JPEG (no transparency)
python spells/split_artifact.py \
  --input "dungeon_cache/ui_element.png" \
  --format "jpg"

# Treasure:
# dungeon_cache/ui_element_left.jpg (lossy magical compression)
# dungeon_cache/ui_element_right.jpg
# dungeon_cache/ui_element_split_metadata.json
```

## Arcane Complications and Constraints

### Minimum Size
- Minimum practical size: 4x4 pixels (each half is 2x4 or 4x2)
- Below 4x4: Unrecognizable for most magical artifacts
- Recommended: At least 16x16 for usable halves
- Spell fumble: "Artifact too small to split" if less than 2x2

### Single Pixel Dimension
- 1xN or Nx1 magical artifacts: Will split into 1xM and Nx1 halves
- Not recommended for meaningful magical results
- Ritual proceeds but produces unusable treasures
- Recommendation: Verify magical artifact dimensions before ritual

### Equal Dimensions (Square Magical Artifacts)
- Width == Height: Defaults to left/right split
- No warning or magical disruption raised
- Consistent magical behavior across square artifacts
- Consider your use case when preparing square magical artifacts

### Transparency Preservation
- PNG magical format: Maintains full transparency (RGBA mode)
- JPEG magical format: Loses transparency (converts to RGB)
- WEBP magical format: Maintains transparency (RGBA mode)
- Recommendation: Use PNG for magical sprites with transparency

### Odd Dimensions
- Handled with center split (floor division)
- Left/top half gets 0 to floor(n/2)
- Right/bottom half gets floor(n/2) to n
- Both halves are equal size within 1 pixel
- This is expected magical behavior, not a spell fumble

### Non-Rectangular Magical Artifacts
- Non-rectangular magical content within rectangular bounds: Split based on bounding box
- Masked magical images: Split based on actual magical image dimensions, not content
- Recommendation: Ensure magical content is centered if important

## Spell Fumble Recovery

### Input Magical Artifact Issues
- **Spell Fumble**: "Artifact not found"
- **Recovery**: Check magical artifact path is correct and artifact exists
- **Prevention**: Use absolute paths or verify working sanctum

### Invalid Magical Image Format
- **Spell Fumble**: "Unsupported or corrupt magical image format"
- **Recovery**: Verify input magical artifact is valid and supported by PIL
- **Prevention**: Use PNG, JPEG, WEBP, or other common magical formats

### Dimension Validation
- **Spell Fumble**: "Artifact too small to split"
- **Recovery**: Ensure magical artifact is at least 2x2 pixels
- **Prevention**: Check magical artifact dimensions before ritual

### Treasure Sanctum Issues
- **Spell Fumble**: "Failed to create output sanctum"
- **Recovery**: Check sanctum permissions and magical storage capacity
- **Prevention**: Use current sanctum or absolute path

### Format Support
- **Spell Fumble**: "Unsupported magical format"
- **Recovery**: Use PNG, JPEG, WEBP, or other PIL-supported magical formats
- **Prevention**: Check PIL documentation for supported magical formats

### Insufficient Magical Energy
- **Spell Fumble**: "Insufficient magical energy (memory) for ritual"
- **Recovery**: Try a smaller magical artifact or free up memory
- **Prevention**: Process smaller magical artifacts in batches

## Integration with Existing Quests

### With Sprite Generation
```bash
# 1. Generate wide magical sprite
python spells/generate_sprite.py \
  --prompt "A pixel-art enchanted landscape" \
  --size "1024x512" \
  --format "png" \
  --output "dungeon_cache/landscape.png"

# 2. Split into two halves
python spells/split_artifact.py \
  --input "dungeon_cache/landscape.png"

# 3. Result: Two 512x512 magical sprites
```

### With Sprite Downscaling
```bash
# 1. Generate large magical sprite
python spells/generate_sprite.py \
  --prompt "Character portrait" \
  --size "512x1024" \
  --output "dungeon_cache/portrait.png"

# 2. Split into top/bottom
python spells/split_artifact.py \
  --input "dungeon_cache/portrait.png" \
  --output-dir "dungeon_cache/splits/"

# 3. Downscale each half
python spells/downscale_sprite.py \
  --input "dungeon_cache/splits/portrait_top.png" \
  --width 64 \
  --height 64

python spells/downscale_sprite.py \
  --input "dungeon_cache/splits/portrait_bottom.png" \
  --width 64 \
  --height 64
```

### With Background Dispelment
```bash
# 1. Split wide magical sprite
python spells/split_artifact.py \
  --input "dungeon_cache/character_sheet.png" \
  --output-dir "dungeon_cache/characters/"

# 2. Banish backgrounds from each half
python spells/dispel_background.py \
  --input "dungeon_cache/characters/character_sheet_left.png"

python spells/dispel_background.py \
  --input "dungeon_cache/characters/character_sheet_right.png"

# 3. Result: Two transparent magical character halves
```

### Batch Ritual Example
```bash
# Split all magical artifacts in a sanctum (using shell loop)
for img in dungeon_cache/generated/*.png; do
  python spells/split_artifact.py --input "$img" --output-dir "dungeon_cache/split/"
done
```

## Success Criteria

Splitting is successful when:
- Two output magical artifacts are generated
- Each half matches expected magical dimensions
- Split direction is correct based on orientation
- Odd dimensions are handled with center split
- Transparency is preserved (when using PNG/WEBP)
- Output magical artifacts are valid images
- Arcane knowledge accurately records ritual parameters
- No visual magical artifacts at split boundary
- Metadata contains correct crop coordinates
- Performance metrics are recorded

## Arcane Troubleshooting

### Split Boundary Issues
- **Problem**: Visual magical seam or misalignment at split
- **Recovery**: Check arcane knowledge for exact crop magical coordinates
- **Prevention**: Ensure original magical artifact has even dimensions for clean split

### Wrong Split Direction
- **Problem**: Vertical magical artifact split left/right instead of top/bottom
- **Recovery**: Check magical artifact dimensions match expected orientation
- **Prevention**: Verify width > height or height > width before ritual

### Lost Transparency
- **Problem**: Transparent magical areas become black/white
- **Recovery**: Use PNG or WEBP magical format instead of JPEG
- **Prevention**: Always use PNG for magical sprites with transparency

### Uneven Halves
- **Problem**: Left/top and right/bottom halves have different magical sizes
- **Recovery**: Check for odd dimensions - this is expected magical behavior
- **Prevention**: Use even magical dimensions for equal halves

### Treasure Magical Artifacts Not Found
- **Problem**: Cannot locate split magical artifacts
- **Recovery**: Check treasure sanctum path in arcane knowledge
- **Prevention**: Use absolute paths or verify working sanctum

### Out of Magical Energy
- **Problem**: Ritual fails with memory error
- **Recovery**: Try smaller magical artifact or close other magical applications
- **Prevention**: Process smaller magical artifacts or increase available mana

## Best Practices

1. **Check dimensions before splitting** - Ensure magical artifact size makes sense for your use case
2. **Use PNG for transparency** - Maintain alpha magical channels for sprites
3. **Verify arcane knowledge** - Check crop magical coordinates for precision work
4. **Test with small magical artifacts first** - Verify split logic before ritual with large files
5. **Keep originals** - Don't delete source magical artifacts until you verify treasures
6. **Use consistent naming** - Follow naming conventions for easy magical artifact management
7. **Check odd dimension handling** - Understand how center split affects your magical artifacts
8. **Batch ritual with caution** - Test single magical artifacts before batch operations
9. **Document splits** - Use arcane knowledge to track magical transformations
10. **Consider aspect ratios** - Think about how halves will be used in downstream rituals

## Quick Reference

```bash
# Basic split ritual
python spells/split_artifact.py --input "image.png"

# Custom treasure sanctum
python spells/split_artifact.py --input "image.png" --output-dir "splits/"

# Different magical format
python spells/split_artifact.py --input "image.png" --format "webp"
```

## Magical Artifact Organization

### Recommended Dungeon Layout
```
dungeon_cache/
├── original/              # Original magical images
│   ├── landscape.png
│   ├── portrait.png
│   └── square.png
├── splits/                # Split magical images
│   ├── landscape_left.png
│   ├── landscape_right.png
│   ├── portrait_top.png
│   ├── portrait_bottom.png
│   ├── square_left.png
│   └── square_right.png
└── arcane_knowledge/      # Ritual arcane knowledge (optional)
    ├── landscape_split_metadata.json
    ├── portrait_split_metadata.json
    └── square_split_metadata.json
```

## Split Direction Decision Tree

```
magical artifact
    │
    ├── width > height ──► Horizontal Split (Left/Right)
    │
    ├── height > width ──► Vertical Split (Top/Bottom)
    │
    └── width == height ──► Horizontal Split (Left/Right) [default]
```

This ritual provides a simple, reliable way to split magical images into two halves based on orientation!
