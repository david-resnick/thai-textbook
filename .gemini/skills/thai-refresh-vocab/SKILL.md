---
name: thai-refresh-vocab
description: Automated workflow to refresh the Thai Anki collection export, identify missing Nilsen frequency words, and generate Natural Thai example sentences.
---

# Thai Refresh Vocab

This skill automates the process of synchronizing local analysis data with Anki, identifying the next batch of missing words from the Nilsen Frequency Dictionary, and generating high-quality sentences for study.

## Workflow

1.  **Sync & Dump**: Run `./thai dump` to export the latest Anki collection state.
2.  **Identify Missing Words**: Run `./thai nilsen-missing` to find the first 50 words missing from your collection.
3.  **Generate Sentences**: Run `./thai generate-sentences <path_to_missing_words_csv>` to produce an Anki-importable CSV file of sentences.

## Sentence Requirements

When generating sentences, the agent must adhere to these strict standards:
- **Style**: Natural Thai (Zero Anaphora, avoid repetitive pronouns, neutral/informal tone without `ครับ`).
- **Persona**: Male speaker (use `ผม` to establish gender, but **do NOT** include the polite particle `ครับ`).
- **Vocabulary**: Prioritize words already in the `Thai::vocab` deck (use `extract_known_vocab.py` to index).
- **Formatting**: CSV with header `Front,Back,Audio,Notes`.
- **Field Cleanliness**: 
    - `Front`: Thai sentence surrounded by triple double-quotes (e.g., `"""ผมสบายดี"""`).
    - `Back`: English translation.
    - `Notes`: `Thai Word (English Translation)`.
    - `Audio`: Empty.

## Execution

To perform the full refresh and generation cycle:

```bash
./thai dump && ./thai nilsen-missing && ./thai generate-sentences nilsen_missing/YYYYMMDD_HHMMSS_nilsen_missing.csv
```

The final sentences file will be saved in `nilsen_missing/` with a `YYYYMMDD_HHMMSS_nilsen_sentences.csv` format.
