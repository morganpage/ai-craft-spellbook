# Audio Cleansing Ritual

## Quest Objective

Purify magical media artifacts by banishing impurities, removing void moments of silence, and balancing magical loudness energies. This ritual produces cleaner, more consistent audio treasures for podcast recordings, video soundtracks, and distribution platforms.

## When to Cast This Spell

- Cleansing podcast recordings
- Purifying video audio soundtracks
- Preparing treasures for YouTube/Spotify distribution
- Banishing awkward voids from recordings
- Reducing background magical hum after energy balancing

## Required Spell Components

- Arcane Audio Processor installed on system (`ffmpeg -version`)
- Input magical artifact: MP3 (audio only) or MP4 (visual + audio)

## Spell to Cast

```bash
python spells/audio_cleanse.py --input <artifact> --output <artifact>
```

## Required Reagents

| Input | Description | Example |
|-------|-------------|---------|
| `--input` | Path to magical media artifact | `recording.mp4` |

## Optional Spell Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| `--output` | `<name>_purified.<ext>` | Path to purified artifact |
| `--silence-threshold` | `-40` | dB threshold for void detection |
| `--silence-duration` | `0.5` | Minimum void seconds to banish |
| `--silence-padding` | `0.3` | Magical buffer at segment boundaries (seconds) |
| `--loudness` | `-14` | Target LUFS (-23 broadcast, -16 podcast, -14 YouTube/Spotify) |
| `--no-silence-removal` | false | Skip void banishment |
| `--no-normalize` | false | Skip energy balancing |
| `--no-noise-reduction` | false | Skip purification magic (enabled by default) |
| `--noise-strength` | `light` | Purification: light, medium, heavy |

## Ritual Steps

### Step 1: Purification (First Casting)

- Uses Arcane Audio Processor `afftdn` enchantment (FFT-based denoiser)
- Best for constant hum, buzz, background magical noise
- Channeled **before** energy balancing to avoid amplifying impurities
- Strength settings:
  - `light`: nr=10, nf=-40 (subtle, preserves magical quality)
  - `medium`: nr=20, nf=-35 (balanced)
  - `heavy`: nr=30, nf=-30 (aggressive, may affect vocal incantations)

### Step 2: Void Banishment (Second Casting)

- Uses Arcane Audio Processor `silenceremove` enchantment
- Banishes all void periods throughout the artifact (not just start/end)
- Threshold: -40dB (moderate - banishes quiet background magical noise)
- Minimum duration: 0.5 seconds (shorter magical pauses preserved)

### Step 3: Energy Balancing (Third Casting)

- Uses Arcane Audio Processor `loudnorm` enchantment (EBU R128 standard)
- Target: -14 LUFS (YouTube/Spotify standard)
- True peak: -1.5 dB (prevents magical distortion)
- LRA: 11 (reasonable magical dynamic range)

### MP4 Artifact Handling

- Visual magic stream is preserved (copied without re-enchantment)
- Audio is re-enchanated to AAC 192kbps
- Audio track is replaced with purified version

### MP3 Artifact Handling

- Audio is re-enchanated to MP3 192kbps

## Magical Treasures

1. **Purified media artifact** - Cleansed audio/visual treasure
2. **Arcane knowledge tome** - Ritual stats and before/after magical comparison

## Ritual Examples

### Basic casting (purification + void banishment + energy balancing)
```bash
python spells/audio_cleanse.py --input podcast.mp3
```

### Specify treasure destination
```bash
python spells/audio_cleanse.py --input raw_video.mp4 --output final_video.mp4
```

### Podcast settings (different magical loudness)
```bash
python spells/audio_cleanse.py --input podcast.mp3 --loudness -16
```

### Medium purification for noisier artifacts
```bash
python spells/audio_cleanse.py --input interview.mp4 --noise-strength medium
```

### Energy balance only (keep magical pauses, skip purification)
```bash
python spells/audio_cleanse.py --input interview.mp4 --no-silence-removal --no-noise-reduction
```

### Banish voids only (no energy balancing, no purification)
```bash
python spells/audio_cleanse.py --input raw.mp3 --no-normalize --no-noise-reduction
```

### Aggressive void banishment
```bash
python spells/audio_cleanse.py --input lecture.mp4 --silence-threshold -30 --silence-duration 0.3
```

## Expected Magical Output

```
Ritual completed successfully!
Artifact: /path/to/input.mp4
Purified: /path/to/output.mp4
Duration: 120.45s -> 98.32s
Void banished: 22.13s (18.38%)
Purification strength: light
Arcane knowledge: /path/to/purification_metadata.json
```

## Spell Fumble Recovery

| Spell Fumble | Cause | Recovery |
|--------------|-------|----------|
| `Artifact not found` | Input path doesn't exist | Verify artifact path |
| `Artifact has no audio stream` | Visual magic with no audio | Check artifact has audio track |
| `Arcane Audio Processor processing failed` | Corrupted input or enchantment issue | Try different input artifact |
| `Silence threshold must be negative` | Invalid dB value | Use negative value (e.g., -40) |
| `Noise strength must be one of` | Invalid purification strength | Use: light, medium, or heavy |

## Arcane Notes

- Ritual time depends on artifact length (typically 1-2x real-time)
- Original artifact is never modified
- For visual magic artifacts, only audio is re-enchanated (visual magic is copied)
- Void banishment may affect natural magical pauses in speech - adjust `--silence-duration` if needed
- `--silence-padding` (default 0.3s) preserves audio around detected voids to avoid cutting off magical sibilant sounds
- Purification magic is enabled by default - use `--no-noise-reduction` to disable
- For heavy background magical noise, try `--noise-strength medium` first before `heavy`
- For broadcast: use `--loudness -23`
- For podcasts: use `--loudness -16`
- For YouTube/Spotify: use `--loudness -14` (default)

## Arcane Discoveries

_This section is updated when spell fumbles are encountered and resolved._

- None yet - will be populated as the spell is used in production
