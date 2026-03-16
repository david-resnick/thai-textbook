#!/usr/bin/env python3
import json
import urllib.request
from collections import Counter

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

def classify_outer_quotes(text):
    if not text: return "Empty"
    
    # Check for nested double wrapping specifically (e.g. "“text”")
    if text.startswith('"') and text.endswith('"') and len(text) > 4:
        inner = text[1:-1]
        if (inner.startswith('“') and inner.endswith('”')) or (inner.startswith('‘') and inner.endswith('’')):
            return "Nested (Standard Double + Smart)"

    quotes = {
        'std_double': ('"', '"'),
        'std_single': ("'", "'"),
        'smart_double': ('“', '”'),
        'smart_single': ('‘', '’'),
    }

    for q_name, (start, end) in quotes.items():
        if text.startswith(start) and text.endswith(end):
            return f"Surrounded by {q_name}"
            
    return "No Outer Quotes"

def analyze_deck(deck_name):
    res = invoke("findNotes", query=f'deck:"{deck_name}"')
    note_ids = res.get("result", [])
    if not note_ids:
        print(f"No notes found in {deck_name}.\n")
        return

    notes_info = invoke("notesInfo", notes=note_ids).get("result", [])
    stats = Counter()
    examples = {}

    for note in notes_info:
        fields = note.get('fields', {})
        val = fields.get('Front', {}).get('value') or fields.get('Thai', {}).get('value', '')
        classification = classify_outer_quotes(val)
        stats[classification] += 1
        if classification != "No Outer Quotes" and classification not in examples:
            examples[classification] = val

    print(f"Statistics for {deck_name}:")
    print("-" * 60)
    for classification, count in stats.most_common():
        percentage = (count / len(note_ids)) * 100
        print(f"{count:4} ({percentage:5.1f}%) : {classification}")
        if classification in examples:
            print(f"       Ex: {examples[classification]}")
    print("-" * 60)
    print(f"Total notes: {len(note_ids)}\n")

def main():
    analyze_deck("Thai::vocab")
    analyze_deck("Thai::~phrases")

if __name__ == "__main__":
    main()
