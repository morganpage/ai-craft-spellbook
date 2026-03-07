import argparse
import json
import os
import sys
from datetime import datetime, timezone
from typing import Dict, Any, Optional

# Add parent directory to path for imports when running as script
if __name__ == "__main__":
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PIL import Image

from spells.utils.common import (
    save_metadata,
    validate_input_file,
    validate_output_path,
    get_spell_metadata_base,
    setup_output_directory,
    get_logger,
    check_dependencies,
    format_bytes,
    PerformanceTracker,
    setup_logging,
)
from spells.utils.error_handling import (
    SpellFumbleError,
    ArcaneDisruptionError,
    InvalidReagentError,
    format_spell_fumble,
    handle_spell_error,
)


# =============================================================================
# SPELL METADATA
# =============================================================================

SPELL_METADATA = {
    "name": "split_artifact",
    "version": "1.0.0",
    "primary_keywords": ["split", "divide", "separate", "halves"],
    "secondary_keywords": {
        "orientation": ["landscape", "wide", "portrait", "tall", "vertical", "square"],
        "direction": ["left and right", "top and bottom"],
        "output_format": ["JPEG", "JPG", "PNG", "WEBP"],
        "location": ["save to", "output to", "folder"]
    },
    "supported_formats": ["png", "jpg", "jpeg", "webp", "gif", "bmp", "tiff"],
    "description": "Divide images into two equal halves based on orientation",
    "common_use_cases": [
        "Separating wide sprite sheets into distinct pieces",
        "Splitting character portraits into top/bottom sections",
        "Dividing large UI elements into manageable components",
        "Preparing assets for game engine import",
        "Creating dual-frame sprites from single source"
    ],
    "examples": [
        "split landscape.png",
        "divide portrait.jpg into top and bottom",
        "separate sprite.png into two halves",
        "split square_512.png",
        "divide wide image into left and right",
        "split and save as JPEG"
    ],
    "output_naming_pattern": "<name>_left/right/top/bottom.<ext>",
    "cli_pattern": "python spells/split_artifact.py --input <file> [options]",
    "cli_parameters": {
        "--input": "Magical image artifact path (required)",
        "--output-dir": "Sanctum for split artifacts (optional, default: same as input)",
        "--format": "Magical format for output: png, jpg, webp, gif, bmp, tiff (default: png)",
        "--log-level": "Logging level: DEBUG, INFO, WARNING, ERROR (default: INFO)",
        "--log-file": "Path to log file (optional)"
    }
}


# =============================================================================
# SPELL CONFIGURATION
# =============================================================================

SUPPORTED_FORMATS = ["png", "jpg", "jpeg", "webp", "gif", "bmp", "tiff"]

# Maximum file size: 100MB default
MAX_FILE_SIZE = 100 * 1024 * 1024


# =============================================================================
# MAIN SPELL FUNCTION
# =============================================================================

