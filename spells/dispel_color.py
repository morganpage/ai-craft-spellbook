#!/usr/bin/env python3
"""
Dispel Color - Chroma Key Spell

Remove pixels from an image that match a sampled color from a reference image.
Useful for green screen effects or removing solid color backgrounds.
"""

SPELL_METADATA = {
    "name": "dispel_color",
    "version": "1.0.0",
    "primary_keywords": ["chroma key", "color key", "remove color", "dispel color"],
    "secondary_keywords": {
        "actions": ["remove", "delete", "make transparent", "key out"],
        "targets": ["background", "color", "green screen", "blue screen"]
    },
    "supported_formats": ["png", "jpg", "jpeg", "bmp", "tiff", "webp"],
    "description": "Remove pixels matching a sampled color using chroma key technique",
    "common_use_cases": [
        "Remove green screen backgrounds",
        "Remove solid color backgrounds",
        "Key out specific colors from images",
        "Create transparent backgrounds from color swatches"
    ],
    "examples": [
        "remove green screen from photo.png",
        "chroma key the blue background using color_palette.png",
        "dispel color #00FF00 from image.png",
        "make all white pixels transparent in photo.jpg"
    ],
    "output_naming_pattern": "<name>_dispelled.<ext>",
    "cli_pattern": "python spells/dispel_color.py --input <image> --color-source <palette_image> --color-x <x> --color-y <y>",
    "cli_parameters": {
        "--input": "Path to the image to process",
        "--color-source": "Path to image containing the color to sample",
        "--color-x": "X coordinate to sample color from color-source image",
        "--color-y": "Y coordinate to sample color from color-source image",
        "--color": "Direct hex color specification (e.g., #00FF00)",
        "--tolerance": "Color matching tolerance 0-100 (default: 30)",
        "--output": "Output path (optional)"
    }
}

import argparse
import json
import os
from datetime import datetime
from typing import Dict, Any, Optional, Tuple
from PIL import Image


def sample_color_from_image(
    image_path: str,
    x: int,
    y: int
) -> Tuple[int, int, int]:
    """Sample a color from specific coordinates in an image.

    Args:
        image_path: Path to the image to sample from
        x: X coordinate (from left)
        y: Y coordinate (from top)

    Returns:
        Tuple of (R, G, B) values
    """
    img = Image.open(image_path)
    img.load()

    # Ensure coordinates are within bounds
    x = max(0, min(x, img.width - 1))
    y = max(0, min(y, img.height - 1))

    pixel = img.getpixel((x, y))

    # Handle different image modes
    if isinstance(pixel, int):
        # Grayscale
        return (pixel, pixel, pixel)
    elif len(pixel) >= 3:
        # RGB or RGBA
        return (pixel[0], pixel[1], pixel[2])
    else:
        raise ValueError(f"Unexpected pixel format: {type(pixel)}")


def hex_to_rgb(hex_color: str) -> Tuple[int, int, int]:
    """Convert hex color string to RGB tuple.

    Args:
        hex_color: Hex color string (e.g., "#00FF00" or "00FF00")

    Returns:
        Tuple of (R, G, B) values
    """
    hex_color = hex_color.strip().lstrip('#')
    if len(hex_color) != 6:
        raise ValueError(f"Invalid hex color: {hex_color}. Must be 6 digits.")

    r = int(hex_color[0:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:6], 16)

    return (r, g, b)


def color_distance(c1: Tuple[int, int, int], c2: Tuple[int, int, int]) -> float:
    """Calculate Euclidean distance between two colors in RGB space.

    Args:
        c1: First color as (R, G, B)
        c2: Second color as (R, G, B)

    Returns:
        Distance value (0 = identical, max ~441.67 for RGB)
    """
    return ((c1[0] - c2[0])**2 + (c1[1] - c2[1])**2 + (c1[2] - c2[2])**2) ** 0.5


def dispel_color(
    input_path: str,
    target_color: Tuple[int, int, int],
    tolerance: int = 30,
    output_path: Optional[str] = None
) -> Dict[str, Any]:
    """Remove pixels matching the target color from an image.

    Args:
        input_path: Path to the image to process
        target_color: RGB color tuple to remove
        tolerance: Color matching tolerance (0-100). Higher = more colors removed.
        output_path: Path for output image (auto-generated if not provided)

    Returns:
        Dict containing processing metadata
    """
    # Generate output path if not provided
    if output_path is None:
        base, ext = os.path.splitext(input_path)
        output_path = f"{base}_dispelled.png"

    # Validate input
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Artifact not found: {input_path}")

    # Load image
    img = Image.open(input_path)
    img.load()

    # Convert to RGBA if necessary
    if img.mode != 'RGBA':
        img = img.convert('RGBA')

    # Calculate max distance from tolerance (0-100 scale)
    # Max Euclidean distance in RGB space is ~441.67 (black to white)
    max_distance = (tolerance / 100.0) * 441.67

    # Process pixels
    pixels = img.load()
    pixels_removed = 0
    total_pixels = img.width * img.height

    for y in range(img.height):
        for x in range(img.width):
            pixel = pixels[x, y]
            current_color = (pixel[0], pixel[1], pixel[2])

            # Calculate distance from target color
            distance = color_distance(current_color, target_color)

            # Make transparent if within tolerance
            if distance <= max_distance:
                pixels[x, y] = (pixel[0], pixel[1], pixel[2], 0)
                pixels_removed += 1

    # Save output
    img.save(output_path, 'PNG', optimize=True)

    # Calculate stats
    input_size = os.path.getsize(input_path)
    output_size = os.path.getsize(output_path)
    size_reduction = ((input_size - output_size) / input_size * 100) if input_size > 0 else 0

    metadata = {
        "input_path": input_path,
        "output_path": output_path,
        "target_color": {
            "r": target_color[0],
            "g": target_color[1],
            "b": target_color[2],
            "hex": f"#{target_color[0]:02X}{target_color[1]:02X}{target_color[2]:02X}"
        },
        "tolerance": tolerance,
        "max_distance": max_distance,
        "dimensions": {
            "width": img.width,
            "height": img.height
        },
        "pixels_removed": pixels_removed,
        "total_pixels": total_pixels,
        "removal_percentage": (pixels_removed / total_pixels * 100) if total_pixels > 0 else 0,
        "input_size_bytes": input_size,
        "output_size_bytes": output_size,
        "size_reduction_percentage": round(size_reduction, 2),
        "processed_at": datetime.now().isoformat()
    }

    return metadata


