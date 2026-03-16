# Thai Language Learning Workflow

This project integrates Gemini CLI, NotebookLM, and Anki to create a streamlined environment for Thai language acquisition.

## System Components

### 1. NotebookLM (The "Textbook")
The core curriculum is hosted in NotebookLM. 
- **Notebook ID:** `a3d415fa-063a-4c51-bc1a-bd7c272e6cb7`
- **Title:** The Architecture of Thai Fluency: A Comprehensive Curriculum Guide
- **Access:** Managed via the `nlm` (NotebookLM MCP) tool. You can query specific chapters or concepts directly from the CLI.

### 2. Anki (The "Memory")
Active recall is handled by Anki.
- **Integration:** The `anki-mcp` server allows Gemini CLI to create, search, and update cards.
- **Usage:** After studying a concept from the NotebookLM "textbook," new vocabulary or grammar rules should be synchronized to your Anki decks.

### 3. Gemini CLI (The "Tutor")
Gemini CLI acts as the orchestrator. You can use it to:
- Summarize or explain sections of the NotebookLM textbook.
- Generate example sentences in Thai based on textbook content.
- Automatically format and push new cards to Anki using the information retrieved from NotebookLM.

## Common Commands

### NotebookLM Interaction
To query your curriculum:
```bash
# Use nlm tools through Gemini CLI to query the notebook
nlm query notebook a3d415fa-063a-4c51-bc1a-bd7c272e6cb7 "Explain Thai tones"
```

### Anki Interaction
To check your learning progress or add cards:
```bash
# Gemini can use anki-mcp tools to:
# - anki_get_deck_names
# - anki_add_note
```

## Setup Verification
Ensure both MCP servers are active in your `~/.gemini/settings.json`:
- `anki-mcp`: For local Anki-Connect integration (`http://localhost:8765`).
- `notebooklm`: For interaction with your curriculum via `/Users/dresnick/.local/bin/notebooklm-mcp`.

*Last Updated: 2026-03-07*