def split_artifact(
    input_path: str,
    output_dir: Optional[str] = None,
    output_format: str = "png",
    logger: Optional[Any] = None,
) -> Dict[str, Any]:
    """Cast the split artifact hex to divide a magical image into two equal halves.

    This incantation uses arcane divination to determine the artifact's orientation,
    then splits it horizontally or vertically accordingly. Wide artifacts are divided
    into left/right halves, tall artifacts into top/bottom halves.

    Args:
        input_path: Path to the magical image artifact
        output_dir: Sanctum to save split artifact treasures (optional)
        output_format: Magical format for output treasures (default: png)
        logger: Optional logger instance for tracking progress

    Returns:
        Dict containing arcane knowledge about the splitting ritual

    Raises:
        InvalidReagentError: If input validation fails
        ArcaneDisruptionError: If the ritual fails during casting
        SpellFumbleError: For general spell failures
    """
    # Set up logger if not provided
    if logger is None:
        logger = get_logger("split_artifact")

    # Validate input file
    logger.info(f"Validating artifact: {input_path}")
    validation = validate_input_file(
        input_path,
        allowed_formats=set(f".{fmt}" for fmt in SUPPORTED_FORMATS),
        max_size_bytes=MAX_FILE_SIZE,
        check_readable=True,
    )
    logger.info(f"Artifact validated: {format_bytes(validation['size_bytes'])}")

    # Validate output format
    if output_format.lower() not in SUPPORTED_FORMATS:
        raise InvalidReagentError(
            f"Unsupported magical format: {output_format}",
            recovery_suggestion=f"Choose from: {', '.join(SUPPORTED_FORMATS)}"
        )

    # Determine output directory
    if output_dir is None:
        output_dir = os.path.dirname(input_path) or "dungeon_cache"

    # Validate and prepare output path
    output_dir = validate_output_path(
        output_dir,
        check_writable=True,
        create_parent_dirs=True,
    )

    # Set up performance tracking
    tracker = PerformanceTracker("split_artifact")
    tracker.set_input_size(validation["size_bytes"])
    tracker.start()

    try:
        # Read input artifact
        logger.info("Reading magical artifact...")
        img = Image.open(input_path)
        width, height = img.size
        original_mode = img.mode

        if width < 2 or height < 2:
            raise InvalidReagentError(
                "Artifact too small to split. Minimum size: 2x2 pixels",
                recovery_suggestion="Provide a larger artifact to split."
            )

        original_name = os.path.splitext(os.path.basename(input_path))[0]

        # Determine split direction based on orientation
        if width > height:
            split_direction = "horizontal"
            half_width = width // 2

            left_crop = (0, 0, half_width, height)
            right_crop = (half_width, 0, width, height)

            left_img = img.crop(left_crop)
            right_img = img.crop(right_crop)

            left_filename = f"{original_name}_left.{output_format}"
            right_filename = f"{original_name}_right.{output_format}"
            left_path = os.path.join(output_dir, left_filename)
            right_path = os.path.join(output_dir, right_filename)

            left_half_info = {
                "path": left_path,
                "size": f"{left_img.width}x{left_img.height}",
                "crop_box": list(left_crop),
                "label": "left",
            }
            right_half_info = {
                "path": right_path,
                "size": f"{right_img.width}x{right_img.height}",
                "crop_box": list(right_crop),
                "label": "right",
            }

        elif height > width:
            split_direction = "vertical"
            half_height = height // 2

            top_crop = (0, 0, width, half_height)
            bottom_crop = (0, half_height, width, height)

            left_img = img.crop(top_crop)
            right_img = img.crop(bottom_crop)

            top_filename = f"{original_name}_top.{output_format}"
            bottom_filename = f"{original_name}_bottom.{output_format}"
            left_path = os.path.join(output_dir, top_filename)
            right_path = os.path.join(output_dir, bottom_filename)

            left_half_info = {
                "path": left_path,
                "size": f"{left_img.width}x{left_img.height}",
                "crop_box": list(top_crop),
                "label": "top",
            }
            right_half_info = {
                "path": right_path,
                "size": f"{right_img.width}x{right_img.height}",
                "crop_box": list(bottom_crop),
                "label": "bottom",
            }
        else:
            # Square: split horizontally by default
            split_direction = "horizontal"
            half_width = width // 2

            left_crop = (0, 0, half_width, height)
            right_crop = (half_width, 0, width, height)

            left_img = img.crop(left_crop)
            right_img = img.crop(right_crop)

            left_filename = f"{original_name}_left.{output_format}"
            right_filename = f"{original_name}_right.{output_format}"
            left_path = os.path.join(output_dir, left_filename)
            right_path = os.path.join(output_dir, right_filename)

            left_half_info = {
                "path": left_path,
                "size": f"{left_img.width}x{left_img.height}",
                "crop_box": list(left_crop),
                "label": "left",
            }
            right_half_info = {
                "path": right_path,
                "size": f"{right_img.width}x{right_img.height}",
                "crop_box": list(right_crop),
                "label": "right",
            }

        # Ensure output directory exists
        setup_output_directory(output_dir)

        # Format mapping
        format_map = {
            "jpg": "JPEG",
            "jpeg": "JPEG",
            "png": "PNG",
            "webp": "WEBP",
            "gif": "GIF",
            "bmp": "BMP",
            "tiff": "TIFF",
        }
        pil_format = format_map.get(output_format.lower(), output_format.upper())

        # Handle transparency conversion for JPEG
        if pil_format == "JPEG" and left_img.mode in ("RGBA", "P"):
            left_img = left_img.convert("RGB")
            right_img = right_img.convert("RGB")

        # Save split artifacts
        logger.info("Preserving split artifacts...")
        left_img.save(left_path, format=pil_format, optimize=True)
        right_img.save(right_path, format=pil_format, optimize=True)

        # Get output file sizes
        left_size_bytes = os.path.getsize(left_path)
        right_size_bytes = os.path.getsize(right_path)
        total_output_bytes = left_size_bytes + right_size_bytes
        tracker.set_output_size(total_output_bytes)
        tracker.stop()

        logger.info("Ritual completed successfully!")

        # Build metadata
        metadata = get_spell_metadata_base("split_artifact")
        metadata.update({
            "input_path": input_path,
            "output_dir": output_dir,
            "original_size": f"{width}x{height}",
            "original_mode": original_mode,
            "split_direction": split_direction,
            "first_half": left_half_info,
            "second_half": right_half_info,
            "output_format": pil_format,
            "first_half_size_bytes": left_size_bytes,
            "second_half_size_bytes": right_size_bytes,
            "total_output_size_bytes": total_output_bytes,
        })
        metadata["performance"] = tracker.get_metrics()

        return metadata

    except MemoryError as e:
        raise ArcaneDisruptionError(
            "Insufficient magical energy (memory) for ritual",
            recovery_suggestion="Try a smaller artifact or free up memory."
        )
    except IOError as e:
        raise ArcaneDisruptionError(
            f"Failed to read or write artifact: {e}",
            recovery_suggestion="Check file permissions and magical storage capacity."
        )
    except Exception as e:
        if isinstance(e, (InvalidReagentError, ArcaneDisruptionError)):
            raise
        raise SpellFumbleError(
            f"Unexpected magical failure: {e}",
            recovery_suggestion="Check the error details and try again."
        )


