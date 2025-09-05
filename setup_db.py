import psycopg2

# Connect to the default postgres database
conn = psycopg2.connect(
    host="localhost",
    database="postgres",   # default db
    user="botuser",       # your postgres username
    password="kAnishka"        # your postgres password
)

conn.autocommit = True
cur = conn.cursor()

# 1. Create a new database
cur.execute("CREATE DATABASE auth_system;")

cur.close()
conn.close()
print("Database created successfully")
