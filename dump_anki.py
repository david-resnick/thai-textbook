#!/usr/bin/env python3
import json
import csv
import urllib.request
import urllib.error
import concurrent.futures
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

def get_notes_info(note_ids):
    response = invoke("notesInfo", notes=note_ids)
    if response.get("error"):
        print(f"Error fetching batch: {response['error']}")
        return []
    return response.get("result", [])

def main():
    print(f"[{datetime.now()}] Starting Anki export...")
    
    # 1. Get Note-to-Deck mapping
    print("Building deck mapping...")
    res_decks = invoke("deckNames")
    if res_decks.get("error"):
        print(f"Failed to get decks: {res_decks['error']}")
        return
    
    deck_names = res_decks.get("result", [])
    note_id_to_deck = {}
    for deck in deck_names:
        ids = invoke("findNotes", query=f'deck:"{deck}"').get("result", [])
        for nid in ids:
            note_id_to_deck[nid] = deck
    
    # 2. Get all note IDs
    print("Finding all notes...")
    res = invoke("findNotes", query="*")
    if res.get("error"):
        print(f"Failed to find notes: {res['error']}")
        return
        
    note_ids = res.get("result", [])
    total_notes = len(note_ids)
    print(f"Found {total_notes} notes.")

    if not note_ids:
        print("No notes found to export.")
        return

    # 3. Batch and Fetch with Multithreading
    batch_size = 100
    batches = [note_ids[i:i + batch_size] for i in range(0, total_notes, batch_size)]
    
    all_notes = []
    print(f"Fetching details in {len(batches)} batches using multithreading...")
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
        future_to_batch = {executor.submit(get_notes_info, batch): batch for batch in batches}
        for i, future in enumerate(concurrent.futures.as_completed(future_to_batch)):
            batch_result = future.result()
            all_notes.extend(batch_result)
            print(f"Progress: {len(all_notes)}/{total_notes} (Batch {i+1}/{len(batches)})")

    print(f"[{datetime.now()}] Data retrieval complete.")

    # 4. Dynamically identify all unique fields
    all_fields = set()
    for note in all_notes:
        if note and 'fields' in note:
            all_fields.update(note['fields'].keys())
    
    to_drop = {'Thai name to English name card', 'Thai name to everything card', 'Transcription'}
    primary_fields = ['Front', 'Back']
    remaining_fields = sorted([f for f in all_fields if f not in to_drop and f not in primary_fields])
    
    # Add new metadata columns
    headers = primary_fields + ['vocab?', 'deckName', 'noteId', 'modelName', 'tags'] + remaining_fields
    
    # 5. Write to CSV
    script_name = os.path.basename(__file__)
    output_dir = os.path.splitext(script_name)[0]
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"Created directory: {output_dir}")

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = os.path.join(output_dir, f'anki_export_{timestamp}.csv')
    print(f"Writing to {output_file}...")
    
    try:
        with open(output_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=headers)
            writer.writeheader()
            
            for note in all_notes:
                if not note: continue
                nid = note.get('noteId')
                deck = note_id_to_deck.get(nid, '')
                
                row = {
                    'noteId': nid,
                    'modelName': note.get('modelName', ''),
                    'tags': ' '.join(note.get('tags', [])),
                    'deckName': deck,
                    'vocab?': str(deck.endswith('::vocab')).upper()
                }
                
                metadata_cols = {'noteId', 'modelName', 'tags', 'deckName', 'vocab?'}
                for field in headers:
                    if field not in metadata_cols:
                        row[field] = note.get('fields', {}).get(field, {}).get('value', '')
                
                writer.writerow(row)
        print(f"Done! Successfully exported {len(all_notes)} notes to {output_file}")
    except Exception as e:
        print(f"Error writing CSV: {e}")

if __name__ == "__main__":
    main()
