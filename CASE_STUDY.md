# 🧪 Phoenix Mentee Screening — Case Study

## Financial Transaction Data Pipeline

**Difficulty:** Beginner–Intermediate  
**Estimated Time:** 1 hour  
**Tools:** Python, Polars, Pydantic, pytest

---

## 📖 Background

You have been given a working **Financial Transaction Data Pipeline** that generates simulated financial data, processes and validates it, and stores it in a DuckDB database. An API layer also exists but is **not the focus** of this assessment.

Your goal is to demonstrate that you can **read and understand** an unfamiliar codebase, **write clean Python**, and **test your work**.

---

## 🚀 Getting Started

```bash
cd financial-transactions-pipeline

# Create and activate a virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # macOS/Linux

# Install dependencies
pip install -r requirements.txt

# Run the pipeline
python -m src.main
```

You should see log output about generating data, processing files, and storing records. If it runs without errors, you're all set.

---

## ✅ Tasks

Complete **all 3 tasks** below.

---

### Task 1: Code Comprehension (answer in `answers.md`)

Review the source code in `src/` and answer these questions:

1. What **Pydantic model** is used to validate CSV transaction data? (Give the class name from `models.py`)
2. In `data_processor.py`, what happens to rows that **fail** Pydantic validation — are they included in the final output or discarded?
3. The `clean_data()` function fills `null` values in certain columns with a default string. What columns are affected, and what default value is used?
4. How does `db.py` prevent **duplicate transactions** from being inserted into the database? Describe the mechanism in 1–2 sentences.
5. In `data_generator.py`, the JSON output uses a **nested** structure for customer data. Name the two nested objects and the fields each contains.

---

### Task 2: Add a Data Processing Feature

The pipeline currently does not track or report any **statistics** about the data it processes. Add a function called `get_processing_stats` to `src/data_processor.py` that takes a Polars DataFrame (after cleaning) and returns a dictionary with the following keys:

```python
{
    "total_records": int,              # Total number of records
    "unique_customers": int,           # Number of distinct customer_id values
    "transactions_by_type": dict,      # Count of each transaction_type, e.g. {"PAYMENT": 45, "DEPOSIT": 30, ...}
    "transactions_by_status": dict,    # Count of each status, e.g. {"COMPLETED": 50, "PENDING": 40, ...}
    "amount_stats": {
        "min": float,                  # Minimum transaction amount
        "max": float,                  # Maximum transaction amount
        "mean": float                  # Average transaction amount (rounded to 2 decimal places)
    }
}
```

Then, **call this function** in `src/main.py` after the data is processed (after the `process_multiple_files` call) and **log the stats** using the existing logger. For example:

```
INFO - Processing Stats: {'total_records': 500, 'unique_customers': 312, ...}
```

---

### Task 3: Write Tests

Create a file `tests/test_data_processor.py` with **at least 3** unit tests using `pytest`:

1. **Test `get_processing_stats` with valid data** — Create a small Polars DataFrame with known values, pass it to your function, and assert the returned dictionary matches expected values.

2. **Test `get_processing_stats` with an empty DataFrame** — Pass an empty DataFrame and assert the function handles it gracefully (no crashes; sensible defaults like zeros).

3. **Test `validate_data` filters out invalid rows** — Create a DataFrame with a mix of valid and invalid rows (e.g., a negative amount or an invalid date), pass it through `validate_data`, and assert only the valid rows remain.

Run your tests with:
```bash
python -m pytest tests/ -v
```

---

## 📦 What to Submit

| Item | Description |
|------|-------------|
| `answers.md` | Answers to Task 1 (in the project root) |
| `src/data_processor.py` | Updated with `get_processing_stats` |
| `src/main.py` | Updated to call and log the stats |
| `tests/test_data_processor.py` | Your unit tests for Task 3 |
| Terminal output or screenshot | Showing (a) the pipeline running with stats logged, and (b) tests passing |

---

## 🏆 Evaluation Criteria

| Criteria | Weight |
|----------|--------|
| **Correctness** — Do the answers, code, and tests work as specified? | 40% |
| **Code Quality** — Is the new code clean, readable, and consistent with the existing style? | 25% |
| **Understanding** — Do the answers show real comprehension of the codebase? | 20% |
| **Testing** — Are the tests meaningful and do they cover edge cases? | 15% |

---

> **Tip:** You are encouraged to explore all files in the repo. The goal is to show you can navigate an unfamiliar codebase and make thoughtful contributions. Good luck! 🚀
