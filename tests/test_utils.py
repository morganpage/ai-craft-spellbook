"""
Tests for AI Craft Spellbook shared utilities.

This module tests the common utility functions used across all spells.
"""

import json
import os
import sys
import tempfile
import pytest
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from spells.utils.common import (
    save_metadata,
    load_metadata,
    get_spell_metadata_base,
    validate_input_file,
    validate_output_path,
    setup_output_directory,
    check_dependencies,
    check_ffmpeg,
    check_ffprobe,
    format_bytes,
    format_duration,
    get_file_hash,
    PerformanceTracker,
)
from spells.utils.error_handling import (
    SpellFumbleError,
    ArcaneDisruptionError,
    InvalidReagentError,
    format_spell_fumble,
)


# =============================================================================
# METADATA TESTS
# =============================================================================

def test_get_spell_metadata_base():
    """Test standardized metadata base generation."""
    metadata = get_spell_metadata_base("test_spell", version="1.0.0")

    assert metadata["spell_name"] == "test_spell"
    assert metadata["version"] == "1.0.0"
    assert "cast_at" in metadata
    assert "settings" in metadata
    assert "performance" in metadata
    assert metadata["performance"]["duration_seconds"] == 0.0


def test_save_and_load_metadata():
    """Test saving and loading metadata files."""
    with tempfile.TemporaryDirectory() as temp_dir:
        metadata = {
            "spell_name": "test_spell",
            "test_key": "test_value",
        }
        metadata_path = os.path.join(temp_dir, "test_metadata.json")

        # Save metadata
        save_metadata(metadata, metadata_path)
        assert os.path.exists(metadata_path)

        # Load metadata
        loaded = load_metadata(metadata_path)
        assert loaded == metadata


def test_save_metadata_creates_directory():
    """Test that save_metadata creates parent directories."""
    with tempfile.TemporaryDirectory() as temp_dir:
        metadata_path = os.path.join(temp_dir, "subdir", "test_metadata.json")

        save_metadata({"test": "data"}, metadata_path)
        assert os.path.exists(metadata_path)


def test_load_metadata_invalid_json():
    """Test loading invalid JSON raises error."""
    with tempfile.TemporaryDirectory() as temp_dir:
        metadata_path = os.path.join(temp_dir, "invalid.json")
        with open(metadata_path, "w") as f:
            f.write("not valid json {]")

        with pytest.raises(InvalidReagentError):
            load_metadata(metadata_path)


# =============================================================================
# INPUT VALIDATION TESTS
# =============================================================================

def test_validate_input_file_success():
    """Test validating a valid input file."""
    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as f:
        f.write(b"test data")
        temp_path = f.name

    try:
        result = validate_input_file(temp_path)
        assert result["exists"] is True
        assert result["size_bytes"] == 9
        assert result["extension"] == ".png"
    finally:
        os.unlink(temp_path)


def test_validate_input_file_not_found():
    """Test validating non-existent file raises error."""
    with pytest.raises(InvalidReagentError) as exc_info:
        validate_input_file("/nonexistent/path/file.txt")

    assert "Artifact not found" in str(exc_info.value)


def test_validate_input_file_invalid_format():
    """Test validating file with wrong format."""
    with tempfile.NamedTemporaryFile(suffix=".txt", delete=False) as f:
        f.write(b"test data")
        temp_path = f.name

    try:
        with pytest.raises(InvalidReagentError) as exc_info:
            validate_input_file(temp_path, allowed_formats={".png", ".jpg"})

        assert "Unsupported artifact format" in str(exc_info.value)
    finally:
        os.unlink(temp_path)


def test_validate_input_file_too_large():
    """Test validating file exceeding size limit."""
    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as f:
        f.write(b"x" * 1000)  # 1000 bytes
        temp_path = f.name

    try:
        with pytest.raises(InvalidReagentError) as exc_info:
            validate_input_file(temp_path, max_size_bytes=500)

        assert "too large" in str(exc_info.value).lower()
    finally:
        os.unlink(temp_path)


