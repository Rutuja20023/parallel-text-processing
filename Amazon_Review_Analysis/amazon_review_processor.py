import csv
import os
import time
import sqlite3
from multiprocessing import Pool
from datetime import datetime

# -----------------------------------
# ENHANCED SCORING RULES
# -----------------------------------
def calculate_product_score(review_text, product_name, rating=None):
    """
    Enhanced scoring with:
    - Negation handling
    - Intensifiers
    - Repetition weight
    - ALL CAPS emphasis
    - Short review handling
    - Star rating correlation
    """
    if not review_text:
        return 0, "No Review"
    
    # E. Short Review Handling
    words = review_text.split()
    if len(words) < 3:
        return 0, "Average"
    
    text_lower = review_text.lower()
    
    # Positive keywords
    positive_words = ["good", "excellent", "best", "premium", "sturdy", "durable", 
                     "strong", "solid", "worth", "affordable", "recommend", "perfect", 
                     "superb", "awesome", "amazing", "quality", "fast", "great"]
    
    # Negative keywords
    negative_words = ["bad", "poor", "worst", "defective", "broken", "damaged", 
                     "issue", "problem", "disappointed", "waste", "terrible", "horrible"]
    
    # Negation words
    negations = ["not", "never", "no"]
    
    # Intensifiers
    intensifiers = ["very", "extremely", "really", "highly", "super", "absolutely"]
    
    total_score = 0
    
    # Process each word with context
    for i, word in enumerate(words):
        word_lower = word.lower().strip('.,!?')
        word_original = word.strip('.,!?')
        
        # Check if word is positive or negative
        is_positive = word_lower in positive_words
        is_negative = word_lower in negative_words
        
        if is_positive or is_negative:
            base_score = 2 if is_positive else -2
            
            # A. Negation Handling
            if i > 0 and words[i-1].lower() in negations:
                base_score = -base_score
            
            # B. Intensifiers
            if i > 0 and words[i-1].lower() in intensifiers:
                base_score = base_score * 2
            
            # D. ALL CAPS Emphasis
            if word_original.isupper() and len(word_original) > 2:
                base_score += 2 if base_score > 0 else -2
            
            total_score += base_score
    
    # C. Repetition Weight (count word frequency)
    for word in positive_words:
        count = text_lower.count(word)
        if count > 1:
            total_score += (count - 1) * 2
    
    for word in negative_words:
        count = text_lower.count(word)
        if count > 1:
            total_score -= (count - 1) * 2
    
    # F. Star Rating Correlation
    if rating:
        try:
            rating_val = float(str(rating).replace('₹', '').strip())
            if rating_val >= 4.0:
                total_score += 2
            elif rating_val <= 2.0:
                total_score -= 2
        except:
            pass
    
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
# AUTO DETECT TEXT COLUMNS
# -----------------------------------
def detect_text_columns(row):
    """Auto-detect review text columns from CSV"""
    possible_columns = ['review_content', 'review_text', 'text', 'review_title', 'summary', 'content']
    
    text_parts = []
    for col in possible_columns:
        if col in row and row[col]:
            text_parts.append(row[col])
    
    return ' '.join(text_parts) if text_parts else ''


# -----------------------------------
# PROCESS SINGLE ROW
# -----------------------------------
def process_review_row(row_data):
    """Process a single review row from CSV with enhanced error handling"""
    row_index = None
    try:
        row_index, row = row_data
        process_id = os.getpid()
        
        print(f"Processing Row {row_index} | Process ID: {process_id}")
        
        # Extract data with fallbacks
        product_name = row.get('product_name', row.get('product', 'Unknown'))
        rating = row.get('rating', 'N/A')
        
        # Auto-detect text columns
        full_review = detect_text_columns(row)
        
        if not full_review:
            raise ValueError("No text content found in row")
        
        # Calculate score with rating
        score, category = calculate_product_score(full_review, product_name, rating)
        
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
    
    except KeyError as e:
        return {
            'row_index': row_index or 0,
            'product_name': 'Error',
            'review_text': '',
            'rating': 'N/A',
            'score': 0,
            'category': 'Error',
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'status': f'Missing column: {str(e)}'
        }
    except Exception as e:
        return {
            'row_index': row_index or 0,
            'product_name': 'Error',
            'review_text': '',
            'rating': 'N/A',
            'score': 0,
            'category': 'Error',
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'status': f'Processing error: {str(e)}'
        }


# -----------------------------------
# READ CSV AND PREPARE DATA
# -----------------------------------
def read_csv_data(csv_path, max_rows=100):
    """Read CSV with enhanced error handling"""
    try:
        if not os.path.exists(csv_path):
            raise FileNotFoundError(f"CSV file not found: {csv_path}")
        
        rows = []
        encodings = ['utf-8', 'latin-1', 'cp1252']
        
        for encoding in encodings:
            try:
                with open(csv_path, 'r', encoding=encoding) as csvfile:
                    reader = csv.DictReader(csvfile)
                    for idx, row in enumerate(reader):
                        if idx >= max_rows:
                            break
                        rows.append((idx + 1, row))
                
                print(f"Loaded {len(rows)} rows from CSV (encoding: {encoding})")
                
                if len(rows) == 0:
                    raise ValueError("CSV file is empty")
                
                return rows
            except UnicodeDecodeError:
                continue
        
        raise ValueError("Could not read CSV with any supported encoding")
    
    except FileNotFoundError as e:
        print(f"File Error: {str(e)}")
        return []
    except ValueError as e:
        print(f"Data Error: {str(e)}")
        return []
    except Exception as e:
        print(f"Unexpected Error reading CSV: {str(e)}")
        return []


