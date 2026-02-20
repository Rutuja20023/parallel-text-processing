import csv
import os
import time
import sqlite3
from multiprocessing import Pool
from datetime import datetime

# -----------------------------------
# PRODUCT-SPECIFIC SCORING RULES
# -----------------------------------
def calculate_product_score(review_text, product_name):
    """
    Calculate score based on product-specific attributes:
    - Quality Score
    - Value for Money Score
    - Performance Score (charging/speed/durability)
    - Issue Score (problems/defects)
    """
    if not review_text:
        return 0, "No Review"
    
    text_lower = review_text.lower()
    
    # Quality indicators (+2 each)
    quality_positive = ["good quality", "excellent quality", "best quality", "premium", 
                       "sturdy", "durable", "strong", "solid", "well built"]
    
    # Value indicators (+2 each)
    value_positive = ["worth", "value for money", "affordable", "cheap", "budget", 
                     "price", "deal", "recommend"]
    
    # Performance indicators (+3 each)
    performance_positive = ["fast charging", "quick charge", "good speed", "works well",
                           "perfect", "excellent", "superb", "awesome", "amazing"]
    
    # Problem indicators (-3 each)
    problem_negative = ["not working", "stopped working", "defective", "broken", "damaged",
                       "poor", "bad", "worst", "issue", "problem", "disappointed", "waste"]
    
    # Calculate scores
    quality_score = sum(2 for word in quality_positive if word in text_lower)
    value_score = sum(2 for word in value_positive if word in text_lower)
    performance_score = sum(3 for word in performance_positive if word in text_lower)
    problem_score = sum(-3 for word in problem_negative if word in text_lower)
    
    # Total score
    total_score = quality_score + value_score + performance_score + problem_score
    
    # Determine category
    if total_score >= 10:
        category = "Highly Recommended"
    elif total_score >= 5:
        category = "Recommended"
    elif total_score >= 0:
        category = "Average"
    elif total_score >= -5:
        category = "Below Average"
    else:
        category = "Not Recommended"
    
    return total_score, category


# -----------------------------------
# PROCESS SINGLE ROW
# -----------------------------------
def process_review_row(row_data):
    """Process a single review row from CSV"""
    try:
        row_index, row = row_data
        process_id = os.getpid()
        
        print(f"Processing Row {row_index} | Process ID: {process_id}")
        
        # Extract data
        product_name = row.get('product_name', 'Unknown')
        review_title = row.get('review_title', '')
        review_content = row.get('review_content', '')
        rating = row.get('rating', 'N/A')
        
        # Combine review text
        full_review = f"{review_title} {review_content}"
        
        # Calculate score
        score, category = calculate_product_score(full_review, product_name)
        
        return {
            'row_index': row_index,
            'product_name': product_name[:100],
            'review_text': full_review[:500],
            'rating': rating,
            'score': score,
            'category': category,
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'status': 'success'
        }
    
    except Exception as e:
        return {
            'row_index': row_index,
            'product_name': 'Error',
            'review_text': '',
            'rating': 'N/A',
            'score': 0,
            'category': 'Error',
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'status': f'error: {str(e)}'
        }


# -----------------------------------
# READ CSV AND PREPARE DATA
# -----------------------------------
def read_csv_data(csv_path, max_rows=100):
    """Read CSV and return list of rows"""
    try:
        rows = []
        with open(csv_path, 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for idx, row in enumerate(reader):
                if idx >= max_rows:
                    break
                rows.append((idx + 1, row))
        
        print(f"Loaded {len(rows)} rows from CSV")
        return rows
    
    except Exception as e:
        print(f"Error reading CSV: {str(e)}")
        return []


# -----------------------------------
# SETUP DATABASE
# -----------------------------------
def setup_database(db_path):
    """Create database and table"""
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS product_reviews (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                row_index INTEGER,
                product_name TEXT,
                review_text TEXT,
                rating TEXT,
                score INTEGER,
                category TEXT,
                timestamp TEXT
            )
        """)
        
        conn.commit()
        conn.close()
        print(f"Database setup complete: {db_path}")
        return True
    
    except Exception as e:
        print(f"Database error: {str(e)}")
        return False


# -----------------------------------
# STORE RESULTS
# -----------------------------------
def store_results(db_path, results):
    """Store results in database"""
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        for result in results:
            if result['status'] == 'success':
                cursor.execute("""
                    INSERT INTO product_reviews 
                    (row_index, product_name, review_text, rating, score, category, timestamp)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (result['row_index'], result['product_name'], result['review_text'],
                      result['rating'], result['score'], result['category'], result['timestamp']))
        
        conn.commit()
        conn.close()
        print(f"Stored {len(results)} results in database")
        return True
    
    except Exception as e:
        print(f"Database storage error: {str(e)}")
        return False


# -----------------------------------
# PARALLEL PROCESSING
# -----------------------------------
def process_parallel(rows):
    """Process rows using multiprocessing"""
    try:
        start_time = time.time()
        
        with Pool(processes=os.cpu_count()) as pool:
            results = pool.map(process_review_row, rows)
        
        end_time = time.time()
        return results, end_time - start_time
    
    except Exception as e:
        print(f"Multiprocessing error: {str(e)}")
        return [], 0


# -----------------------------------
# MAIN EXECUTION
# -----------------------------------
if __name__ == "__main__":
    
    # Configuration
    CSV_PATH = r"E:\Internship\Amazon_Review_Analysis\amazon.csv"
    DATABASE_PATH = r"E:\Internship\Amazon_Review_Analysis\amazon_reviews.db"
    MAX_ROWS = 50  # Process first 50 reviews
    
    print("=" * 70)
    print("AMAZON PRODUCT REVIEW ANALYSIS - PARALLEL PROCESSING")
    print("=" * 70)
    print(f"CPU Cores Available: {os.cpu_count()}\n")
    
    # Step 1: Read CSV data
    print("Step 1: Reading CSV data...")
    rows = read_csv_data(CSV_PATH, MAX_ROWS)
    
    if not rows:
        print("No data to process. Exiting.")
        exit()
    
    # Step 2: Setup database
    print("\nStep 2: Setting up database...")
    if not setup_database(DATABASE_PATH):
        print("Database setup failed. Exiting.")
        exit()
    
    # Step 3: Process in parallel
    print("\nStep 3: Processing reviews with multiprocessing...")
    results, processing_time = process_parallel(rows)
    
    # Step 4: Analyze results
    print("\n" + "=" * 70)
    print("PROCESSING RESULTS")
    print("=" * 70)
    
    highly_recommended = sum(1 for r in results if r['category'] == 'Highly Recommended')
    recommended = sum(1 for r in results if r['category'] == 'Recommended')
    average = sum(1 for r in results if r['category'] == 'Average')
    below_average = sum(1 for r in results if r['category'] == 'Below Average')
    not_recommended = sum(1 for r in results if r['category'] == 'Not Recommended')
    
    print(f"\nTotal Reviews Processed: {len(results)}")
    print(f"Highly Recommended: {highly_recommended}")
    print(f"Recommended: {recommended}")
    print(f"Average: {average}")
    print(f"Below Average: {below_average}")
    print(f"Not Recommended: {not_recommended}")
    print(f"\nProcessing Time: {processing_time:.2f} seconds")
    
    # Step 5: Store in database
    print("\nStep 4: Storing results in database...")
    store_results(DATABASE_PATH, results)
    
    print("\n" + "=" * 70)
    print("PROCESS COMPLETED SUCCESSFULLY")
    print("=" * 70)
    print(f"Database saved at: {DATABASE_PATH}")
