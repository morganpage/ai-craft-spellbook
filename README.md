# AI Craft Spellbook Framework

A Dungeons & Dragons themed AI workflow automation framework that separates probabilistic AI reasoning from deterministic magical spell execution.

**Version 2.0.0** - Enhanced with testing infrastructure, batch processing, structured logging, and comprehensive error handling!

> **New here?** Start with [START_HERE.md](START_HERE.md) for a 3-step quick start guide!

## ⚡ Quick Examples

Start using AI Craft Spellbook immediately with these natural language commands in Claude Code:

| What You Say | What Happens |
|---------------|---------------|
| "Cleanse audio in podcast.mp3" | Runs audio cleansing ritual |
| "Remove background from character.png" | Casts dispel background hex |
| "Purify my video.mp4" | Cleanses audio in video file |
| "Dispel background on sprite.png with human model" | Uses u2net_human_seg crystal |
| "Process all images in sprites/ with batch mode" | Batch processes multiple files |
| "Cleanse audio with debug logging" | Runs with detailed logging |

Simply type these commands in Claude Code and watch the magic happen!

## 🎭 The Concept

AI Craft Spellbook transforms mundane software automation into an epic adventure:
- **Quest Logs** (adventure guides) define what needs to be done
- **Dungeon Master** (Claude Code) orchestrates intelligent decision-making
- **Spells** (deterministic scripts) handle actual magical execution

This separation ensures reliability: while AI reasoning is probabilistic (~90% accurate per step), combining five steps would drop to 59% success. By offloading execution to deterministic spells, we maintain accuracy and focus AI on what it does best—strategy and orchestration.

For complete agent instructions, see [AI_CRAFT_SPELLBOOK.md](AI_CRAFT_SPELLBOOK.md).

## 🏰 Architecture

```
quests/          # Quest logs - your adventure guides (Markdown)
spells/          # Spell scrolls - magical execution scripts (Python)
  ├── utils/     # Shared magical utilities
tests/           # Test suite - verify spell functionality
examples/        # Sample files for testing
dungeon_cache/   # Temporary treasures - intermediate processing files
logs/            # Spell logs - detailed execution records
.env             # Arcane keys - your API keys and secrets
AI_CRAFT_SPELLBOOK.md  # Agent framework instructions
CONTRIBUTING.md  # Development guide
```

### Layer 1: Quest Logs (The Adventure Guides)
Markdown documents stored in `quests/` that define:
- Quest objectives
- Required reagents (inputs)
- Which spells to cast
- Expected treasures (outputs)
- How to handle magical complications

### Layer 2: Dungeon Master (The Storyteller)
The AI agent (Claude Code) responsible for intelligent party coordination:
- Reading quest logs
- Invoking spells in correct sequence
- Recovering from spell fumbles
- Learning and leveling up

### Layer 3: Spells (The Arcane Arsenal)
Python scripts in `spells/` that execute deterministically:
- Magical invocations (API calls)
- Alchemical transformations (data processing)
- Tome operations (file manipulation)
- Arcane knowledge queries (database lookups)

### Layer 4: Shared Utilities (New in v2.0)
The `spells/utils/` package provides:
- **Input validation** - File format, size, and permission checks
- **Output sanitization** - Path validation and security
- **Structured logging** - Themed log messages with configurable levels
- **Performance tracking** - Duration and size metrics
- **Error handling** - Themed exceptions with recovery suggestions
- **Dependency checking** - Runtime verification of required tools

## 📜 Available Spells

### Audio Cleansing Ritual (`audio_cleanse.py`)
Purify audio artifacts by removing impurities, banishing void moments, and balancing magical loudness.

**Perfect for:**
- Podcast recordings
- Video audio tracks
- Content distribution prep
- Noisy environments

**Features:**
- Silence removal with configurable thresholds
- Audio normalization to target LUFS
- Noise reduction (light/medium/heavy)
- Video audio track support
- Structured logging and performance tracking
- Comprehensive error handling

