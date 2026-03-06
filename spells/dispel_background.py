import argparse
import io
import json
import os
import sys
from datetime import datetime, timezone
from typing import Dict, Any, Optional, List

# Add parent directory to path for imports when running as script
if __name__ == "__main__":
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from rembg import remove
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
# SPELL CONFIGURATION
# =============================================================================

SUPPORTED_MODELS = [
    "u2net",
    "u2netp",
    "u2net_human_seg",
    "u2net_cloth_seg",
    "silueta",
]

SUPPORTED_FORMATS = {".jpg", ".jpeg", ".png", ".webp", ".bmp", ".tiff", ".gif"}

# Maximum file size: 50MB default
MAX_FILE_SIZE = 50 * 1024 * 1024


# =============================================================================
# MAIN SPELL FUNCTION
# =============================================================================

def remove_background(
    input_path: str,
    output_path: Optional[str] = None,
    model: str = "u2net",
    alpha_matting: bool = False,
    alpha_matting_foreground_threshold: int = 240,
    alpha_matting_background_threshold: int = 10,
    alpha_matting_erode_size: int = 10,
    logger: Optional[Any] = None,
) -> Dict[str, Any]:
    """Cast the dispel background hex to vanish unwanted magical backgrounds.

    This powerful incantation uses arcane vision to detect foreground subjects
    and banish the magical background, leaving behind a transparent treasure.

    Args:
        input_path: Path to the magical image artifact
        output_path: Path to the dispelled image artifact (optional, auto-generated if not provided)
        model: Arcane crystal to use for background detection (default: u2net)
        alpha_matting: Apply alpha matting for cleaner edges (default: False)
        alpha_matting_foreground_threshold: Foreground threshold for alpha matting (default: 240)
        alpha_matting_background_threshold: Background threshold for alpha matting (default: 10)
        alpha_matting_erode_size: Erosion size for alpha matting (default: 10)
        logger: Optional logger instance for tracking progress

    Returns:
        Dict containing arcane knowledge about the dispelling ritual

    Raises:
        InvalidReagentError: If input validation fails
        ArcaneDisruptionError: If the ritual fails during casting
        SpellFumbleError: For general spell failures
    """
    # Set up logger if not provided
    if logger is None:
        logger = get_logger("dispel_background")

    # Validate input file
    logger.info(f"Validating artifact: {input_path}")
    validation = validate_input_file(
        input_path,
        allowed_formats=SUPPORTED_FORMATS,
        max_size_bytes=MAX_FILE_SIZE,
        check_readable=True,
    )
    logger.info(f"Artifact validated: {format_bytes(validation['size_bytes'])}")

    # Validate model choice
    if model not in SUPPORTED_MODELS:
        raise InvalidReagentError(
            f"Unsupported arcane crystal: {model}",
            recovery_suggestion=f"Choose from: {', '.join(SUPPORTED_MODELS)}"
        )

    # Determine output path
    original_name = os.path.splitext(os.path.basename(input_path))[0]

    if output_path is None:
        output_dir = os.path.dirname(input_path) or "dungeon_cache"
        output_path = os.path.join(output_dir, f"{original_name}_dispelled.png")

    # Validate and prepare output path
    output_path = validate_output_path(
        output_path,
        check_writable=True,
        create_parent_dirs=True,
    )

    # Set up performance tracking
    tracker = PerformanceTracker("dispel_background")
    tracker.set_input_size(validation["size_bytes"])
    tracker.start()

    try:
        # Read input image
        logger.info("Reading magical artifact...")
        input_img = Image.open(input_path)
        input_size = input_img.size
        input_mode = input_img.mode
        input_img.close()

        # Process the image
        logger.info(f"Channeling dispel background hex with {model} crystal...")
        with open(input_path, "rb") as input_file:
            input_data = input_file.read()

        # Apply background removal
        output_data = remove(
            input_data,
            session_name=model,
            alpha_matting=alpha_matting,
            alpha_matting_foreground_threshold=alpha_matting_foreground_threshold,
            alpha_matting_background_threshold=alpha_matting_background_threshold,
            alpha_matting_erode_size=alpha_matting_erode_size,
        )

        # Save output
        logger.info("Preserving dispelled artifact...")
        output_img = Image.open(io.BytesIO(output_data))
        output_img.save(output_path, format="PNG", optimize=True)
        output_size = output_img.size
        output_img.close()

        # Get output file size
        output_size_bytes = os.path.getsize(output_path)
        tracker.set_output_size(output_size_bytes)
        tracker.stop()

        logger.info("Ritual completed successfully!")

        # Build metadata
        metadata = get_spell_metadata_base("dispel_background")
        metadata.update({
            "input_path": input_path,
            "output_path": output_path,
            "input_size": f"{input_size[0]}x{input_size[1]}",
            "output_size": f"{output_size[0]}x{output_size[1]}",
            "input_mode": input_mode,
            "output_mode": "RGBA",
            "input_size_bytes": validation["size_bytes"],
            "output_size_bytes": output_size_bytes,
            "size_change_percent": (
                round((output_size_bytes / validation["size_bytes"] - 1) * 100, 2)
                if validation["size_bytes"] > 0
                else 0
            ),
            "model": model,
            "alpha_matting": alpha_matting,
            "alpha_matting_settings": {
                "foreground_threshold": alpha_matting_foreground_threshold if alpha_matting else None,
                "background_threshold": alpha_matting_background_threshold if alpha_matting else None,
                "erode_size": alpha_matting_erode_size if alpha_matting else None,
            } if alpha_matting else None,
        })
        metadata["performance"] = tracker.get_metrics()

        return metadata

    except MemoryError as e:
        raise ArcaneDisruptionError(
            "Insufficient magical energy (memory) for ritual",
            recovery_suggestion="Try a smaller image or a different model (u2netp is lighter)."
        )
    except IOError as e:
        raise ArcaneDisruptionError(
            f"Failed to read or write artifact: {e}",
            recovery_suggestion="Check file permissions and disk space."
        )
    except Exception as e:
        if isinstance(e, (InvalidReagentError, ArcaneDisruptionError)):
            raise
        raise SpellFumbleError(
            f"Unexpected magical failure: {e}",
            recovery_suggestion="Check the error details and try again."
        )


