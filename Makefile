.PHONY: update-docs help

update-docs:
	python tools/update_spell_docs.py

help:
	@echo "Available targets:"
	@echo "  update-docs    - Generate spell invocation documentation"
	@echo "  help           - Show this help message"
