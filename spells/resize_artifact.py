import argparse
import json
import os
import sys
from datetime import datetime, timezone
from typing import Dict, Any, Optional, Tuple

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
    "name": "resize_artifact",
    "version": "1.0.0",
    "primary_keywords": ["resize", "scale", "resize image", "scale image", "resize artifact"],
    "secondary_keywords": {
        "dimensions": ["width", "height", "size", "resolution", "px", "pixels"],
        "scale_mode": ["percentage", "percent", "fit", "contain", "cover", "exact", "maintain aspect"],
        "quality": ["high quality", "fast", "thumbnail", "optimized"],
        "direction": ["larger", "smaller", "bigger", "downscale", "upscale"]
    },
    "supported_formats": ["jpg", "jpeg", "png", "webp", "bmp", "tiff", "gif"],
    "description": "Transmute the size of magical image artifacts while preserving their essence",
    "common_use_cases": [
        "Game asset preparation at multiple resolutions",
        "Thumbnail generation for previews",
        "Batch resizing sprite sheets for different device sizes",
        "Creating optimized versions for web distribution",
        "Preparing images for specific display dimensions"
    ],
    "examples": [
        "resize character.png to 512x512",
        "scale down all sprites by 50%",
        "resize landscape.jpg to fit within 1920x1080",
        "create 256x256 thumbnail from photo.png",
        "resize artifact to 80% of original size"
    ],
    "output_naming_pattern": "<name>_resized.<ext>",
    "cli_pattern": "python spells/resize_artifact.py --input <file> [resize options]",
    "cli_parameters": {
        "--input": "Path to magical image artifact (required)",
        "--output": "Path to transmuted artifact (optional)",
        "--width": "Target width in pixels (short: -w)",
        "--height": "Target height in pixels",
        "--scale": "Scale percentage (short: -s, e.g., 50 for half size)",
        "--fit": "Fit within bounds (maintains aspect ratio)",
        "--cover": "Cover bounds exactly (may crop, maintains aspect ratio)",
        "--exact": "Exact dimensions (may distort, ignores aspect ratio)",
        "--no-maintain-aspect": "Don't maintain aspect ratio (only applies when both width and height specified)",
        "--quality": "Output quality for lossy formats 1-100 (short: -q, default: 95)",
        "--resampling": "Resampling filter: nearest, bilinear, bicubic, lanczos (short: -r, default: lanczos)",
        "--log-level": "Logging level: DEBUG, INFO, WARNING, ERROR (default: INFO)",
        "--log-file": "Path to log file (optional)"
    }
}


# =============================================================================
# SPELL CONFIGURATION
# =============================================================================

# Maximum file size: 100MB default
MAX_FILE_SIZE = 100 * 1024 * 1024

# Resampling filters for different quality/speed needs
RESAMPLING_FILTERS = {
    "nearest": Image.NEAREST,
    "bilinear": Image.BILINEAR,
    "bicubic": Image.BICUBIC,
    "lanczos": Image.LANCZOS,
}

# Default quality for lossy formats
DEFAULT_QUALITY = 95


# =============================================================================
# RESIZING FUNCTIONS
# =============================================================================

