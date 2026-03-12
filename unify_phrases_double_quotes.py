#!/usr/bin/env python3
import json
import urllib.request
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
    deck_query = 'deck:"Thai::~phrases*"'
    print(f"[{datetime.now()}] Finding notes in {deck_query}...")
    res = invoke("findNotes", query=deck_query)
    note_ids = res.get("result", [])
    
    if not note_ids:
        print("No notes found.")
        return

    print(f"Fetching details for {len(note_ids)} notes...")
    notes_info = invoke("notesInfo", notes=note_ids).get("result", [])
    
    updated_count = 0
    
    for note in notes_info:
        nid = note['noteId']
        fields = note.get('fields', {})
        
        field_name = 'Front' if 'Front' in fields else 'Thai' if 'Thai' in fields else None
        if not field_name:
            continue
            
        old_val = fields[field_name]['value']
        
        single_quotes = [
            ("'", "'"),
            ('‘', '’'),
        ]
        
        needs_update = False
        new_val = old_val
        
        for start, end in single_quotes:
            if old_val.startswith(start) and old_val.endswith(end):
                content = old_val[1:-1]
                new_val = f'"{content}"'
                needs_update = True
                break
        
        if needs_update and new_val != old_val:
            res = invoke("updateNoteFields", note={
                "id": nid,
                "fields": {
                    field_name: new_val
                }
            })
            if not res.get("error"):
                updated_count += 1
                if updated_count % 100 == 0:
                    print(f"Updated {updated_count} notes so far...")
            else:
                print(f"Error updating note {nid}: {res['error']}")

    print(f"Done! Successfully unified {updated_count} notes in {deck_query} to standard double quotes.")

if __name__ == "__main__":
    main()
