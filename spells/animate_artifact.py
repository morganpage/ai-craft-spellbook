import argparse
import json
import os
import sys
from datetime import datetime, timezone
from typing import Dict, Any, Optional, List, Tuple

# Add parent directory to path for imports when running as script
if __name__ == "__main__":
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PIL import Image

from spells.utils.common import (
    save_metadata,
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
    "name": "animate_artifact",
    "version": "1.0.0",
    "primary_keywords": [
        "create gif", "make gif", "generate gif", "animate", "create animation",
        "make animation", "gif from images", "gif from directory", "frames to gif"
    ],
    "secondary_keywords": {
        "timing": ["duration", "frame rate", "fps", "speed", "temporal", "interval"],
        "looping": ["loop", "infinite", "repeat", "eternal", "finite"],
        "optimization": ["optimize", "compress", "reduce size", "smaller"],
        "resizing": ["resize", "scale", "size", "dimensions", "width", "height"]
    },
    "supported_formats": ["png", "jpg", "jpeg", "webp", "bmp", "tiff"],
    "description": "Weave magical image panels into an animated scroll that captures chronomantic essence",
    "common_use_cases": [
        "Game sprite animation for character movements",
        "UI element animations for interface feedback",
        "Demonstration GIFs for tutorials and documentation",
        "Preview animations for game asset development",
        "Animated icons and loading indicators"
    ],
    "examples": [
        "create gif from frames/",
        "make animation from sprite_frames/ with 200ms duration",
        "generate gif from panels/ with 3 loops",
        "animate frames/ and resize to 256x256",
        "create optimized gif from rendered_frames/"
    ],
    "output_naming_pattern": "<dirname>_animated.gif",
    "cli_pattern": "python spells/animate_artifact.py --input <directory> [animation options]",
    "cli_parameters": {
        "--input": "Path to panel archive directory (required)",
        "--output": "Path to animated scroll (optional)",
        "--duration": "Temporal power per panel in milliseconds (short: -d, default: 100)",
        "--loop": "Eternal binding (0) or finite incantation count (default: 0)",
        "--optimize": "Apply arcane compression (default: True)",
        "--no-optimize": "Disable arcane compression",
        "--width": "Target width for dimensional harmonization (short: -w)",
        "--height": "Target height for dimensional harmonization",
        "--no-maintain-aspect": "Don't preserve aspect ratio during harmonization"
    }
}


# =============================================================================
# SPELL CONFIGURATION
# =============================================================================

# Animation parameter limits
MIN_DURATION = 10  # milliseconds
MAX_DURATION = 5000  # milliseconds
DEFAULT_DURATION = 100  # milliseconds

MIN_LOOP = 0  # 0 = infinite
DEFAULT_LOOP = 0  # infinite by default

# Minimum panel count for animation
MIN_PANELS = 2

# Maximum total file size for input panels: 500MB
MAX_TOTAL_SIZE = 500 * 1024 * 1024


# =============================================================================
# VALIDATION FUNCTIONS
# =============================================================================

