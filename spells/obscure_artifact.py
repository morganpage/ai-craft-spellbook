import argparse
import json
import os
import sys
from datetime import datetime, timezone
from typing import Dict, Any, Optional

# Add parent directory to path for imports when running as script
if __name__ == "__main__":
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PIL import Image, ImageFilter

from spells.utils.common import (
    save_metadata,
    validate_input_file,
    validate_output_path,
    get_spell_metadata_base,
    setup_output_directory,
    get_logger,
    format_bytes,
    PerformanceTracker,
    setup_logging,
    SUPPORTED_IMAGE_FORMATS,
)
from spells.utils.error_handling import (
    SpellFumbleError,
    ArcaneDisruptionError,
    InvalidReagentError,
    handle_spell_error,
)


# =============================================================================
# SPELL METADATA
# =============================================================================

SPELL_METADATA = {
    "name": "obscure_artifact",
    "version": "1.0.0",
    "primary_keywords": ["blur", "obscure", "blur image", "obscure image", "apply blur"],
    "secondary_keywords": {
        "blur_types": ["gaussian", "box", "blur type", "blur style"],
        "intensity": ["radius", "strength", "power", "intensity", "heavy", "light", "subtle"],
        "iterations": ["passes", "multiple", "repeat", "times"],
        "quality": ["output quality", "compression", "optimize"],
    },
    "supported_formats": ["jpg", "jpeg", "png", "webp", "bmp", "tiff", "gif"],
    "description": "Cast the obscure artifact hex to shroud magical images in mystical haze",
    "common_use_cases": [
        "Privacy protection by blurring sensitive information",
        "Background softening for portraits and product photos",
        "Artistic depth-of-field effects",
        "Image preprocessing before further processing",
        "Creating placeholder or preview versions",
    ],
    "examples": [
        "blur photo.jpg",
        "obscure sensitive.png with heavy blur",
        "apply subtle blur to portrait.png",
        "blur background in image.jpg with radius 10",
        "obscure artifact with gaussian ritual",
    ],
    "output_naming_pattern": "<name>_obscured.<ext>",
    "cli_pattern": "python spells/obscure_artifact.py --input <file> [--radius <value>] [--blur-type <type>]",
    "cli_parameters": {
        "--input": "Path to magical image artifact (required)",
        "--output": "Path to obscured artifact (optional)",
        "--radius": "Obscuration power 0.1-100.0 (short: -r, default: 5.0)",
        "--blur-type": "Ritual type: gaussian, box (default: gaussian)",
        "--iterations": "Number of blur passes 1-10 (default: 1)",
        "--quality": "Output quality for lossy formats 1-100 (short: -q, default: 95)",
        "--log-level": "Logging level: DEBUG, INFO, WARNING, ERROR (default: INFO)",
        "--log-file": "Path to log file (optional)",
    }
}


# =============================================================================
# SPELL CONFIGURATION
# =============================================================================

# Supported blur rituals
SUPPORTED_BLUR_TYPES = ["gaussian", "box"]

# Obscuration power limits
MIN_RADIUS = 0.1
MAX_RADIUS = 100.0
DEFAULT_RADIUS = 5.0

# Iteration limits
MIN_ITERATIONS = 1
MAX_ITERATIONS = 10
DEFAULT_ITERATIONS = 1

# Maximum file size: 100MB default
MAX_FILE_SIZE = 100 * 1024 * 1024

# Default quality for lossy formats
DEFAULT_QUALITY = 95


# =============================================================================
# OBSCURATION FUNCTIONS
# =============================================================================

