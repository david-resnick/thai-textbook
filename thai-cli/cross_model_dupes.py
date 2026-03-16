#!/usr/bin/env python3
import json
import urllib.request
import csv
import os
import re
from collections import defaultdict
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

def clean_text(text):
    if not text: return ""
    # Strip HTML and Sound tags
    text = re.sub(r'<.*?>', '', text)
    text = re.sub(r'\[sound:.*?\]', '', text)
    # Strip quotes and extra space
    text = text.strip().strip('\'"“”‘’').strip()
    return text

def main():
    print(f"[{datetime.now()}] Starting cross-model duplicate audit (excluding ~Freq 4000)...")
    
    res = invoke("findNotes", query='-deck:"~Freq 4000"')
    note_ids = res.get("result", [])
    if not note_ids:
        print("No notes found.")
        return
        
    print(f"Fetching details for {len(note_ids)} notes...")
    
    text_to_notes = defaultdict(list)
    batch_size = 500
    
    for i in range(0, len(note_ids), batch_size):
        batch = note_ids[i:i + batch_size]
        notes_info = invoke("notesInfo", notes=batch).get("result", [])
        
        for note in notes_info:
            if not note or 'fields' not in note: continue
            fields = note['fields']
            
            # Use specific known names or fallback to first field
            front_raw = ""
            if 'Front' in fields:
                front_raw = fields['Front']['value']
            elif 'Thai' in fields:
                front_raw = fields['Thai']['value']
            elif 'Thai name' in fields:
                front_raw = fields['Thai name']['value']
            else:
                first_key = list(fields.keys())[0] if fields else None
                if first_key:
                    front_raw = fields[first_key]['value']
            
            cleaned = clean_text(front_raw)
            if cleaned:
                text_to_notes[cleaned].append({
                    'noteId': note['noteId'],
                    'model': note['modelName']
                })

    duplicates = {text: notes for text, notes in text_to_notes.items() if len(notes) > 1}
    
    script_name = os.path.basename(__file__)
    output_dir = os.path.splitext(script_name)[0]
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = os.path.join(output_dir, f"cross_model_dupes_{timestamp}.csv")
    
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["Cleaned Text", "Note Count", "Models Involved", "Note IDs"])
        
        # Sort by most frequent duplicates
        for text, notes in sorted(duplicates.items(), key=lambda x: len(x[1]), reverse=True):
            models = ", ".join(sorted(list(set(n['model'] for n in notes))))
            ids = ", ".join(str(n['noteId']) for n in notes)
            writer.writerow([text, len(notes), models, ids])

    print(f"\nDone! Found {len(duplicates)} text entries with duplicates.")
    print(f"Report saved to: {output_file}")

if __name__ == "__main__":
    main()
