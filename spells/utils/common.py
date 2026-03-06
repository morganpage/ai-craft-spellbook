"""
AI Craft Spellbook - Shared Magical Utilities

This module provides common utilities used across all spells including:
- Metadata management and standardization
- Input validation and sanitization
- Dependency checking
- Structured logging with themed output
- Performance tracking

All spells should use these utilities to maintain consistency across the framework.
"""

import json
import os
import shutil
import subprocess
import logging
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Any, Optional, List, Tuple, Set
import hashlib

from .error_handling import InvalidReagentError, ArcaneDisruptionError


# =============================================================================
# METADATA MANAGEMENT
# =============================================================================

def get_spell_metadata_base(
    spell_name: str,
    version: str = "2.0.0"
) -> Dict[str, Any]:
    """Generate standardized base metadata for spell results.

    Args:
        spell_name: Name of the spell being cast
        version: Version of the spell

    Returns:
        Dict with standardized metadata structure
    """
    return {
        "spell_name": spell_name,
        "version": version,
        "cast_at": datetime.now(timezone.utc).isoformat(),
        "settings": {},
        "performance": {
            "duration_seconds": 0.0,
            "input_size_bytes": 0,
            "output_size_bytes": 0,
        },
    }


def save_metadata(
    metadata: Dict[str, Any],
    output_path: str,
    format: str = "json"
) -> None:
    """Preserve arcane knowledge in a magical tome.

    Args:
        metadata: Arcane knowledge dictionary
        output_path: Path to the magical tome
        format: Format to save in ('json' only, extensible for future)
    """
    output_dir = os.path.dirname(output_path)
    if output_dir:
        setup_output_directory(output_dir)

    if format == "json":
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(metadata, f, indent=2)
    else:
        raise InvalidReagentError(
            f"Unsupported tome format: {format}",
            recovery_suggestion="Use 'json' format for metadata files."
        )


