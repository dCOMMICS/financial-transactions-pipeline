import polars as pl
import pytest
from src.data_processor import get_processing_stats, validate_data


def make_sample_df() -> pl.DataFrame:
    return pl.DataFrame({
        "transaction_id":   ["t1", "t2", "t3", "t4"],
        "customer_id":      ["c1", "c1", "c2", "c3"],
        "transaction_type": ["PAYMENT", "DEPOSIT", "PAYMENT", "WITHDRAWAL"],
        "status":           ["COMPLETED", "COMPLETED", "PENDING", "COMPLETED"],
        "amount":           [100.0, 200.0, 50.0, 150.0],
        "currency":         ["KES", "KES", "KES", "KES"],
        "date":             ["2026-01-01", "2026-01-02", "2026-01-03", "2026-01-04"],
        "customer_name":    ["Alice", "Alice", "Bob", "Charlie"],
        "customer_email":   ["a@example.com", "a@example.com", "b@example.com", "c@example.com"],
        "ip_address":       ["192.168.0.1", "192.168.0.2", "192.168.0.3", "192.168.0.4"],
        "device":           ["mobile", "desktop", "tablet", "mobile"],
        "location":         ["Nairobi", "Mombasa", "Kisumu", "Nakuru"],
    })


# Test 1: Valid data returns correct stats
def test_get_processing_stats_valid_data():
    df = make_sample_df()
    stats = get_processing_stats(df)

    assert stats["total_records"] == 4
    assert stats["unique_customers"] == 3
    assert stats["transactions_by_type"]["PAYMENT"] == 2
    assert stats["transactions_by_type"]["DEPOSIT"] == 1
    assert stats["transactions_by_status"]["COMPLETED"] == 3
    assert stats["amount_stats"]["min"] == 50.0
    assert stats["amount_stats"]["max"] == 200.0
    assert stats["amount_stats"]["mean"] == 125.0


# Test 2: Empty DataFrame is handled gracefully
def test_get_processing_stats_empty_dataframe():
    df = pl.DataFrame({
        "transaction_id":   [],
        "customer_id":      [],
        "transaction_type": [],
        "status":           [],
        "amount":           pl.Series([], dtype=pl.Float64),
        "currency":         [],
        "date":             [],
        "customer_name":    [],
        "customer_email":   [],
        "ip_address":       [],
        "device":           [],
        "location":         [],
    })
    stats = get_processing_stats(df)

    assert stats["total_records"] == 0
    assert stats["unique_customers"] == 0
    assert stats["transactions_by_type"] == {}
    assert stats["transactions_by_status"] == {}
    assert stats["amount_stats"] == {"min": 0.0, "max": 0.0, "mean": 0.0}


# Test 3: validate_data filters out invalid rows
def test_validate_data_filters_invalid_rows():
    df = pl.DataFrame({
        "transaction_id":   ["t1", "t2", "t3"],
        "customer_id":      ["c1", "c2", "c3"],
        "transaction_type": ["PAYMENT", "DEPOSIT", "PAYMENT"],
        "status":           ["COMPLETED", "PENDING", "COMPLETED"],
        "amount":           [100.0, -50.0, 75.0],  # t2 is invalid (negative amount)
        "currency":         ["KES", "KES", "KES"],
        "date":             ["2026-01-01", "2026-01-02", "2026-01-03"],
        "customer_name":    ["Alice", "Bob", "Charlie"],
        "customer_email":   ["a@example.com", "b@example.com", "c@example.com"],
        "ip_address":       ["192.168.0.1", "192.168.0.2", "192.168.0.3"],
        "device":           ["mobile", "desktop", "tablet"],
        "location":         ["Nairobi", "Mombasa", "Kisumu"],
    })
    result = validate_data(df)

    assert len(result) == 2  # only t1 and t3 pass
    assert all(amount >= 0 for amount in result["amount"].to_list())


# Test 4 (bonus): All required keys are present in stats
def test_get_processing_stats_has_all_keys():
    df = make_sample_df()
    stats = get_processing_stats(df)

    assert "total_records" in stats
    assert "unique_customers" in stats
    assert "transactions_by_type" in stats
    assert "transactions_by_status" in stats
    assert "amount_stats" in stats
    assert {"min", "max", "mean"} == set(stats["amount_stats"].keys())