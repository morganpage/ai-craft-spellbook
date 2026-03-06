import argparse
import io
import json
import os
from datetime import datetime
from typing import Dict, Any, Optional

from rembg import remove
from PIL import Image


def remove_background(
    input_path: str,
    output_path: Optional[str] = None,
    model: str = "u2net",
) -> Dict[str, Any]:
    """Cast the dispel background hex to vanish unwanted magical backgrounds.

    This powerful incantation uses arcane vision to detect foreground subjects
    and banish the magical background, leaving behind a transparent treasure.

    Args:
        input_path: Path to the magical image artifact
        output_path: Path to the dispelled image artifact (optional, auto-generated if not provided)
        model: Arcane crystal to use for background detection (default: u2net)

    Returns:
        Dict containing arcane knowledge about the dispelling ritual

    Raises:
        FileNotFoundError: If the input artifact doesn't exist
        ValueError: If spell components are invalid
    """
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Artifact not found: {input_path}")

    supported_models = ["u2net", "u2netp", "u2net_human_seg", "u2net_cloth_seg", "silueta"]
    if model not in supported_models:
        raise ValueError(
            f"Unsupported arcane crystal: {model}. Supported crystals: {', '.join(supported_models)}"
        )

    original_name = os.path.splitext(os.path.basename(input_path))[0]

    if output_path is None:
        output_dir = os.path.dirname(input_path) or "dungeon_cache"
        output_path = os.path.join(output_dir, f"{original_name}_dispelled.png")

    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)

    input_img = Image.open(input_path)
    input_size = input_img.size
    input_mode = input_img.mode
    input_img.close()

    original_size_bytes = os.path.getsize(input_path)

    with open(input_path, "rb") as input_file:
        input_data = input_file.read()

    output_data = remove(input_data, session_name=model)
    output_img = Image.open(io.BytesIO(output_data))

    output_img.save(output_path, format="PNG", optimize=True)
    output_size = output_img.size
    output_img.close()

    output_size_bytes = os.path.getsize(output_path)

    metadata = {
        "input_path": input_path,
        "output_path": output_path,
        "input_size": f"{input_size[0]}x{input_size[1]}",
        "output_size": f"{output_size[0]}x{output_size[1]}",
        "input_mode": input_mode,
        "output_mode": "RGBA",
        "input_size_bytes": original_size_bytes,
        "output_size_bytes": output_size_bytes,
        "size_change_percent": (
            round((output_size_bytes / original_size_bytes - 1) * 100, 2)
            if original_size_bytes > 0
            else 0
        ),
        "model": model,
        "processed_at": datetime.utcnow().isoformat(),
    }

    return metadata


def save_metadata(metadata: Dict[str, Any], output_path: str) -> None:
    """Preserve arcane knowledge in a magical tome.

    Args:
        metadata: Arcane knowledge dictionary
        output_path: Path to the magical tome
    """
    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2)


def main():
    parser = argparse.ArgumentParser(
        description="Cast the dispel background hex using arcane vision"
    )
    parser.add_argument("--input", required=True, help="Path to the magical image artifact")
    parser.add_argument("--output", help="Path to the dispelled artifact (optional)")
    parser.add_argument(
        "--model",
        default="u2net",
        choices=["u2net", "u2netp", "u2net_human_seg", "u2net_cloth_seg", "silueta"],
        help="Arcane crystal to use for background dispelling (default: u2net)",
    )

    args = parser.parse_args()

    try:
        metadata = remove_background(
            input_path=args.input,
            output_path=args.output,
            model=args.model,
        )

        original_name = os.path.splitext(os.path.basename(args.input))[0]
        metadata_dir = os.path.dirname(metadata["output_path"]) or "dungeon_cache"
        metadata_path = os.path.join(
            metadata_dir, f"{original_name}_dispel_metadata.json"
        )

        save_metadata(metadata, metadata_path)

        print(f"Background dispelled successfully!")
        print(f"Artifact: {metadata['input_path']} ({metadata['input_mode']})")
        print(f"Dispelled: {metadata['output_path']} ({metadata['output_mode']})")
        print(f"Dimensions: {metadata['input_size']}")
        print(
            f"Artifact size: {metadata['input_size_bytes']:,} → {metadata['output_size_bytes']:,} bytes"
        )
        print(f"Size change: {metadata['size_change_percent']:+}%")
        print(f"Arcane crystal: {metadata['model']}")
        print(f"Arcane knowledge: {metadata_path}")

    except FileNotFoundError as e:
        print(f"Spell fumble: {e}")
        raise
    except ValueError as e:
        print(f"Invalid reagent: {e}")
        raise
    except Exception as e:
        print(f"Unexpected magical failure: {e}")
        raise


if __name__ == "__main__":
    main()
