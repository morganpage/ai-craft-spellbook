"""
Test spell metadata extraction and documentation generation.

This test suite verifies:
- All spells have required SPELL_METADATA
- Spell metadata structure is valid
- Documentation generation works correctly
- AI_CRAFT_SPELLBOOK.md section updates correctly
"""

import json
import os
import sys
from pathlib import Path
from typing import Dict, Any, List

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


def load_spell_metadata(spell_path: Path) -> Dict[str, Any]:
    """Load SPELL_METADATA from a spell file.

    Args:
        spell_path: Path to spell .py file

    Returns:
        Dict containing SPELL_METADATA

    Raises:
        FileNotFoundError: If spell file not found
        ValueError: If SPELL_METADATA not found or invalid
    """
    import importlib.util

    module_name = f"spells.{spell_path.stem}"
    spec = importlib.util.spec_from_file_location(module_name, spell_path)
    if spec is None or spec.loader is None:
        raise ValueError(f"Could not load spec for {spell_path.name}")

    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)

    if not hasattr(module, "SPELL_METADATA"):
        raise ValueError(f"No SPELL_METADATA found in {spell_path.name}")

    metadata = getattr(module, "SPELL_METADATA")

    if not isinstance(metadata, dict):
        raise ValueError(f"SPELL_METADATA is not a dict in {spell_path.name}")

    return metadata


def validate_metadata_structure(metadata: Dict[str, Any], spell_name: str) -> List[str]:
    """Validate SPELL_METADATA has all required fields.

    Args:
        metadata: SPELL_METADATA dict
        spell_name: Name of spell for error messages

    Returns:
        List of validation error messages (empty if valid)
    """
    errors = []

    # Required fields
    required_fields = [
        "name",
        "version",
        "primary_keywords",
        "supported_formats",
        "description",
        "examples",
        "output_naming_pattern",
        "cli_pattern",
        "cli_parameters"
    ]

    for field in required_fields:
        if field not in metadata:
            errors.append(f"{spell_name}: Missing required field '{field}'")
        elif not metadata[field]:
            errors.append(f"{spell_name}: Field '{field}' is empty or None")

    # Validate specific field types
    if "primary_keywords" in metadata and not isinstance(metadata["primary_keywords"], list):
        errors.append(f"{spell_name}: 'primary_keywords' must be a list")

    if "supported_formats" in metadata and not isinstance(metadata["supported_formats"], list):
        errors.append(f"{spell_name}: 'supported_formats' must be a list")

    if "examples" in metadata and not isinstance(metadata["examples"], list):
        errors.append(f"{spell_name}: 'examples' must be a list")

    if "cli_parameters" in metadata and not isinstance(metadata["cli_parameters"], dict):
        errors.append(f"{spell_name}: 'cli_parameters' must be a dict")

    # Validate secondary_keywords if present
    if "secondary_keywords" in metadata and not isinstance(metadata["secondary_keywords"], dict):
        errors.append(f"{spell_name}: 'secondary_keywords' must be a dict")

    # Validate name matches filename
    if "name" in metadata and spell_name != metadata["name"]:
        errors.append(f"{spell_name}: 'name' field ('{metadata['name']}') doesn't match filename")

    return errors


def test_all_spells_have_metadata():
    """Test 1: Verify all spells have SPELL_METADATA."""
    print("\n" + "="*70)
    print("TEST 1: All spells have SPELL_METADATA")
    print("="*70)

    spells_dir = project_root / "spells"
    spell_files = [
        f for f in spells_dir.glob("*.py")
        if f.name != "__init__.py" and not f.name.startswith("_")
    ]

    failures = []
    for spell_file in sorted(spell_files):
        try:
            metadata = load_spell_metadata(spell_file)
            print(f"  ✓ {spell_file.name}: {metadata['name']}")
        except Exception as e:
            print(f"  ✗ {spell_file.name}: {e}")
            failures.append(spell_file.name)

    if failures:
        print(f"\n✗ FAIL: {len(failures)} spells missing metadata: {', '.join(failures)}")
        return False
    else:
        print(f"\n✓ PASS: All {len(spell_files)} spells have metadata")
        return True


