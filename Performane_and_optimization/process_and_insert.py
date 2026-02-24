import csv
import sqlite3
import time
from scoring_engine import calculate_product_score

CSV_PATH = r"E:\Internship\Performane_and_optimization\expanded_1million.csv"
DB_PATH = r"amazon_reviews.db"

def create_database():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS reviews (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        product_name TEXT,
        review_text TEXT,
        rating REAL,
        score INTEGER,
        category TEXT
    )
    """)

    conn.commit()
    conn.close()

def process_and_insert():

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    start_time = time.time()

    with open(CSV_PATH, "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        batch = []
        batch_size = 5000

        for row in reader:

            review_text = row.get("review_text", "")
            product_name = row.get("product_name", "")
            rating = row.get("rating", 0)

            score, category = calculate_product_score(
                review_text,
                product_name,
                rating
            )

            batch.append((
                product_name,
                review_text,
                rating,
                score,
                category
            ))

            if len(batch) >= batch_size:
                cursor.executemany("""
                INSERT INTO reviews
                (product_name, review_text, rating, score, category)
                VALUES (?, ?, ?, ?, ?)
                """, batch)
                batch.clear()

        if batch:
            cursor.executemany("""
            INSERT INTO reviews
            (product_name, review_text, rating, score, category)
            VALUES (?, ?, ?, ?, ?)
            """, batch)

    conn.commit()
    conn.close()

    end_time = time.time()

    print("Insertion Time:", end_time - start_time)

if __name__ == "__main__":
    create_database()
    process_and_insert()