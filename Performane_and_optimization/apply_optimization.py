import sqlite3

DB_PATH = "amazon_reviews.db"

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

print("Applying Indexes...")

cursor.execute("CREATE INDEX idx_category ON reviews(category);")
cursor.execute("CREATE INDEX idx_rating ON reviews(rating);")
cursor.execute("CREATE INDEX idx_score ON reviews(score);")

conn.commit()
conn.close()

print("Indexes Created Successfully")