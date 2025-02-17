import sqlite3

# Connect to the database
conn = sqlite3.connect('db.sqlite3')

# Create a cursor object
cursor = conn.cursor()

# Find orphaned records
cursor.execute("""
SELECT id, user_id FROM myapp_profile
WHERE user_id NOT IN (SELECT id FROM auth_user);
""")
orphaned_records = cursor.fetchall()

# Print orphaned records (for reference)
print("Orphaned records:", orphaned_records)

# Delete orphaned records
cursor.execute("""
DELETE FROM myapp_profile
WHERE user_id NOT IN (SELECT id FROM auth_user);
""")
conn.commit()

# Close the connection
conn.close()