def main():
    parser = argparse.ArgumentParser(
        description="Remove pixels matching a sampled color using chroma key technique",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Sample color from palette image at coordinates
  python spells/dispel_color.py --input photo.png --color-source palette.png --color-x 10 --color-y 10

  # Remove green screen color directly
  python spells/dispel_color.py --input photo.png --color "#00FF00"

  # Sample color with custom tolerance
  python spells/dispel_color.py --input photo.png --color-source palette.png --color-x 50 --color-y 50 --tolerance 50

  # Specify output path
  python spells/dispel_color.py --input photo.png --color "#FFFFFF" --output photo_no_white.png
        """
    )

    parser.add_argument(
        "--input", "-i",
        required=True,
        help="Path to the image to process"
    )
    parser.add_argument(
        "--color-source",
        help="Path to image containing the color to sample from"
    )
    parser.add_argument(
        "--color-x",
        type=int,
        help="X coordinate to sample color from color-source image"
    )
    parser.add_argument(
        "--color-y",
        type=int,
        help="Y coordinate to sample color from color-source image"
    )
    parser.add_argument(
        "--color",
        help="Direct hex color specification (e.g., #00FF00 or 00FF00)"
    )
    parser.add_argument(
        "--tolerance",
        type=int,
        default=30,
        help="Color matching tolerance 0-100 (default: 30). Higher = more colors removed."
    )
    parser.add_argument(
        "--output", "-o",
        help="Path for output image (default: <input>_dispelled.png)"
    )
    parser.add_argument(
        "--log-level",
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        default="INFO",
        help="Logging level (default: INFO)"
    )

    args = parser.parse_args()

    # Validate color source options
    if args.color and (args.color_source or args.color_x or args.color_y):
        parser.error("Cannot use --color with --color-source/--color-x/--color-y")

    if not args.color and not args.color_source:
        parser.error("Must provide either --color or --color-source with --color-x and --color-y")

    if args.color_source and (args.color_x is None or args.color_y is None):
        parser.error("--color-source requires both --color-x and --color-y coordinates")

    if args.color_source and not os.path.exists(args.color_source):
        parser.error(f"Color source image not found: {args.color_source}")

    # Validate tolerance
    if not 0 <= args.tolerance <= 100:
        parser.error("--tolerance must be between 0 and 100")

    try:
        # Get target color
        if args.color:
            target_color = hex_to_rgb(args.color)
            print(f"[SPELL] Target color: #{target_color[0]:02X}{target_color[1]:02X}{target_color[2]:02X}")
        else:
            target_color = sample_color_from_image(args.color_source, args.color_x, args.color_y)
            print(f"[SPELL] Sampled color from ({args.color_x}, {args.color_y}): #{target_color[0]:02X}{target_color[1]:02X}{target_color[2]:02X}")

        print(f"[SPELL] Tolerance: {args.tolerance}")
        print(f"[SPELL] Processing artifact: {args.input}")

        # Process image
        metadata = dispel_color(
            input_path=args.input,
            target_color=target_color,
            tolerance=args.tolerance,
            output_path=args.output
        )

        print(f"[SPELL] Ritual completed successfully!")
        print()
        print("✓ Color dispelled successfully!")
        print(f"  Artifact: {metadata['input_path']}")
        print(f"  Dispelled: {metadata['output_path']}")
        print(f"  Dimensions: {metadata['dimensions']['width']}x{metadata['dimensions']['height']}")
        print(f"  Target color: {metadata['target_color']['hex']}")
        print(f"  Tolerance: {metadata['tolerance']} (max distance: {metadata['max_distance']:.2f})")
        print(f"  Pixels removed: {metadata['pixels_removed']:,} / {metadata['total_pixels']:,} ({metadata['removal_percentage']:.1f}%)")
        print(f"  Size change: {metadata['input_size_bytes'] / 1024:.2f} KB → {metadata['output_size_bytes'] / 1024:.2f} KB ({metadata['size_reduction_percentage']:.2f}%)")

        # Save metadata
        metadata_path = args.output.replace('.png', '_metadata.json') if args.output else \
                        args.input.replace('.png', '_dispel_metadata.json').replace('.jpg', '_dispel_metadata.json').replace('.jpeg', '_dispel_metadata.json')
        with open(metadata_path, 'w') as f:
            json.dump(metadata, f, indent=2)
        print(f"  Arcane knowledge: {metadata_path}")

    except FileNotFoundError as e:
        print(f"Spell fumble: {e}")
        raise
    except Exception as e:
        print(f"Spell fumble: {e}")
        raise


if __name__ == "__main__":
    main()
