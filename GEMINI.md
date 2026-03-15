# Thai Textbook - Anki Management Guidelines

This project contains a unified CLI toolkit for managing a large Anki collection of Thai language materials. All utilities are accessible via the `thai` command.

## Usage

Run the CLI from the project root:
```bash
./thai <command> [args]
```
Use `./thai --help` to see all available categories and subcommands.

## Command Categories

### Anki Sync & Export
- `dump`: Exports all Anki notes to a timestamped CSV. Uses multithreading for speed.
- `dump-freq`: Exports the `Freq 4000` deck to CSV, stripping sound tags and HTML.

### Duplicate Auditing
- `audit-dupes`: Identifies duplicate entries in the `Front` field across different note types (excluding `Freq 4000`).
- `process-dupes`: Interactive utility to review duplicates and flag them with a `delete-me` tag.

### Vocab Analysis
- `nilsen-missing`: Finds words from the Jørgen Nilsen dictionary missing from Anki.
- `fetch-common`: Downloads the top 5000 common Thai words.
- `compare-vocab`: Cross-references Anki vocab with common word lists.
- `translate-missing`: Translates missing words using Google Translate.

### Quote Handling
- `classify-quotes`: Analyzes quotation styles in specific decks.
- `quote-stats`: Provides detailed quotation statistics.
- `strip-quotes`: Removes nested or unnecessary outer quotes across all decks.
- `unify-quotes`: Unifies quotation styles (e.g., standardizing double quotes in phrases).

## Workflow Mandates
- **Field Cleanliness:** The `Front` field should generally be plain text. Stripping HTML and decoding entities is mandatory for new processing.
- **Vocab Formatting:** Notes in `Thai::vocab` must **NOT** have outer quotation marks.
- **Phrase Formatting:** Notes in `Thai::~phrases` must be surrounded by standard double quotes (e.g., `"phrase"`). 
- **AnkiConnect:** Anki must be running locally with the AnkiConnect add-on enabled on port 8765.
- **GitHub Account:** Always use the `david-resnick` account for git operations in this repository. Use `gh auth switch --hostname github.com --user david-resnick` if needed.

## Script Standards
- **Location:** All logic resides in the `thai-cli/` directory.
- **Interpreter:** All Python scripts must start with `#!/usr/bin/env python3`.
- **Permissions:** Scripts must be executable (`chmod +x`).

## Project Structure
- `thai`: Symbolic link to the CLI entry point (`thai-cli/main.py`).
- `thai-cli/`: Contains all utility scripts and the dispatcher.
- `dump_anki/`: Default output directory for Anki exports.
- `cross_model_dupes/`: Output directory for duplicate reports.
- `nilsen_missing/`: Output directory for missing frequency word reports.
- `compare_common_vocab/`: Data and results for vocab gap analysis.
