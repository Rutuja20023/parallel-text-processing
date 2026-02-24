# Database Performance Optimization with Indexing

## Overview
This project demonstrates the impact of database indexing on query performance using SQLite with 1 million Amazon product reviews.

---

## Features
- Process and insert 1 million records into SQLite database
- Rule-based sentiment scoring system
- Query performance comparison (Before vs After indexing)
- Performance metrics and improvement analysis

---

## Project Structure
```
Performane_and_optimization/
├── scoring_engine.py              # Sentiment scoring logic
├── expand_data.py                 # Expand dataset to 1M records
├── process_and_insert.py          # Insert data into database
├── query_before_optimization.py   # Test queries without indexes
├── apply_optimization.py          # Create database indexes
├── query_after_optimization.py    # Test queries with indexes
├── performance_report.txt         # Performance results
├── 7817_1.csv                     # Original dataset
└── .gitignore
```

---

## How to Run

### Step 1: Process and Insert Data
```bash
python process_and_insert.py
```
- Reads CSV file
- Calculates sentiment scores
- Inserts 1 million records into database

### Step 2: Test Performance Before Optimization
```bash
python query_before_optimization.py
```
- Runs 3 test queries without indexes
- Records execution times

### Step 3: Apply Optimization
```bash
python apply_optimization.py
```
- Creates indexes on: `category`, `rating`, `score`

### Step 4: Test Performance After Optimization
```bash
python query_after_optimization.py
```
- Runs same 3 queries with indexes
- Records improved execution times

---

## Test Queries

**Query 1:** Count reviews by category
```sql
SELECT COUNT(*) FROM reviews WHERE category='Highly Recommended';
```

**Query 2:** Calculate average score
```sql
SELECT AVG(score) FROM reviews;
```

**Query 3:** Filter by rating
```sql
SELECT * FROM reviews WHERE rating >= 4;
```

---

## Performance Results

| Query | Before (seconds) | After (seconds) | Improvement |
|-------|------------------|-----------------|-------------|
| Query 1 | 0.3007 | 0.0004 | 99.88% faster |
| Query 2 | 0.0610 | 0.0459 | 24.75% faster |
| Query 3 | 0.0630 | 0.0002 | 99.62% faster |

**Key Insight:** Indexes on filtered columns (category, rating) provide 800x+ speedup!

---

## Technologies Used
- Python
- SQLite3
- CSV Processing
- Database Indexing

---

## Requirements
```bash
pip install pandas
```

---

## Notes
- Database file (`amazon_reviews.db`) is excluded from Git (large file)
- Expanded CSV (`expanded_1million.csv`) is excluded from Git (large file)
- Original dataset (`7817_1.csv`) is included for reference