def validate_panels_directory(input_dir: str) -> List[str]:
    """Validate the panel archive and return list of image files.

    Args:
        input_dir: Path to the panel archive directory

    Returns:
        List of image file paths sorted alphabetically

    Raises:
        InvalidReagentError: If directory is invalid or contains no images
    """
    # Check if directory exists
    if not os.path.exists(input_dir):
        raise InvalidReagentError(
            f"Panel archive not found: {input_dir}",
            recovery_suggestion="Check that the directory path is correct and exists."
        )

    if not os.path.isdir(input_dir):
        raise InvalidReagentError(
            f"Path is not a directory: {input_dir}",
            recovery_suggestion="Provide a path to a directory containing image panels."
        )

    # Find all image files
    panel_files = []
    total_size = 0

    try:
        for filename in os.listdir(input_dir):
            file_path = os.path.join(input_dir, filename)
            if os.path.isfile(file_path):
                # Check file extension
                _, ext = os.path.splitext(filename)
                if ext.lower() in SUPPORTED_IMAGE_FORMATS:
                    panel_files.append(file_path)
                    total_size += os.path.getsize(file_path)
    except PermissionError as e:
        raise ArcaneDisruptionError(
            f"Cannot read panel archive: {input_dir}",
            recovery_suggestion=f"Check directory permissions: {e}"
        )

    # Check if any panels were found
    if not panel_files:
        raise InvalidReagentError(
            f"No magical panels found in: {input_dir}",
            recovery_suggestion=f"Add supported image files: {', '.join(sorted(SUPPORTED_IMAGE_FORMATS))}"
        )

    # Check minimum panel count
    if len(panel_files) < MIN_PANELS:
        raise InvalidReagentError(
            f"Animation requires at least {MIN_PANELS} magical panels, found {len(panel_files)}",
            recovery_suggestion=f"Add at least {MIN_PANELS} image files to the directory."
        )

    # Check total size
    if total_size > MAX_TOTAL_SIZE:
        max_mb = MAX_TOTAL_SIZE / (1024 * 1024)
        total_mb = total_size / (1024 * 1024)
        raise InvalidReagentError(
            f"Panel archive too large: {total_mb:.2f}MB (max: {max_mb:.2f}MB)",
            recovery_suggestion="Process smaller batches or reduce image file sizes."
        )

    # Sort alphabetically for consistent frame ordering
    panel_files.sort()

    return panel_files


def validate_duration(duration: int) -> None:
    """Validate temporal power (frame duration).

    Args:
        duration: Frame duration in milliseconds

    Raises:
        InvalidReagentError: If duration is out of valid range
    """
    if not MIN_DURATION <= duration <= MAX_DURATION:
        raise InvalidReagentError(
            f"Temporal power must be between {MIN_DURATION}ms and {MAX_DURATION}ms, got {duration}ms",
            recovery_suggestion=f"Use a value between {MIN_DURATION} (fast) and {MAX_DURATION} (slow) milliseconds."
        )


def validate_loop(loop: int) -> None:
    """Validate incantation count (loop parameter).

    Args:
        loop: Number of loops (0 = infinite)

    Raises:
        InvalidReagentError: If loop value is invalid
    """
    if loop < MIN_LOOP:
        raise InvalidReagentError(
            f"Incantation count must be {MIN_LOOP} or positive, got {loop}",
            recovery_suggestion="Use 0 for infinite loop or a positive number for finite loops."
        )


# =============================================================================
# DIMENSIONAL HARMONIZATION
# =============================================================================

def harmonize_dimensions(
    panels: List[Image.Image],
    width: Optional[int] = None,
    height: Optional[int] = None,
    maintain_aspect: bool = True,
    logger: Optional[Any] = None,
) -> Tuple[List[Image.Image], Tuple[int, int]]:
    """Harmonize all panels to the same dimensions.

    Args:
        panels: List of PIL Image objects
        width: Target width (optional)
        height: Target height (optional)
        maintain_aspect: Whether to maintain aspect ratio
        logger: Optional logger instance

    Returns:
        Tuple of (harmonized panels list, (final_width, final_height))

    Raises:
        InvalidReagentError: If dimensions are invalid
    """
    if logger is None:
        logger = get_logger("animate_artifact")

    # Get dimensions of first panel as reference
    first_panel = panels[0]
    original_width, original_height = first_panel.size

    # Determine target dimensions
    if width is None and height is None:
        # Use dimensions of first panel
        target_width, target_height = original_width, original_height
        logger.info(f"Using original dimensions: {target_width}x{target_height}")
    elif width is not None and height is not None:
        if maintain_aspect:
            # Fit within bounds
            scale_x = width / original_width
            scale_y = height / original_height
            scale_factor = min(scale_x, scale_y)
            target_width = int(original_width * scale_factor)
            target_height = int(original_height * scale_factor)
            logger.info(f"Fitting within {width}x{height}: {target_width}x{target_height}")
        else:
            # Exact dimensions
            target_width, target_height = width, height
            logger.info(f"Using exact dimensions: {target_width}x{target_height}")
    elif width is not None:
        # Calculate height to maintain aspect ratio
        aspect_ratio = original_height / original_width
        target_width = width
        target_height = int(width * aspect_ratio)
        logger.info(f"Width {width}: calculated height {target_height}")
    else:  # height is not None
        # Calculate width to maintain aspect ratio
        aspect_ratio = original_width / original_height
        target_height = height
        target_width = int(height * aspect_ratio)
        logger.info(f"Height {height}: calculated width {target_width}")

    # Validate target dimensions
    if target_width < 1 or target_height < 1:
        raise InvalidReagentError(
            f"Invalid target dimensions: {target_width}x{target_height}",
            recovery_suggestion="Use larger dimension values."
        )

    # Harmonize all panels
    harmonized = []
    for i, panel in enumerate(panels):
        if panel.size != (target_width, target_height):
            logger.debug(f"Harmonizing panel {i+1}/{len(panels)}: {panel.size[0]}x{panel.size[1]} -> {target_width}x{target_height}")
            # Use high-quality resampling
            resized = panel.resize((target_width, target_height), Image.Resampling.LANCZOS)
            harmonized.append(resized)
        else:
            harmonized.append(panel)

    return harmonized, (target_width, target_height)


