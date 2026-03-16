#!/usr/bin/env python3
"""Dump first 50 Nilsen freq-4000 words not in the latest Anki export."""
import csv
import glob
import os
from datetime import datetime

NILSEN_CSV = "dump_freq_4000/Thai Frequency Dictionary (Jørgen Nilsen) 4000 dump.csv"
ANKI_DIR = "dump_anki"
OUTPUT_DIR = "nilsen_missing"
TAG = "nilsen"
DECK = "Thai::vocab"
LIMIT = 50


def latest_anki_export():
    files = sorted(glob.glob(os.path.join(ANKI_DIR, "*.csv")))
    if not files:
        raise FileNotFoundError(f"No CSV files found in {ANKI_DIR}/")
    return files[-1]


def main():
    anki_file = latest_anki_export()
    print(f"Using Anki export: {anki_file}")

    anki_fronts = set()
    with open(anki_file, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            front = row.get("Front", "").strip()
            if front:
                anki_fronts.add(front)

    print(f"Loaded {len(anki_fronts)} fronts from Anki export.")

    missing = []
    with open(NILSEN_CSV, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if len(missing) >= LIMIT:
                break
            front = row.get("Front", "").strip()
            back = row.get("Back", "").strip()
            if front and front not in anki_fronts:
                audio = row.get("Audio", "").strip()
                missing.append({"Front": front, "Back": back, "Audio": audio, "tags": TAG})

    print(f"Found {len(missing)} missing words (limit {LIMIT}).")

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = os.path.join(OUTPUT_DIR, f"nilsen_missing_{timestamp}.csv")

    with open(output_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["Front", "Back", "Audio", "tags"])
        writer.writeheader()
        writer.writerows(missing)

    print(f"Written to {output_file}")


if __name__ == "__main__":
    main()
