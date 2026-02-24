import sqlite3
import time

DB_PATH = "amazon_reviews.db"

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

queries = [
    "SELECT COUNT(*) FROM reviews WHERE category='Highly Recommended';",
    "SELECT AVG(score) FROM reviews;",
    "SELECT * FROM reviews WHERE rating >= 4;"
]

for query in queries:
    start = time.time()
    cursor.execute(query)
    cursor.fetchall()
    end = time.time()

    print("Query:", query)
    print("Execution Time:", end - start)
    print("-" * 50)

conn.close()