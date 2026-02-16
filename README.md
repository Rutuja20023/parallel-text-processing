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



