import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from typing import Dict, Any, Optional, List, Tuple

# Add parent directory to path for imports when running as script
if __name__ == "__main__":
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from spells.utils.common import (
    save_metadata,
    validate_input_file,
    validate_output_path,
    get_spell_metadata_base,
    setup_output_directory,
    get_logger,
    check_ffmpeg,
    check_ffprobe,
    format_bytes,
    format_duration,
    PerformanceTracker,
    setup_logging,
)
from spells.utils.error_handling import (
    SpellFumbleError,
    ArcaneDisruptionError,
    InvalidReagentError,
    handle_spell_error,
)


# =============================================================================
# SPELL CONFIGURATION
# =============================================================================

NOISE_STRENGTH_SETTINGS = {
    "light": "afftdn=nr=10:nf=-40",
    "medium": "afftdn=nr=20:nf=-35",
    "heavy": "afftdn=nr=30:nf=-30",
}

SUPPORTED_FORMATS = {
    ".mp3", ".wav", ".m4a", ".aac", ".ogg", ".flac", ".wma",
    ".mp4", ".avi", ".mov", ".mkv", ".webm", ".flv", ".wmv"
}

# Maximum file size: 500MB default
MAX_FILE_SIZE = 500 * 1024 * 1024


# =============================================================================
# MEDIA ANALYSIS
# =============================================================================

