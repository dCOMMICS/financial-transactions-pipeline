# Task 1 - Code Comprehension Answers

**Q1.** The Pydantic model used to validate CSV transaction data is `TransactionFlat`. 

**Q2.** Rows that fail Pydantic validation are discarded. 

**Q3.** The `clean_data()` function fills null values in three columns: `ip_address`, `device`, and `location`. All three are filled with the default string `"unknown"`.

**Q4.** Duplicate transactions are prevented in two ways. First, the `transactions` table defines `transaction_id` as a `PRIMARY KEY`, enforcing uniqueness at the database level. Second, the `store_data` function fetches all existing `transaction_id` values before inserting and filters them out — so only records with new IDs are inserted.

**Q5.** The JSON output contains two nested objects per transaction: `customer` and `metadata`. The `customer` object contains `customer_id`, `name`, and `email`. The `metadata` object contains `ip_address`, `device`, and `location`.