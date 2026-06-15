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
    sentences_file = 'nilsen_missing/nilsen_sentences_20260511_101211.csv'
    source_words_file = 'nilsen_missing/nilsen_missing_20260511_101211.csv'

    anki_vocab = set()
    with open(anki_export, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Check ALL fields for Thai text
            for val in row.values():
                cleaned = clean_thai(val)
                for w in cleaned.split():
                    if len(w) > 1: anki_vocab.add(w)

    with open(source_words_file, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            w = clean_thai(row.get('Front', ''))
            if w: anki_vocab.add(w)

    # Common particles
    anki_vocab.update(["ครับ", "ที่", "และ", "คือ", "มี", "ไป", "จะ", "มา", "ใน", "ให้", "ของ", "การ", "ความ", "มาก", "ก้", "ก็", "ช่วง", "แล้ว", "กำลัง"])

    sentences = []
    with open(sentences_file, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            sentences.append(row.get('Front', ''))

    sorted_anki = sorted(list(anki_vocab), key=len, reverse=True)

    potential_missing = set()
    for sentence in sentences:
        working = "".join(re.findall(r'[\u0e00-\u0e7f]+', sentence))
        
        for word in sorted_anki:
            if word in working:
                working = working.replace(word, " ")
        
        chunks = working.split()
        for chunk in chunks:
            if len(chunk) > 1:
                potential_missing.add(chunk)

    if not potential_missing:
        print("No significant missing words found.")
    else:
        print("Potential missing segments/words:")
        for item in sorted(list(potential_missing)):
            print(item)

if __name__ == "__main__":
    main()
