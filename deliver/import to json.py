import sqlite3
import json

def import_json_to_sqlite(json_file, db_file, table_name):
    # Connect to the SQLite database
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    # Read JSON data from file
    with open(json_file, 'r') as file:
        data = json.load(file)

    # Insert data into SQLite table
    for row in data:
        placeholders = ', '.join(['?'] * len(row))
        columns = ', '.join(row.keys())
        sql = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
        cursor.execute(sql, tuple(row.values()))

    # Commit changes and close connection
    conn.commit()
    conn.close()

    print("Data imported into SQLite database.")

if _name_ == "_main_":
    json_file = 'C:\Users\yapyu\Projects\GitExercise-TT5L-10\Deliver\data.json'
    db_file = 'db.sqlite3'
    table_name = 'customer_menuitem'
    import_json_to_sqlite(json_file, db_file, table_name)