"""
AI Craft Spellbook - Themed Error Handling

This module provides custom exception classes and error formatting functions
that maintain the D&D theme while providing clear, actionable error messages.

All spells should use these exception types for consistent error handling
across the framework.
"""

import sys
from typing import Optional, Dict, Any


class SpellFumbleError(Exception):
    """Base exception for all spell-related errors.

    This represents a general failure during spell casting where the ritual
    could not be completed as intended.
    """

    def __init__(self, message: str, recovery_suggestion: Optional[str] = None):
        """Initialize a spell fumble error.

        Args:
            message: Description of what went wrong
            recovery_suggestion: Optional hint for how to recover from the error
        """
        self.recovery_suggestion = recovery_suggestion
        super().__init__(message)


class ArcaneDisruptionError(SpellFumbleError):
    """Exception for external service or system failures.

    This represents failures in external systems like FFmpeg, rembg,
    file system operations, or network requests.
    """

    pass


class InvalidReagentError(SpellFumbleError):
    """Exception for invalid input parameters or files.

    This represents errors where the spell components (inputs, parameters,
    or configuration) are not valid for the ritual being performed.
    """

    pass


def format_spell_fumble(
    error: Exception,
    spell_name: str,
    context: Optional[Dict[str, Any]] = None
) -> str:
    """Format an error message with D&D theme and recovery suggestions.

    Args:
        error: The exception that occurred
        spell_name: Name of the spell that failed
        context: Optional additional context about the error

    Returns:
        Formatted error message with themed text and recovery suggestions
    """
    error_type = type(error).__name__
    error_message = str(error)

    # Base error message
    output = [f"\n✗ Spell Fumble: {spell_name}"]
    output.append(f"  Error Type: {error_type}")
    output.append(f"  Details: {error_message}")

    # Add recovery suggestion if available
    recovery = None
    if isinstance(error, SpellFumbleError):
        recovery = error.recovery_suggestion
    elif isinstance(error, FileNotFoundError):
        recovery = "Check that the file path is correct and the file exists."
    elif isinstance(error, PermissionError):
        recovery = "Check file permissions and ensure you have write access."
    elif isinstance(error, ValueError):
        recovery = "Verify all parameters are within valid ranges."
    elif isinstance(error, RuntimeError):
        recovery = "Check system dependencies and available resources."

    if recovery:
        output.append(f"  Recovery: {recovery}")

    # Add context if provided
    if context:
        output.append("\n  Arcane Context:")
        for key, value in context.items():
            output.append(f"    {key}: {value}")

    return "\n".join(output)


def handle_spell_error(
    error: Exception,
    spell_name: str,
    context: Optional[Dict[str, Any]] = None,
    exit_on_error: bool = True
) -> None:
    """Handle a spell error with themed output and optional exit.

    Args:
        error: The exception that occurred
        spell_name: Name of the spell that failed
        context: Optional additional context about the error
        exit_on_error: Whether to exit the program after handling
    """
    print(format_spell_fumble(error, spell_name, context), file=sys.stderr)

    if exit_on_error:
        sys.exit(1)