# =============================================================================
# BATCH PROCESSING
# =============================================================================

def remove_background_batch(
    input_paths: List[str],
    output_dir: Optional[str] = None,
    model: str = "u2net",
    logger: Optional[Any] = None,
) -> List[Dict[str, Any]]:
    """Cast the dispel background hex on multiple artifacts.

    Args:
        input_paths: List of paths to magical image artifacts
        output_dir: Directory for dispelled artifacts (optional)
        model: Arcane crystal to use for background detection
        logger: Optional logger instance

    Returns:
        List of metadata dicts for each processed artifact
    """
    if logger is None:
        logger = get_logger("dispel_background")

    results = []
    total = len(input_paths)

    logger.info(f"Starting batch ritual: {total} artifacts")

    for i, input_path in enumerate(input_paths, 1):
        try:
            logger.info(f"Processing artifact {i}/{total}: {input_path}")

            # Determine output path for this file
            original_name = os.path.splitext(os.path.basename(input_path))[0]
            if output_dir:
                os.makedirs(output_dir, exist_ok=True)
                output_path = os.path.join(output_dir, f"{original_name}_dispelled.png")
            else:
                output_path = None

            metadata = remove_background(
                input_path=input_path,
                output_path=output_path,
                model=model,
                logger=logger,
            )
            results.append(metadata)

        except Exception as e:
            logger.error(f"Failed to process {input_path}: {e}")
            results.append({
                "input_path": input_path,
                "success": False,
                "error": str(e),
            })

    successful = sum(1 for r in results if r.get("success", True))
    logger.info(f"Batch ritual completed: {successful}/{total} successful")

    return results


# =============================================================================
# COMMAND LINE INTERFACE
# =============================================================================

