"""Add metadata_json column to transactions table"""
import sqlite3

# Connect to the database
conn = sqlite3.connect('concierge.db')
cursor = conn.cursor()

try:
    # Check if column already exists
    cursor.execute("PRAGMA table_info(transactions)")
    columns = [col[1] for col in cursor.fetchall()]
    
    if 'metadata_json' not in columns:
        # Add the column
        cursor.execute("ALTER TABLE transactions ADD COLUMN metadata_json TEXT")
        conn.commit()
        print("Successfully added metadata_json column to transactions table")
    else:
        print("metadata_json column already exists")
        
except Exception as e:
    print(f"Error: {e}")
    conn.rollback()
finally:
    conn.close()