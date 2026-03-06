#!/usr/bin/env python3
"""
AI Craft Spellbook - Demonstration Script

This script demonstrates the key features of the AI Craft Spellbook framework
including shared utilities, error handling, logging, and performance tracking.
"""

import os
import sys
import tempfile
from PIL import Image

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from spells.utils.common import (
    format_bytes,
    format_duration,
    PerformanceTracker,
    get_spell_metadata_base,
    validate_input_file,
    save_metadata,
)
from spells.utils.error_handling import (
    SpellFumbleError,
    InvalidReagentError,
    format_spell_fumble,
)


def demo_utility_functions():
    """Demonstrate shared utility functions."""
    print("=" * 60)
    print("✓ Shared Utilities Demo")
    print("=" * 60)

    # Format bytes
    print("\n📊 Byte Formatting:")
    sizes = [500, 1024, 1024*1024, 10*1024*1024]
    for size in sizes:
        print(f"  {size:,} bytes → {format_bytes(size)}")

    # Format duration
    print("\n⏱️  Duration Formatting:")
    durations = [30, 90, 3661]
    for duration in durations:
        print(f"  {duration} seconds → {format_duration(duration)}")


def demo_performance_tracking():
    """Demonstrate performance tracking."""
    print("\n" + "=" * 60)
    print("✓ Performance Tracking Demo")
    print("=" * 60)

    tracker = PerformanceTracker("demo_spell")
    tracker.set_input_size(1024 * 1024)  # 1MB

    print("\n⏳ Tracking spell execution...")
    tracker.start()

    # Simulate some work
    import time
    time.sleep(0.5)

    tracker.stop()
    tracker.set_output_size(512 * 1024)  # 512KB

    metrics = tracker.get_metrics()
    print(f"\n📈 Performance Metrics:")
    print(f"  Spell: {metrics['spell_name']}")
    print(f"  Duration: {metrics['duration_seconds']:.2f}s")
    print(f"  Input: {format_bytes(metrics['input_size_bytes'])}")
    print(f"  Output: {format_bytes(metrics['output_size_bytes'])}")


def demo_metadata_generation():
    """Demonstrate metadata generation."""
    print("\n" + "=" * 60)
    print("✓ Metadata Generation Demo")
    print("=" * 60)

    metadata = get_spell_metadata_base("demo_spell", version="2.0.0")
    metadata.update({
        "input_path": "/path/to/input.png",
        "output_path": "/path/to/output.png",
        "transformation": "demo transformation",
    })

    print("\n📜 Generated Metadata:")
    print(f"  Spell: {metadata['spell_name']}")
    print(f"  Version: {metadata['version']}")
    print(f"  Cast at: {metadata['cast_at']}")
    print(f"  Settings: {metadata['settings']}")
    print(f"  Performance: {metadata['performance']}")


def demo_error_handling():
    """Demonstrate themed error handling."""
    print("\n" + "=" * 60)
    print("✓ Error Handling Demo")
    print("=" * 60)

    # Demonstrate different error types
    errors = [
        InvalidReagentError("Invalid file format", recovery_suggestion="Use PNG or JPG"),
        SpellFumbleError("Spell failed mysteriously", recovery_suggestion="Check your mana"),
    ]

    for error in errors:
        print("\n" + format_spell_fumble(error, "demo_spell"))


def demo_input_validation():
    """Demonstrate input validation."""
    print("\n" + "=" * 60)
    print("✓ Input Validation Demo")
    print("=" * 60)

    # Create a temporary test file
    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as f:
        # Create a simple PNG
        img = Image.new('RGB', (100, 100), color='red')
        img.save(f, format='PNG')
        temp_path = f.name

    try:
        print(f"\n✅ Validating: {temp_path}")
        result = validate_input_file(
            temp_path,
            allowed_formats={".png", ".jpg"},
            max_size_bytes=10 * 1024 * 1024,  # 10MB
        )
        print(f"  File exists: {result['exists']}")
        print(f"  Size: {format_bytes(result['size_bytes'])}")
        print(f"  Format: {result['extension']}")
        print(f"  Readable: {result['is_readable']}")

    finally:
        os.unlink(temp_path)

    # Demonstrate validation error
    print("\n❌ Testing validation error:")
    try:
        validate_input_file(
            "/nonexistent/file.png",
            allowed_formats={".png"},
        )
    except InvalidReagentError as e:
        print(f"  {e}")


def main():
    """Run all demonstrations."""
    print("\n" + "=" * 60)
    print("🧙 AI Craft Spellbook - Feature Demonstration")
    print("=" * 60)
    print("\nVersion 2.0.0 - Enhanced Framework")
    print("\nThis demo showcases the new features:")
    print("  • Shared utilities for common operations")
    print("  • Performance tracking with metrics")
    print("  • Standardized metadata generation")
    print("  • Themed error handling with recovery")
    print("  • Comprehensive input validation")

    # Run demonstrations
    demo_utility_functions()
    demo_performance_tracking()
    demo_metadata_generation()
    demo_error_handling()
    demo_input_validation()

    print("\n" + "=" * 60)
    print("✨ Demonstration Complete!")
    print("=" * 60)
    print("\nFor more information, see:")
    print("  • README.md - Complete documentation")
    print("  • CONTRIBUTING.md - Development guide")
    print("  • CHANGELOG.md - Version history")
    print("  • spells/utils/ - Shared utilities source")
    print("\nHappy spell crafting! 🎭")


if __name__ == "__main__":
    main()