def main():
    parser = argparse.ArgumentParser(
        description="Cast the dispel background hex using arcane vision",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic usage
  python spells/dispel_background.py --input portrait.jpg

  # Specify output and model
  python spells/dispel_background.py --input photo.png --output photo_no_bg.png --model u2netp

  # Batch process multiple files
  python spells/dispel_background.py --batch --input "*.jpg" --output-dir dispelled/

  # Use alpha matting for cleaner edges
  python spells/dispel_background.py --input photo.jpg --alpha-matting

Available Models:
  u2net              - Best quality, slower (default)
  u2netp             - Good quality, faster
  u2net_human_seg    - Optimized for human subjects
  u2net_cloth_seg    - Optimized for clothing
  silueta            - Lightweight, fastest
        """
    )

    # Input/output arguments
    parser.add_argument(
        "--input", "-i",
        required=True,
        help="Path to the magical image artifact (or glob pattern for batch mode)"
    )
    parser.add_argument(
        "--output", "-o",
        help="Path to the dispelled artifact (optional, auto-generated if not provided)"
    )
    parser.add_argument(
        "--output-dir",
        help="Directory for dispelled artifacts in batch mode"
    )

    # Spell configuration
    parser.add_argument(
        "--model", "-m",
        default="u2net",
        choices=SUPPORTED_MODELS,
        help="Arcane crystal to use for background dispelling (default: u2net)"
    )
    parser.add_argument(
        "--alpha-matting",
        action="store_true",
        help="Apply alpha matting for cleaner edges (slower)"
    )
    parser.add_argument(
        "--alpha-matting-foreground-threshold",
        type=int,
        default=240,
        metavar="N",
        help="Foreground threshold for alpha matting (default: 240)"
    )
    parser.add_argument(
        "--alpha-matting-background-threshold",
        type=int,
        default=10,
        metavar="N",
        help="Background threshold for alpha matting (default: 10)"
    )
    parser.add_argument(
        "--alpha-matting-erode-size",
        type=int,
        default=10,
        metavar="N",
        help="Erosion size for alpha matting (default: 10)"
    )

    # Processing options
    parser.add_argument(
        "--batch", "-b",
        action="store_true",
        help="Batch process multiple files using glob pattern"
    )
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
        "dispel_background",
        log_level=args.log_level,
        log_file=args.log_file,
    )

    try:
        # Check dependencies
        deps = check_dependencies(required_modules=["rembg", "PIL"])
        if not deps["all_available"]:
            missing = [k for k, v in deps["modules"].items() if not v]
            raise InvalidReagentError(
                f"Missing required spell components: {', '.join(missing)}",
                recovery_suggestion="Install with: pip install -r requirements.txt"
            )

        # Process single file or batch
        if args.batch:
            import glob
            input_files = glob.glob(args.input)
            if not input_files:
                raise InvalidReagentError(
                    f"No artifacts found matching pattern: {args.input}",
                    recovery_suggestion="Check the glob pattern and try again."
                )

            results = remove_background_batch(
                input_paths=input_files,
                output_dir=args.output_dir,
                model=args.model,
                logger=logger,
            )

            # Save batch metadata
            if results:
                metadata_path = os.path.join(
                    args.output_dir or "dungeon_cache",
                    f"batch_dispel_metadata_{datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')}.json"
                )
                save_metadata({"results": results}, metadata_path)
                logger.info(f"Batch metadata saved: {metadata_path}")

        else:
            # Single file processing
            metadata = remove_background(
                input_path=args.input,
                output_path=args.output,
                model=args.model,
                alpha_matting=args.alpha_matting,
                alpha_matting_foreground_threshold=args.alpha_matting_foreground_threshold,
                alpha_matting_background_threshold=args.alpha_matting_background_threshold,
                alpha_matting_erode_size=args.alpha_matting_erode_size,
                logger=logger,
            )

            # Save metadata
            original_name = os.path.splitext(os.path.basename(args.input))[0]
            metadata_dir = os.path.dirname(metadata["output_path"]) or "dungeon_cache"
            metadata_path = os.path.join(
                metadata_dir, f"{original_name}_dispel_metadata.json"
            )
            save_metadata(metadata, metadata_path)

            # Print success message
            print(f"\n✓ Background dispelled successfully!")
            print(f"  Artifact: {metadata['input_path']} ({metadata['input_mode']})")
            print(f"  Dispelled: {metadata['output_path']} ({metadata['output_mode']})")
            print(f"  Dimensions: {metadata['input_size']}")
            print(f"  Artifact size: {format_bytes(metadata['input_size_bytes'])} → {format_bytes(metadata['output_size_bytes'])}")
            print(f"  Size change: {metadata['size_change_percent']:+}%")
            print(f"  Arcane crystal: {metadata['model']}")
            print(f"  Duration: {metadata['performance']['duration_seconds']:.2f}s")
            print(f"  Arcane knowledge: {metadata_path}")

    except Exception as e:
        handle_spell_error(e, "dispel_background", exit_on_error=True)


if __name__ == "__main__":
    main()
