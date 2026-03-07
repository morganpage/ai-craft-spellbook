#!/usr/bin/env python3
"""
Spell Documentation Generator

This tool scans all spells in the spells/ directory, extracts SPELL_METADATA,
and generates/updates documentation files for spell invocation guidance.
"""

import argparse
import ast
import importlib
import inspect
import json
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


def extract_spell_metadata(spell_path: Path) -> Optional[Dict[str, Any]]:
    """Extract SPELL_METADATA from a spell file.

    Args:
        spell_path: Path to the spell .py file

    Returns:
        Dict containing SPELL_METADATA or None if not found
    """
    try:
        # Import the spell module
        module_name = f"spells.{spell_path.stem}"
        spec = importlib.util.spec_from_file_location(module_name, spell_path)
        if spec is None or spec.loader is None:
            print(f"  ✗ Could not load spec for {spell_path.name}")
            return None

        module = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = module
        spec.loader.exec_module(module)

        # Extract SPELL_METADATA
        if hasattr(module, "SPELL_METADATA"):
            return getattr(module, "SPELL_METADATA")
        else:
            print(f"  ✗ No SPELL_METADATA found in {spell_path.name}")
            return None

    except Exception as e:
        print(f"  ✗ Error processing {spell_path.name}: {e}")
        return None


def scan_spells(spells_dir: Path) -> List[Dict[str, Any]]:
    """Scan spells directory and extract metadata from all spells.

    Args:
        spells_dir: Path to spells/ directory

    Returns:
        List of SPELL_METADATA dicts
    """
    spell_files = list(spells_dir.glob("*.py"))

    # Exclude __init__.py and utility files
    spell_files = [
        f for f in spell_files
        if f.name != "__init__.py" and not f.name.startswith("_")
    ]

    print(f"\nScanning {len(spell_files)} spells in {spells_dir}/...")

    metadata_list = []
    for spell_file in sorted(spell_files):
        print(f"\n  Processing: {spell_file.name}")
        metadata = extract_spell_metadata(spell_file)
        if metadata:
            metadata_list.append(metadata)
            print(f"  ✓ Metadata extracted: {metadata['name']}")
        else:
            print(f"  ✗ No metadata found")

    return metadata_list