def obscure_artifact(
    input_path: str,
    output_path: Optional[str] = None,
    radius: float = DEFAULT_RADIUS,
    blur_type: str = "gaussian",
    iterations: int = DEFAULT_ITERATIONS,
    quality: int = DEFAULT_QUALITY,
    logger: Optional[Any] = None,
) -> Dict[str, Any]:
    """Cast the obscure artifact hex to shroud magical images in mystical haze.

    This powerful ritual applies blur effects to image artifacts, creating
    an obscuring mist that can hide details, soften backgrounds, or create
    artistic effects. Choose between Gaussian ritual for smooth results or
    Box enchantment for faster processing.

    Args:
        input_path: Path to the source magical image artifact
        output_path: Path to the obscured artifact
        radius: Obscuration power (0.1-100.0), higher values create more blur
        blur_type: Ritual type ('gaussian' for smooth, 'box' for fast)
        iterations: Number of blur passes (1-10), for stronger effects
        quality: Output quality for lossy formats (1-100)
        logger: Optional logger instance

    Returns:
        Dict containing arcane knowledge about the obscuration ritual

    Raises:
        InvalidReagentError: If input validation or parameters are invalid
        ArcaneDisruptionError: If the obscuration fails during casting
        SpellFumbleError: For general spell failures
    """
    # Set up logger if not provided
    if logger is None:
        logger = get_logger("obscure_artifact")

    # Validate blur type
    if blur_type not in SUPPORTED_BLUR_TYPES:
        raise InvalidReagentError(
            f"Unknown ritual type: {blur_type}",
            recovery_suggestion=f"Choose from: {', '.join(SUPPORTED_BLUR_TYPES)}"
        )

    # Validate radius
    if not MIN_RADIUS <= radius <= MAX_RADIUS:
        raise InvalidReagentError(
            f"Obscuration power must be between {MIN_RADIUS} and {MAX_RADIUS}, got {radius}",
            recovery_suggestion=f"Use a value between {MIN_RADIUS} (subtle) and {MAX_RADIUS} (heavy)"
        )

    # Validate iterations
    if not MIN_ITERATIONS <= iterations <= MAX_ITERATIONS:
        raise InvalidReagentError(
            f"Iterations must be between {MIN_ITERATIONS} and {MAX_ITERATIONS}, got {iterations}",
            recovery_suggestion=f"Use a value between {MIN_ITERATIONS} and {MAX_ITERATIONS} passes"
        )

    # Validate quality
    if not 1 <= quality <= 100:
        raise InvalidReagentError(
            f"Quality must be between 1 and 100, got {quality}",
            recovery_suggestion="Use a value between 1 (lowest) and 100 (highest)"
        )

    # Validate input file
    logger.info(f"Validating artifact: {input_path}")
    validation = validate_input_file(
        input_path,
        allowed_formats=SUPPORTED_IMAGE_FORMATS,
        max_size_bytes=MAX_FILE_SIZE,
        check_readable=True,
    )
    logger.info(f"Artifact validated: {format_bytes(validation['size_bytes'])}")

    # Validate and prepare output path
    output_path = validate_output_path(
        output_path,
        check_writable=True,
        create_parent_dirs=True,
    )

    # Set up performance tracking
    tracker = PerformanceTracker("obscure_artifact")
    tracker.set_input_size(validation["size_bytes"])
    tracker.start()

    # Open and process the image
    logger.info("Opening magical artifact...")
    try:
        with Image.open(input_path) as img:
            original_size = img.size
            original_mode = img.mode
            logger.info(f"Original dimensions: {original_size[0]}x{original_size[1]}")
            logger.info(f"Color mode: {original_mode}")

            # Convert RGBA to RGB if saving as JPEG
            output_format = os.path.splitext(output_path)[1].lower()
            if output_format in ['.jpg', '.jpeg'] and img.mode == 'RGBA':
                logger.info("Converting RGBA to RGB for JPEG output...")
                # Create white background
                background = Image.new('RGB', img.size, (255, 255, 255))
                background.paste(img, mask=img.split()[3])  # Use alpha channel as mask
                img = background

            # Apply blur filter for specified iterations
            logger.info(f"Casting {blur_type} obscuration ritual with radius {radius}...")
            logger.info(f"Applying {iterations} iteration(s)...")

            for i in range(iterations):
                if blur_type == "gaussian":
                    img = img.filter(ImageFilter.GaussianBlur(radius=radius))
                else:  # box
                    img = img.filter(ImageFilter.BoxBlur(radius=radius))
                logger.debug(f"Completed iteration {i + 1}/{iterations}")

            # Save the obscured image
            logger.info(f"Preserving obscured artifact to: {output_path}")
            save_kwargs = {}
            if output_format in ['.jpg', '.jpeg']:
                save_kwargs['quality'] = quality
                save_kwargs['optimize'] = True
            elif output_format == '.png':
                save_kwargs['optimize'] = True
            elif output_format == '.webp':
                save_kwargs['quality'] = quality
                save_kwargs['method'] = 6

            img.save(output_path, **save_kwargs)

    except IOError as e:
        raise ArcaneDisruptionError(
            f"Failed to process magical artifact: {e}",
            recovery_suggestion="Check that the file is a valid image and is not corrupted"
        )
    except Exception as e:
        raise ArcaneDisruptionError(
            f"Unexpected error during obscuration ritual: {e}",
            recovery_suggestion="Try a different radius value or blur type"
        )

    # Get output file size
    output_size = os.path.getsize(output_path)
    tracker.set_output_size(output_size)
    tracker.stop()

    logger.info("Obscuration ritual completed successfully!")

    # Build metadata
    metadata = get_spell_metadata_base("obscure_artifact")
    metadata.update({
        "input_path": input_path,
        "output_path": output_path,
        "settings": {
            "blur_type": blur_type,
            "radius": radius,
            "iterations": iterations,
            "quality": quality,
        },
        "transmutation": {
            "original_dimensions": {
                "width": original_size[0],
                "height": original_size[1],
                "pixels": original_size[0] * original_size[1],
            },
            "new_dimensions": {
                "width": original_size[0],
                "height": original_size[1],
                "pixels": original_size[0] * original_size[1],
            },
            "color_mode": original_mode,
        },
        "input_info": {
            "size_bytes": validation["size_bytes"],
            "format": validation["extension"],
        },
        "output_info": {
            "size_bytes": output_size,
            "format": os.path.splitext(output_path)[1].lower(),
        },
    })
    metadata["performance"] = tracker.get_metrics()

    return metadata


