# AI Craft Spellbook - Changelog

All notable changes to the AI Craft Spellbook framework will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.0.0] - 2025-03-06

### Added - Framework Foundation

#### Phase 1: Shared Infrastructure
- Created `spells/utils/` package with shared utilities
- Added `spells/utils/common.py` with:
  - `save_metadata()` and `load_metadata()` for metadata management
  - `validate_input_file()` for comprehensive input validation
  - `validate_output_path()` for path sanitization and security
  - `setup_output_directory()` for safe directory creation
  - `get_spell_metadata_base()` for standardized metadata
  - `check_dependencies()` for runtime dependency verification
  - Structured logging with `setup_logging()` and `get_logger()`
  - `PerformanceTracker` class for performance metrics
  - Utility functions: `format_bytes()`, `format_duration()`, `get_file_hash()`
- Added `spells/utils/error_handling.py` with:
  - `SpellFumbleError` - Base exception for spell failures
  - `ArcaneDisruptionError` - External system failures
  - `InvalidReagentError` - Input validation errors
  - `format_spell_fumble()` - Themed error message formatting
  - `handle_spell_error()` - Centralized error handling

#### Phase 2: Spell Enhancements
- **Refactored `spells/audio_cleanse.py`:**
  - Integrated shared utilities (validation, logging, performance tracking)
  - Added comprehensive input validation (file format, size, permissions)
  - Replaced generic errors with themed exceptions
  - Added progress tracking via structured logging
  - Added FFmpeg/FFprobe dependency checks
  - Standardized metadata format with performance metrics
  - Enhanced CLI with logging options and better help text
  - Added max file size validation (500MB default)
  - Improved error messages with recovery suggestions

- **Refactored `spells/dispel_background.py`:**
  - Integrated shared utilities (validation, logging, performance tracking)
  - Added comprehensive input validation
  - Added alpha matting options for cleaner edges
  - Added batch processing support with glob patterns
  - Replaced generic errors with themed exceptions
  - Standardized metadata format with performance metrics
  - Enhanced CLI with batch mode and logging options
  - Added max file size validation (50MB default)
  - Improved error messages with recovery suggestions

#### Phase 3: Development Infrastructure
- Created `tests/` directory with:
  - `tests/test_utils.py` - Comprehensive tests for shared utilities
  - `tests/test_dispel_background.py` - Tests for background removal spell
  - `tests/pytest.ini` - Pytest configuration
  - Test fixtures and integration test support
- Created `logs/` directory for spell-specific log files
- Created `examples/` directory for sample files
- Updated `requirements.txt` with:
  - Testing framework: pytest, pytest-cov, pytest-mock
  - Code quality tools: black, flake8, mypy
  - Type stubs for better IDE support

#### Phase 4: Security & Robustness
- Enhanced input validation:
  - File format whitelisting for all spells
  - Configurable file size limits
  - Path traversal protection in output validation
  - Permission checks before operations
- Added error recovery:
  - Themed error messages with recovery suggestions
  - Graceful handling of missing dependencies
  - Meaningful error messages for all failure modes
- Updated `.gitignore` with:
  - Mypy cache
  - Security-related patterns

#### Phase 5: Documentation
- Created `CONTRIBUTING.md` with:
  - Complete development setup guide
  - Step-by-step spell creation tutorial
  - Code style guidelines (D&D theme vs technical)
  - Testing requirements and examples
  - Documentation standards
  - Pull request process and template
- Created `CHANGELOG.md` for tracking improvements
- Updated `.env.example` with:
  - Expanded configuration options
  - Spell-specific defaults
  - Logging configuration
  - Performance tuning parameters
  - Development settings

### Changed
- **Breaking change:** Both spells now require the utils package
- Metadata format now includes:
  - Standardized structure with `spell_name`, `version`, `cast_at`
  - Performance metrics (`duration_seconds`, `input_size_bytes`, `output_size_bytes`)
  - Spell-specific data
- Error handling now uses themed exceptions throughout
- All paths are validated and sanitized before use

### Improved
- Consistent error messages with D&D theme across all spells
- Better logging with configurable levels and file output
- Performance tracking for all operations
- Input validation prevents common errors
- Security hardening with path validation
- More informative CLI help text

### Security
- Added path traversal protection
- Added file size limits
- Added permission checks
- Input sanitization for all user inputs

---

## [1.0.0] - Initial Release

### Added
- Initial framework with three-layer architecture
- `spells/audio_cleanse.py` - Audio cleansing spell
- `spells/dispel_background.py` - Background removal spell
- Basic error handling with D&D theme
- Metadata saving for both spells
- Quest logs in `quests/` directory

### Features
- Audio silence removal
- Audio normalization
- Noise reduction
- Background removal from images
- Multiple model support for background removal
- Metadata tracking

---

## Version Convention

- **Major version (X.0.0):** Breaking changes, architectural changes
- **Minor version (0.X.0):** New features, backward compatible
- **Patch version (0.0.X):** Bug fixes, small improvements

## Legend

- **Added:** New features
- **Changed:** Changes to existing functionality
- **Deprecated:** Soon-to-be removed features
- **Removed:** Removed features
- **Fixed:** Bug fixes
- **Security:** Security improvements
