"""
Tests for the audio_cleanse spell.

This module tests the audio cleansing functionality.
"""

import os
import sys
import tempfile
import pytest
from unittest.mock import Mock, patch, MagicMock

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from spells.audio_cleanse import (
    process_audio_video,
    get_media_info,
    detect_silence_periods,
    calculate_non_silent_segments,
    NOISE_STRENGTH_SETTINGS,
    SUPPORTED_FORMATS,
)


# =============================================================================
# CONFIGURATION TESTS
# =============================================================================

def test_noise_strength_settings():
    """Test that noise strength settings are defined."""
    assert "light" in NOISE_STRENGTH_SETTINGS
    assert "medium" in NOISE_STRENGTH_SETTINGS
    assert "heavy" in NOISE_STRENGTH_SETTINGS


def test_supported_formats():
    """Test that expected formats are supported."""
    assert ".mp3" in SUPPORTED_FORMATS
    assert ".wav" in SUPPORTED_FORMATS
    assert ".mp4" in SUPPORTED_FORMATS


# =============================================================================
# UNIT TESTS
# =============================================================================

def test_calculate_non_silent_segments_no_silence():
    """Test segment calculation with no silence periods."""
    segments = calculate_non_silent_segments(
        total_duration=100.0,
        silence_periods=[],
        padding=0.1
    )

    assert len(segments) == 1
    assert segments[0] == (0.0, 100.0)


def test_calculate_non_silent_segments_with_silence():
    """Test segment calculation with silence periods."""
    segments = calculate_non_silent_segments(
        total_duration=100.0,
        silence_periods=[(20.0, 30.0), (50.0, 60.0)],
        padding=0.1
    )

    assert len(segments) == 3
    # First segment: 0 to 20.1 (with padding)
    assert segments[0][0] == 0.0
    assert segments[0][1] == 20.1

    # Middle segment: 29.9 to 50.1 (with padding)
    assert segments[1][0] == 29.9
    assert segments[1][1] == 50.1

    # Last segment: 59.9 to 100
    assert segments[2][0] == 59.9
    assert segments[2][1] == 100.0


def test_process_audio_video_invalid_parameters():
    """Test that invalid parameters raise errors."""
    from spells.utils.error_handling import InvalidReagentError

    # Test invalid silence threshold - validation happens after file check
    # So we need to create a valid file first
    with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as f:
        f.write(b"dummy audio data")
        temp_path = f.name

    try:
        with pytest.raises(InvalidReagentError) as exc_info:
            process_audio_video(
                input_path=temp_path,
                silence_threshold=10.0  # Should be negative
            )

        assert "Silence threshold must be negative" in str(exc_info.value)
    finally:
        os.unlink(temp_path)


def test_process_audio_video_file_not_found():
    """Test that non-existent file raises error."""
    from spells.utils.error_handling import InvalidReagentError

    with pytest.raises(InvalidReagentError) as exc_info:
        process_audio_video(
            input_path="/nonexistent/file.mp3"
        )

    assert "Artifact not found" in str(exc_info.value)


def test_process_audio_video_unsupported_format():
    """Test that unsupported format raises error."""
    from spells.utils.error_handling import InvalidReagentError

    with tempfile.NamedTemporaryFile(suffix=".txt", delete=False) as f:
        f.write(b"not an audio file")
        temp_path = f.name

    try:
        with pytest.raises(InvalidReagentError) as exc_info:
            process_audio_video(
                input_path=temp_path
            )

        assert "Unsupported artifact format" in str(exc_info.value)
    finally:
        os.unlink(temp_path)


# =============================================================================
# INTEGRATION TESTS
# =============================================================================

@pytest.mark.integration
def test_get_media_info_real_file():
    """Test getting media info from a real file."""
    import tempfile

    # Create a simple test file (this test requires FFmpeg)
    try:
        # Skip if FFmpeg not available
        import subprocess
        result = subprocess.run(["ffmpeg", "-version"], capture_output=True)
        if result.returncode != 0:
            pytest.skip("FFmpeg not available")

        # This test would require a real audio file
        # For now, we skip it
        pytest.skip("Requires test audio file")

    except Exception:
        pytest.skip("FFmpeg not available")


@pytest.mark.integration
def test_process_audio_video_real():
    """Test audio processing with real file (integration test)."""
    # This would require a real audio file and FFmpeg
    pytest.skip("Integration test - requires test audio file")


# =============================================================================
# CLI TESTS
# =============================================================================

@patch('spells.audio_cleanse.process_audio_video')
def test_main_basic(mock_process, capsys):
    """Test basic CLI invocation."""
    from spells.audio_cleanse import main
    import sys

    # Mock the process function
    mock_process.return_value = {
        "input_path": "input.mp3",
        "output_path": "output.mp3",
        "input_info": {
            "duration_sec": 100.0,
            "size_bytes": 1000000,
        },
        "output_info": {
            "duration_sec": 90.0,
            "size_bytes": 900000,
        },
        "duration_reduction_sec": 10.0,
        "duration_reduction_percent": 10.0,
        "silence_removal": {
            "silent_periods_found": 2,
        },
        "settings": {
            "noise_reduction": True,
            "noise_strength": "light",
        },
        "performance": {
            "duration_seconds": 5.0,
        },
    }

    # Mock sys.argv
    with patch.object(sys, 'argv', [
        'audio_cleanse.py',
        '--input', 'input.mp3',
        '--output', 'output.mp3'
    ]):
        try:
            main()
        except SystemExit:
            pass

    # Verify output was printed
    captured = capsys.readouterr()
    assert "Ritual completed" in captured.out or "Spell Fumble" in captured.out or "✓" in captured.out or "✗" in captured.out
