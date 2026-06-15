#!/usr/bin/env python3
import csv
import os

def main():
    source_words_file = 'nilsen_missing/nilsen_missing_20260511_101211.csv'
    sentences_file = 'nilsen_missing/nilsen_sentences_20260511_101211.csv'
    temp_file = 'nilsen_missing/nilsen_sentences_temp.csv'

    # Load source words and translations in order
    vocab_entries = []
    with open(source_words_file, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Format: "Thai (English)"
            entry = f"{row['Front']} ({row['Back']})"
            vocab_entries.append(entry)

    # Read sentences and write back with modified Notes
    with open(sentences_file, mode='r', encoding='utf-8') as f_in, \
         open(temp_file, mode='w', encoding='utf-8', newline='') as f_out:
        
        reader = csv.DictReader(f_in)
        fieldnames = ['Front', 'Back', 'Audio', 'Notes']
        writer = csv.DictWriter(f_out, fieldnames=fieldnames)
        writer.writeheader()

        for i, row in enumerate(reader):
            if i < len(vocab_entries):
                row['Notes'] = vocab_entries[i]
            writer.writerow(row)

    # Replace original file with refined one
    os.replace(temp_file, sentences_file)
    print(f"Enhanced {sentences_file}: Notes now include Thai word and English translation.")

if __name__ == "__main__":
    main()
