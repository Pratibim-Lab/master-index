import sqlite3
import json
import sys
import os

def update_db():
    # 1. Get payload from Env (JSON from Shard) or Sys Args
    payload_raw = os.environ.get("SHARD_PAYLOAD") or (sys.argv[1] if len(sys.argv) > 1 else None)
    
    if not payload_raw or payload_raw == "null":
        print("⚠️ No payload received. This is normal for a manual test run.")
        # Create dummy data for manual testing so the script doesn't fail
        data = {
            "name": "Manual-Test-Part",
            "desc": "Testing the engine",
            "tags": ["test", "debug"],
            "footprint": "TEST_FP",
            "datasheet": "https://test.com",
            "base_url": "https://github.com/Pratibim-Lab"
        }
    else:
        data = json.loads(payload_raw)
    
    # 2. Ensure data folder exists
    os.makedirs('data', exist_ok=True)

    conn = sqlite3.connect('data/registry.db')
    cursor = conn.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS registry 
        (name TEXT PRIMARY KEY, description TEXT, tags TEXT, 
         footprint TEXT, datasheet TEXT, base_url TEXT, updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')

    cursor.execute('''INSERT INTO registry (name, description, tags, footprint, datasheet, base_url)
                      VALUES (?, ?, ?, ?, ?, ?)
                      ON CONFLICT(name) DO UPDATE SET
                      description=excluded.description,
                      tags=excluded.tags,
                      footprint=excluded.footprint,
                      datasheet=excluded.datasheet,
                      base_url=excluded.base_url,
                      updated_at=CURRENT_TIMESTAMP''', 
                   (data['name'], data['desc'], ",".join(data['tags']), 
                    data['footprint'], data['datasheet'], data['base_url']))

    conn.commit()
    conn.close()
    print(f"✅ Successfully processed: {data['name']}")

if __name__ == "__main__":
    update_db()