def load_metadata(input_path: str) -> Dict[str, Any]:
    """Load arcane knowledge from a magical tome.

    Args:
        input_path: Path to the magical tome

    Returns:
        Dict containing the arcane knowledge

    Raises:
        InvalidReagentError: If the tome format is invalid
    """
    try:
        with open(input_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        raise InvalidReagentError(
            f"Invalid tome format: {e}",
            recovery_suggestion="Ensure the metadata file is valid JSON."
        )


# =============================================================================
# INPUT VALIDATION
# =============================================================================

# Supported file formats for different spell types
SUPPORTED_AUDIO_FORMATS: Set[str] = {
    ".mp3", ".wav", ".m4a", ".aac", ".ogg", ".flac", ".wma"
}

SUPPORTED_VIDEO_FORMATS: Set[str] = {
    ".mp4", ".avi", ".mov", ".mkv", ".webm", ".flv", ".wmv"
}

SUPPORTED_IMAGE_FORMATS: Set[str] = {
    ".jpg", ".jpeg", ".png", ".webp", ".bmp", ".tiff", ".gif"
}

SUPPORTED_MEDIA_FORMATS = SUPPORTED_AUDIO_FORMATS | SUPPORTED_VIDEO_FORMATS


def validate_input_file(
    input_path: str,
    allowed_formats: Optional[Set[str]] = None,
    max_size_bytes: Optional[int] = None,
    check_readable: bool = True,
) -> Dict[str, Any]:
    """Validate an input file for spell casting.

    Args:
        input_path: Path to the input file
        allowed_formats: Set of allowed file extensions (e.g., {'.mp3', '.wav'})
        max_size_bytes: Maximum file size in bytes
        check_readable: Whether to verify the file is readable

    Returns:
        Dict with validation results including file info

    Raises:
        InvalidReagentError: If validation fails
    """
    # Check if path exists
    if not os.path.exists(input_path):
        raise InvalidReagentError(
            f"Artifact not found: {input_path}",
            recovery_suggestion="Check that the file path is correct and the file exists."
        )

    # Check if it's a file (not a directory)
    if not os.path.isfile(input_path):
        raise InvalidReagentError(
            f"Path is not a file: {input_path}",
            recovery_suggestion="Provide a path to a file, not a directory."
        )

    # Check file extension
    file_ext = Path(input_path).suffix.lower()
    if allowed_formats and file_ext not in allowed_formats:
        allowed_list = ", ".join(sorted(allowed_formats))
        raise InvalidReagentError(
            f"Unsupported artifact format: {file_ext}",
            recovery_suggestion=f"Use one of these formats: {allowed_list}"
        )

    # Check file size
    file_size = os.path.getsize(input_path)
    if max_size_bytes and file_size > max_size_bytes:
        max_mb = max_size_bytes / (1024 * 1024)
        file_mb = file_size / (1024 * 1024)
        raise InvalidReagentError(
            f"Artifact too large: {file_mb:.2f}MB (max: {max_mb:.2f}MB)",
            recovery_suggestion="Provide a smaller file or increase the size limit."
        )

    # Check if readable
    if check_readable and not os.access(input_path, os.R_OK):
        raise InvalidReagentError(
            f"Artifact not readable: {input_path}",
            recovery_suggestion="Check file permissions to ensure read access."
        )

    return {
        "path": input_path,
        "exists": True,
        "size_bytes": file_size,
        "extension": file_ext,
        "is_readable": os.access(input_path, os.R_OK),
    }


def validate_output_path(
    output_path: str,
    check_writable: bool = True,
    create_parent_dirs: bool = False,
) -> str:
    """Validate and sanitize an output path.

    Args:
        output_path: Path to validate
        check_writable: Whether to verify write permissions
        create_parent_dirs: Whether to create parent directories

    Returns:
        Sanitized absolute path

    Raises:
        InvalidReagentError: If validation fails
    """
    # Convert to absolute path
    output_path = os.path.abspath(output_path)

    # Check for path traversal attempts
    if ".." in output_path:
        # We allow ".." in paths but normalize them to prevent traversal issues
        output_path = os.path.normpath(output_path)

    # Check parent directory
    parent_dir = os.path.dirname(output_path)

    if parent_dir and not os.path.exists(parent_dir):
        if create_parent_dirs:
            try:
                os.makedirs(parent_dir, exist_ok=True)
            except OSError as e:
                raise InvalidReagentError(
                    f"Cannot create output directory: {parent_dir}",
                    recovery_suggestion=f"Check permissions: {e}"
                )
        else:
            raise InvalidReagentError(
                f"Output directory does not exist: {parent_dir}",
                recovery_suggestion="Create the directory first or use --create-dirs flag."
            )

    # Check write permissions
    if check_writable:
        if parent_dir and not os.access(parent_dir, os.W_OK):
            raise InvalidReagentError(
                f"Cannot write to output directory: {parent_dir}",
                recovery_suggestion="Check write permissions for the directory."
            )

        # If file exists, check if we can overwrite it
        if os.path.exists(output_path) and not os.access(output_path, os.W_OK):
            raise InvalidReagentError(
                f"Cannot overwrite existing file: {output_path}",
                recovery_suggestion="Check write permissions for the file."
            )

    return output_path


def setup_output_directory(directory: str) -> None:
    """Create an output directory if it doesn't exist.

    Args:
        directory: Directory path to create

    Raises:
        ArcaneDisruptionError: If directory creation fails
    """
    try:
        os.makedirs(directory, exist_ok=True)
    except OSError as e:
        raise ArcaneDisruptionError(
            f"Failed to create output directory: {directory}",
            recovery_suggestion=f"Check permissions and path: {e}"
        )


# =============================================================================
# DEPENDENCY CHECKING
# =============================================================================

def check_dependencies(
    required_commands: Optional[List[str]] = None,
    required_modules: Optional[List[str]] = None,
) -> Dict[str, Any]:
    """Check if required system commands and Python modules are available.

    Args:
        required_commands: List of command names to check (e.g., ['ffmpeg', 'ffprobe'])
        required_modules: List of Python module names to check

    Returns:
        Dict with check results for each dependency
    """
    results = {
        "commands": {},
        "modules": {},
        "all_available": True,
    }

    # Check system commands
    if required_commands:
        for command in required_commands:
            available = shutil.which(command) is not None
            results["commands"][command] = available
            if not available:
                results["all_available"] = False

    # Check Python modules
    if required_modules:
        for module in required_modules:
            try:
                __import__(module)
                results["modules"][module] = True
            except ImportError:
                results["modules"][module] = False
                results["all_available"] = False

    return results


def check_ffmpeg() -> bool:
    """Check if FFmpeg is available on the system.

    Returns:
        True if FFmpeg is available, False otherwise
    """
    return shutil.which("ffmpeg") is not None


def check_ffprobe() -> bool:
    """Check if FFprobe is available on the system.

    Returns:
        True if FFprobe is available, False otherwise
    """
    return shutil.which("ffprobe") is not None


# =============================================================================
# LOGGING
# =============================================================================

# Custom log level names with D&D theme
LOG_LEVEL_NAMES = {
    logging.DEBUG: "ARCANE",
    logging.INFO: "SPELL",
    logging.WARNING: "WARNING",
    logging.ERROR: "FUMBLE",
    logging.CRITICAL: "CRITICAL",
}


class SpellFormatter(logging.Formatter):
    """Custom log formatter with D&D themed level names."""

    def __init__(self, fmt: Optional[str] = None, datefmt: Optional[str] = None):
        """Initialize the spell formatter.

        Args:
            fmt: Log message format string
            datefmt: Date format string
        """
        super().__init__(fmt, datefmt)
        self.level_names = LOG_LEVEL_NAMES

    def format(self, record: logging.LogRecord) -> str:
        """Format a log record with themed level names.

        Args:
            record: Log record to format

        Returns:
            Formatted log message
        """
        record.levelname = self.level_names.get(
            record.levelno,
            record.levelname
        )
        return super().format(record)


def setup_logging(
    spell_name: str,
    log_level: str = "INFO",
    log_file: Optional[str] = None,
    console_output: bool = True,
) -> logging.Logger:
    """Set up structured logging for a spell.

    Args:
        spell_name: Name of the spell for the logger
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: Optional path to log file
        console_output: Whether to output to console

    Returns:
        Configured logger instance
    """
    # Create logger
    logger = logging.getLogger(spell_name)

    # Set log level
    numeric_level = getattr(logging, log_level.upper(), logging.INFO)
    logger.setLevel(numeric_level)

    # Remove existing handlers to avoid duplicates
    logger.handlers.clear()

    # Create formatter
    formatter = SpellFormatter(
        fmt="%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # Add console handler
    if console_output:
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

    # Add file handler
    if log_file:
        log_dir = os.path.dirname(log_file)
        if log_dir:
            os.makedirs(log_dir, exist_ok=True)

        file_handler = logging.FileHandler(log_file, encoding="utf-8")
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger


def get_logger(spell_name: str) -> logging.Logger:
    """Get or create a logger for a spell.

    Args:
        spell_name: Name of the spell

    Returns:
        Logger instance
    """
    return logging.getLogger(spell_name)


# =============================================================================
# PERFORMANCE TRACKING
# =============================================================================

class PerformanceTracker:
    """Track performance metrics for spell execution."""

    def __init__(self, spell_name: str):
        """Initialize the performance tracker.

        Args:
            spell_name: Name of the spell being tracked
        """
        self.spell_name = spell_name
        self.start_time = None
        self.end_time = None
        self.input_size = 0
        self.output_size = 0

    def start(self) -> None:
        """Start tracking performance."""
        self.start_time = time.time()

    def stop(self) -> None:
        """Stop tracking performance."""
        self.end_time = time.time()

    def get_duration(self) -> float:
        """Get the duration in seconds.

        Returns:
            Duration in seconds, or 0 if tracking not complete
        """
        if self.start_time and self.end_time:
            return self.end_time - self.start_time
        return 0.0

    def get_metrics(self) -> Dict[str, Any]:
        """Get performance metrics.

        Returns:
            Dict with performance metrics
        """
        return {
            "spell_name": self.spell_name,
            "duration_seconds": self.get_duration(),
            "input_size_bytes": self.input_size,
            "output_size_bytes": self.output_size,
        }

    def set_input_size(self, size: int) -> None:
        """Set the input file size.

        Args:
            size: Size in bytes
        """
        self.input_size = size

    def set_output_size(self, size: int) -> None:
        """Set the output file size.

        Args:
            size: Size in bytes
        """
        self.output_size = size


# =============================================================================
# FILE UTILITIES
# =============================================================================

def get_file_hash(file_path: str, algorithm: str = "sha256") -> str:
    """Calculate hash of a file for verification.

    Args:
        file_path: Path to the file
        algorithm: Hash algorithm to use (default: sha256)

    Returns:
        Hex digest of the file hash
    """
    hash_obj = hashlib.new(algorithm)
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_obj.update(chunk)
    return hash_obj.hexdigest()


def format_bytes(size_bytes: int) -> str:
    """Format bytes into human-readable string.

    Args:
        size_bytes: Size in bytes

    Returns:
        Formatted string (e.g., "1.23 MB")
    """
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.2f} PB"


def format_duration(seconds: float) -> str:
    """Format seconds into human-readable duration.

    Args:
        seconds: Duration in seconds

    Returns:
        Formatted string (e.g., "1m 23s")
    """
    if seconds < 60:
        return f"{seconds:.1f}s"
    minutes = int(seconds // 60)
    secs = seconds % 60
    if minutes < 60:
        return f"{minutes}m {secs:.0f}s"
    hours = minutes // 60
    mins = minutes % 60
    return f"{hours}h {mins}m"