# =============================================================================
# ANIMATION FUNCTIONS
# =============================================================================

def animate_artifact(
    input_dir: str,
    output_path: Optional[str] = None,
    duration: int = DEFAULT_DURATION,
    loop: int = DEFAULT_LOOP,
    optimize: bool = True,
    width: Optional[int] = None,
    height: Optional[int] = None,
    maintain_aspect: bool = True,
    logger: Optional[Any] = None,
) -> Dict[str, Any]:
    """Weave magical image panels into an animated scroll.

    This powerful ritual combines multiple magical image panels into a
    single animated scroll (GIF) that captures the chronomantic essence
    of movement. The panels are woven together with precise temporal
    power and can be bound eternally or for a finite number of cycles.

    Args:
        input_dir: Path to the panel archive directory
        output_path: Path to the animated scroll (optional)
        duration: Temporal power per panel in milliseconds (10-5000)
        loop: Eternal binding (0) or finite incantation count
        optimize: Apply arcane compression to reduce file size
        width: Target width for dimensional harmonization (optional)
        height: Target height for dimensional harmonization (optional)
        maintain_aspect: Preserve aspect ratio during harmonization
        logger: Optional logger instance

    Returns:
        Dict containing arcane knowledge about the animation ritual

    Raises:
        InvalidReagentError: If input validation or parameters are invalid
        ArcaneDisruptionError: If the animation fails during casting
        SpellFumbleError: For general spell failures
    """
    # Set up logger if not provided
    if logger is None:
        logger = get_logger("animate_artifact")

    # Validate parameters
    validate_duration(duration)
    validate_loop(loop)

    # Validate directory and get panel files
    logger.info(f"Validating panel archive: {input_dir}")
    panel_files = validate_panels_directory(input_dir)
    logger.info(f"Found {len(panel_files)} magical panels")

    # Calculate total input size
    total_input_size = sum(os.path.getsize(f) for f in panel_files)
    logger.info(f"Total panel archive size: {format_bytes(total_input_size)}")

    # Validate and prepare output path
    if output_path is None:
        # Auto-generate output path from directory name
        dir_name = os.path.basename(os.path.normpath(input_dir))
        output_dir = os.path.dirname(input_dir) or "dungeon_cache"
        output_path = os.path.join(output_dir, f"{dir_name}_animated.gif")

    output_path = validate_output_path(
        output_path,
        check_writable=True,
        create_parent_dirs=True,
    )

    # Set up performance tracking
    tracker = PerformanceTracker("animate_artifact")
    tracker.set_input_size(total_input_size)
    tracker.start()

    # Load all panels
    logger.info("Loading magical panels...")
    panels = []
    original_dimensions = []

    for i, panel_file in enumerate(panel_files):
        try:
            with Image.open(panel_file) as img:
                logger.debug(f"Panel {i+1}/{len(panel_files)}: {panel_file} ({img.size[0]}x{img.size[1]}, {img.mode})")
                original_dimensions.append((img.size[0], img.size[1]))

                # Convert RGBA to RGB for GIF compatibility
                # GIF format doesn't support alpha channel properly
                if img.mode == 'RGBA':
                    logger.debug(f"Converting RGBA to RGB for GIF compatibility")
                    # Create white background for transparency
                    background = Image.new('RGB', img.size, (255, 255, 255))
                    background.paste(img, mask=img.split()[3])  # Use alpha channel as mask
                    img = background

                # Ensure RGB mode
                if img.mode != 'RGB':
                    img = img.convert('RGB')

                # Load into memory and store
                img.load()
                panels.append(img)

        except (IOError, OSError) as e:
            raise ArcaneDisruptionError(
                f"Failed to load magical panel: {panel_file}",
                recovery_suggestion=f"Check that the file is a valid image: {e}"
            )

    # Check original dimensions consistency
    unique_dimensions = set(original_dimensions)
    if len(unique_dimensions) > 1:
        logger.info(f"Panels have varying dimensions: {unique_dimensions}")
        logger.info("Dimensional harmonization will be applied")

    # Get reference dimensions
    ref_width, ref_height = original_dimensions[0]
    logger.info(f"Reference panel dimensions: {ref_width}x{ref_height}")

    # Apply dimensional harmonization if needed
    if width is not None or height is not None or len(unique_dimensions) > 1:
        logger.info("Applying dimensional harmonization...")
        panels, (final_width, final_height) = harmonize_dimensions(
            panels,
            width=width,
            height=height,
            maintain_aspect=maintain_aspect,
            logger=logger,
        )
    else:
        final_width, final_height = ref_width, ref_height

    # Create animated GIF
    logger.info(f"Weaving {len(panels)} panels into animated scroll...")
    logger.info(f"Temporal power: {duration}ms per panel")
    logger.info(f"Incantation binding: {'eternal' if loop == 0 else f'{loop} cycles'}")
    logger.info(f"Arcane compression: {'enabled' if optimize else 'disabled'}")

    try:
        # Save first frame as GIF with append_images for the rest
        panels[0].save(
            output_path,
            save_all=True,
            append_images=panels[1:],
            duration=duration,
            loop=loop,
            optimize=optimize,
            disposal=2,  # Clear background between frames for cleaner animation
        )

    except Exception as e:
        raise ArcaneDisruptionError(
            f"Failed to weave animated scroll: {e}",
            recovery_suggestion="Try reducing frame count or dimensions, or disable optimization"
        )

    # Get output file size
    output_size = os.path.getsize(output_path)
    tracker.set_output_size(output_size)
    tracker.stop()

    # Calculate animation metrics
    frame_rate_fps = 1000.0 / duration
    duration_seconds = (len(panels) * duration) / 1000.0

    logger.info("Animation ritual completed successfully!")

    # Build metadata
    metadata = get_spell_metadata_base("animate_artifact")
    metadata.update({
        "input_dir": input_dir,
        "output_path": output_path,
        "settings": {
            "duration": duration,
            "loop": loop,
            "optimize": optimize,
            "width": width,
            "height": height,
            "maintain_aspect": maintain_aspect,
        },
        "animation": {
            "frame_count": len(panels),
            "original_dimensions": {
                "width": ref_width,
                "height": ref_height,
            },
            "final_dimensions": {
                "width": final_width,
                "height": final_height,
            },
            "frame_rate_fps": round(frame_rate_fps, 2),
            "duration_seconds": round(duration_seconds, 2),
            "is_infinite_loop": loop == 0,
            "loop_count": "infinite" if loop == 0 else loop,
        },
        "panels": {
            "count": len(panels),
            "files": [os.path.basename(f) for f in panel_files],
        },
        "input_info": {
            "total_size_bytes": total_input_size,
            "panel_count": len(panel_files),
        },
        "output_info": {
            "size_bytes": output_size,
            "format": ".gif",
        },
    })
    metadata["performance"] = tracker.get_metrics()

    return metadata


