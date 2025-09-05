import psycopg2

conn = psycopg2.connect(
    host="localhost",
    database="auth_system",
    user="botuser",
    password="kAnishka"
)
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(200) NOT NULL
)
""")

conn.commit()
cur.close()
conn.close()
print("Users table created ")