def test_validate_output_path_success():
    """Test validating output path."""
    with tempfile.TemporaryDirectory() as temp_dir:
        output_path = os.path.join(temp_dir, "output.png")

        result = validate_output_path(output_path, create_parent_dirs=True)
        assert os.path.isabs(result)


def test_validate_output_path_creates_directory():
    """Test that validate_output_path creates parent directories."""
    with tempfile.TemporaryDirectory() as temp_dir:
        output_path = os.path.join(temp_dir, "subdir", "output.png")

        validate_output_path(output_path, create_parent_dirs=True)
        assert os.path.exists(os.path.dirname(output_path))


def test_setup_output_directory():
    """Test creating output directory."""
    with tempfile.TemporaryDirectory() as temp_dir:
        new_dir = os.path.join(temp_dir, "new", "nested", "dir")

        setup_output_directory(new_dir)
        assert os.path.exists(new_dir)


# =============================================================================
# DEPENDENCY CHECKING TESTS
# =============================================================================

def test_check_dependencies_commands():
    """Test checking for system commands."""
    # Test with commands that should exist
    result = check_dependencies(required_commands=["python"])
    assert "commands" in result
    assert "python" in result["commands"]


def test_check_ffmpeg():
    """Test FFmpeg availability check."""
    # This test passes regardless of whether FFmpeg is installed
    result = check_ffmpeg()
    assert isinstance(result, bool)


def test_check_ffprobe():
    """Test FFprobe availability check."""
    # This test passes regardless of whether FFprobe is installed
    result = check_ffprobe()
    assert isinstance(result, bool)


# =============================================================================
# FORMATTING TESTS
# =============================================================================

def test_format_bytes():
    """Test byte formatting."""
    assert format_bytes(500) == "500.00 B"
    assert format_bytes(1024) == "1.00 KB"
    assert format_bytes(1024 * 1024) == "1.00 MB"
    assert format_bytes(1024 * 1024 * 1024) == "1.00 GB"


def test_format_duration():
    """Test duration formatting."""
    assert format_duration(30) == "30.0s"
    assert format_duration(90) == "1m 30s"
    assert format_duration(3661) == "1h 1m"


# =============================================================================
# PERFORMANCE TRACKER TESTS
# =============================================================================

def test_performance_tracker():
    """Test performance tracking."""
    import time

    tracker = PerformanceTracker("test_spell")

    tracker.set_input_size(1000)
    assert tracker.input_size == 1000

    tracker.start()
    time.sleep(0.1)
    tracker.stop()

    assert tracker.get_duration() >= 0.1

    tracker.set_output_size(500)
    metrics = tracker.get_metrics()

    assert metrics["spell_name"] == "test_spell"
    assert metrics["input_size_bytes"] == 1000
    assert metrics["output_size_bytes"] == 500
    assert metrics["duration_seconds"] >= 0.1


# =============================================================================
# ERROR HANDLING TESTS
# =============================================================================

def test_spell_fumble_error():
    """Test SpellFumbleError exception."""
    error = SpellFumbleError("Test error", recovery_suggestion="Fix it")
    assert "Test error" in str(error)
    assert error.recovery_suggestion == "Fix it"


def test_invalid_reagent_error():
    """Test InvalidReagentError exception."""
    error = InvalidReagentError("Invalid input")
    assert isinstance(error, SpellFumbleError)


def test_arcane_disruption_error():
    """Test ArcaneDisruptionError exception."""
    error = ArcaneDisruptionError("System failed")
    assert isinstance(error, SpellFumbleError)


def test_format_spell_fumble():
    """Test error message formatting."""
    error = ValueError("Test error")
    formatted = format_spell_fumble(error, "test_spell")

    assert "Spell Fumble" in formatted
    assert "test_spell" in formatted
    assert "Test error" in formatted
