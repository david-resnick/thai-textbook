#!/usr/bin/env python3
import csv
import re

def clean_thai(text):
    if not text: return ""
    text = re.sub(r'<[^>]+>', '', text)
    found = re.findall(r'[\u0e00-\u0e7f]+', text)
    return " ".join(found)

def main():
    anki_export = 'dump_anki/anki_export_20260511_101211.csv'
    known_vocab = set()
    
    with open(anki_export, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            deck = row.get('deckName', '')
            if 'Thai::vocab' in deck:
                word = clean_thai(row.get('Front', ''))
                if word:
                    # Some entries might be multiple words, add them all
                    for w in word.split():
                        if len(w) > 1:
                            known_vocab.add(w)
                            
    # Save to a temporary file for the next step
    with open('nilsen_missing/known_vocab_list.txt', 'w', encoding='utf-8') as f:
        for word in sorted(list(known_vocab)):
            f.write(word + '\n')
            
    print(f"Extracted {len(known_vocab)} known words from Thai::vocab.")

if __name__ == "__main__":
    main()
