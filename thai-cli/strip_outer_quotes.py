#!/usr/bin/env python3
import json
import urllib.request
import sys
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

def strip_all_outer_quotes(text):
    if not text:
        return text
    
    # Check if the text is surrounded by standard double quotes
    if text.startswith('"') and text.endswith('"') and len(text) > 2:
        content = text[1:-1]
        smart_quotes = '“”‘’'
        # Check if the content inside the double quotes is ALSO surrounded by smart quotes
        if len(content) > 1 and content[0] in smart_quotes and content[-1] in smart_quotes:
            # Strip the inner smart quotes but keep the outer double quotes
            return f'"{content[1:-1]}"'
            
    return text.strip()

def main():
    dry_run = "--commit" not in sys.argv
    if dry_run:
        print("DRY RUN MODE: No changes will be saved. Use '--commit' to actually update Anki.")
    else:
        print("COMMIT MODE: Changes will be saved to Anki.")

    print(f"[{datetime.now()}] Starting outer quote stripping cleanup...")
    res = invoke("findNotes", query="*")
    note_ids = res.get("result", [])
    print(f"Checking {len(note_ids)} notes...")

    batch_size = 100
    change_count = 0
    
    for i in range(0, len(note_ids), batch_size):
        batch = note_ids[i:i + batch_size]
        notes_info = invoke("notesInfo", notes=batch).get("result", [])
        
        for note in notes_info:
            if not note: continue
            nid = note['noteId']
            fields = note.get('fields', {})
            field_name = 'Front' if 'Front' in fields else 'Thai' if 'Thai' in fields else None
            if not field_name:
                continue
                
            old_val = fields[field_name]['value']
            new_val = strip_all_outer_quotes(old_val)
            
            if new_val != old_val:
                print(f"[{'DRY' if dry_run else 'COMMIT'}] {nid}: {old_val} -> {new_val}")
                change_count += 1
                
                if not dry_run:
                    invoke("updateNoteFields", note={
                        "id": nid,
                        "fields": {
                            field_name: new_val
                        }
                    })

    print(f"Done! {change_count} notes identified for changes.")

if __name__ == "__main__":
    main()