# =============================================================================
# COMMAND LINE INTERFACE
# =============================================================================

def main():
    parser = argparse.ArgumentParser(
        description="Cast the split artifact hex to divide magical images into two halves",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Split a wide artifact (width > height)
  python spells/split_artifact.py --input "dungeon_cache/landscape.png"

  # Split a tall artifact to custom sanctum
  python spells/split_artifact.py \
    --input "dungeon_cache/portrait.jpg" \
    --output-dir "dungeon_cache/splits/"

  # Split and save as JPEG
  python spells/split_artifact.py \
    --input "dungeon_cache/sprite.png" \
    --format "jpg"

  # Square artifact splits left/right by default
  python spells/split_artifact.py --input "dungeon_cache/square_512.png"

Split Direction Logic:
  - Wide artifact (width > height): Splits left/right
  - Tall artifact (height > width): Splits top/bottom
  - Square artifact (width == height): Splits left/right (default)
        """
    )

    # Input/output arguments
    parser.add_argument(
        "--input", "-i",
        required=True,
        help="Path to the magical image artifact"
    )
    parser.add_argument(
        "--output-dir", "-o",
        default=None,
        help="Sanctum for split artifacts (default: same directory as input)"
    )
    parser.add_argument(
        "--format", "-f",
        default="png",
        choices=SUPPORTED_FORMATS,
        help="Magical format for output artifacts (default: png)"
    )

    # Processing options
    parser.add_argument(
        "--max-size",
        type=int,
        default=MAX_FILE_SIZE,
        metavar="BYTES",
        help=f"Maximum artifact size in bytes (default: {MAX_FILE_SIZE})"
    )
    parser.add_argument(
        "--log-level",
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        default="INFO",
        help="Logging level (default: INFO)"
    )
    parser.add_argument(
        "--log-file",
        metavar="PATH",
        help="Path to log file (optional)"
    )

    args = parser.parse_args()

    # Set up logging
    logger = setup_logging(
        "split_artifact",
        log_level=args.log_level,
        log_file=args.log_file,
    )

    try:
        # Check dependencies
        deps = check_dependencies(required_modules=["PIL"])
        if not deps["all_available"]:
            missing = [k for k, v in deps["modules"].items() if not v]
            raise InvalidReagentError(
                f"Missing required spell components: {', '.join(missing)}",
                recovery_suggestion="Install with: pip install -r requirements.txt"
            )

        # Cast the spell
        metadata = split_artifact(
            input_path=args.input,
            output_dir=args.output_dir,
            output_format=args.format,
            logger=logger,
        )

        # Save metadata
        original_name = os.path.splitext(os.path.basename(args.input))[0]
        metadata_path = os.path.join(
            metadata["output_dir"], f"{original_name}_split_metadata.json"
        )
        save_metadata(metadata, metadata_path)

        # Print success message
        print(f"\n✓ Artifact split successfully!")
        print(f"  Artifact: {metadata['input_path']} ({metadata['original_mode']})")
        print(f"  Original size: {metadata['original_size']}")
        print(f"  Split direction: {metadata['split_direction']}")

        first_half = metadata["first_half"]
        second_half = metadata["second_half"]

        if metadata["split_direction"] == "horizontal":
            print(f"  Left half: {first_half['path']} ({first_half['size']})")
            print(f"  Right half: {second_half['path']} ({second_half['size']})")
        else:
            print(f"  Top half: {first_half['path']} ({first_half['size']})")
            print(f"  Bottom half: {second_half['path']} ({second_half['size']})")

        print(f"  Format: {metadata['output_format']}")
        print(f"  Duration: {metadata['performance']['duration_seconds']:.2f}s")
        print(f"  Arcane knowledge: {metadata_path}")

    except Exception as e:
        handle_spell_error(e, "split_artifact", exit_on_error=True)


if __name__ == "__main__":
    main()