```bash
# Basic usage
python spells/audio_cleanse.py --input recording.mp3 --output purified.mp3

# With custom settings
python spells/audio_cleanse.py --input podcast.wav \
  --silence-threshold -50 \
  --loudness -16 \
  --noise-strength heavy

# With debug logging
python spells/audio_cleanse.py --input audio.mp3 \
  --log-level DEBUG \
  --log-file logs/audio_cleanse.log
```

See [quests/audio_cleanse.md](quests/audio_cleanse.md) for full quest guide.

### Dispel Background Hex (`dispel_background.py`)
Banish unwanted backgrounds from magical image artifacts using arcane vision.

**Perfect for:**
- Game asset preparation
- UI element creation
- Sprite sheet generation
- Image extraction

**Features:**
- Multiple model support (u2net, u2netp, u2net_human_seg, etc.)
- Alpha matting for cleaner edges
- Batch processing with glob patterns
- Structured logging and performance tracking
- Comprehensive error handling

```bash
# Basic usage
python spells/dispel_background.py --input character.png --output character_no_bg.png

# With alpha matting
python spells/dispel_background.py --input photo.png \
  --alpha-matting \
  --model u2net_human_seg

# Batch processing
python spells/dispel_background.py \
  --batch \
  --input "sprites/*.png" \
  --output-dir sprites_no_bg/

# With debug logging
python spells/dispel_background.py --input image.png \
  --log-level DEBUG \
  --log-file logs/dispel_background.log
```

