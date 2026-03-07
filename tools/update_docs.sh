#!/bin/bash

# AI Craft Spellbook - Update Documentation Script
# This script generates spell invocation documentation from SPELL_METADATA

cd "$(dirname "$0")/.."
python tools/update_spell_docs.py "$@"
