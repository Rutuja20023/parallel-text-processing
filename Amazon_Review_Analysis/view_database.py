import sqlite3

# Connect to database
conn = sqlite3.connect(r"E:\Internship\Amazon_Review_Analysis\amazon_reviews.db")
cursor = conn.cursor()

# Get total count
cursor.execute("SELECT COUNT(*) FROM product_reviews")
total = cursor.fetchone()[0]

print(f"\nTotal Records in Database: {total}\n")
print("=" * 80)

# Show category summary
cursor.execute("SELECT category, COUNT(*) FROM product_reviews GROUP BY category ORDER BY COUNT(*) DESC")
summary = cursor.fetchall()

print("\nCATEGORY SUMMARY:")
print("-" * 80)
for cat, count in summary:
    print(f"{cat:25} : {count:3} reviews")

print("\n" + "=" * 80)

# Show top 5 highest scored reviews
print("\nTOP 5 HIGHEST SCORED REVIEWS:")
print("-" * 80)
cursor.execute("SELECT row_index, score, category, rating FROM product_reviews ORDER BY score DESC LIMIT 5")
top_reviews = cursor.fetchall()

for idx, score, cat, rating in top_reviews:
    print(f"Row {idx:2} | Score: {score:3} | Category: {cat:20} | Rating: {rating}")

print("\n" + "=" * 80)

# Show bottom 5 lowest scored reviews
print("\nBOTTOM 5 LOWEST SCORED REVIEWS:")
print("-" * 80)
cursor.execute("SELECT row_index, score, category, rating FROM product_reviews ORDER BY score ASC LIMIT 5")
bottom_reviews = cursor.fetchall()

for idx, score, cat, rating in bottom_reviews:
    print(f"Row {idx:2} | Score: {score:3} | Category: {cat:20} | Rating: {rating}")

print("\n" + "=" * 80)

conn.close()
print("\nDatabase check complete!")
