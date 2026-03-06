# Dispel Background Hex

## Quest Objective

Banish unwanted backgrounds from magical image artifacts using arcane vision detection. This powerful incantation leverages machine learning to accurately separate foreground subjects from backgrounds, producing transparent PNG treasures suitable for game assets, UI elements, and design work.

## Context

This ritual is useful for:
- Banishing backgrounds from character sprites for game development
- Creating transparent treasures for UI elements and icons
- Preparing magical images for sprite sheet generation
- Extracting objects from photographs for design work
- Cleansing AI-generated artifacts for production use

## Required Reagents

### Input Image Artifact
- **Path**: Path to magical image artifact
- **Format**: PNG, JPG, WEBP, or any format supported by PIL
- **Requirements**: Valid image artifact that can be read by PIL

### Treasure Options
- **Treasure destination**: Path to output PNG artifact (optional, auto-generated if not provided)
- **Arcane Crystal**: AI model to use (default: u2net)

## Spells to Cast

### spells/dispel_background.py
Banish background from a magical image using arcane vision detection.

**Reagents:**
- `--input`: Magical image artifact path (required)
- `--output`: Treasure destination path (optional)
- `--model`: Arcane crystal to use (u2net, u2netp, u2net_human_seg, u2net_cloth_seg, silueta) (default: u2net)

**Incantation:**
```bash
# Basic background dispelling
python spells/dispel_background.py \
  --input "dungeon_cache/image.png"

# Custom treasure destination
python spells/dispel_background.py \
  --input "dungeon_cache/image.png" \
  --output "dungeon_cache/output/dispelled.png"

# Use different arcane crystal
python spells/dispel_background.py \
  --input "dungeon_cache/character.png" \
  --model "u2netp"
```

**Treasure:**
- Background-dispelled PNG artifact with transparent background
- `{name}_dispel_metadata.json` - Ritual details and magical artifact information

## Expected Magical Treasures

### Treasure Artifacts
- **Background-dispelled magical image**: `{name}_dispelled.png` at specified path or same sanctum as input
- **Arcane knowledge**: `{name}_dispel_metadata.json` containing:
  - Input and treasure destination paths
  - Magical image dimensions before and after
  - Color modes
  - Artifact sizes before and after
  - Size change percentage
  - Arcane crystal used
  - Ritual timestamp

### Arcane Knowledge Example
```json
{
  "input_path": "dungeon_cache/character.png",
  "output_path": "dungeon_cache/character_dispelled.png",
  "input_size": "512x512",
  "output_size": "512x512",
  "input_mode": "RGB",
  "output_mode": "RGBA",
  "input_size_bytes": 2048576,
  "output_size_bytes": 1536000,
  "size_change_percent": -25.0,
  "model": "u2net",
  "processed_at": "2024-02-19T12:00:00.000Z"
}
```

## Arcane Crystal Options

### Available Crystals

**u2net (default)**
- General-purpose crystal
- Good arcane accuracy for most subjects
- Balances speed and magical quality
- Best for: Character sprites, objects, general use

**u2netp**
- Lightweight version of u2net
- Faster ritual casting
- Slightly lower arcane accuracy
- Best for: Quick magical previews, batch processing

**u2net_human_seg**
- Specialized for human subjects
- Better hair and edge detection
- Best for: Character portraits, photos of adventurers

**u2net_cloth_seg**
- Specialized for clothing
- Separates clothing from background
- Best for: Fashion assets, character costumes

**silueta**
- Fast silhouette extraction
- Good for simple magical shapes
- Best for: Icons, simple objects

## Manual Ritual Casting

### Basic Background Dispelment

```bash
# Banish background with default settings
python spells/dispel_background.py --input "dungeon_cache/character.png"

# Treasure:
# dungeon_cache/character_dispelled.png
# dungeon_cache/character_dispel_metadata.json
```

### Custom Treasure Destination

```bash
# Cast to specific sanctum
python spells/dispel_background.py \
  --input "dungeon_cache/image.png" \
  --output "dungeon_cache/assets/transparent.png"

# Treasure:
# dungeon_cache/assets/transparent.png
# dungeon_cache/assets/transparent_dispel_metadata.json
```

