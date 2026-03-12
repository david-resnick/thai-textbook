# Thai Textbook - Anki Management Guidelines

This project contains utility scripts for managing a large Anki collection of Thai language materials.

## Custom Scripts

### 1. `dump_anki.py`
**Purpose:** Exports all Anki notes to a timestamped CSV file (`anki_export_YYYYMMDD_HHMMSS.csv`).
- **Features:**
    - Uses multithreading for fast retrieval from AnkiConnect.
    - **Column Order:** `Front`, `Back`, `vocab?`, `deckName`, `noteId`, `modelName`, `tags`, followed by all other dynamic fields.
    - **`vocab?` Column:** A boolean column (TRUE/FALSE) indicating if the deck name ends with `::vocab`.
    - **Exclusions:** Automatically drops "Thai name to English name card", "Thai name to everything card", and "Transcription" columns.

### 2. `clean_anki_front.py`
**Purpose:** Performs a surgical cleanup of the `Front` field for all notes.
- **Rules:**
    - Strips all HTML tags (e.g., `<b>`, `<div>`, `<span>`).
    - Decodes common HTML entities.
    - **Phrase Formatting:** For notes in decks ending with `::phrases` or `::~phrases`, the content is wrapped in single quotes (e.g., `'phrase'`). It prevents double-wrapping if quotes are already present.

### 3. `list_vocab_quotes.py`
**Purpose:** Audits the `Thai::vocab` deck for any notes that still contain quotes in the `Front` field.

## Workflow Mandates
- **Field Cleanliness:** The `Front` field should generally be plain text unless formatting is explicitly required.
- **Phrase Consistency:** Phrases must be wrapped in single quotes when stored in phrase-specific sub-decks.
- **Exporting:** Always use `dump_anki.py` to ensure the CSV structure matches the expected analysis format (Front/Back first).
- **AnkiConnect:** These scripts assume Anki is running locally with the AnkiConnect add-on enabled on port 8765.

## Script Standards
- **Interpreter:** All Python scripts must start with `#!/usr/bin/env python3`.
- **Permissions:** All scripts must be marked as executable (`chmod +x`).
- **Dependencies:** Prefer standard libraries (like `urllib`) over external ones (like `requests`) to ensure portability.

## Project Structure
- `export_notes.py`: (Legacy) Initial single-threaded export script.
- `dump_anki.py`: Current multithreaded export script.
- `clean_anki_front.py`: Main cleanup utility.
- `list_vocab_quotes.py`: Audit utility.
- `move_vocab_to_phrases.py`: Utility to move quoted vocab notes to the phrases deck.
- `get_thai_5000.py`: Downloads the top 5000 most common Thai words.
- `compare_common_vocab.py`: Cross-references the `Thai::vocab` deck with the common words list.
- `classify_quotes.py`: Utility to analyze quotation styles. Accepts an optional deck name argument (default: `Thai::phrases`).
- `unify_quotes.py`: Utility to unify quotation styles (replaces smart single quotes with standard double quotes).
- `unify_phrases_double_quotes.py`: Utility to unify quotation styles in Thai::~phrases (replaces single quotes with standard double quotes).
