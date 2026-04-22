import sqlite3
import json
import sys

def main():
    # Payload sent from the shard
    payload = json.loads(sys.argv[1])
    part_name = payload.get('part_name')
    repo_url = payload.get('repo')
    cdn_url = payload.get('url')

    conn = sqlite3.connect('data/registry.db')
    cursor = conn.cursor()
    
    # Create table if it doesn't exist
    cursor.execute('''CREATE TABLE IF NOT EXISTS registry 
                      (part_name TEXT PRIMARY KEY, repo TEXT, url TEXT, updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')

    # Insert or Update
    cursor.execute('''INSERT INTO registry (part_name, repo, url) VALUES (?, ?, ?)
                      ON CONFLICT(part_name) DO UPDATE SET repo=excluded.repo, url=excluded.url, updated_at=CURRENT_TIMESTAMP''', 
                   (part_name, repo_url, cdn_url))
    
    conn.commit()
    conn.close()

if __name__ == "__main__":
    main()