def generate_spell_invocation_guide(metadata_list: List[Dict[str, Any]]) -> str:
    """Generate SPELL_INVOCATION.md content.

    Args:
        metadata_list: List of SPELL_METADATA dicts

    Returns:
        String containing the full SPELL_INVOCATION.md content
    """
    sections = []

    # Header
    sections.append("# Spell Invocation Guide for AI Assistants\n")
    sections.append(f"*Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n")
    sections.append("\nThis guide helps AI assistants recognize when to invoke spells in the AI Craft Spellbook framework.\n")

    # Quick Reference Table
    sections.append("## Quick Reference Table\n")
    sections.append("| Spell | Primary Keywords | Supported Formats | Command Pattern |\n")
    sections.append("|-------|-----------------|-------------------|----------------|\n")

    for meta in sorted(metadata_list, key=lambda x: x["name"]):
        keywords = ", ".join(meta["primary_keywords"][:3]) + ("..." if len(meta["primary_keywords"]) > 3 else "")
        formats = ", ".join(meta["supported_formats"][:4]) + ("..." if len(meta["supported_formats"]) > 4 else "")
        sections.append(
            f"| {meta['name']} | {keywords} | {formats} | `{meta['cli_pattern']}` |\n"
        )

    sections.append("\n")

    # Decision Tree
    sections.append("## Decision Tree: When to Use Spells vs Bash Commands\n")
    sections.append("```\n")
    sections.append("User Request\n")
    sections.append("    │\n")
    sections.append("    ├── Contains spell keyword?\n")
    sections.append("    │   ├── Yes → Check file type matches spell support?\n")
    sections.append("    │   │   ├── Yes → Check if quest exists in quests/?\n")
    sections.append("    │   │   │   ├── Yes → INVOKE THE SPELL\n")
    sections.append("    │   │   │   └── No  → Use bash commands\n")
    sections.append("    │   │   └── No  → Use bash commands\n")
    sections.append("    │\n")
    sections.append("    ├── File operation (copy, move, list)?\n")
    sections.append("    │   └── Yes → Use Bash tool\n")
    sections.append("    │\n")
    sections.append("    ├── Git operation?\n")
    sections.append("    │   └── Yes → Use Bash tool\n")
    sections.append("    │\n")
    sections.append("    └── Other operation?\n")
    sections.append("        └── Use appropriate tool (Read, Glob, Grep, Bash)\n")
    sections.append("```\n\n")

    # Keyword Detection Rules
    sections.append("## Keyword Detection Rules\n")
    sections.append("### Primary Keywords (Must Match)\n")
    sections.append("| Spell | Keywords |\n")
    sections.append("|-------|----------|\n")

    for meta in sorted(metadata_list, key=lambda x: x["name"]):
        keywords = ", ".join(f"`{kw}`" for kw in meta["primary_keywords"])
        sections.append(f"| {meta['name']} | {keywords} |\n")

    sections.append("\n")

    # Spell-by-Spell Guide
    sections.append("## Spell-by-Spell Invocation Guide\n\n")

    for meta in sorted(metadata_list, key=lambda x: x["name"]):
        sections.append(f"### {meta['name']}\n\n")
        sections.append(f"**Description:** {meta['description']}\n\n")

        # Primary Keywords
        sections.append(f"**Primary Keywords:** {', '.join(meta['primary_keywords'])}\n\n")

        # Secondary Keywords
        if meta.get("secondary_keywords"):
            sections.append("**Secondary Keywords:**\n")
            for category, keywords in meta["secondary_keywords"].items():
                sections.append(f"- *{category}:* {', '.join(keywords)}\n")
            sections.append("\n")

        # Supported Formats
        sections.append(f"**Supported Formats:** {', '.join(meta['supported_formats'])}\n\n")

        # Common Use Cases
        if meta.get("common_use_cases"):
            sections.append("**Common Use Cases:**\n")
            for use_case in meta["common_use_cases"]:
                sections.append(f"- {use_case}\n")
            sections.append("\n")

        # Examples
        if meta.get("examples"):
            sections.append("**Natural Language Examples:**\n")
            for example in meta["examples"]:
                sections.append(f"- \"{example}\"\n")
            sections.append("\n")

        # CLI Pattern
        sections.append(f"**CLI Pattern:** `{meta['cli_pattern']}`\n\n")

        # CLI Parameters
        if meta.get("cli_parameters"):
            sections.append("**CLI Parameters:**\n")
            for param, description in meta["cli_parameters"].items():
                sections.append(f"- `{param}`: {description}\n")
            sections.append("\n")

        # Output Naming
        sections.append(f"**Output Naming:** `{meta['output_naming_pattern']}`\n\n")

        sections.append("---\n\n")

    # Parameter Extraction Patterns
    sections.append("## Natural Language to CLI Parameter Extraction\n\n")

    for meta in sorted(metadata_list, key=lambda x: x["name"]):
        sections.append(f"### {meta['name']}\n\n")

        # Extract patterns from examples and secondary keywords
        patterns = []

        if "cleanse" in meta["name"] or "audio" in meta["name"]:
            patterns.append("`with heavy noise reduction` → --noise-strength heavy")
            patterns.append("`for podcast` → --loudness -16")
            patterns.append("`for YouTube` → --loudness -14")
            patterns.append("`for broadcast` → --loudness -23")
            patterns.append("`don't remove silence` → --no-silence-removal")
            patterns.append("`keep pauses` → --no-silence-removal")
            patterns.append("`skip noise reduction` → --no-noise-reduction")
            patterns.append("`only normalize` → --no-silence-removal --no-noise-reduction")

        elif "dispel" in meta["name"] or "background" in meta["name"]:
            patterns.append("`human model` / `portrait` → --model u2net_human_seg")
            patterns.append("`clothing` / `fashion` → --model u2net_cloth_seg")
            patterns.append("`fast` / `quick` / `lightweight` → --model u2netp")
            patterns.append("`silhouette` / `icon` → --model silueta")
            patterns.append("`cleaner edges` / `better edges` → --alpha-matting")
            patterns.append("`high quality` → use u2net (default)")
            patterns.append("`batch process` → --batch --input \"*.png\"")

        elif "split" in meta["name"] or "divide" in meta["name"]:
            patterns.append("`JPEG` / `JPG` → --format jpg")
            patterns.append("`PNG` → --format png (default)")
            patterns.append("`WEBP` → --format webp")
            patterns.append("`save to folder/` → --output-dir folder/")
            patterns.append("`landscape` / `wide` → horizontal split (auto)")
            patterns.append("`portrait` / `tall` → vertical split (auto)")

        if patterns:
            sections.append("| Natural Language | CLI Flag |\n")
            sections.append("|------------------|----------|\n")
            for pattern in patterns:
                parts = pattern.split(" → ")
                if len(parts) == 2:
                    sections.append(f"| {parts[0]} | `{parts[1]}` |\n")
            sections.append("\n")

    # File Type Validation Matrix
    sections.append("## File Type Validation Matrix\n\n")
    sections.append("| Spell | Supported Extensions |\n")
    sections.append("|-------|-------------------|\n")

    for meta in sorted(metadata_list, key=lambda x: x["name"]):
        extensions = ", ".join([f".{fmt}" for fmt in meta["supported_formats"]])
        sections.append(f"| {meta['name']} | {extensions} |\n")

    sections.append("\n")

    # Output Naming Conventions
    sections.append("## Output Naming Conventions\n\n")
    sections.append("All spells follow consistent output naming:\n\n")
    sections.append("| Spell | Output Pattern | Example |\n")
    sections.append("|-------|---------------|---------|\n")

    for meta in sorted(metadata_list, key=lambda x: x["name"]):
        example = meta["output_naming_pattern"].replace("<name>", "artifact").replace("<ext>", "png")
        sections.append(f"| {meta['name']} | `{meta['output_naming_pattern']}` | `{example}` |\n")

    sections.append("\n")

    # Troubleshooting
    sections.append("## Troubleshooting Spell Invocation\n\n")

    issues = [
        ("Spell not recognized", "Check spelling and verify spell exists in spells/ directory", "Refer to Quick Reference Table"),
        ("Metadata missing", "Add SPELL_METADATA dict to spell file", "See templates/new_spell.py.template"),
        ("Wrong spell invoked", "Verify primary keyword matches spell intent", "Check file type against supported formats"),
        ("File type not supported", "Use different format or bash commands", "Check File Type Validation Matrix"),
        ("Parameters not extracted", "Use explicit CLI flags", "Spell keywords may not match natural language")
    ]

    sections.append("| Issue | Diagnosis | Solution |\n")
    sections.append("|-------|------------|----------|\n")

    for issue, diagnosis, solution in issues:
        sections.append(f"| {issue} | {diagnosis} | {solution} |\n")

    sections.append("\n")

    # Footer
    sections.append("---\n")
    sections.append("*This guide is automatically generated from SPELL_METADATA in each spell. Run `python tools/update_spell_docs.py` to update.*\n")

    return "".join(sections)