### Arcane Crystal Selection

```bash
# Use human segmentation crystal for portraits
python spells/dispel_background.py \
  --input "dungeon_cache/portrait.png" \
  --model "u2net_human_seg"

# Use lightweight crystal for fast ritual casting
python spells/dispel_background.py \
  --input "dungeon_cache/icon.png" \
  --model "u2netp"
```

## Arcane Complications and Constraints

### First Ritual Casting
- Arcane crystals are downloaded automatically on first use (~170MB for u2net)
- Astral connection required for initial crystal download
- Crystals are cached locally after first download

### Large Magical Artifacts
- Ritual time scales with magical image dimensions
- Very large magical images (>4000x4000) may require significant ritual time
- Mana usage scales with magical image size
- Recommendation: Downscale large magical images before ritual

### Complex Magical Backgrounds
- Arcane vision performs best with distinct foreground/background magical separation
- Similar magical colors between subject and background may reduce arcane accuracy
- Complex magical backgrounds (magical forests, crowds) may be challenging
- Fine magical details (hair, fur) may have minor artifacts

### Input Artifact Formats
- Any format supported by PIL can be processed
- Treasure destination is always PNG with RGBA mode (transparency)
- Input transparency is preserved when applicable

### Magical Color Accuracy
- Original subject magical colors are preserved
- Edge magical pixels may be semi-transparent for smooth boundaries
- No magical color space conversion issues (maintains original magical color space)

## Spell Fumble Recovery

### Input Artifact Issues
- **Spell Fumble**: "Artifact not found"
- **Recovery**: Check magical artifact path is correct and artifact exists
- **Prevention**: Use absolute paths or verify working sanctum

### Invalid Magical Image Format
- **Spell Fumble**: "Unsupported or corrupt magical image format"
- **Recovery**: Verify input artifact is a valid magical image supported by PIL
- **Prevention**: Use PNG, JPEG, WEBP, or other common magical formats

### Arcane Crystal Issues
- **Spell Fumble**: "Failed to load arcane crystal"
- **Recovery**: Check astral connection for first ritual, verify crystal name
- **Prevention**: Use valid crystal name from supported options

### Treasure Destination Issues
- **Spell Fumble**: "Failed to create treasure destination sanctum"
- **Recovery**: Check sanctum permissions and magical storage capacity
- **Prevention**: Use current sanctum or absolute path

### Mana Issues
- **Spell Fumble**: "Out of mana" or ritual hangs
- **Recovery**: Downscale magical image or use smaller crystal (u2netp)
- **Prevention**: Process smaller magical batches or use lighter crystals

## Integration with Existing Quests

### With Sprite Generation
```bash
# 1. Generate magical sprite with background
python spells/generate_sprite.py \
  --prompt "A pixel-art knight" \
  --size "512x512" \
  --output "dungeon_cache/knight.png"

# 2. Banish background
python spells/dispel_background.py \
  --input "dungeon_cache/knight.png"
```

### With Sprite Sheet Creation
```bash
# 1. Generate multiple magical frames
python spells/generate_character_animation.py \
  --prompt "Walking knight" \
  --frames "1,2,3,4" \
  --output "dungeon_cache/walking_"

# 2. Banish backgrounds from all magical frames
for frame in dungeon_cache/walking_*.png; do
  python spells/dispel_background.py --input "$frame"
done

# 3. Create magical sprite sheet from transparent frames
python spells/create_pixel_spritesheet.py \
  --input "dungeon_cache/walking_*_dispelled.png" \
  --output "dungeon_cache/walking_spritesheet.png"
```

### With Image Processing Pipeline
```bash
# 1. Generate magical image
python spells/generate_sprite.py \
  --prompt "Character portrait" \
  --size "512x512" \
  --output "dungeon_cache/portrait.png"

# 2. Banish background
python spells/dispel_background.py \
  --input "dungeon_cache/portrait.png" \
  --model "u2net_human_seg"

# 3. Downscale for web
python spells/downscale_sprite.py \
  --input "dungeon_cache/portrait_dispelled.png" \
  --width 128 \
  --height 128
```

