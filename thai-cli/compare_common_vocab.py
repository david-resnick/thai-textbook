#!/usr/bin/env python3
import json
import urllib.request
import csv
import os
from datetime import datetime

ANKI_CONNECT_URL = "http://localhost:8765"

def invoke(action, **params):
    data = json.dumps({"action": action, "version": 6, "params": params}).encode('utf-8')
    try:
        req = urllib.request.Request(ANKI_CONNECT_URL, data=data, method='POST')
        req.add_header('Content-Type', 'application/json')
        with urllib.request.urlopen(req, timeout=30) as response:
            return json.loads(response.read().decode('utf-8'))
    except Exception as e:
        return {"error": str(e)}

def main():
    common_file = "freq-4000-Thai Frequency Dictionary (Jørgen Nilsen) dump.csv"
    deck_name = "Thai::vocab"
    
    script_name = os.path.basename(__file__)
    output_dir = os.path.splitext(script_name)[0]
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"Created directory: {output_dir}")

    print(f"[{datetime.now()}] Starting comparison with Nilsen 4000...")

    try:
        common_words = []
        with open(common_file, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                word = row['Front'].strip()
                if word:
                    common_words.append(word)
    except FileNotFoundError:
        print(f"Error: '{common_file}' not found.")
        return
    except KeyError:
        print(f"Error: Could not find 'Front' column in {common_file}")
        return
    
    common_set = set(common_words)
    print(f"Loaded {len(common_words)} common words from Nilsen list.")

    print(f"Fetching notes from '{deck_name}'...")
    res = invoke("findNotes", query=f'deck:"{deck_name}"')
    note_ids = res.get("result", [])
    
    if not note_ids:
        print(f"No notes found in {deck_name}.")
        return

    notes_info = invoke("notesInfo", notes=note_ids).get("result", [])
    
    anki_vocab = []
    for note in notes_info:
        fields = note.get('fields', {})
        val = fields.get('Front', {}).get('value') or fields.get('Thai', {}).get('value', '')
        front = val.strip().strip('\'"')
        if front:
            anki_vocab.append(front)
            
    anki_set = set(anki_vocab)
    print(f"Found {len(anki_vocab)} notes in Anki vocab deck.")

    common_out = os.path.join(output_dir, "nilsen_vs_anki.csv")
    print(f"Generating {common_out}...")
    common_in_anki_count = 0
    with open(common_out, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Word", "In Anki?"])
        for word in common_words:
            is_in_anki = word in anki_set
            if is_in_anki:
                common_in_anki_count += 1
            writer.writerow([word, is_in_anki])

    anki_out = os.path.join(output_dir, "anki_vs_nilsen.csv")
    print(f"Generating {anki_out}...")
    anki_in_common_count = 0
    with open(anki_out, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Anki Word", "In Nilsen List?"])
        for word in anki_vocab:
            is_in_common = word in common_set
            if is_in_common:
                anki_in_common_count += 1
            writer.writerow([word, is_in_common])

    total_common = len(common_words)
    total_anki = len(anki_vocab)
    
    stats_lines = [
        "Comparison Statistics (Nilsen 4000):",
        "-" * 60,
        f"Generated on: {datetime.now()}",
        "",
        f"NILSEN LIST SUMMARY (Source: {common_file})",
        f"  Total words in common list: {total_common}",
        f"  Words present in Anki:      {common_in_anki_count} ({common_in_anki_count/total_common:.1%})",
        f"  Words missing from Anki:    {total_common - common_in_anki_count} ({(total_common - common_in_anki_count)/total_common:.1%})",
        "",
        f"ANKI DECK SUMMARY (Deck: {deck_name})",
        f"  Total notes in Anki deck:   {total_anki}",
        f"  Words found in Nilsen list: {anki_in_common_count} ({anki_in_common_count/total_anki:.1%})",
        f"  Words NOT in Nilsen list:   {total_anki - anki_in_common_count} ({(total_anki - anki_in_common_count)/total_anki:.1%})",
        "-" * 60
    ]
    
    stats_text = "\n".join(stats_lines)
    print(f"\n{stats_text}")
    
    stats_out = os.path.join(output_dir, "nilsen_statistics.txt")
    print(f"Saving statistics to {stats_out}...")
    with open(stats_out, "w", encoding="utf-8") as f:
        f.write(stats_text)

    print(f"Done! Files created in '{output_dir}/'")

if __name__ == "__main__":
    main()
