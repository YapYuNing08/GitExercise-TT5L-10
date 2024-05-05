import sqlite3
import json

def export_to_json(database_file, table_name, output_file):
    # Connect to the SQLite database
    conn = sqlite3.connect(database_file)
    cursor = conn.cursor()

    # Execute a query to select the data from the specified table
    cursor.execute(f"SELECT * FROM {table_name}")

    # Fetch all rows from the query result
    rows = cursor.fetchall()

    # Extract column names from the cursor description
    column_names = [desc[0] for desc in cursor.description]

    # Convert fetched data into a list of dictionaries
    data = []
    for row in rows:
        data.append(dict(zip(column_names, row)))

    # Write data to a JSON file
    with open(output_file, 'w') as json_file:
        json.dump(data, json_file, indent=4)

    # Close the database connection
    conn.close()

# Example usage:
export_to_json('db.sqlite3', 'customer_menuitem', 'data.json')