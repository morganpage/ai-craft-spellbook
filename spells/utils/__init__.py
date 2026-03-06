"""
AI Craft Spellbook - Magical Utilities

This package contains shared magical utilities used across all spells.
These utilities provide common functionality for metadata management,
input validation, logging, and error handling while maintaining the
D&D theme consistency required by the framework.
"""

from .common import (
    save_metadata,
    validate_input_file,
    validate_output_path,
    setup_output_directory,
    get_spell_metadata_base,
    check_dependencies,
    setup_logging,
    get_logger,
)
from .error_handling import (
    SpellFumbleError,
    ArcaneDisruptionError,
    InvalidReagentError,
    format_spell_fumble,
)

__all__ = [
    "save_metadata",
    "validate_input_file",
    "validate_output_path",
    "setup_output_directory",
    "get_spell_metadata_base",
    "check_dependencies",
    "setup_logging",
    "get_logger",
    "SpellFumbleError",
    "ArcaneDisruptionError",
    "InvalidReagentError",
    "format_spell_fumble",
]
