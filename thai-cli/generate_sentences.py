#!/usr/bin/env python3
import csv
import os
import sys
import re
from typing import List, Dict

# This script is intended to be called by an AI agent that can generate the actual content.
# Since it needs an LLM to generate 'Natural Thai' sentences, the script itself 
# will serve as a structured orchestration point or a placeholder for an agent 
# to fill. However, to fulfill the "skill" requirement, we'll define the logic 
# and expectations here.

def main():
    if len(sys.argv) < 2:
        print("Usage: ./generate_sentences.py <missing_words_csv>")
        sys.exit(1)

    input_file = sys.argv[1]
    if not os.path.exists(input_file):
        print(f"Error: {input_file} not found")
        sys.exit(1)

    input_filename = os.path.basename(input_file)
    if "nilsen_missing" in input_filename:
        output_filename = input_filename.replace("nilsen_missing", "nilsen_sentences")
    else:
        output_filename = "nilsen_sentences_" + input_filename
    
    output_file = os.path.join(os.path.dirname(input_file), output_filename)
    
    print(f"Source: {input_file}")
    print(f"Target: {output_file}")
    print("\n[MANDATE FOR AI AGENT]")
    print("1. Read the vocabulary words from the source CSV.")
    print("2. Generate 50 Natural Thai sentences for these words.")
    print("3. Persona: Male speaker (use 'ผม' where needed, but do NOT include 'ครับ').")
    print("4. Vocabulary: Prioritize words from the 'Thai::vocab' deck (run extract_known_vocab.py first).")
    print("5. Format: CSV with header 'Front,Back,Audio,Notes'.")
    print("6. Front field: Thai sentence surrounded by triple double-quotes.")
    print("7. Notes field: 'Thai Word (English Translation)'.")
    print("\nProceeding with generation via agent invocation...")

if __name__ == "__main__":
    main()
