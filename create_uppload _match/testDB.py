import psycopg2 
from config import DATABASE_CONFIG

# Connect to the database
conn = psycopg2.connect(
    host=DATABASE_CONFIG['host'],
    database=DATABASE_CONFIG['database'],
    user=DATABASE_CONFIG['user'],
    password=DATABASE_CONFIG['password']
)

# Print a message if the connection is successful
print("Connected to the database!")

# Close the connection
conn.close()
