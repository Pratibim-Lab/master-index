import sqlite3
import json
import sys
import os

def main():
    if len(sys.argv) < 2:
        print("Error: No payload provided")
        return

    # 1. Catch the "Rich" Payload from the Shard
    payload = json.loads(sys.argv[1])
    
    # Mapping the payload from the Shard's extractor.py
    name = payload.get('name')
    description = payload.get('desc', '')
    tags = json.dumps(payload.get('tags', [])) # Store tags as a JSON string
    base_url = payload.get('base_url')
    schema_ver = payload.get('schema_version', '1.0')

    # 2. Connect to the Brain (SQLite)
    os.makedirs('data', exist_ok=True)
    conn = sqlite3.connect('data/registry.db')
    cursor = conn.cursor()
    
    # 3. Create a Professional, Semantic-Ready Schema
    cursor.execute('''CREATE TABLE IF NOT EXISTS registry (
                        name TEXT PRIMARY KEY, 
                        description TEXT, 
                        tags TEXT, 
                        base_url TEXT, 
                        schema_version TEXT,
                        vector_embedding BLOB,  -- Reserved for Semantic Search
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )''')

    # 4. Upsert (Insert or Update if exists)
    cursor.execute('''INSERT INTO registry (name, description, tags, base_url, schema_version) 
                      VALUES (?, ?, ?, ?, ?)
                      ON CONFLICT(name) DO UPDATE SET 
                        description=excluded.description, 
                        tags=excluded.tags, 
                        base_url=excluded.base_url, 
                        schema_version=excluded.schema_version,
                        updated_at=CURRENT_TIMESTAMP''', 
                   (name, description, tags, base_url, schema_ver))
    
    conn.commit()
    conn.close()
    print(f"Successfully indexed: {name}")

if __name__ == "__main__":
    main()
