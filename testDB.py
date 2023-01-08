import psycopg2 

# Connect to the database
conn = psycopg2.connect(
    host="localhost",
    database="elo_baby",
    user="postgres",
    password="519173"
)

# Print a message if the connection is successful
print("Connected to the database!")

# Close the connection
conn.close()
