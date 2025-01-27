import sqlite3

# Connect to the database
conn = sqlite3.connect('db.sqlite3')

# Create a cursor object
cursor = conn.cursor()

# Get table names
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()

# Print table names
print("Tables in the database:")
for table in tables:
    print(table[0])

# Close the connection
conn.close()