def calculate_new_dimensions(
    original_size: Tuple[int, int],
    width: Optional[int] = None,
    height: Optional[int] = None,
    scale: Optional[float] = None,
    fit: bool = False,
    cover: bool = False,
    exact: bool = False,
    maintain_aspect: bool = True,
) -> Tuple[int, int, str]:
    """Calculate the new dimensions for the artifact transmutation.

    This subroutine determines the proper dimensions based on the requested
    transformation method, preserving the artifact's essence when appropriate.

    Args:
        original_size: Original (width, height) tuple
        width: Target width in pixels
        height: Target height in pixels
        scale: Scale percentage (e.g., 50 for half size)
        fit: Fit within bounds (maintains aspect ratio)
        cover: Cover bounds exactly (may crop, maintains aspect ratio)
        exact: Exact dimensions (may distort)
        maintain_aspect: Whether to maintain aspect ratio by default

    Returns:
        Tuple of (new_width, new_height, method_used)

    Raises:
        InvalidReagentError: If parameters are invalid or insufficient
    """
    orig_width, orig_height = original_size

    # Scale by percentage
    if scale is not None:
        new_width = int(orig_width * scale / 100)
        new_height = int(orig_height * scale / 100)
        return (new_width, new_height, "scale")

    # Exact dimensions (may distort)
    if exact:
        if width is None or height is None:
            raise InvalidReagentError(
                "Exact mode requires both --width and --height",
                recovery_suggestion="Provide both dimensions or use --fit/--cover mode"
            )
        return (width, height, "exact")

    # Fit within bounds (maintain aspect ratio)
    if fit:
        if width is None or height is None:
            raise InvalidReagentError(
                "Fit mode requires both --width and --height",
                recovery_suggestion="Provide maximum bounds for both dimensions"
            )
        # Calculate scaling factor to fit within bounds
        scale_x = width / orig_width
        scale_y = height / orig_height
        scale_factor = min(scale_x, scale_y)
        new_width = int(orig_width * scale_factor)
        new_height = int(orig_height * scale_factor)
        return (new_width, new_height, "fit")

    # Cover bounds exactly (may crop, maintains aspect ratio)
    if cover:
        if width is None or height is None:
            raise InvalidReagentError(
                "Cover mode requires both --width and --height",
                recovery_suggestion="Provide target dimensions for both axes"
            )
        # Calculate scaling factor to cover bounds
        scale_x = width / orig_width
        scale_y = height / orig_height
        scale_factor = max(scale_x, scale_y)
        new_width = int(orig_width * scale_factor)
        new_height = int(orig_height * scale_factor)
        return (new_width, new_height, "cover")

    # Default: resize with aspect ratio preservation
    if width and height:
        if maintain_aspect:
            # Fit within bounds
            scale_x = width / orig_width
            scale_y = height / orig_height
            scale_factor = min(scale_x, scale_y)
            new_width = int(orig_width * scale_factor)
            new_height = int(orig_height * scale_factor)
            return (new_width, new_height, "fit")
        else:
            # Exact dimensions
            return (width, height, "exact")

    if width:
        # Calculate height to maintain aspect ratio
        aspect_ratio = orig_height / orig_width
        new_width = width
        new_height = int(width * aspect_ratio)
        return (new_width, new_height, "width")

    if height:
        # Calculate width to maintain aspect ratio
        aspect_ratio = orig_width / orig_height
        new_height = height
        new_width = int(height * aspect_ratio)
        return (new_width, new_height, "height")

    raise InvalidReagentError(
        "Must specify at least one of: --width, --height, --scale, or use --fit/--cover mode",
        recovery_suggestion="Provide target dimensions or scale percentage"
    )