def test_metadata_structure():
    """Test 2: Validate SPELL_METADATA structure."""
    print("\n" + "="*70)
    print("TEST 2: SPELL_METADATA structure validation")
    print("="*70)

    spells_dir = project_root / "spells"
    spell_files = [
        f for f in spells_dir.glob("*.py")
        if f.name != "__init__.py" and not f.name.startswith("_")
    ]

    all_errors = []
    for spell_file in sorted(spell_files):
        try:
            metadata = load_spell_metadata(spell_file)
            spell_name = spell_file.stem
            errors = validate_metadata_structure(metadata, spell_name)

            if errors:
                for error in errors:
                    print(f"  ✗ {error}")
                    all_errors.append(error)
            else:
                print(f"  ✓ {spell_name}: Valid structure")

        except Exception as e:
            print(f"  ✗ {spell_file.name}: {e}")
            all_errors.append(str(e))

    if all_errors:
        print(f"\n✗ FAIL: {len(all_errors)} validation errors found")
        return False
    else:
        print(f"\n✓ PASS: All metadata structures are valid")
        return True


def test_documentation_generation():
    """Test 3: Test documentation generation."""
    print("\n" + "="*70)
    print("TEST 3: Documentation generation")
    print("="*70)

    try:
        # Import documentation generator
        import importlib.util
        tools_dir = project_root / "tools"

        doc_gen_path = tools_dir / "update_spell_docs.py"
        if not doc_gen_path.exists():
            print(f"  ✗ Documentation generator not found: {doc_gen_path}")
            return False

        print(f"  ✓ Documentation generator found: {doc_gen_path}")

        # Test loading the module
        spec = importlib.util.spec_from_file_location("update_spell_docs", doc_gen_path)
        if spec is None or spec.loader is None:
            print(f"  ✗ Could not load documentation generator module")
            return False

        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        print(f"  ✓ Documentation generator module loaded")

        # Check that key functions exist
        required_functions = [
            "extract_spell_metadata",
            "scan_spells",
            "generate_spell_invocation_guide",
            "generate_ai_craft_spellbook_section"
        ]

        for func_name in required_functions:
            if hasattr(module, func_name):
                print(f"  ✓ Function exists: {func_name}")
            else:
                print(f"  ✗ Function missing: {func_name}")
                return False

        print(f"\n✓ PASS: Documentation generator is valid")
        return True

    except Exception as e:
        print(f"  ✗ Error: {e}")
        return False


def test_spell_invocation_guide_exists():
    """Test 4: Verify SPELL_INVOCATION.md exists."""
    print("\n" + "="*70)
    print("TEST 4: SPELL_INVOCATION.md exists")
    print("="*70)

    guide_path = project_root / "SPELL_INVOCATION.md"

    if not guide_path.exists():
        print(f"  ✗ SPELL_INVOCATION.md not found at: {guide_path}")
        return False

    print(f"  ✓ SPELL_INVOCATION.md found")

    # Check key sections exist
    content = guide_path.read_text(encoding="utf-8")

    required_sections = [
        "Quick Reference Table",
        "Decision Tree",
        "Keyword Detection Rules",
        "Spell-by-Spell Invocation Guide",
        "File Type Validation Matrix"
    ]

    all_found = True
    for section in required_sections:
        if section in content:
            print(f"  ✓ Section found: {section}")
        else:
            print(f"  ✗ Section missing: {section}")
            all_found = False

    if all_found:
        print(f"\n✓ PASS: SPELL_INVOCATION.md is complete")
        return True
    else:
        print(f"\n✗ FAIL: SPELL_INVOCATION.md is missing sections")
        return False