# =============================================================================
# COMMAND LINE INTERFACE
# =============================================================================

def main():
    parser = argparse.ArgumentParser(
        description="Weave magical image panels into an animated scroll that captures chronomantic essence",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic animation with default settings (10fps, infinite loop)
  python spells/animate_artifact.py --input frames/

  # Custom frame rate (20fps = 50ms per frame)
  python spells/animate_artifact.py --input sprite_frames/ --duration 50

  # Finite loop (play 3 times then stop)
  python spells/animate_artifact.py --input frames/ --loop 3

  # Resize during animation
  python spells/animate_artifact.py --input frames/ --width 256 --height 256

  # Disable optimization for faster processing
  python spells/animate_artifact.py --input frames/ --no-optimize

  # Custom output path
  python spells/animate_artifact.py --input frames/ --output animations/my_animation.gif

  # Slow animation (5fps = 200ms per frame)
  python spells/animate_artifact.py --input frames/ --duration 200

  # Fast animation (20fps = 50ms per frame)
  python spells/animate_artifact.py --input frames/ --duration 50
        """
    )

    # Input/output arguments
    parser.add_argument(
        "--input", "-i",
        required=True,
        help="Path to panel archive directory"
    )
    parser.add_argument(
        "--output", "-o",
        help="Path to animated scroll (optional)"
    )

    # Animation arguments
    parser.add_argument(
        "--duration", "-d",
        type=int,
        default=DEFAULT_DURATION,
        metavar="MILLISECONDS",
        help=f"Temporal power per panel in milliseconds {MIN_DURATION}-{MAX_DURATION} (default: {DEFAULT_DURATION})"
    )
    parser.add_argument(
        "--loop",
        type=int,
        default=DEFAULT_LOOP,
        metavar="COUNT",
        help=f"Eternal binding (0) or finite incantation count (default: {DEFAULT_LOOP})"
    )

    # Optimization argument
    parser.add_argument(
        "--no-optimize",
        action="store_true",
        help="Disable arcane compression"
    )

    # Dimensional harmonization arguments
    parser.add_argument(
        "--width", "-w",
        type=int,
        metavar="PIXELS",
        help="Target width for dimensional harmonization"
    )
    parser.add_argument(
        "--height",
        type=int,
        metavar="PIXELS",
        help="Target height for dimensional harmonization"
    )
    parser.add_argument(
        "--no-maintain-aspect",
        action="store_true",
        help="Don't preserve aspect ratio during harmonization"
    )

    # Processing options
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
        "animate_artifact",
        log_level=args.log_level,
        log_file=args.log_file,
    )

    try:
        metadata = animate_artifact(
            input_dir=args.input,
            output_path=args.output,
            duration=args.duration,
            loop=args.loop,
            optimize=not args.no_optimize,
            width=args.width,
            height=args.height,
            maintain_aspect=not args.no_maintain_aspect,
            logger=logger,
        )

        # Save metadata
        dir_name = os.path.basename(os.path.normpath(args.input))
        metadata_dir = os.path.dirname(metadata["output_path"]) or "dungeon_cache"
        metadata_path = os.path.join(
            metadata_dir, f"{dir_name}_animated_metadata.json"
        )
        save_metadata(metadata, metadata_path)

        # Print success message
        settings = metadata["settings"]
        animation = metadata["animation"]
        loop_text = "Eternal" if animation['is_infinite_loop'] else f"{animation['loop_count']} times"
        print(f"\n✓ Animation ritual completed successfully!")
        print(f"  Panel archive: {metadata['input_dir']}")
        print(f"  Animated scroll: {metadata['output_path']}")
        print(f"  Frame count: {animation['frame_count']}")
        print(f"  Frame rate: {animation['frame_rate_fps']} fps")
        print(f"  Duration: {animation['duration_seconds']}s")
        print(f"  Incantation binding: {loop_text}")
        print(f"  Dimensions: {animation['final_dimensions']['width']}x{animation['final_dimensions']['height']}")
        print(f"  Optimization: {'Enabled' if settings['optimize'] else 'Disabled'}")
        print(f"  Size: {format_bytes(metadata['input_info']['total_size_bytes'])} → {format_bytes(metadata['output_info']['size_bytes'])}")

        # Calculate compression ratio
        if metadata['input_info']['total_size_bytes'] > 0:
            ratio = metadata['output_info']['size_bytes'] / metadata['input_info']['total_size_bytes']
            print(f"  Compression ratio: {ratio:.2%}")

        print(f"  Duration: {metadata['performance']['duration_seconds']:.2f}s")
        print(f"  Arcane knowledge: {metadata_path}")

    except Exception as e:
        handle_spell_error(e, "animate_artifact", exit_on_error=True)


if __name__ == "__main__":
    main()
