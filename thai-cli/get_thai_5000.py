#!/usr/bin/env python3
import urllib.request
import os

URL = "https://raw.githubusercontent.com/frekwencja/most-common-words-multilingual/main/data/wordfrequency.info/th.txt"
OUTPUT = "thai_5000_common.txt"

def download_list():
    print(f"Downloading common Thai words from: {URL}")
    try:
        with urllib.request.urlopen(URL) as response:
            data = response.read().decode('utf-8')
            with open(OUTPUT, "w", encoding='utf-8') as f:
                f.write(data)
        print(f"Successfully saved to {OUTPUT}")
        
        # Print first 10
        lines = data.strip().split('\n')
        print("\nTop 10 words:")
        for line in lines[:10]:
            print(f"- {line}")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    download_list()