def get_media_info(
    file_path: str,
    logger: Optional[Any] = None
) -> Dict[str, Any]:
    """Analyze magical media artifact to reveal its arcane properties.

    This spell examines the artifact using the ancient scrying glass ffprobe
    to determine its duration, magical streams, and other properties.

    Args:
        file_path: Path to the magical media artifact
        logger: Optional logger instance

    Returns:
        Dict containing duration, audio codec, video codec, and other arcane properties

    Raises:
        ArcaneDisruptionError: If the scrying glass fails to reveal information
    """
    cmd = [
        "ffprobe",
        "-v", "quiet",
        "-print_format", "json",
        "-show_format",
        "-show_streams",
        file_path
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise ArcaneDisruptionError(
            "Scrying glass failed to analyze artifact",
            recovery_suggestion=f"FFprobe error: {result.stderr}"
        )

    data = json.loads(result.stdout)

    info = {
        "duration": float(data.get("format", {}).get("duration", 0)),
        "size_bytes": int(data.get("format", {}).get("size", 0)),
        "bit_rate": int(data.get("format", {}).get("bit_rate", 0)),
        "has_video": False,
        "has_audio": False,
        "audio_codec": None,
        "video_codec": None,
        "sample_rate": None,
        "channels": None,
    }

    for stream in data.get("streams", []):
        if stream.get("codec_type") == "audio":
            info["has_audio"] = True
            info["audio_codec"] = stream.get("codec_name")
            info["sample_rate"] = stream.get("sample_rate")
            info["channels"] = stream.get("channels")
        elif stream.get("codec_type") == "video":
            info["has_video"] = True
            info["video_codec"] = stream.get("codec_name")

    if logger:
        logger.debug(f"Media info: {info}")

    return info


def detect_silence_periods(
    file_path: str,
    silence_threshold: float = -40.0,
    silence_duration: float = 0.5,
    logger: Optional[Any] = None,
) -> List[Tuple[float, float]]:
    """Detect void moments of silence within the magical audio.

    This incantation searches for periods of magical stillness that represent
    unwanted voids in the audio stream using the silencedetection ritual.

    Args:
        file_path: Path to the magical media artifact
        silence_threshold: dB threshold for void detection
        silence_duration: Minimum void duration in seconds
        logger: Optional logger instance

    Returns:
        List of (start, end) tuples for each void period discovered
    """
    cmd = [
        "ffmpeg",
        "-i", file_path,
        "-af", f"silencedetect=noise={silence_threshold}dB:d={silence_duration}",
        "-f", "null",
        "-"
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)

    silence_periods = []
    silence_start = None

    for line in result.stderr.split('\n'):
        if 'silence_start:' in line:
            match = re.search(r'silence_start:\s*([\d.]+)', line)
            if match:
                silence_start = float(match.group(1))
        elif 'silence_end:' in line:
            match = re.search(r'silence_end:\s*([\d.]+)', line)
            if match and silence_start is not None:
                silence_end = float(match.group(1))
                silence_periods.append((silence_start, silence_end))
                silence_start = None

    if logger:
        logger.debug(f"Detected {len(silence_periods)} silence periods")

    return silence_periods


def calculate_non_silent_segments(
    total_duration: float,
    silence_periods: List[Tuple[float, float]],
    padding: float = 0.1,
) -> List[Tuple[float, float]]:
    """Calculate the magical segments that remain after void banishment.

    This subroutine computes which portions of the artifact should be preserved
    after removing the void moments of silence.

    Args:
        total_duration: Total duration of the magical media artifact
        silence_periods: List of (start, end) tuples for void periods
        padding: Extra magical buffer to add at segment boundaries (seconds)

    Returns:
        List of (start, end) tuples for magical segments to preserve
    """
    if not silence_periods:
        return [(0, total_duration)]

    segments = []
    current_pos = 0.0

    for silence_start, silence_end in silence_periods:
        if current_pos < silence_start:
            end_with_padding = min(silence_start + padding, total_duration)
            segments.append((current_pos, end_with_padding))
        current_pos = max(current_pos, silence_end - padding)

    if current_pos < total_duration:
        segments.append((current_pos, total_duration))

    return segments


# =============================================================================
# SEGMENT PROCESSING
# =============================================================================

def extract_segment_with_fades(
    input_path: str,
    start: float,
    end: float,
    fade_duration: float,
    output_path: str,
    has_video: bool,
    is_final: bool = False,
) -> None:
    """Extract a magical segment with smooth fade in/out enchantments.

    This spell carves out a portion of the artifact and applies gentle magical
    transitions to prevent harsh magical disruptions at the boundaries.

    Args:
        input_path: Path to the source magical media artifact
        start: Start time in seconds
        end: End time in seconds
        fade_duration: Duration of magical fade in/out in seconds
        output_path: Path to the extracted segment artifact
        has_video: Whether the artifact contains visual magic
        is_final: Whether this is the final segment (skip fade out)
    """
    segment_duration = end - start

    cmd = [
        "ffmpeg", "-y",
        "-ss", str(start),
        "-i", input_path,
        "-t", str(segment_duration),
    ]

    fade_filters = []
    if fade_duration > 0:
        fade_filters.append(f"afade=t=in:st=0:d={fade_duration}")
        if not is_final:
            fade_out_start = segment_duration - fade_duration
            if fade_out_start > fade_duration:
                fade_filters.append(f"afade=t=out:st={fade_out_start}:d={fade_duration}")

    audio_filter = ",".join(fade_filters) if fade_filters else "anull"

    if has_video:
        cmd.extend([
            "-c:v", "copy",
            "-c:a", "aac",
            "-b:a", "192k",
            "-af", audio_filter,
            output_path
        ])
    else:
        cmd.extend([
            "-c:a", "libmp3lame",
            "-b:a", "192k",
            "-af", audio_filter,
            output_path
        ])

    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise ArcaneDisruptionError(
            f"Failed to extract segment ({start}-{end})",
            recovery_suggestion=f"FFmpeg error: {result.stderr}"
        )


def concatenate_segments(
    segment_paths: List[str],
    output_path: str,
    has_video: bool,
) -> None:
    """Fuse multiple magical segments into a single artifact.

    This ritual combines all the preserved magical segments into one
    coherent artifact using ancient binding magics.

    Args:
        segment_paths: List of paths to segment artifacts
        output_path: Path to the fused magical artifact
        has_video: Whether the segments contain visual magic
    """
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
        for path in segment_paths:
            f.write(f"file '{path}'\n")
        concat_list_path = f.name

    try:
        if has_video:
            cmd = [
                "ffmpeg", "-y",
                "-f", "concat",
                "-safe", "0",
                "-i", concat_list_path,
                "-c:v", "copy",
                "-c:a", "aac",
                "-b:a", "192k",
                output_path
            ]
        else:
            cmd = [
                "ffmpeg", "-y",
                "-f", "concat",
                "-safe", "0",
                "-i", concat_list_path,
                "-c:a", "libmp3lame",
                "-b:a", "192k",
                output_path
            ]

        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            raise ArcaneDisruptionError(
                "Failed to concatenate segments",
                recovery_suggestion=f"FFmpeg error: {result.stderr}"
            )
    finally:
        os.unlink(concat_list_path)


def apply_filters(
    input_path: str,
    output_path: str,
    filters: List[str],
    has_video: bool,
) -> None:
    """Apply magical purification filters to a media artifact.

    This spell channels various audio enchantments to purify and balance
    the magical energies within the artifact.

    Args:
        input_path: Path to the source magical media artifact
        output_path: Path to the transformed magical artifact
        filters: List of FFmpeg audio filter enchantment strings
        has_video: Whether the artifact contains visual magic
    """
    audio_filter = ",".join(filters) if filters else "anull"

    cmd = ["ffmpeg", "-y", "-i", input_path]

    if has_video:
        cmd.extend([
            "-c:v", "copy",
            "-c:a", "aac",
            "-b:a", "192k",
            "-af", audio_filter,
            output_path
        ])
    else:
        cmd.extend([
            "-c:a", "libmp3lame",
            "-b:a", "192k",
            "-af", audio_filter,
            output_path
        ])

    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise ArcaneDisruptionError(
            "Failed to apply magical filters",
            recovery_suggestion=f"FFmpeg error: {result.stderr}"
        )


# =============================================================================
# MAIN SPELL FUNCTION
# =============================================================================

def process_audio_video(
    input_path: str,
    output_path: Optional[str] = None,
    silence_threshold: float = -40.0,
    silence_duration: float = 0.5,
    loudness_target: float = -14.0,
    remove_silence: bool = True,
    normalize: bool = True,
    noise_reduction: bool = True,
    noise_strength: str = "light",
    fade_duration: float = 0.01,
    silence_padding: float = 0.3,
    keep_temp_files: bool = False,
    logger: Optional[Any] = None,
) -> Dict[str, Any]:
    """Channel the audio cleansing ritual to purify magical media artifacts.

    This powerful ritual performs three sacred cleansing steps:
    1. Purification: Remove impurities and background hum (noise reduction)
    2. Void Banishment: Remove unwanted moments of magical stillness (silence removal)
    3. Energy Balancing: Normalize magical loudness to standard levels

    Args:
        input_path: Path to the magical media artifact to cleanse
        output_path: Path to the purified artifact (optional, auto-generated if not provided)
        silence_threshold: dB threshold for void detection (default: -40)
        silence_duration: Minimum void duration in seconds to banish (default: 0.5)
        loudness_target: Target magical loudness in LUFS (default: -14)
        remove_silence: Whether to banish voids (default: True)
        normalize: Whether to balance magical energies (default: True)
        noise_reduction: Whether to apply purification magic (default: True)
        noise_strength: Purification strength: light, medium, heavy (default: light)
        fade_duration: Magical fade in/out duration at segment boundaries (default: 0.01)
        silence_padding: Magical buffer to add at segment boundaries (default: 0.3)
        keep_temp_files: Keep intermediate segment artifacts (default: False)
        logger: Optional logger instance

    Returns:
        Dict containing arcane knowledge about the cleansing ritual

    Raises:
        InvalidReagentError: If input validation or parameters are invalid
        ArcaneDisruptionError: If the ritual fails during casting
        SpellFumbleError: For general spell failures
    """
    # Set up logger if not provided
    if logger is None:
        logger = get_logger("audio_cleanse")

    # Check dependencies
    if not check_ffmpeg() or not check_ffprobe():
        raise InvalidReagentError(
            "FFmpeg and FFprobe are required for this ritual",
            recovery_suggestion="Install FFmpeg: brew install ffmpeg (macOS) or apt-get install ffmpeg (Linux)"
        )

    # Validate input file
    logger.info(f"Validating artifact: {input_path}")
    validation = validate_input_file(
        input_path,
        allowed_formats=SUPPORTED_FORMATS,
        max_size_bytes=MAX_FILE_SIZE,
        check_readable=True,
    )
    logger.info(f"Artifact validated: {format_bytes(validation['size_bytes'])}")

    # Validate parameters
    if silence_threshold >= 0:
        raise InvalidReagentError(
            "Silence threshold must be negative (in dB)",
            recovery_suggestion="Use values like -40, -50, or -60"
        )

    if not -30 <= loudness_target <= -5:
        raise InvalidReagentError(
            "Loudness target should be between -30 and -5 LUFS",
            recovery_suggestion="Common values: -14 (YouTube/Spotify), -16 ( podcasts)"
        )

    if noise_strength not in NOISE_STRENGTH_SETTINGS:
        raise InvalidReagentError(
            f"Noise strength must be one of: {', '.join(NOISE_STRENGTH_SETTINGS.keys())}",
            recovery_suggestion="Choose from: light, medium, heavy"
        )

    # Determine output path
    original_name = os.path.splitext(os.path.basename(input_path))[0]
    input_ext = os.path.splitext(input_path)[1]

    if output_path is None:
        output_dir = os.path.dirname(input_path) or "dungeon_cache"
        output_path = os.path.join(output_dir, f"{original_name}_purified{input_ext}")

    # Validate and prepare output path
    output_path = validate_output_path(
        output_path,
        check_writable=True,
        create_parent_dirs=True,
    )

    # Set up performance tracking
    tracker = PerformanceTracker("audio_cleanse")
    tracker.set_input_size(validation["size_bytes"])
    tracker.start()

    # Get media info
    logger.info("Analyzing artifact with scrying glass...")
    input_info = get_media_info(input_path, logger=logger)

    if not input_info["has_audio"]:
        raise InvalidReagentError(
            "Artifact has no audio stream to cleanse",
            recovery_suggestion="Provide a file with audio content"
        )

    logger.info(f"Artifact duration: {format_duration(input_info['duration'])}")

    # Processing
    temp_dir = tempfile.mkdtemp(prefix="audio_cleanse_")
    segment_paths = []
    silence_periods = []
    segments_removed = 0

    try:
        current_input = input_path

        # Step 1: Remove silence
        if remove_silence:
            logger.info("Detecting void moments of silence...")
            silence_periods = detect_silence_periods(
                input_path, silence_threshold, silence_duration, logger
            )

            if silence_periods:
                logger.info(f"Discovered {len(silence_periods)} void periods")
                segments = calculate_non_silent_segments(
                    input_info["duration"], silence_periods, silence_padding
                )
                logger.info(f"Extracting {len(segments)} magical segments...")

                for i, (start, end) in enumerate(segments):
                    segment_path = os.path.join(temp_dir, f"segment_{i:04d}{input_ext}")
                    is_final = (i == len(segments) - 1)

                    if logger:
                        logger.debug(f"Extracting segment {i+1}/{len(segments)}: {start:.2f}s - {end:.2f}s")

                    extract_segment_with_fades(
                        current_input, start, end, fade_duration, segment_path,
                        input_info["has_video"], is_final
                    )
                    segment_paths.append(segment_path)

                concatenated_path = os.path.join(temp_dir, f"concatenated{input_ext}")
                logger.info("Fusing magical segments...")
                concatenate_segments(segment_paths, concatenated_path, input_info["has_video"])
                current_input = concatenated_path

                segments_removed = len(silence_periods)
            else:
                logger.info("No voids detected, skipping void banishment")

        # Step 2 & 3: Apply filters (noise reduction and normalization)
        filters = []
        if noise_reduction:
            filters.append(NOISE_STRENGTH_SETTINGS[noise_strength])
        if normalize:
            filters.append(f"loudnorm=I={loudness_target}:TP=-1.5:LRA=11")

        if filters:
            logger.info("Channeling purification and balancing magic...")
            apply_filters(current_input, output_path, filters, input_info["has_video"])
        else:
            shutil.copy(current_input, output_path)

        # Handle temp files
        if keep_temp_files:
            temp_save_dir = os.path.join(
                os.path.dirname(output_path) or ".",
                f"{original_name}_temp_segments"
            )
            shutil.move(temp_dir, temp_save_dir)
            logger.info(f"Temp artifacts saved to: {temp_save_dir}")

    finally:
        if not keep_temp_files and os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)

    # Get output info
    output_info = get_media_info(output_path, logger=logger)
    tracker.set_output_size(output_info["size_bytes"])
    tracker.stop()

    logger.info("Ritual completed successfully!")

    # Build metadata
    metadata = get_spell_metadata_base("audio_cleanse")
    metadata.update({
        "input_path": input_path,
        "output_path": output_path,
        "settings": {
            "silence_threshold_db": silence_threshold,
            "silence_duration_sec": silence_duration,
            "loudness_target_lufs": loudness_target,
            "remove_silence": remove_silence,
            "normalize": normalize,
            "noise_reduction": noise_reduction,
            "noise_strength": noise_strength if noise_reduction else None,
            "fade_duration_sec": fade_duration,
            "silence_padding_sec": silence_padding,
        },
        "input_info": {
            "duration_sec": round(input_info["duration"], 2),
            "size_bytes": input_info["size_bytes"],
            "has_video": input_info["has_video"],
            "has_audio": input_info["has_audio"],
            "audio_codec": input_info["audio_codec"],
        },
        "output_info": {
            "duration_sec": round(output_info["duration"], 2),
            "size_bytes": output_info["size_bytes"],
            "has_video": output_info["has_video"],
            "has_audio": output_info["has_audio"],
            "audio_codec": output_info["audio_codec"],
        },
        "silence_removal": {
            "silent_periods_found": len(silence_periods),
            "silent_periods": silence_periods if silence_periods else None,
        },
        "duration_reduction_sec": round(input_info["duration"] - output_info["duration"], 2),
        "duration_reduction_percent": round(
            (1 - output_info["duration"] / input_info["duration"]) * 100, 2
        ) if input_info["duration"] > 0 else 0,
    })
    metadata["performance"] = tracker.get_metrics()

    return metadata


