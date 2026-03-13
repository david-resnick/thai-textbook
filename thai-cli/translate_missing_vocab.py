#!/usr/bin/env python3
import csv
import json
import os
import sys
import urllib.request
import urllib.parse
from datetime import datetime
import time

def google_translate(text):
    """Uses the free Google Translate API endpoint."""
    url = f"https://translate.googleapis.com/translate_a/single?client=gtx&sl=th&tl=en&dt=t&q={urllib.parse.quote(text)}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as response:
            res_data = json.loads(response.read().decode('utf-8'))
            return res_data[0][0][0]
    except Exception as e:
        return f"Error: {str(e)}"

def main():
    N = int(sys.argv[1]) if len(sys.argv) > 1 else 50
    input_file = "compare_common_vocab/common_vs_anki.csv"
    
    script_name = os.path.basename(__file__)
    output_dir = os.path.splitext(script_name)[0]
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    print(f"[{datetime.now()}] Starting translation of missing words...")
    
    if not os.path.exists(input_file):
        print(f"Error: {input_file} not found. Run compare_common_vocab.py first.")
        return

    missing_words = []
    with open(input_file, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row['In Anki?'] == 'False':
                missing_words.append(row['Word'])
            if len(missing_words) >= N:
                break

    if not missing_words:
        print("No missing words found to translate.")
        return

    print(f"Found {len(missing_words)} words to translate.")

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = os.path.join(output_dir, f"missing_translated_{timestamp}.csv")
    
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["Front", "Back"])
        
        for i, word in enumerate(missing_words):
            print(f"[{i+1}/{len(missing_words)}] Translating '{word}'...")
            translation = google_translate(word)
            writer.writerow([word, translation])
            time.sleep(0.5)

    print(f"\nDone! Successfully translated {len(missing_words)} words.")
    print(f"Output: {output_file}")

if __name__ == "__main__":
    main()
