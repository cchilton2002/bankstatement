import ollama
from df import extract_and_parse 
import pandas as pd
import subprocess
import json
import os

# pdf_route = '/home/cchilton2002/Downloads/fd statement ••• 20240814.pdf'
# df = extract_and_parse(pdf_route)


cache_file_path = 'transaction_category_cache.json'

def load_cache() -> dict:
    if os.path.exists(cache_file_path):
        try:
            with open(cache_file_path, 'r') as f:
                cache = json.load(f)
                return cache
        except json.JSONDecodeError:
            print("Warning: Cache file is corrupted or empty. Starting with an empty cache.")
            return {}
    return {}

def update_and_save_cache(cache: dict, detail: str, category: str) -> None:
    cache[detail] = category  # Add the new category to the cache
    try:
        with open(cache_file_path, 'w') as f:
            json.dump(cache, f)
            f.flush()  # Ensure data is written to disk
    except Exception as e:
        print(f"Error saving cache: {e}")
        
category_cache = load_cache()

def categorise_transaction(detail: str) -> str:
    if detail in category_cache:
        return category_cache[detail]
    try:
        response = ollama.generate(model="ipe", prompt=f"Categorize the following transaction: {detail}")
        category = response.get('response', 'Unknown').strip()
        update_and_save_cache(category_cache, detail, category)  # Save immediately
        return category
    except Exception as e:
        print(f"Error categorizing transaction '{detail}': {e}")
        return 'Unknown'
    
    

# Use apply to process each transaction separately
# df['Category'] = df['Details'].apply(categorise_transaction)

# print(df)