# =============================================================================
# COMMAND LINE INTERFACE
# =============================================================================

def main():
    parser = argparse.ArgumentParser(
        description="Channel the audio cleansing ritual: banish voids and balance magical energies",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic usage with all features
  python spells/audio_cleanse.py --input recording.mp3

  # Normalize only (no silence removal)
  python spells/audio_cleanse.py --input audio.wav --no-silence-removal

  # Heavy noise reduction with custom threshold
  python spells/audio_cleanse.py --input video.mp4 --noise-strength heavy --silence-threshold -50

  # Target specific loudness for podcasts
  python spells/audio_cleanse.py --input podcast.wav --loudness -16
        """
    )

    # Input/output arguments
    parser.add_argument(
        "--input", "-i",
        required=True,
        help="Path to the magical media artifact"
    )
    parser.add_argument(
        "--output", "-o",
        help="Path to the purified artifact (optional)"
    )

    # Silence detection settings
    parser.add_argument(
        "--silence-threshold",
        type=float,
        default=-40.0,
        help="dB threshold for void detection (default: -40)",
    )
    parser.add_argument(
        "--silence-duration",
        type=float,
        default=0.5,
        help="Minimum void duration in seconds to banish (default: 0.5)",
    )

    # Loudness settings
    parser.add_argument(
        "--loudness",
        type=float,
        default=-14.0,
        help="Target magical loudness in LUFS (default: -14 for YouTube/Spotify)",
    )

    # Feature toggles
    parser.add_argument(
        "--no-silence-removal",
        action="store_true",
        help="Skip void banishment",
    )
    parser.add_argument(
        "--no-normalize",
        action="store_true",
        help="Skip magical energy balancing",
    )
    parser.add_argument(
        "--no-noise-reduction",
        action="store_true",
        help="Skip purification magic (enabled by default)",
    )

    # Noise reduction settings
    parser.add_argument(
        "--noise-strength",
        choices=["light", "medium", "heavy"],
        default="light",
        help="Purification strength (default: light)",
    )

    # Advanced settings
    parser.add_argument(
        "--fade-duration",
        type=float,
        default=0.01,
        help="Magical fade in/out duration at segment boundaries in seconds (default: 0.01)",
    )
    parser.add_argument(
        "--silence-padding",
        type=float,
        default=0.3,
        help="Magical buffer to add at segment boundaries in seconds (default: 0.3)",
    )
    parser.add_argument(
        "--keep-temp",
        action="store_true",
        help="Keep intermediate segment artifacts for debugging",
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
        "audio_cleanse",
        log_level=args.log_level,
        log_file=args.log_file,
    )

    try:
        metadata = process_audio_video(
            input_path=args.input,
            output_path=args.output,
            silence_threshold=args.silence_threshold,
            silence_duration=args.silence_duration,
            loudness_target=args.loudness,
            remove_silence=not args.no_silence_removal,
            normalize=not args.no_normalize,
            noise_reduction=not args.no_noise_reduction,
            noise_strength=args.noise_strength,
            fade_duration=args.fade_duration,
            silence_padding=args.silence_padding,
            keep_temp_files=args.keep_temp,
            logger=logger,
        )

        # Save metadata
        original_name = os.path.splitext(os.path.basename(args.input))[0]
        metadata_dir = os.path.dirname(metadata["output_path"]) or "dungeon_cache"
        metadata_path = os.path.join(
            metadata_dir, f"{original_name}_purification_metadata.json"
        )
        save_metadata(metadata, metadata_path)

        # Print success message
        print(f"\n✓ Ritual completed successfully!")
        print(f"  Artifact: {metadata['input_path']}")
        print(f"  Purified: {metadata['output_path']}")
        print(f"  Duration: {format_duration(metadata['input_info']['duration_sec'])} → {format_duration(metadata['output_info']['duration_sec'])}")

        if metadata["duration_reduction_sec"] > 0:
            print(f"  Void banished: {format_duration(metadata['duration_reduction_sec'])} ({metadata['duration_reduction_percent']}%)")

        if metadata["silence_removal"]["silent_periods_found"] > 0:
            print(f"  Void periods banished: {metadata['silence_removal']['silent_periods_found']}")

        if metadata["settings"]["noise_reduction"]:
            print(f"  Purification strength: {metadata['settings']['noise_strength']}")

        print(f"  Duration: {metadata['performance']['duration_seconds']:.2f}s")
        print(f"  Arcane knowledge: {metadata_path}")

    except Exception as e:
        handle_spell_error(e, "audio_cleanse", exit_on_error=True)


if __name__ == "__main__":
    main()
