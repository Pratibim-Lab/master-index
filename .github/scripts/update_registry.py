import sqlite3
import json
import sys
import os

def main():
    if len(sys.argv) < 2: return
    payload = json.loads(sys.argv[1])
    
    # 1. Extract the new fields from your "Rich" Manifest
    name = payload.get('name')
    description = payload.get('desc', '')
    tags = json.dumps(payload.get('tags', []))
    footprint = payload.get('footprint', '')
    datasheet = payload.get('datasheet', '')
    base_url = payload.get('base_url')

    os.makedirs('data', exist_ok=True)
    conn = sqlite3.connect('data/registry.db')
    cursor = conn.cursor()
    
    # 2. Updated Schema with Footprint and Datasheet
    cursor.execute('''CREATE TABLE IF NOT EXISTS registry (
                        name TEXT PRIMARY KEY, 
                        description TEXT, 
                        tags TEXT, 
                        footprint TEXT,
                        datasheet TEXT,
                        base_url TEXT, 
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )''')

    # 3. Enhanced Upsert
    cursor.execute('''INSERT INTO registry (name, description, tags, footprint, datasheet, base_url) 
                      VALUES (?, ?, ?, ?, ?, ?)
                      ON CONFLICT(name) DO UPDATE SET 
                        description=excluded.description, 
                        tags=excluded.tags, 
                        footprint=excluded.footprint,
                        datasheet=excluded.datasheet,
                        base_url=excluded.base_url, 
                        updated_at=CURRENT_TIMESTAMP''', 
                   (name, description, tags, footprint, datasheet, base_url))
    
    conn.commit()
    conn.close()

if __name__ == "__main__":
    main()