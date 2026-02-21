<<<<<<< HEAD
# Amazon Product Review Analysis

Parallel text processing system for analyzing Amazon product reviews using multiprocessing and SQLite.

## Features

- **Product-Specific Scoring Rules**: Quality, Value, Performance, and Issue detection
- **Parallel Processing**: Uses all CPU cores for faster processing
- **SQLite Database**: Stores analyzed results with timestamps
- **Exception Handling**: Comprehensive error handling for files, database, and processing
- **Review Categories**: 
  - Highly Recommended (Score ≥ 10)
  - Recommended (Score 5-9)
  - Average (Score 0-4)
  - Below Average (Score -1 to -5)
  - Not Recommended (Score < -5)

## Scoring System

### Quality Score (+2 each)
- good quality, excellent quality, premium, sturdy, durable, strong, solid, well built

### Value Score (+2 each)
- worth, value for money, affordable, cheap, budget, price, deal, recommend

### Performance Score (+3 each)
- fast charging, quick charge, good speed, works well, perfect, excellent, superb, awesome, amazing

### Problem Score (-3 each)
- not working, stopped working, defective, broken, damaged, poor, bad, worst, issue, problem, disappointed, waste

## Installation

1. Clone the repository:
```bash
git clone <your-repo-url>
cd Amazon_Review_Analysis
```

2. Ensure Python 3.x is installed

3. Place your `amazon.csv` dataset in the folder

## Usage

### Process Reviews
```bash
python amazon_review_processor.py
```

### View Database Results
```bash
python view_database.py
```

## File Structure

```
Amazon_Review_Analysis/
├── amazon.csv                    # Dataset (not included in git)
├── amazon_review_processor.py    # Main processing script
├── view_database.py              # Database viewer
├── amazon_reviews.db             # SQLite database (not included in git)
├── .gitignore                    # Git ignore file
└── README.md                     # This file
```

## Configuration

Edit `amazon_review_processor.py` to change:
- `MAX_ROWS`: Number of reviews to process (default: 50)
- `CSV_PATH`: Path to your CSV file
- `DATABASE_PATH`: Path to database file

## Database Schema

```sql
CREATE TABLE product_reviews (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    row_index INTEGER,
    product_name TEXT,
    review_text TEXT,
    rating TEXT,
    score INTEGER,
    category TEXT,
    timestamp TEXT
)
```

## Requirements

- Python 3.x
- Standard library modules: csv, os, time, sqlite3, multiprocessing, datetime

## Exception Handling

The system handles:
- File reading errors (missing files, encoding issues)
- Database errors (connection, SQL errors)
- Data processing errors (missing columns, type errors)
- Multiprocessing errors (worker failures)

## Performance

- Uses all available CPU cores
- Processes 50 reviews in ~2-3 seconds (depends on CPU)
- Parallel processing significantly faster than sequential

## License

MIT License

## Author

Your Name
=======
# Parallel Text Processing with Multiprocessing & SQLite

## Overview
This project demonstrates the difference between **Sequential Processing** and **Multiprocessing (Parallel Processing)** for customer review sentiment analysis.

The system reads multiple text files, applies a rule-based sentiment scoring system, compares execution time, and stores results in a SQLite database.

---

## Features

-  Rule-based Sentiment Score System (+1 positive / -1 negative)
-  Review Classification (Positive / Negative / Neutral)
-  Sequential Processing (one-by-one execution)
-  Multiprocessing (parallel execution using CPU cores)
- Execution Time Comparison
- SQLite Database Storage of Results
- Process ID visualization to demonstrate parallel execution

---

## How It Works

1. Reads multiple text files containing customer reviews.
2. Applies rule-based sentiment scoring:
   - Positive words → +1
   - Negative words → -1
3. Calculates final sentiment category:
   - Score > 0 → Positive Review
   - Score < 0 → Negative Review
   - Score = 0 → Neutral Review
4. Compares performance:
   - Sequential execution time
   - Multiprocessing execution time
5. Stores final results in `reviews.db` (SQLite database).

---

## Technologies Used

- Python
- Multiprocessing Module
- SQLite (sqlite3)
- Time Module
- OS Module

---



>>>>>>> 3a7040bd6ed05a9c248279dfbb94189e42a95b59
