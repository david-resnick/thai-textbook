#!/usr/bin/env python3
import json
import csv
import urllib.request
import re
import os
from datetime import datetime

ANKI_CONNECT_URL = "http://localhost:8765"

def invoke(action, **params):
    data = json.dumps({"action": action, "version": 6, "params": params}).encode('utf-8')
    try:
        req = urllib.request.Request(ANKI_CONNECT_URL, data=data, method='POST')
        req.add_header('Content-Type', 'application/json')
        with urllib.request.urlopen(req, timeout=60) as response:
            return json.loads(response.read().decode('utf-8'))
    except Exception as e:
        return {"error": str(e)}

def extract_and_clean_front(text):
    if not text:
        return "", ""
    # Extract sound tags [sound:...]
    sound_tags = re.findall(r'\[sound:.*?\]', text)
    sound = " ".join(sound_tags)
    # Remove sound tags from text
    text = re.sub(r'\[sound:.*?\]', '', text)
    # Remove HTML tags
    text = re.sub(r'<.*?>', '', text)
    # Decode basic entities
    text = text.replace('&nbsp;', ' ').replace('&quot;', '"').replace('&apos;', "'")
    return text.strip(), sound

def main():
    deck_name = "Freq 4000"
    script_name = os.path.basename(__file__)
    output_dir = os.path.splitext(script_name)[0]
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"Created directory: {output_dir}")

    print(f"[{datetime.now()}] Starting export of deck '{deck_name}'...")

    res = invoke("findNotes", query=f'deck:"{deck_name}"')
    note_ids = res.get("result", [])
    if not note_ids:
        print(f"No notes found in deck '{deck_name}'.")
        return
    
    print(f"Found {len(note_ids)} notes. Fetching details...")
    notes_info = invoke("notesInfo", notes=note_ids).get("result", [])

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = os.path.join(output_dir, f"export_freq4000_{timestamp}.csv")
    
    all_fields = set()
    for note in notes_info:
        if note and 'fields' in note:
            all_fields.update(note['fields'].keys())
    
    # Ensure Front, Back, and Audio are first
    primary = ['Front', 'Back', 'Audio']
    other_fields = sorted([f for f in all_fields if f not in primary])
    headers = primary + other_fields + ['noteId', 'tags']

    print(f"Writing to {output_file}...")
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        
        for note in notes_info:
            if not note: continue
            
            row = {
                'noteId': note.get('noteId'),
                'tags': ' '.join(note.get('tags', []))
            }
            
            cleaned_front, extracted_audio = extract_and_clean_front(note['fields'].get('Front', {}).get('value', ''))
            
            for field_name in all_fields:
                val = note['fields'].get(field_name, {}).get('value', '')
                if field_name == 'Front':
                    val = cleaned_front
                row[field_name] = val
            
            # Explicitly set Audio field
            row['Audio'] = extracted_audio
                
            writer.writerow(row)

    print(f"Done! Successfully exported {len(notes_info)} notes to {output_file}")

if __name__ == "__main__":
    main()
