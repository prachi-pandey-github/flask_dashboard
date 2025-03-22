import json
import mysql.connector

# Load JSON data
with open("jsondata.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# Connect to MySQL
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="prachi",
    database="dashboard_db"
)
cursor = conn.cursor()

# Clear existing data
cursor.execute("TRUNCATE TABLE insights")
print("Table cleared successfully!")

# Insert data with NULL handling and debug logging
for item in data:
    source_value = item.get("source", "")
    print(f"Inserting source value: {source_value}")  # Debug log
    
    cursor.execute("""
        INSERT INTO insights (end_year, intensity, sector, topic, region, country, likelihood, relevance, pestle, source, insight, title)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, (
        item.get("end_year", None),
        int(item["intensity"]) if item.get("intensity") and item["intensity"] != "" else None,
        item.get("sector", ""),
        item.get("topic", ""),
        item.get("region", ""),
        item.get("country", ""),
        int(item["likelihood"]) if item.get("likelihood") and item["likelihood"] != "" else None,
        int(item["relevance"]) if item.get("relevance") and item["relevance"] != "" else None,
        item.get("pestle", ""),
        source_value,  # Using the stored source value
        item.get("insight", ""),
        item.get("title", "")
    ))

conn.commit()
conn.close()
print("Data inserted successfully!")
# The database.py script reads the JSON data from jsondata.json, connects to a MySQL database, and inserts the data into the insights table.
# The script uses the mysql.connector library to interact with the MySQL database.
# The data is inserted into the insights table with NULL handling for missing values.
# Finally, the script commits the changes and closes the database connection.
# To run the database.py script, you can execute it using the Python interpreter:

# python database.py