## Success Criteria

Background dispelling is successful when:
- Treasure PNG artifact is created with transparent background
- Foreground subject is preserved with arcane accuracy
- Background magical pixels are fully transparent
- Edge magical transitions are smooth (no jagged magical edges)
- Subject magical colors match input
- Dimensions match input (no magical resize occurs)
- Arcane knowledge accurately records ritual parameters
- Treasure artifact is a valid PNG with alpha magical channel
- No visual magical artifacts or corruption in subject

## Arcane Troubleshooting

### Poor Edge Detection
- **Problem**: Jagged magical edges or background artifacts
- **Recovery**: Try different crystal (u2net_human_seg for better magical edges)
- **Prevention**: Use higher resolution input magical images

### Subject Cut Off
- **Problem**: Part of subject is banished as background
- **Recovery**: Try different crystal or use u2net for general use
- **Prevention**: Ensure good magical contrast between subject and background

### Background Not Banished
- **Problem**: Background remains or partially transparent
- **Recovery**: Check crystal loaded correctly, try u2net crystal
- **Prevention**: Ensure distinct foreground/background magical separation

### Slow Ritual Casting
- **Problem**: Takes too long to complete ritual
- **Recovery**: Use u2netp crystal or downscale magical image first
- **Prevention**: Process smaller magical images or use lighter crystals

### Crystal Download Fails
- **Problem**: First ritual fails with astral connection error
- **Recovery**: Check astral connection, try again
- **Prevention**: Ensure stable astral connection for first ritual

### Treasure Has White Background
- **Problem**: Treasure has solid background instead of transparent
- **Recovery**: Verify artifact is PNG, check magical viewer supports transparency
- **Prevention**: Use magical image viewers that support alpha magical channel

## Best Practices

1. **Choose the right arcane crystal** - u2net for general use, specialized crystals for specific subjects
2. **Test with sample** - Process one magical image before batch ritual
3. **Check edge magical quality** - Zoom in to verify smooth magical transitions
4. **Preserve originals** - Don't delete input magical artifacts until you verify treasures
5. **Use appropriate magical resolution** - Higher resolution for better edge detection
6. **Review arcane knowledge** - Check crystal used and magical artifact size changes
7. **Handle first ritual** - Allow time for crystal download on initial use
8. **Batch ritual carefully** - Process smaller magical batches to manage mana
9. **Verify transparency** - Test treasure in your target magical application
10. **Iterate if needed** - Try different crystals if results aren't perfect

## Quick Reference

```bash
# Basic banishment
python spells/dispel_background.py --input "image.png"

# Custom treasure destination
python spells/dispel_background.py --input "image.png" --output "output.png"

# Specific arcane crystal
python spells/dispel_background.py --input "image.png" --model "u2net_human_seg"
```

## Magical Artifact Organization

### Recommended Dungeon Layout
```
dungeon_cache/
├── original/              # Original magical images with backgrounds
│   ├── character1.png
│   ├── character2.png
│   └── character3.png
├── dispelled/            # Background-dispelled magical images
│   ├── character1_dispelled.png
│   ├── character2_dispelled.png
│   └── character3_dispelled.png
└── arcane_knowledge/      # Ritual arcane knowledge
    ├── character1_dispel_metadata.json
    ├── character2_dispel_metadata.json
    └── character3_dispel_metadata.json
```

## Arcane Crystal Comparison

| Crystal | Size | Speed | Arcane Accuracy | Best For |
|---------|------|-------|------------------|----------|
| u2net | ~170MB | Medium | High | General purpose |
| u2netp | ~4MB | Fast | Good | Quick magical previews |
| u2net_human_seg | ~170MB | Medium | Very High (humans) | Portraits, adventurers |
| u2net_cloth_seg | ~170MB | Medium | High (clothing) | Fashion, costumes |
| silueta | ~5MB | Very Fast | Medium | Silhouettes, icons |

This ritual provides accurate arcane vision-powered background dispelling for PNG magical images!
