# AI Craft Spellbook - Contribution Guide

Welcome, brave adventurer! This guide will help you contribute new spells and improvements to the AI Craft Spellbook framework.

## Table of Contents

1. [Getting Started](#getting-started)
2. [Development Setup](#development-setup)
3. [Adding New Spells](#adding-new-spells)
4. [Code Style Guidelines](#code-style-guidelines)
5. [Testing Requirements](#testing-requirements)
6. [Documentation Standards](#documentation-standards)
7. [Pull Request Process](#pull-request-process)

---

## Getting Started

### Prerequisites

- Python 3.8 or higher
- FFmpeg (for audio/video spells)
- Git
- A text editor or IDE

### First-Time Setup

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd ai-craft-spellbook
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Copy environment template:**
   ```bash
   cp .env.example .env
   # Edit .env with your API keys and configuration
   ```

5. **Run tests to verify setup:**
   ```bash
   pytest -v
   ```

---

## Development Setup

### Recommended Tools

- **Code Editor:** VS Code, PyCharm, or your preferred editor
- **Linter:** `flake8` for code quality
- **Formatter:** `black` for code formatting
- **Type Checker:** `mypy` for static type checking

### Pre-commit Hooks (Optional)

Install pre-commit hooks for automated code quality checks:

```bash
pip install pre-commit
pre-commit install
```

### Running Tests

Run all tests:
```bash
pytest -v
```

Run specific test file:
```bash
pytest tests/test_utils.py -v
```

Run with coverage:
```bash
pytest --cov=spells --cov-report=html
```

Run only unit tests (skip integration tests):
```bash
pytest -v -m "not integration"
```

---

## Adding New Spells

### Step 1: Plan Your Spell

Before coding, create a quest log in `quests/`:

```markdown
# Spell Name

## Quest Objective
[D&D themed description of what this spell accomplishes]

## When to Cast This Spell
[Use cases in D&D theme]

## Required Spell Components
[Prerequisites and dependencies]

## Spell to Cast
```bash
python spells/your_spell.py --input <artifact>
```

## Required Reagents
[Input parameters table]

## Expected Magical Treasures
[Output description]

## Spell Fumble Recovery
[Error handling table]
```

### Step 2: Create the Spell File

Create your spell in `spells/your_spell.py`:

```python
import argparse
import os
import sys
from typing import Dict, Any, Optional

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.common import (
    save_metadata,
    validate_input_file,
    validate_output_path,
    get_spell_metadata_base,
    setup_logging,
    get_logger,
    PerformanceTracker,
)
from utils.error_handling import (
    SpellFumbleError,
    ArcaneDisruptionError,
    InvalidReagentError,
    handle_spell_error,
)


def your_spell_function(
    input_path: str,
    output_path: Optional[str] = None,
    # ... other parameters
    logger: Optional[Any] = None,
) -> Dict[str, Any]:
    """Brief D&D themed description of what this spell does.

    This detailed description explains the magical transformation
    that will be performed on the artifact.

    Args:
        input_path: Technical description of input
        output_path: Technical description of output
        logger: Optional logger instance

    Returns:
        Dict containing arcane knowledge (metadata)

    Raises:
        InvalidReagentError: If input validation fails
        ArcaneDisruptionError: If the ritual fails during casting
    """
    # Set up logger if not provided
    if logger is None:
        logger = get_logger("your_spell")

    # Validate input file
    logger.info(f"Validating artifact: {input_path}")
    validation = validate_input_file(
        input_path,
        allowed_formats={".png", ".jpg"},  # Your formats
        max_size_bytes=50 * 1024 * 1024,  # 50MB
    )

    # Determine output path
    if output_path is None:
        original_name = os.path.splitext(os.path.basename(input_path))[0]
        output_dir = os.path.dirname(input_path) or "dungeon_cache"
        output_path = os.path.join(output_dir, f"{original_name}_transformed.png")

    # Validate output path
    output_path = validate_output_path(
        output_path,
        check_writable=True,
        create_parent_dirs=True,
    )

    # Set up performance tracking
    tracker = PerformanceTracker("your_spell")
    tracker.set_input_size(validation["size_bytes"])
    tracker.start()

    try:
        # YOUR SPELL LOGIC HERE
        logger.info("Channeling magical transformation...")

        # Process the file
        # ...

        tracker.stop()
        logger.info("Ritual completed successfully!")

        # Build metadata
        metadata = get_spell_metadata_base("your_spell")
        metadata.update({
            "input_path": input_path,
            "output_path": output_path,
            # Add your specific metadata
        })
        metadata["performance"] = tracker.get_metrics()

        return metadata

    except Exception as e:
        if isinstance(e, (InvalidReagentError, ArcaneDisruptionError)):
            raise
        raise SpellFumbleError(
            f"Unexpected magical failure: {e}",
            recovery_suggestion="Check the error details and try again."
        )


def main():
    parser = argparse.ArgumentParser(
        description="Technical, user-friendly description",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument("--input", "-i", required=True, help="Input file path")
    parser.add_argument("--output", "-o", help="Output file path")
    parser.add_argument(
        "--log-level",
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        default="INFO",
        help="Logging level (default: INFO)"
    )

    args = parser.parse_args()

    # Set up logging
    logger = setup_logging(
        "your_spell",
        log_level=args.log_level,
    )

    try:
        metadata = your_spell_function(
            input_path=args.input,
            output_path=args.output,
            logger=logger,
        )

        # Save metadata
        original_name = os.path.splitext(os.path.basename(args.input))[0]
        metadata_dir = os.path.dirname(metadata["output_path"]) or "dungeon_cache"
        metadata_path = os.path.join(
            metadata_dir, f"{original_name}_spell_metadata.json"
        )
        save_metadata(metadata, metadata_path)

        # Print success
        print(f"\n✓ Spell completed successfully!")
        print(f"  Input: {metadata['input_path']}")
        print(f"  Output: {metadata['output_path']}")
        print(f"  Duration: {metadata['performance']['duration_seconds']:.2f}s")
        print(f"  Arcane knowledge: {metadata_path}")

    except Exception as e:
        handle_spell_error(e, "your_spell", exit_on_error=True)


if __name__ == "__main__":
    main()
```

### Step 3: Create Tests

Create `tests/test_your_spell.py`:

```python
"""
Tests for the your_spell spell.
"""

import os
import sys
import pytest

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from spells.your_spell import your_spell_function


@pytest.fixture
def sample_input(tmp_path):
    """Create a sample input file."""
    input_file = tmp_path / "input.png"
    # Create your test file
    return str(input_file)


def test_your_spell_basic(sample_input):
    """Test basic spell functionality."""
    metadata = your_spell_function(
        input_path=sample_input,
    )

    assert "input_path" in metadata
    assert "output_path" in metadata
    assert "performance" in metadata


def test_your_spell_invalid_input():
    """Test that invalid input raises error."""
    from spells.utils.error_handling import InvalidReagentError

    with pytest.raises(InvalidReagentError):
        your_spell_function(
            input_path="/nonexistent/file.png"
        )
```

### Step 4: Update Documentation

Add your spell to `README.md`:

```markdown
### Your Spell Name

Technical description of what the spell does.

```bash
python spells/your_spell.py --input <file>
```

**Quest Log:** `quests/your_spell.md`
```

**Important: Update User-Facing Documentation**

When adding a new spell, you MUST add example usage to these files:

1. **README.md:**
   - Add to "Quick Examples" table in ⚡ Quick Examples section
   - Add complete spell description in 📜 Available Spells section
   - Add to "Spell Reference" table in 🧙 Creating Your Own Spells section
   - Add command example to "Command Quick Reference" section
   - Add quest link in Documentation section

2. **START_HERE.md:**
   - Add example usage in Step 3: Speak Naturally! section
   - Show natural language command and expected output

3. **EXAMPLES.md:**
   - Add new section "Your Spell Name Examples"
   - Include 3-5 example scenarios (basic, advanced, edge cases)
   - Update "Common Patterns" section if applicable
   - Update example session to show spell in use

**Why this matters:**
Users discover spells through natural language examples. Without documentation updates, your spell won't be discoverable or usable by Claude Code's natural language understanding.

---

## Code Style Guidelines

### D&D Theme Consistency

**Maintain D&D theme in:**
- Module docstrings
- Function docstrings (describe as magical subroutines)
- Print statements
- Error messages
- Quest logs

**Keep technical in:**
- Variable names (input_path, output_path, metadata)
- Function names (remove_background, process_audio)
- Model names (u2net, u2netp)
- Command-line help text

### Examples:

**✅ Good (Themed):**
```python
def channel_transformation(artifact: str) -> Dict:
    """Channel magical energies to transform the artifact.

    This spell invokes ancient powers to transmute the
    artifact into its purified form.
    """
    logger.info("Channeling magical transformation...")
    # Technical code here
```

**❌ Bad (Not Themed):**
```python
def channel_transformation(artifact: str) -> Dict:
    """This function processes the file."""
    print("Processing...")
    # Technical code here
```

### Code Quality Standards

1. **Use type hints:**
   ```python
   def process_file(input_path: str, output_path: Optional[str] = None) -> Dict[str, Any]:
   ```

2. **Write docstrings:**
   ```python
   def function(param: str) -> str:
       """Brief description.

       Args:
           param: Description

       Returns:
           Description
       """
   ```

3. **Handle errors gracefully:**
   ```python
   try:
       # Spell logic
   except SpecificError as e:
       raise ThemedError("Message", recovery_suggestion="Fix")
   ```

4. **Use shared utilities:**
   - Import from `utils.common` and `utils.error_handling`
   - Don't duplicate existing functionality

---

## Testing Requirements

### Test Coverage

- Aim for at least 80% code coverage
- Test both success and failure cases
- Test edge cases (empty files, large files, etc.)

### Test Types

1. **Unit Tests:** Test individual functions
2. **Integration Tests:** Test complete spell execution
3. **Error Tests:** Test error handling

### Running Tests

Before submitting a PR:

```bash
# Run all tests
pytest -v

# Run with coverage
pytest --cov=spells --cov-report=html

# Check code style
flake8 spells/
black --check spells/

# Type checking
mypy spells/
```

---

## Documentation Standards

### Spell Documentation

Each spell must have:

1. **Quest log** in `quests/`
2. **Module docstring** explaining the spell
3. **Function docstrings** for all public functions
4. **CLI help text** (technical and clear)

### Documentation Template

```python
"""
Spell Name - D&D themed description.

This module provides functionality for brief technical description.

Example usage:
    python spells/this_spell.py --input file.png --output file_processed.png

Dependencies:
    - List external dependencies
    - FFmpeg, system tools, etc.
"""
```

---

## Pull Request Process

### Before Submitting

1. **Run tests:** `pytest -v`
2. **Check code style:** `flake8 spells/` and `black --check spells/`
3. **Update documentation:** README.md, quest logs
4. **Test manually:** Run your spell with real files

### PR Description Template

```markdown
## Spell: [Spell Name]

### Quest Objective
[Brief description of what this spell does]

### Changes Made
- [ ] Added new spell file
- [ ] Created quest log
- [ ] Added tests
- [ ] Updated README
- [ ] Tested manually

### Testing
- [ ] All tests pass
- [ ] Manual testing completed
- [ ] Code coverage adequate

### Screenshots/Demo
[If applicable, show the spell in action]

### Checklist
- [ ] Code follows style guidelines
- [ ] D&D theme maintained
- [ ] Documentation updated
- [ ] Tests added
- [ ] No breaking changes
```

### Review Process

1. Automated checks must pass
2. At least one approval required
3. Address all review feedback
4. Squash commits if needed

---

## Questions?

- Check existing spells for examples
- Read `AI_CRAFT_SPELLBOOK.md` for architecture details
- Open an issue for discussion

**Happy spell crafting!** 🧙‍♂️✨