def generate_ai_craft_spellbook_section(metadata_list: List[Dict[str, Any]]) -> str:
    """Generate the spell invocation section for AI_CRAFT_SPELLBOOK.md.

    Args:
        metadata_list: List of SPELL_METADATA dicts

    Returns:
        String containing the section content
    """
    lines = []

    lines.append("\n## Spell Invocation Guidelines for AI Assistants\n")
    lines.append("\n### When to Use Spells vs Bash Commands\n")
    lines.append("\nAI assistants should use spells instead of bash commands when:\n")
    lines.append("- User request contains **primary keywords** matching a spell\n")
    lines.append("- File type is **supported** by the spell\n")
    lines.append("- A corresponding **quest** exists in `quests/` directory\n")
    lines.append("\nOtherwise, use appropriate bash commands or tools (Read, Glob, Grep, Bash).\n")

    lines.append("\n### Spell Invocation Decision Process\n")
    lines.append("\n1. **Identify Intent**: Extract action and target from user request\n")
    lines.append("2. **Check Spell Book**: Look for matching primary keywords\n")
    lines.append("3. **Validate File**: Check if file exists and matches supported formats\n")
    lines.append("4. **Read Quest**: If unclear about parameters, read the quest\n")
    lines.append("5. **Invoke Spell**: Construct CLI command with appropriate flags\n")
    lines.append("6. **Report Results**: Show output location and any errors\n")

    lines.append("\n### Quick Keyword Reference\n")
    lines.append("\n| Keyword | Spell | File Types |\n")
    lines.append("|----------|--------|-----------|\n")

    for meta in sorted(metadata_list, key=lambda x: x["name"]):
        keywords = ", ".join(f"`{kw}`" for kw in meta["primary_keywords"][:2])
        formats = ", ".join(meta["supported_formats"][:3])
        lines.append(f"| {keywords} | {meta['name']} | {formats}... |\n")

    lines.append("\n### Common Invocation Patterns\n")
    lines.append("\n| User Says | Spell | CLI Command |\n")
    lines.append("|-----------|-------|------------|\n")

    # Add example patterns
    for meta in sorted(metadata_list, key=lambda x: x["name"]):
        if meta.get("examples") and len(meta["examples"]) > 0:
            example = meta["examples"][0]
            spell_file = f"spells/{meta['name']}.py"
            cmd = f"python {spell_file} --input <file>"

            # Extract simple file path from example
            import re
            file_match = re.search(r'[\w\-\.]+\.(png|jpg|jpeg|mp3|wav|mp4|mkv|mov)', example)
            if file_match:
                cmd = f"python {spell_file} --input {file_match.group()}"

            lines.append(f"| \"{example}\" | {meta['name']} | `{cmd}` |\n")

    lines.append("\n### Spell Metadata Requirements\n")
    lines.append("\nAll spells must include a `SPELL_METADATA` dict at the top of the file:\n")
    lines.append("```python\n")
    lines.append("SPELL_METADATA = {\n")
    lines.append('    "name": "spell_name",\n')
    lines.append('    "version": "1.0.0",\n')
    lines.append('    "primary_keywords": ["keyword1", "keyword2"],\n')
    lines.append('    "secondary_keywords": {...},\n')
    lines.append('    "supported_formats": ["png", "jpg"],\n')
    lines.append('    "description": "Brief description",\n')
    lines.append('    "common_use_cases": [...],\n')
    lines.append('    "examples": [...],\n')
    lines.append('    "output_naming_pattern": "<name>_output.<ext>",\n')
    lines.append('    "cli_pattern": "python spells/<name>.py --input <file>",\n')
    lines.append('    "cli_parameters": {...}\n')
    lines.append("}\n")
    lines.append("```\n")

    lines.append("\n**Required Fields:**\n")
    required_fields = [
        ("name", "Spell filename without .py extension"),
        ("version", "Semantic version (e.g., 1.0.0)"),
        ("primary_keywords", "List of keywords that should trigger this spell"),
        ("supported_formats", "List of supported file extensions without dots"),
        ("description", "Brief description of what the spell does"),
        ("examples", "List of natural language examples of invoking the spell"),
        ("output_naming_pattern", "Pattern for output file naming"),
        ("cli_pattern", "Basic CLI pattern showing required parameters"),
        ("cli_parameters", "Dict of CLI flags to descriptions")
    ]

    for field, description in required_fields:
        lines.append(f"- **{field}**: {description}\n")

    lines.append("\n**Optional Fields:**\n")
    lines.append("- **secondary_keywords**: Dict of keyword categories to additional keywords\n")
    lines.append("- **common_use_cases**: List of common use cases for the spell\n")

    lines.append("\n**Updating Documentation:**\n")
    lines.append("After adding or modifying a spell's SPELL_METADATA, run:\n")
    lines.append("```bash\n")
    lines.append("make update-docs\n")
    lines.append("# or\n")
    lines.append("./tools/update_docs.sh\n")
    lines.append("# or\n")
    lines.append("python tools/update_spell_docs.py\n")
    lines.append("```\n")

    lines.append("\nThis will regenerate SPELL_INVOCATION.md and update this section of AI_CRAFT_SPELLBOOK.md.\n")

    return "".join(lines)