# =============================================================================
# COMMAND LINE INTERFACE
# =============================================================================

def main():
    parser = argparse.ArgumentParser(
        description="Cast the obscure artifact hex to shroud magical images in mystical haze",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic blur with default settings
  python spells/obscure_artifact.py --input photo.jpg

  # Heavy blur for privacy
  python spells/obscure_artifact.py --input sensitive.png --radius 20

  # Subtle blur for softening
  python spells/obscure_artifact.py --input portrait.png --radius 2

  # Fast box blur
  python spells/obscure_artifact.py --input sprite.png --blur-type box --radius 10

  # Multiple iterations for stronger effect
  python spells/obscure_artifact.py --input background.jpg --radius 5 --iterations 3

  # Custom output path
  python spells/obscure_artifact.py --input image.png --output blurred/image.png
        """
    )

    # Input/output arguments
    parser.add_argument(
        "--input", "-i",
        required=True,
        help="Path to the magical image artifact"
    )
    parser.add_argument(
        "--output", "-o",
        help="Path to the obscured artifact (optional)"
    )

    # Blur effect arguments
    parser.add_argument(
        "--radius", "-r",
        type=float,
        default=DEFAULT_RADIUS,
        help=f"Obscuration power {MIN_RADIUS}-{MAX_RADIUS} (default: {DEFAULT_RADIUS})"
    )
    parser.add_argument(
        "--blur-type",
        choices=SUPPORTED_BLUR_TYPES,
        default="gaussian",
        help="Ritual type: gaussian (smooth), box (fast) (default: gaussian)"
    )
    parser.add_argument(
        "--iterations",
        type=int,
        default=DEFAULT_ITERATIONS,
        help=f"Number of blur passes {MIN_ITERATIONS}-{MAX_ITERATIONS} (default: {DEFAULT_ITERATIONS})"
    )

    # Quality arguments
    parser.add_argument(
        "--quality", "-q",
        type=int,
        default=DEFAULT_QUALITY,
        help=f"Output quality for lossy formats 1-100 (default: {DEFAULT_QUALITY})"
    )

    # Processing options
    parser.add_argument(
        "--max-size",
        type=int,
        default=MAX_FILE_SIZE,
        metavar="BYTES",
        help=f"Maximum file size in bytes (default: {MAX_FILE_SIZE})"
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
        "obscure_artifact",
        log_level=args.log_level,
        log_file=args.log_file,
    )

    try:
        # Determine output path if not specified
        if args.output is None:
            original_name = os.path.splitext(os.path.basename(args.input))[0]
            input_ext = os.path.splitext(args.input)[1]
            output_dir = os.path.dirname(args.input) or "dungeon_cache"
            args.output = os.path.join(output_dir, f"{original_name}_obscured{input_ext}")

        metadata = obscure_artifact(
            input_path=args.input,
            output_path=args.output,
            radius=args.radius,
            blur_type=args.blur_type,
            iterations=args.iterations,
            quality=args.quality,
            logger=logger,
        )

        # Save metadata
        original_name = os.path.splitext(os.path.basename(args.input))[0]
        metadata_dir = os.path.dirname(metadata["output_path"]) or "dungeon_cache"
        metadata_path = os.path.join(
            metadata_dir, f"{original_name}_obscure_metadata.json"
        )
        save_metadata(metadata, metadata_path)

        # Print success message
        settings = metadata["settings"]
        transmutation = metadata["transmutation"]
        print(f"\n✓ Obscuration ritual completed successfully!")
        print(f"  Artifact: {metadata['input_path']}")
        print(f"  Obscured: {metadata['output_path']}")
        print(f"  Ritual: {settings['blur_type']}")
        print(f"  Obscuration power: {settings['radius']}")
        print(f"  Iterations: {settings['iterations']}")
        print(f"  Dimensions: {transmutation['new_dimensions']['width']}x{transmutation['new_dimensions']['height']}")
        print(f"  Size: {format_bytes(metadata['input_info']['size_bytes'])} → {format_bytes(metadata['output_info']['size_bytes'])}")
        print(f"  Duration: {metadata['performance']['duration_seconds']:.2f}s")
        print(f"  Arcane knowledge: {metadata_path}")

    except Exception as e:
        handle_spell_error(e, "obscure_artifact", exit_on_error=True)


if __name__ == "__main__":
    main()
