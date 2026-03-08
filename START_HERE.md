# New User Quick Start Guide

Start using the AI Craft Spellbook in 3 simple steps!

## 📋 Step 1: Get Started

1. **Clone the repository**
    ```bash
    git clone https://github.com/morganpage/ai-craft-spellbook.git
    cd ai-craft-spellbook
    ```
2. **Install Claude Code** (if you haven't already)
   ```bash
   # Via npm
   npm install -g @anthropic-ai/claude-code

   # Or via Python
   pip install claude-code
   ```

3. **Install spell dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## 🎤 Step 2: Start Claude Code

```bash
claude
```

## ⚡ Step 3: Speak Naturally!

Now just say what you want:

### For Audio:
```
You: Cleanse audio in podcast.mp3
Claude: I'll cleanse the audio in podcast.mp3 for you.
[Executes the spell automatically]
Claude: Ritual completed! Your purified artifact is at dungeon_cache/podcast_purified.mp3
```

### For Images:
```
You: Remove background from character.png
Claude: I'll dispel the background from character.png.
[Executes the spell automatically]
Claude: Background dispelled! Your artifact is at dungeon_cache/character_dispelled.png
```

### For Splitting Images:
```
You: Split landscape.png into two halves
Claude: I'll split landscape.png into two equal halves based on its orientation.
[Executes the spell automatically]
Claude: Artifact split successfully! Left half: dungeon_cache/landscape_left.png, Right half: dungeon_cache/landscape_right.png
```

### For Resizing Images:
```
You: Resize character.png to 512x512
Claude: I'll transmute character.png to 512x512 dimensions.
[Executes the spell automatically]
Claude: Transmutation complete! Your resized artifact is at dungeon_cache/character_resized.png
```

### For Blurring Images:
```
You: Blur photo.jpg
Claude: I'll obscure photo.jpg with a Gaussian blur ritual.
[Executes the spell automatically]
Claude: Obscuration complete! Your artifact is at dungeon_cache/photo_obscured.jpg
```

### For Creating Animated GIFs:
```
You: Create gif from frames/
Claude: I'll weave those magical panels into an animated scroll.
[Executes the spell automatically]
Claude: Animation ritual complete! Your scroll is at frames_animated.gif
```

## 📚 What Just Happened

You didn't need to:
- ❌ Remember any command-line syntax
- ❌ Look up spell parameters
- ❌ Read documentation first
- ❌ Write any Python code

Claude Code automatically:
- ✅ Understood your natural language
- ✅ Found the right spell
- ✅ Read the quest guide
- ✅ Executed with correct parameters
- ✅ Showed you the results

## 🎯 More Examples

See [EXAMPLES.md](EXAMPLES.md) for complete sessions with dialogue!

**That's it - you're ready to cast spells!** 🧙‍♂️✨
