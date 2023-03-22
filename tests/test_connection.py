import psycopg2
from config import DATABASE_CONFIG

def test_connection():
    try:
        connection = psycopg2.connect(
            host=DATABASE_CONFIG['host'],
            dbname=DATABASE_CONFIG['database'],
            user=DATABASE_CONFIG['user'],
            password=DATABASE_CONFIG['password'],
            port=DATABASE_CONFIG['port']
        )

        print("Connection successful")
        connection.close()

    except Exception as e:
        print("Connection failed:")
        print(e)

if __name__ == "__main__":
    test_connection()