def update_ai_craft_spellbook(section_content: str, output_path: Path) -> None:
    """Update AI_CRAFT_SPELLBOOK.md with the spell invocation section.

    Args:
        section_content: Content to insert/replace
        output_path: Path to AI_CRAFT_SPELLBOOK.md
    """
    if not output_path.exists():
        print(f"  ✗ {output_path} not found")
        return

    content = output_path.read_text(encoding="utf-8")

    # Check if section already exists
    section_start_marker = "## Spell Invocation Guidelines for AI Assistants"
    section_end_marker = "## Your Quest"

    if section_start_marker in content:
        # Replace existing section
        print(f"  Replacing existing spell invocation section...")

        # Find the section
        start_idx = content.find(section_start_marker)
        end_idx = content.find(section_end_marker, start_idx)

        if end_idx == -1:
            # No end marker found, append to end
            new_content = content[:start_idx] + section_content + "\n\n" + content[end_idx:]
        else:
            # Replace between markers
            new_content = content[:start_idx] + section_content + "\n\n" + content[end_idx:]
    else:
        # Insert new section before "## Your Quest"
        print(f"  Inserting new spell invocation section...")

        if section_end_marker in content:
            idx = content.find(section_end_marker)
            new_content = content[:idx] + section_content + "\n\n" + content[idx:]
        else:
            new_content = content + "\n\n" + section_content

    output_path.write_text(new_content, encoding="utf-8")
    print(f"  ✓ {output_path} updated")