def test_ai_craft_spellbook_section_exists():
    """Test 5: Verify AI_CRAFT_SPELLBOOK.md has spell invocation section."""
    print("\n" + "="*70)
    print("TEST 5: AI_CRAFT_SPELLBOOK.md spell invocation section")
    print("="*70)

    ai_craft_path = project_root / "AI_CRAFT_SPELLBOOK.md"

    if not ai_craft_path.exists():
        print(f"  ✗ AI_CRAFT_SPELLBOOK.md not found at: {ai_craft_path}")
        return False

    print(f"  ✓ AI_CRAFT_SPELLBOOK.md found")

    content = ai_craft_path.read_text(encoding="utf-8")

    # Check for key elements
    required_elements = [
        "## Spell Invocation Guidelines for AI Assistants",
        "### When to Use Spells vs Bash Commands",
        "### Spell Invocation Decision Process",
        "### Quick Keyword Reference",
        "### Common Invocation Patterns",
        "### Spell Metadata Requirements"
    ]

    all_found = True
    for element in required_elements:
        if element in content:
            print(f"  ✓ Section found: {element}")
        else:
            print(f"  ✗ Section missing: {element}")
            all_found = False

    if all_found:
        print(f"\n✓ PASS: AI_CRAFT_SPELLBOOK.md has spell invocation section")
        return True
    else:
        print(f"\n✗ FAIL: AI_CRAFT_SPELLBOOK.md is missing sections")
        return False


def test_keyword_detection():
    """Test 6: Test keyword detection patterns."""
    print("\n" + "="*70)
    print("TEST 6: Keyword detection patterns")
    print("="*70)

    # Define test cases: user request -> expected spell
    test_cases = [
        ("split landscape.png", "split_artifact"),
        ("cleanse audio in podcast.mp3", "audio_cleanse"),
        ("remove background from character.png", "dispel_background"),
        ("divide portrait.jpg", "split_artifact"),
        ("purify video.mp4", "audio_cleanse"),
        ("dispel background on sprite.png", "dispel_background")
    ]

    spells_dir = project_root / "spells"
    spell_files = [
        f for f in spells_dir.glob("*.py")
        if f.name != "__init__.py" and not f.name.startswith("_")
    ]

    # Load all spell metadata
    spell_metadata = {}
    for spell_file in spell_files:
        try:
            metadata = load_spell_metadata(spell_file)
            spell_metadata[metadata["name"]] = metadata
        except Exception as e:
            print(f"  ✗ Could not load metadata for {spell_file.name}")

    passed = 0
    failed = 0

    for user_request, expected_spell in test_cases:
        # Find matching spell
        matched_spell = None

        for spell_name, metadata in spell_metadata.items():
            for keyword in metadata["primary_keywords"]:
                if keyword in user_request.lower():
                    matched_spell = spell_name
                    break
            if matched_spell:
                break

        if matched_spell == expected_spell:
            print(f"  ✓ \"{user_request}\" → {matched_spell}")
            passed += 1
        else:
            print(f"  ✗ \"{user_request}\" → expected {expected_spell}, got {matched_spell}")
            failed += 1

    if failed == 0:
        print(f"\n✓ PASS: All {passed} keyword detection tests passed")
        return True
    else:
        print(f"\n✗ FAIL: {failed}/{passed+failed} tests failed")
        return False


def main():
    """Run all tests."""
    print("\n" + "="*70)
    print("Spell Metadata Test Suite")
    print("="*70)
    print(f"Project root: {project_root}")

    tests = [
        test_all_spells_have_metadata,
        test_metadata_structure,
        test_documentation_generation,
        test_spell_invocation_guide_exists,
        test_ai_craft_spellbook_section_exists,
        test_keyword_detection
    ]

    results = []
    for test_func in tests:
        try:
            result = test_func()
            results.append((test_func.__name__, result))
        except Exception as e:
            print(f"\n✗ EXCEPTION in {test_func.__name__}: {e}")
            import traceback
            traceback.print_exc()
            results.append((test_func.__name__, False))

    # Summary
    print("\n" + "="*70)
    print("TEST SUMMARY")
    print("="*70)

    passed = sum(1 for _, result in results if result)
    failed = len(results) - passed

    for test_name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"  {status}: {test_name}")

    print(f"\nTotal: {passed} passed, {failed} failed")

    if failed == 0:
        print("\n✓ All tests passed!")
        return 0
    else:
        print(f"\n✗ {failed} test(s) failed")
        return 1


if __name__ == "__main__":
    sys.exit(main())
