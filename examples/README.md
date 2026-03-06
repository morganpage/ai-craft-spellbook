# Examples Directory

This directory contains example scripts and sample files demonstrating the AI Craft Spellbook framework.

## Available Examples

### demo_script.py
A comprehensive demonstration script showcasing:
- Shared utility functions (format_bytes, format_duration)
- Performance tracking with metrics
- Standardized metadata generation
- Themed error handling
- Input validation

### Running the Demo

```bash
# From the project root directory
python examples/demo_script.py
```

This will display:
```
🧙 AI Craft Spellbook - Feature Demonstration

✓ Shared Utilities Demo
📊 Byte Formatting:
  500 bytes → 500.00 B
  1,024 bytes → 1.00 KB
  ...

✓ Performance Tracking Demo
⏳ Tracking spell execution...
📈 Performance Metrics:
  Spell: demo_spell
  Duration: 0.52s
  ...
```

## Test Fixtures

The `tests/fixtures/` directory contains sample files for testing:

- **sample.png** - Sample PNG image for testing image spells
- **sample.jpg** - Sample JPEG image
- **sample.mp3** - Sample MP3 audio file (when needed)
- **sample.wav** - Sample WAV audio file (when needed)

### Adding Test Fixtures

To add new test fixtures:

1. Place files in `tests/fixtures/`
2. Use them in your tests:

```python
import os
from pathlib import Path

FIXTURES_DIR = Path(__file__).parent / "fixtures"

def test_with_fixture():
    fixture_path = FIXTURES_DIR / "sample.png"
    # Use fixture_path in your test
```

## Example Spell Usage

### Audio Cleansing

```bash
# Basic usage
python spells/audio_cleanse.py --input examples/sample.mp3

# With custom settings
python spells/audio_cleanse.py \
  --input examples/sample.mp3 \
  --loudness -16 \
  --noise-strength medium \
  --log-level DEBUG
```

### Background Removal

```bash
# Basic usage
python spells/dispel_background.py --input examples/sample.png

# With alpha matting
python spells/dispel_background.py \
  --input examples/sample.png \
  --alpha-matting \
  --log-level DEBUG
```

## Creating Your Own Examples

To create your own example scripts:

1. Create a new file in `examples/your_example.py`
2. Import from the framework:
   ```python
   import sys
   sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

   from spells.utils.common import (
       save_metadata,
       validate_input_file,
       # ... other utilities
   )
   ```
3. Document what your example demonstrates
4. Add usage instructions to this README

## Notes

- All example scripts should be runnable from the project root
- Keep examples simple and focused on specific features
- Include comments explaining what's happening
- Use the D&D theme in output messages
