# AI Craft Spellbook Framework

A Dungeons & Dragons themed AI workflow automation framework that separates probabilistic AI reasoning from deterministic magical spell execution.

> **New here?** Start with [START_HERE.md](START_HERE.md) for a 3-step quick start guide!

## ⚡ Quick Examples

Start using AI Craft Spellbook immediately with these natural language commands in Claude Code:

| What You Say | What Happens |
|---------------|---------------|
| "Cleanse audio in podcast.mp3" | Runs audio cleansing ritual |
| "Remove background from character.png" | Casts dispel background hex |
| "Purify my video.mp4" | Cleanses audio in video file |
| "Dispel background on sprite.png with human model" | Uses u2net_human_seg crystal |

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
dungeon_cache/   # Temporary treasures - intermediate processing files
.env             # Arcane keys - your API keys and secrets
AI_CRAFT_SPELLBOOK.md  # Agent framework instructions
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

## 📜 Available Spells

### Audio Cleansing Ritual (`audio_cleanse.py`)
Purify audio artifacts by removing impurities, banishing void moments, and balancing magical loudness.

**Perfect for:**
- Podcast recordings
- Video audio tracks
- Content distribution prep
- Noisy environments

```bash
python spells/audio_cleanse.py --input recording.mp3 --output purified.mp3
```

See [quests/audio_cleanse.md](quests/audio_cleanse.md) for full quest guide.

### Dispel Background Hex (`dispel_background.py`)
Banish unwanted backgrounds from magical image artifacts using arcane vision.

**Perfect for:**
- Game asset preparation
- UI element creation
- Sprite sheet generation
- Image extraction

```bash
python spells/dispel_background.py --input character.png --output character_no_bg.png
```

See [quests/dispel_background.md](quests/dispel_background.md) for full quest guide.

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- FFmpeg (for audio cleansing rituals)
- Required Python packages (install per spell documentation)

### Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/ai-craft-spellbook.git
cd ai-craft-spellbook
```

2. Install spell dependencies:
```bash
# For audio cleansing
pip install ffmpeg-python

# For background dispelling
pip install rembg pillow
```

3. Configure your arcane keys:
```bash
cp .env.example .env
# Edit .env with your API keys
```

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

Claude Code will:
1. Read the appropriate quest log from `quests/`
2. Check the spell in `spells/`
3. Invoke the spell with the correct parameters
4. Show you the results

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
```

### What Claude Code Can Do

- Read and understand quest logs in `quests/`
- Execute spells from `spells/` with appropriate parameters
- Debug spell fumbles by reading error traces
- Create new spells following the D&D theme
- Update quest logs with discoveries and fixes
- Coordinate complex multi-step rituals

### Best Practices

- Be specific about which quest and spell you're working with
- Provide actual file paths when invoking spells
- Let Claude read the quest log before making changes
- Ask Claude to explain what it's doing before it executes

## 🧙 Creating Your Own Spells

Want to craft your own magical incantations? Here's how:

### Step 1: Plan Your Spell

Decide what magical transformation you want to perform:
- What inputs does it need? (images, audio, text, etc.)
- What transformation should happen? (process, transform, extract)
- What outputs should it produce? (files, data, metadata)

### Step 2: Create the Spell

Create a Python file in the `spells/` directory:
```bash
# Example: spells/my_spell.py
touch spells/my_spell.py
```

Follow the spell template shown in [AI_CRAFT_SPELLBOOK.md](AI_CRAFT_SPELLBOOK.md#creating-new-spells) for structure and theming.

### Step 3: Create the Quest Log

Create a corresponding Markdown file in `quests/`:
```bash
# Example: quests/my_spell.md
touch quests/my_spell.md
```

Write the quest following the template in [AI_CRAFT_SPELLBOOK.md](AI_CRAFT_SPELLBOOK.md#creating-new-spells).

### Step 4: Test Your Spell

Test it manually first:
```bash
python spells/my_spell.py --help  # Check your parameters
python spells/my_spell.py --input test_file.png  # Try it out
```

### Step 5: Let AI Help

Use Claude Code to:
- Review your spell for bugs
- Check theme consistency
- Improve error handling
- Add tests (if desired)

## ⚡ Quick Reference

- **[EXAMPLES.md](EXAMPLES.md)** - Complete natural language examples with sample sessions
- **[QUICKSTART.md](QUICKSTART.md)** - Concise command reference
- **[quests/audio_cleanse.md](quests/audio_cleanse.md)** - Audio cleansing quest guide
- **[quests/dispel_background.md](quests/dispel_background.md)** - Background dispelling quest guide

### Spell Reference

| Spell | Purpose | Input | Output | Use Case |
|--------|---------|--------|----------|
| audio_cleanse | Purify audio | MP3/MP4 | Podcasts, videos |
| dispel_background | Remove background | PNG | Sprites, assets |

### Command Quick Reference

```bash
# Clean audio
python spells/audio_cleanse.py --input file.mp3 --output clean.mp3

# Remove background
python spells/dispel_background.py --input image.png --output clean.png

# List all spells
ls spells/

# Read a quest
cat quests/audio_cleanse.md
```

## 🤝 Contributing

We welcome contributions from fellow magical practitioners!

### How to Contribute

1. **Fork the repository** on GitHub
2. **Create a new branch** for your feature:
   ```bash
   git checkout -b feat/my-new-spell
   ```
3. **Create your spell** following the guidelines in [AI_CRAFT_SPELLBOOK.md](AI_CRAFT_SPELLBOOK.md)
4. **Create the quest log** with full documentation
5. **Test thoroughly** - verify your spell works with various inputs
6. **Commit your changes** with a clear message:
   ```bash
   git add spells/my_spell.py quests/my_spell.md
   git commit -m "Add transmute image spell with quest log"
   ```
7. **Push and create a pull request** describing your contribution

### Contribution Guidelines

- Keep the D&D theme consistent (quests, spells, artifacts, treasures)
- Write clear, comprehensive quest logs
- Include error handling for all spell fumbles
- Document any new dependencies in `requirements.txt`
- Update this README with new spell descriptions
- Test with real files before submitting

### What We're Looking For

- New spells for common automation tasks
- Improvements to existing spells
- Bug fixes and error handling
- Documentation improvements
- Quest log enhancements

## 📄 License

[Your License Here]

## 🙏 Acknowledgments

Inspired by the philosophy that AI should handle reasoning while code handles execution—just as a Dungeon Master guides adventurers through their quests, leaving the actual spell-casting to the specialists.

## 📚 Additional Resources

- [AI_CRAFT_SPELLBOOK.md](AI_CRAFT_SPELLBOOK.md) - Complete agent instructions
- [QUICKSTART.md](QUICKSTART.md) - Concise command reference
- [quests/](quests/) - Detailed quest guides for each spell
