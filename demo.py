import time
import os
from multiprocessing import Pool

# -----------------------------------
# RULE CHECKER WITH SENTIMENT SCORE
# -----------------------------------
def rule_checker(text):
    words = text.lower().split()

    positive_words = ["happy", "satisfied", "excellent", "good", "helpful", "recommend"]
    negative_words = ["unhappy", "poor", "damaged", "delayed", "disappointed", "bad"]

    score = 0
    for word in words:
        if word in positive_words:
            score += 1
        elif word in negative_words:
            score -= 1

    if score > 0:
        category = "Positive Review"
    elif score < 0:
        category = "Negative Review"
    else:
        category = "Neutral Review"

    return category, score


# -----------------------------------
# FILE PROCESSING FUNCTION
# -----------------------------------
def process_file(file_path):
    process_id = os.getpid()

    print(f"START Processing {file_path} | Process ID: {process_id}")

    # Simulate heavy processing (2 seconds)
    time.sleep(2)

    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read()

    category, score = rule_checker(text)

    print(f"END   Processing {file_path} | Process ID: {process_id}")

    return file_path, category, score


# -----------------------------------
# SEQUENTIAL PROCESSING
# -----------------------------------
def run_sequential(files):
    start = time.time()

    results = []
    for file in files:
        results.append(process_file(file))

    end = time.time()
    return results, end - start


# -----------------------------------
# MULTIPROCESSING
# -----------------------------------
def run_multiprocessing(files):
    start = time.time()

    with Pool(processes=os.cpu_count()) as pool:
        results = pool.map(process_file, files)

    end = time.time()
    return results, end - start


# -----------------------------------
# MAIN
# -----------------------------------
if __name__ == "__main__":

    files = [
        r"E:\Internship\text1.txt",
        r"E:\Internship\text2.txt",
        r"E:\Internship\text3.txt",
        r"E:\Internship\text4.txt",
    ]

    print("CPU Cores Available:", os.cpu_count())

    # -------- Sequential --------
    print("\n===== SEQUENTIAL PROCESSING =====\n")
    seq_results, seq_time = run_sequential(files)

    print("\nSequential Final Results:")
    for file, category, score in seq_results:
        print(f"{file} → {category} | Score: {score}")

    print(f"\nSequential Time: {seq_time:.2f} seconds")


    # -------- Multiprocessing --------
    print("\n===== MULTIPROCESSING =====\n")
    mp_results, mp_time = run_multiprocessing(files)

    print("\nMultiprocessing Final Results:")
    for file, category, score in mp_results:
        print(f"{file} → {category} | Score: {score}")

    print(f"\nMultiprocessing Time: {mp_time:.2f} seconds")


    # -------- Comparison --------
    print("\n===== PERFORMANCE COMPARISON =====")
    print(f"Sequential Time      : {seq_time:.2f} seconds")
    print(f"Multiprocessing Time : {mp_time:.2f} seconds")

    if mp_time < seq_time:
        print("Multiprocessing is Faster 🚀 (Parallel Confirmed)")
    else:
        print("Sequential is Faster (Small Workload Case)")
