"""
Tests for the dispel_background spell.

This module tests the background removal functionality.
"""

import os
import sys
import tempfile
import pytest
from io import BytesIO
from unittest.mock import Mock, patch, MagicMock

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PIL import Image

from spells.dispel_background import (
    remove_background,
    SUPPORTED_MODELS,
    SUPPORTED_FORMATS,
)


# =============================================================================
# FIXTURES
# =============================================================================

@pytest.fixture
def sample_image():
    """Create a sample test image."""
    img = Image.new('RGB', (100, 100), color='red')
    return img


@pytest.fixture
def sample_image_file(sample_image, tmp_path):
    """Create a sample test image file."""
    image_path = tmp_path / "test_image.png"
    sample_image.save(image_path)
    return str(image_path)


# =============================================================================
# CONFIGURATION TESTS
# =============================================================================

def test_supported_models():
    """Test that expected models are supported."""
    assert "u2net" in SUPPORTED_MODELS
    assert "u2netp" in SUPPORTED_MODELS
    assert "u2net_human_seg" in SUPPORTED_MODELS


def test_supported_formats():
    """Test that expected formats are supported."""
    assert ".png" in SUPPORTED_FORMATS
    assert ".jpg" in SUPPORTED_FORMATS
    assert ".jpeg" in SUPPORTED_FORMATS


# =============================================================================
# UNIT TESTS
# =============================================================================

def test_remove_background_invalid_parameters():
    """Test that invalid parameters raise errors."""
    from spells.utils.error_handling import InvalidReagentError

    # Test invalid model
    with pytest.raises(InvalidReagentError) as exc_info:
        from spells.dispel_background import remove_background
        # We'll use a real file but invalid model
        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as f:
            img = Image.new('RGB', (100, 100), color='red')
            img.save(f, format='PNG')
            temp_path = f.name

        try:
            # This should fail during model validation before file processing
            remove_background(
                input_path=temp_path,
                model="invalid_model_name"
            )
        finally:
            os.unlink(temp_path)

    assert "Unsupported arcane crystal" in str(exc_info.value)


@patch('spells.dispel_background.remove')
def test_remove_background_invalid_model(mock_remove, sample_image_file):
    """Test that invalid model raises error."""
    from spells.utils.error_handling import InvalidReagentError

    with pytest.raises(InvalidReagentError) as exc_info:
        remove_background(
            input_path=sample_image_file,
            model="invalid_model"
        )

    assert "Unsupported arcane crystal" in str(exc_info.value)


def test_remove_background_file_not_found(tmp_path):
    """Test that non-existent file raises error."""
    from spells.utils.error_handling import InvalidReagentError

    with pytest.raises(InvalidReagentError) as exc_info:
        remove_background(
            input_path=str(tmp_path / "nonexistent.png")
        )

    assert "Artifact not found" in str(exc_info.value)


def test_remove_background_unsupported_format(tmp_path):
    """Test that unsupported format raises error."""
    from spells.utils.error_handling import InvalidReagentError

    # Create a text file
    text_file = tmp_path / "test.txt"
    text_file.write_text("not an image")

    with pytest.raises(InvalidReagentError) as exc_info:
        remove_background(
            input_path=str(text_file)
        )

    assert "Unsupported artifact format" in str(exc_info.value)


# =============================================================================
# INTEGRATION TESTS
# =============================================================================

@pytest.mark.integration
def test_remove_background_real_image(sample_image_file):
    """Test background removal with real image (integration test)."""
    try:
        from rembg import remove as rembg_remove

        # Create output path
        output_path = os.path.join(
            os.path.dirname(sample_image_file),
            "test_output.png"
        )

        # Run actual background removal
        metadata = remove_background(
            input_path=sample_image_file,
            output_path=output_path,
            model="u2net"
        )

        # Verify output file was created
        assert os.path.exists(output_path)

        # Verify output is a valid PNG
        with Image.open(output_path) as img:
            assert img.format == "PNG"
            assert img.mode == "RGBA"

        # Verify metadata
        assert metadata["input_path"] == sample_image_file
        assert metadata["output_path"] == output_path
        assert metadata["model"] == "u2net"

    except ImportError:
        pytest.skip("rembg not installed")


# =============================================================================
# CLI TESTS
# =============================================================================

def test_cli_argument_parsing():
    """Test that CLI arguments are parsed correctly."""
    from spells.dispel_background import main
    import sys

    # Test that --help works
    with patch.object(sys, 'argv', ['dispel_background.py', '--help']):
        try:
            main()
        except SystemExit as e:
            # --help causes sys.exit(0)
            assert e.code == 0