# -----------------------------------
# SETUP DATABASE
# -----------------------------------
def setup_database(db_path):
    """Create database tables with enhanced error handling"""
    try:
        conn = sqlite3.connect(db_path, timeout=10)
        cursor = conn.cursor()
        
        # Create product_reviews table
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
        
        # Create summary_report table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS summary_report (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                total_reviews INTEGER,
                highly_recommended INTEGER,
                recommended INTEGER,
                average INTEGER,
                below_average INTEGER,
                not_recommended INTEGER,
                average_score REAL,
                processing_time REAL,
                method_used TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        conn.commit()
        conn.close()
        print(f"Database setup complete: {db_path}")
        return True
    
    except sqlite3.OperationalError as e:
        print(f"Database Lock Error: {str(e)}. Try closing other programs using the database.")
        return False
    except Exception as e:
        print(f"Database Setup Error: {str(e)}")
        return False


# -----------------------------------
# STORE RESULTS
# -----------------------------------
def store_results(db_path, results):
    """Store results in database with error handling"""
    try:
        conn = sqlite3.connect(db_path, timeout=10)
        cursor = conn.cursor()
        
        success_count = 0
        for result in results:
            if result['status'] == 'success':
                cursor.execute("""
                    INSERT INTO product_reviews 
                    (row_index, product_name, review_text, rating, score, category, timestamp)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (result['row_index'], result['product_name'], result['review_text'],
                      result['rating'], result['score'], result['category'], result['timestamp']))
                success_count += 1
        
        conn.commit()
        conn.close()
        print(f"Stored {success_count} results in database")
        return True
    
    except sqlite3.OperationalError as e:
        print(f"Database Lock Error: {str(e)}")
        return False
    except Exception as e:
        print(f"Database Storage Error: {str(e)}")
        return False


# -----------------------------------
# STORE SUMMARY REPORT
# -----------------------------------
def store_summary(db_path, stats, processing_time, method):
    """Store summary report in database"""
    try:
        conn = sqlite3.connect(db_path, timeout=10)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO summary_report 
            (total_reviews, highly_recommended, recommended, average, 
             below_average, not_recommended, average_score, processing_time, method_used)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (stats['total'], stats['highly_recommended'], stats['recommended'],
              stats['average'], stats['below_average'], stats['not_recommended'],
              stats['avg_score'], processing_time, method))
        
        conn.commit()
        conn.close()
        return True
    
    except Exception as e:
        print(f"Summary Storage Error: {str(e)}")
        return False


# -----------------------------------
# PARALLEL PROCESSING
# -----------------------------------
def process_parallel(rows):
    """Process rows using multiprocessing"""
    try:
        start_time = time.time()
        
        cpu_count = os.cpu_count() or 1
        with Pool(processes=cpu_count) as pool:
            results = pool.map(process_review_row, rows)
        
        end_time = time.time()
        return results, end_time - start_time
    
    except Exception as e:
        print(f"Multiprocessing Error: {str(e)}")
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
    print("AMAZON PRODUCT REVIEW ANALYSIS - ENHANCED VERSION")
    print("=" * 70)
    print(f"CPU Cores Available: {os.cpu_count()}\n")
    
    # Step 1: Read CSV data
    print("Step 1: Reading CSV data...")
    rows = read_csv_data(CSV_PATH, MAX_ROWS)
    
    if not rows:
        print("ERROR: No data to process. Exiting.")
        exit(1)
    
    # Step 2: Setup database
    print("\nStep 2: Setting up database...")
    if not setup_database(DATABASE_PATH):
        print("ERROR: Database setup failed. Exiting.")
        exit(1)
    
    # Step 3: Process with Parallel Processing
    print("\nStep 3: Processing reviews with multiprocessing...")
    results, processing_time = process_parallel(rows)
    
    if not results:
        print("ERROR: Processing failed. Exiting.")
        exit(1)
    
    # Step 4: Calculate statistics
    highly_recommended = sum(1 for r in results if r['category'] == 'Highly Recommended')
    recommended = sum(1 for r in results if r['category'] == 'Recommended')
    average = sum(1 for r in results if r['category'] == 'Average')
    below_average = sum(1 for r in results if r['category'] == 'Below Average')
    not_recommended = sum(1 for r in results if r['category'] == 'Not Recommended')
    
    total_score = sum(r['score'] for r in results if r['status'] == 'success')
    success_count = sum(1 for r in results if r['status'] == 'success')
    avg_score = total_score / success_count if success_count > 0 else 0
    
    stats = {
        'total': len(results),
        'highly_recommended': highly_recommended,
        'recommended': recommended,
        'average': average,
        'below_average': below_average,
        'not_recommended': not_recommended,
        'avg_score': avg_score
    }
    
    # Step 5: Store in database
    print("\nStep 4: Storing results in database...")
    store_results(DATABASE_PATH, results)
    store_summary(DATABASE_PATH, stats, processing_time, "Parallel")
    
    # Step 6: Final Report
    print("\n" + "=" * 70)
    print("AMAZON REVIEW ANALYSIS REPORT")
    print("=" * 70)
    print(f"Total Reviews:           {stats['total']}")
    print(f"Highly Recommended:      {highly_recommended}")
    print(f"Recommended:             {recommended}")
    print(f"Average:                 {average}")
    print(f"Below Average:           {below_average}")
    print(f"Not Recommended:         {not_recommended}")
    print(f"Average Score:           {avg_score:.2f}")
    print(f"\nProcessing Method Used:  Parallel (Multiprocessing)")
    print(f"Processing Time:         {processing_time:.2f} seconds")
    print("=" * 70)
    print(f"\nDatabase saved at: {DATABASE_PATH}")