def resize_image(
    input_path: str,
    output_path: str,
    width: Optional[int] = None,
    height: Optional[int] = None,
    scale: Optional[float] = None,
    fit: bool = False,
    cover: bool = False,
    exact: bool = False,
    maintain_aspect: bool = True,
    quality: int = DEFAULT_QUALITY,
    resampling: str = "lanczos",
    logger: Optional[Any] = None,
) -> Dict[str, Any]:
    """Transmute the size of a magical image artifact.

    This powerful ritual changes the dimensions of image artifacts while
    preserving their magical essence through careful alchemical transformation.

    Args:
        input_path: Path to the source magical image artifact
        output_path: Path to the transformed artifact
        width: Target width in pixels
        height: Target height in pixels
        scale: Scale percentage (e.g., 50 for half size)
        fit: Fit within bounds (maintains aspect ratio)
        cover: Cover bounds exactly (may crop, maintains aspect ratio)
        exact: Exact dimensions (may distort)
        maintain_aspect: Whether to maintain aspect ratio by default
        quality: Output quality for lossy formats (1-100)
        resampling: Resampling filter (nearest, bilinear, bicubic, lanczos)
        logger: Optional logger instance

    Returns:
        Dict containing arcane knowledge about the transmutation

    Raises:
        InvalidReagentError: If input validation or parameters are invalid
        ArcaneDisruptionError: If the transmutation fails during casting
        SpellFumbleError: For general spell failures
    """
    # Set up logger if not provided
    if logger is None:
        logger = get_logger("resize_artifact")

    # Validate resampling filter
    if resampling not in RESAMPLING_FILTERS:
        raise InvalidReagentError(
            f"Invalid resampling filter: {resampling}",
            recovery_suggestion=f"Choose from: {', '.join(RESAMPLING_FILTERS.keys())}"
        )

    resampling_filter = RESAMPLING_FILTERS[resampling]

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
    tracker = PerformanceTracker("resize_artifact")
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

            # Calculate new dimensions
            logger.info("Calculating transmutation parameters...")
            new_width, new_height, method = calculate_new_dimensions(
                original_size=original_size,
                width=width,
                height=height,
                scale=scale,
                fit=fit,
                cover=cover,
                exact=exact,
                maintain_aspect=maintain_aspect,
            )
            logger.info(f"Method: {method}")
            logger.info(f"New dimensions: {new_width}x{new_height}")

            # Convert RGBA to RGB if saving as JPEG
            output_format = os.path.splitext(output_path)[1].lower()
            if output_format in ['.jpg', '.jpeg'] and img.mode == 'RGBA':
                logger.info("Converting RGBA to RGB for JPEG output...")
                # Create white background
                background = Image.new('RGB', img.size, (255, 255, 255))
                background.paste(img, mask=img.split()[3])  # Use alpha channel as mask
                img = background

            # Handle cover mode (center crop after resize)
            if cover and (new_width > width or new_height > height):
                logger.info(f"Applying center crop to {width}x{height}...")
                # Resize to cover
                resized = img.resize((new_width, new_height), resampling_filter)
                # Calculate crop position
                left = (new_width - width) // 2
                top = (new_height - height) // 2
                right = left + width
                bottom = top + height
                # Crop
                img = resized.crop((left, top, right, bottom))
                new_width, new_height = width, height
            else:
                # Standard resize
                logger.info(f"Transmuting artifact using {resampling} filter...")
                img = img.resize((new_width, new_height), resampling_filter)

            # Save the resized image
            logger.info(f"Preserving transmuted artifact to: {output_path}")
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
            f"Unexpected error during transmutation: {e}",
            recovery_suggestion="Try a different resampling filter or output format"
        )

    # Get output file size
    output_size = os.path.getsize(output_path)
    tracker.set_output_size(output_size)
    tracker.stop()

    logger.info("Transmutation completed successfully!")

    # Build metadata
    metadata = get_spell_metadata_base("resize_artifact")
    metadata.update({
        "input_path": input_path,
        "output_path": output_path,
        "settings": {
            "width": width,
            "height": height,
            "scale": scale,
            "fit": fit,
            "cover": cover,
            "exact": exact,
            "maintain_aspect": maintain_aspect,
            "quality": quality,
            "resampling": resampling,
        },
        "transmutation": {
            "original_dimensions": {
                "width": original_size[0],
                "height": original_size[1],
                "pixels": original_size[0] * original_size[1],
            },
            "new_dimensions": {
                "width": new_width,
                "height": new_height,
                "pixels": new_width * new_height,
            },
            "method": method,
            "color_mode": original_mode,
            "scale_factor": round(new_width / original_size[0], 4) if original_size[0] > 0 else 0,
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
        description="Transmute the size of magical image artifacts while preserving their essence",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Resize to exact dimensions (maintains aspect ratio by default)
  python spells/resize_artifact.py --input character.png --width 512 --height 512

  # Scale to 50% of original size
  python spells/resize_artifact.py --input sprite.png --scale 50

  # Fit within maximum bounds (maintains aspect ratio)
  python spells/resize_artifact.py --input landscape.jpg --width 1920 --height 1080 --fit

  # Cover exact bounds (may crop, maintains aspect ratio)
  python spells/resize_artifact.py --input photo.png --width 800 --height 600 --cover

  # Resize to exact width (height calculated automatically)
  python spells/resize_artifact.py --input icon.png --width 256

  # Exact dimensions (may distort)
  python spells/resize_artifact.py --input square.png --width 200 --height 300 --exact
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
        help="Path to the transmuted artifact (optional)"
    )

    # Dimension arguments
    parser.add_argument(
        "--width", "-w",
        type=int,
        help="Target width in pixels"
    )
    parser.add_argument(
        "--height",
        type=int,
        help="Target height in pixels"
    )
    parser.add_argument(
        "--scale", "-s",
        type=float,
        help="Scale percentage (e.g., 50 for half size, 200 for double size)"
    )

    # Mode arguments
    parser.add_argument(
        "--fit",
        action="store_true",
        help="Fit within bounds (maintains aspect ratio, image fits entirely within bounds)"
    )
    parser.add_argument(
        "--cover",
        action="store_true",
        help="Cover bounds exactly (may crop, maintains aspect ratio, fills bounds completely)"
    )
    parser.add_argument(
        "--exact",
        action="store_true",
        help="Exact dimensions (may distort, ignores aspect ratio)"
    )
    parser.add_argument(
        "--no-maintain-aspect",
        action="store_true",
        help="Don't maintain aspect ratio (only applies when both width and height specified)"
    )

    # Quality arguments
    parser.add_argument(
        "--quality", "-q",
        type=int,
        default=DEFAULT_QUALITY,
        help=f"Output quality for lossy formats 1-100 (default: {DEFAULT_QUALITY})"
    )
    parser.add_argument(
        "--resampling", "-r",
        choices=list(RESAMPLING_FILTERS.keys()),
        default="lanczos",
        help="Resampling filter (default: lanczos)"
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
        "resize_artifact",
        log_level=args.log_level,
        log_file=args.log_file,
    )

    try:
        # Determine output path if not specified
        if args.output is None:
            original_name = os.path.splitext(os.path.basename(args.input))[0]
            input_ext = os.path.splitext(args.input)[1]
            output_dir = os.path.dirname(args.input) or "dungeon_cache"
            args.output = os.path.join(output_dir, f"{original_name}_resized{input_ext}")

        metadata = resize_image(
            input_path=args.input,
            output_path=args.output,
            width=args.width,
            height=args.height,
            scale=args.scale,
            fit=args.fit,
            cover=args.cover,
            exact=args.exact,
            maintain_aspect=not args.no_maintain_aspect,
            quality=args.quality,
            resampling=args.resampling,
            logger=logger,
        )

        # Save metadata
        original_name = os.path.splitext(os.path.basename(args.input))[0]
        metadata_dir = os.path.dirname(metadata["output_path"]) or "dungeon_cache"
        metadata_path = os.path.join(
            metadata_dir, f"{original_name}_resize_metadata.json"
        )
        save_metadata(metadata, metadata_path)

        # Print success message
        transmutation = metadata["transmutation"]
        print(f"\n✓ Transmutation completed successfully!")
        print(f"  Artifact: {metadata['input_path']}")
        print(f"  Transmuted: {metadata['output_path']}")
        print(f"  Original dimensions: {transmutation['original_dimensions']['width']}x{transmutation['original_dimensions']['height']}")
        print(f"  New dimensions: {transmutation['new_dimensions']['width']}x{transmutation['new_dimensions']['height']}")
        print(f"  Method: {transmutation['method']}")

        if transmutation['scale_factor'] != 1.0:
            scale_pct = transmutation['scale_factor'] * 100
            print(f"  Scale factor: {scale_pct:.1f}%")

        print(f"  Size: {format_bytes(metadata['input_info']['size_bytes'])} → {format_bytes(metadata['output_info']['size_bytes'])}")
        print(f"  Duration: {metadata['performance']['duration_seconds']:.2f}s")
        print(f"  Arcane knowledge: {metadata_path}")

    except Exception as e:
        handle_spell_error(e, "resize_artifact", exit_on_error=True)


if __name__ == "__main__":
    main()
