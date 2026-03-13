#!/usr/bin/env python3
import json
import urllib.request
import sys
from collections import Counter

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

def classify_text(text):
    if not text:
        return "Empty"
    
    quotes = {
        'std_double': ('"', '"'),
        'std_single': ("'", "'"),
        'smart_double': ('“', '”'),
        'smart_single': ('‘', '’'),
    }
    
    results = []
    
    surrounded = False
    for q_type, (start, end) in quotes.items():
        if text.startswith(start) and text.endswith(end):
            results.append(f"Surrounded by {q_type}")
            surrounded = True
            break
            
    if not surrounded:
        found_internal = []
        for q_type, (start, end) in quotes.items():
            if start in text or end in text:
                found_internal.append(q_type)
        
        if found_internal:
            results.append(f"Internal {', '.join(found_internal)}")
        else:
            results.append("No Quotes")
            
    return " | ".join(results)

def main():
    deck_name = sys.argv[1] if len(sys.argv) > 1 else "Thai::phrases"
    deck_query = f'deck:"{deck_name}*"'
    
    res = invoke("findNotes", query=deck_query)
    note_ids = res.get("result", [])
    
    if not note_ids:
        print(f"No notes found for query: {deck_query}")
        return

    notes_info = invoke("notesInfo", notes=note_ids).get("result", [])
    
    stats = Counter()
    examples = {}

    for note in notes_info:
        fields = note.get('fields', {})
        front_val = fields.get('Front', {}).get('value') or fields.get('Thai', {}).get('value', '')
        
        classification = classify_text(front_val)
        stats[classification] += 1
        
        if classification not in examples and classification != "No Quotes":
            examples[classification] = front_val

    print(f"\nQuote Classification Report for {deck_name}:")
    print("-" * 60)
    for classification, count in stats.most_common():
        print(f"{count:4} : {classification}")
        if classification in examples:
            print(f"       Ex: {examples[classification]}")
    print("-" * 60)
    print(f"Total notes analyzed: {len(note_ids)}")

if __name__ == "__main__":
    main()
