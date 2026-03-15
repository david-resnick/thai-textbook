---
name: thai-refresh-vocab
description: Automated workflow to refresh the Thai Anki collection export and identify missing Nilsen frequency words. Use when the user wants to sync the local analysis data with the current Anki state and see new words to add.
---

# Thai Refresh Vocab

This skill automates the two-step process of synchronizing the local analysis data with Anki and identifying the next batch of missing words from the Nilsen Frequency Dictionary.

## Workflow

1. **Dump Latest Anki State**: Execute `./thai dump` to create a fresh CSV export of the current Anki collection (excluding the `~Freq 4000` deck).
2. **Identify Missing Words**: Execute `./thai nilsen-missing` to compare the latest export against the Nilsen Frequency Dictionary and generate a report of the first 50 missing words.

## Execution

To perform the refresh, run the following commands in sequence:

```bash
./thai dump && ./thai nilsen-missing
```

The resulting report will be saved in the `nilsen_missing/` directory as a timestamped CSV file.