See [quests/dispel_background.md](quests/dispel_background.md) for full quest guide.

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- FFmpeg (for audio cleansing rituals)
  - macOS: `brew install ffmpeg`
  - Linux: `sudo apt-get install ffmpeg`
  - Windows: Download from [ffmpeg.org](https://ffmpeg.org/download.html)

### Installation

1. **Clone this repository:**
```bash
git clone https://github.com/morganpage/ai-craft-spellbook.git
cd ai-craft-spellbook
```

2. **Create a virtual environment:**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install spell dependencies:**
```bash
# Install all dependencies (including testing tools)
pip install -r requirements.txt

# Or install only core dependencies
pip install rembg Pillow python-dateutil
```

4. **Configure your arcane keys:**
```bash
cp .env.example .env
# Edit .env with your API keys and configuration
```

5. **Verify installation:**
```bash
# Run tests to verify everything works
pytest -v

# Check spell availability
python spells/audio_cleanse.py --help
python spells/dispel_background.py --help
```

### Development Setup

For contributors and those wanting to run tests:

```bash
# Install development dependencies
pip install -r requirements.txt

# Run tests
pytest -v

# Run tests with coverage
pytest --cov=spells --cov-report=html

# Check code style
flake8 spells/
black --check spells/

# Type checking
mypy spells/
```

See [CONTRIBUTING.md](CONTRIBUTING.md) for complete development guide.

### First Adventure

1. Read the framework documentation in [AI_CRAFT_SPELLBOOK.md](AI_CRAFT_SPELLBOOK.md)
2. Choose a quest from the `quests/` directory
3. Follow the quest guide to invoke the appropriate spell
4. Collect your treasures from `dungeon_cache/`

## 🤖 Using Claude Code

Claude Code is your Dungeon Master for this framework.

### Natural Language Commands

Claude Code understands natural language requests like:
- "Cleanse audio in my_file.mp3"
- "Remove background from image.png"
- "Purify podcast and make it -16 LUFS"
- "Use the human model to dispel background from portrait.png"
- "Batch process all PNGs in the sprites directory"
- "Run audio cleanse with debug logging enabled"

Claude Code will:
1. Read the appropriate quest log from `quests/`
2. Check the spell in `spells/`
3. Invoke the spell with the correct parameters
4. Show you the results and any errors

### Why Natural Language Works

Claude Code is designed to understand your intent and execute the right commands. When you say:
> "Cleanse audio in podcast.mp3"

Claude Code automatically:
1. ✅ Recognizes "Cleanse audio" → `audio_cleanse` spell
2. ✅ Identifies `podcast.mp3` as the input reagent
3. ✅ Reads `quests/audio_cleanse.md` to understand the ritual
4. ✅ Executes: `python spells/audio_cleanse.py --input podcast.mp3`
5. ✅ Shows you the magical results

No need to remember exact command syntax—just speak naturally!

### Installation

```bash
# Install Claude Code CLI
npm install -g @anthropic-ai/claude-code

# Or via Python
pip install claude-code
```

### Basic Usage

```bash
# Start Claude Code in your project
cd ai-craft-spellbook
claude

# Ask Claude to help with tasks:
- "Read the audio cleanse quest and cast the spell on podcast.mp3"
- "Help me create a new spell to resize images"
- "Fix the dispel background spell - it's failing on large images"
- "Batch process all sprites with background removal"
- "Run the test suite and show me the results"
```

### What Claude Code Can Do

- Read and understand quest logs in `quests/`
- Execute spells from `spells/` with appropriate parameters
- Debug spell fumbles by reading error traces
- Create new spells following the D&D theme
- Update quest logs with discoveries and fixes
- Coordinate complex multi-step rituals
- Run tests and validate changes
- Review code for theme consistency

### Best Practices

- Be specific about which quest and spell you're working with
- Provide actual file paths when invoking spells
- Let Claude read the quest log before making changes
- Ask Claude to explain what it's doing before it executes
- Use logging flags when debugging issues

## 🧪 Testing (New in v2.0)

The framework includes a comprehensive test suite:

```bash
# Run all tests
pytest -v

# Run specific test file
pytest tests/test_utils.py -v

# Run with coverage report
pytest --cov=spells --cov-report=html

# Run only unit tests (skip integration tests)
pytest -v -m "not integration"

# Run with verbose output
pytest -vv -s
```

### Test Structure

- `tests/test_utils.py` - Tests for shared utilities
- `tests/test_audio_cleanse.py` - Tests for audio cleansing spell
- `tests/test_dispel_background.py` - Tests for background removal spell
- `tests/fixtures/` - Sample test files

## 📊 Logging & Debugging (New in v2.0)

All spells now support structured logging:

```bash
# Enable debug logging
python spells/audio_cleanse.py --input file.mp3 --log-level DEBUG

# Log to file
python spells/dispel_background.py --input image.png \
  --log-file logs/spell.log

# Both console and file logging
python spells/audio_cleanse.py --input file.mp3 \
  --log-level DEBUG \
  --log-file logs/debug.log
```

### Log Levels

- **ARCANE (DEBUG)** - Detailed diagnostic information
- **SPELL (INFO)** - General informational messages (default)
- **WARNING** - Warning messages for potential issues
- **FUMBLE (ERROR)** - Error messages when spells fail
- **CRITICAL** - Critical errors that prevent spell execution

### Log Files

Logs are stored in the `logs/` directory (automatically created):
- `logs/audio_cleanse.log` - Audio cleansing spell logs
- `logs/dispel_background.log` - Background removal spell logs
- Custom paths can be specified with `--log-file`

## 🎯 Performance Tracking (New in v2.0)

All spells automatically track performance metrics:

```json
{
  "performance": {
    "duration_seconds": 2.45,
    "input_size_bytes": 12345678,
    "output_size_bytes": 9876543
  }
}
```

Performance data is included in all metadata files and logged during execution.

## 🔒 Error Handling (New in v2.0)

Enhanced error handling with themed messages:

```bash
# Spell fumble with recovery suggestion
✗ Spell Fumble: audio_cleanse
  Error Type: InvalidReagentError
  Details: Artifact not found: podcast.mp3
  Recovery: Check that the file path is correct and the file exists.
```

### Error Types

- **SpellFumbleError** - General spell failures
- **InvalidReagentError** - Invalid inputs or parameters
- **ArcaneDisruptionError** - External system failures (FFmpeg, rembg, etc.)

## 🧙 Creating Your Own Spells

Want to craft your own magical incantations? Here's how:

### Quick Start

1. **Plan your spell** - What inputs, transformation, and outputs?
2. **Use shared utilities** - Import from `spells.utils.common`
3. **Follow the template** - Use the spell template in [CONTRIBUTING.md](CONTRIBUTING.md)
4. **Create quest log** - Document in `quests/your_spell.md`
5. **Write tests** - Add tests in `tests/test_your_spell.py`
6. **Test thoroughly** - Verify with various inputs

### Using Shared Utilities

All new spells should use the shared utilities:

```python
from spells.utils.common import (
    save_metadata,
    validate_input_file,
    validate_output_path,
    get_spell_metadata_base,
    setup_logging,
    get_logger,
    PerformanceTracker,
)
from spells.utils.error_handling import (
    SpellFumbleError,
    ArcaneDisruptionError,
    InvalidReagentError,
    handle_spell_error,
)
```

See [CONTRIBUTING.md](CONTRIBUTING.md) for complete spell creation guide.

## ⚡ Quick Reference

### Documentation

- **[AI_CRAFT_SPELLBOOK.md](AI_CRAFT_SPELLBOOK.md)** - Complete agent instructions
- **[CONTRIBUTING.md](CONTRIBUTING.md)** - Development and contribution guide
- **[CHANGELOG.md](CHANGELOG.md)** - Version history and changes
- **[quests/audio_cleanse.md](quests/audio_cleanse.md)** - Audio cleansing quest guide
- **[quests/dispel_background.md](quests/dispel_background.md)** - Background dispelling quest guide

### Spell Reference

| Spell | Purpose | Input | Output | Features |
|--------|---------|--------|----------|----------|
| audio_cleanse | Purify audio | MP3/WAV/MP4 | Cleansed audio | Silence removal, normalization, noise reduction, logging |
| dispel_background | Remove background | PNG/JPG | Transparent PNG | Multiple models, batch processing, alpha matting, logging |

### Command Quick Reference

```bash
# Clean audio
python spells/audio_cleanse.py --input file.mp3 --output clean.mp3

# Remove background
python spells/dispel_background.py --input image.png --output clean.png

# Batch process
python spells/dispel_background.py --batch --input "*.png" --output-dir output/

# With logging
python spells/audio_cleanse.py --input file.mp3 --log-level DEBUG --log-file debug.log

# List all spells
ls spells/

# Read a quest
cat quests/audio_cleanse.md

# Run tests
pytest -v

# Run tests with coverage
pytest --cov=spells --cov-report=html
```

## 🤝 Contributing

We welcome contributions from fellow magical practitioners!

### How to Contribute

1. Read [CONTRIBUTING.md](CONTRIBUTING.md) for complete guidelines
2. Fork the repository and create a feature branch
3. Create your spell following the development guide
4. Write tests for your spell
5. Ensure all tests pass: `pytest -v`
6. Check code style: `flake8 spells/` and `black --check spells/`
7. Update documentation (README, quest logs)
8. Submit a pull request

### Contribution Guidelines

- Follow the D&D theme (quests, spells, artifacts, treasures)
- Use shared utilities from `spells.utils`
- Write comprehensive tests
- Include error handling for all spell fumbles
- Document dependencies in `requirements.txt`
- Update README with new spell descriptions
- Test with real files before submitting

### What We're Looking For

- New spells for common automation tasks
- Improvements to existing spells
- Bug fixes and error handling
- Test coverage improvements
- Documentation enhancements
- Performance optimizations

## 📄 License

[Your License Here]

## 🙏 Acknowledgments

Inspired by the philosophy that AI should handle reasoning while code handles execution—just as a Dungeon Master guides adventurers through their quests, leaving the actual spell-casting to the specialists.

## 📚 Additional Resources

- [AI_CRAFT_SPELLBOOK.md](AI_CRAFT_SPELLBOOK.md) - Complete agent instructions
- [CONTRIBUTING.md](CONTRIBUTING.md) - Development guide
- [CHANGELOG.md](CHANGELOG.md) - Version history
- [quests/](quests/) - Detailed quest guides for each spell

---

**Version 2.0.0** - Enhanced with testing, batch processing, logging, and comprehensive error handling! ✨
