#!/usr/bin/env python3
import csv
import json
import urllib.request
import sys
import os
import glob

def invoke(action, **params):
    request = {"action": action, "version": 6, "params": params}
    try:
        response = urllib.request.urlopen(
            urllib.request.Request("http://localhost:8765", json.dumps(request).encode("utf-8"))
        ).read()
    except Exception as e:
        print(f"Error connecting to AnkiConnect: {e}")
        print("Make sure Anki is running and AnkiConnect is installed.")
        sys.exit(1)
        
    res = json.loads(response)
    if res.get("error"):
        raise Exception(res["error"])
    return res["result"]

def main():
    csv_dir = "cross_model_dupes"
    csv_files = glob.glob(os.path.join(csv_dir, "*.csv"))
    
    if not csv_files:
        print(f"Error: No CSV files found in {csv_dir}")
        return

    # Find the most recent file
    csv_path = max(csv_files, key=os.path.getmtime)
    print(f"Processing most recent file: {csv_path}")
    
    try:
        with open(csv_path, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                text = row['Cleaned Text']
                note_ids = [nid.strip() for nid in row['Note IDs'].split(',')]
                
                print(f"\n{'='*80}")
                print(f"DUPLICATE GROUP: {text} ({len(note_ids)} notes)")
                print(f"{'='*80}")
                
                try:
                    notes_info = invoke("notesInfo", notes=[int(nid) for nid in note_ids])
                    
                    # Notes don't have decks, cards do. Fetch deck from the first card of each note.
                    card_ids = [info['cards'][0] for info in notes_info if info['cards']]
                    cards_info = invoke("cardsInfo", cards=card_ids)
                    
                    # Map noteId to deckName
                    nid_to_deck = {str(c['note']): c['deckName'] for c in cards_info}
                    
                    # Filter out Freq 4000 notes
                    visible_notes = [info for info in notes_info if nid_to_deck.get(str(info['noteId'])) != "Freq 4000"]
                except Exception as e:
                    print(f"Error fetching notes/cards info for {note_ids}: {e}")
                    continue

                if not visible_notes:
                    continue

                for i, info in enumerate(visible_notes, 1):
                    nid_str = str(info['noteId'])
                    deck = nid_to_deck.get(nid_str, "Unknown Deck")
                    print(f"\n[{i}] Note ID: {info['noteId']} | Deck: {deck} | Model: {info['modelName']}")
                    print(f"    Tags: {', '.join(info['tags'])}")
                    # Show all fields
                    for field_name, field_data in info['fields'].items():
                        val = field_data['value'].replace('<br>', '\n').replace('<div>', '\n').replace('</div>', '').strip()
                        if val:
                            # Truncate very long fields if necessary, but here we want full fields
                            print(f"    {field_name}: {val}")

                if len(visible_notes) > 2:
                    prompt = f"Select note(s) to flag (1-{len(visible_notes)}, comma-separated) or <Enter> to skip: "
                elif len(visible_notes) == 2:
                    prompt = "Select note to flag (1 or 2) or <Enter> to skip: "
                else:
                    prompt = "Select note to flag (1) or <Enter> to skip: "
                
                choice = input(f"\n{prompt}").strip()
                
                if not choice:
                    continue

                # Handle multiple selections like "1, 2" or "1 2"
                selections = [s.strip() for s in choice.replace(' ', ',').split(',') if s.strip()]
                
                for s in selections:
                    if s.isdigit():
                        idx = int(s) - 1
                        if 0 <= idx < len(visible_notes):
                            nid = int(visible_notes[idx]['noteId'])
                            invoke("addTags", notes=[nid], tags="delete-me")
                            print(f"  >> Flagged note {nid} with 'delete-me'")
                        else:
                            print(f"  !! Invalid selection: {s}")
                    else:
                        print(f"  !! Invalid input: {s}")

    except FileNotFoundError:
        print(f"Error: Could not find {csv_path}")
    except KeyboardInterrupt:
        print("\nExiting...")
        sys.exit(0)

if __name__ == "__main__":
    main()