def main():
    parser = argparse.ArgumentParser(
        description="Generate spell invocation documentation from SPELL_METADATA"
    )
    parser.add_argument(
        "--spells-dir",
        default="spells",
        help="Path to spells directory (default: spells)"
    )
    parser.add_argument(
        "--output-dir",
        default=".",
        help="Path to output directory (default: current directory)"
    )
    parser.add_argument(
        "--skip-invocation-guide",
        action="store_true",
        help="Skip generating SPELL_INVOCATION.md"
    )
    parser.add_argument(
        "--skip-ai-craft-update",
        action="store_true",
        help="Skip updating AI_CRAFT_SPELLBOOK.md"
    )

    args = parser.parse_args()

    spells_dir = Path(args.spells_dir)
    output_dir = Path(args.output_dir)

    if not spells_dir.exists():
        print(f"✗ Spells directory not found: {spells_dir}")
        sys.exit(1)

    # Scan spells
    metadata_list = scan_spells(spells_dir)

    if not metadata_list:
        print("\n✗ No spell metadata found!")
        print("  Ensure all spells have SPELL_METADATA dict defined.")
        sys.exit(1)

    print(f"\n✓ Extracted metadata from {len(metadata_list)} spells")

    # Generate SPELL_INVOCATION.md
    if not args.skip_invocation_guide:
        print("\nGenerating SPELL_INVOCATION.md...")
        guide_content = generate_spell_invocation_guide(metadata_list)

        guide_path = output_dir / "SPELL_INVOCATION.md"
        guide_path.write_text(guide_content, encoding="utf-8")
        print(f"  ✓ Generated: {guide_path}")

    # Update AI_CRAFT_SPELLBOOK.md
    if not args.skip_ai_craft_update:
        print("\nUpdating AI_CRAFT_SPELLBOOK.md...")
        section_content = generate_ai_craft_spellbook_section(metadata_list)

        ai_craft_path = output_dir / "AI_CRAFT_SPELLBOOK.md"
        update_ai_craft_spellbook(section_content, ai_craft_path)
        print(f"  ✓ Updated: {ai_craft_path}")

    print("\n✓ Documentation generation complete!")


if __name__ == "__main__":
    main()
