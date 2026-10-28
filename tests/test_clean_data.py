"""
test_clean_data.py
Unit tests for data cleaning, category normalization, and dataset validation.
"""

import os
import pytest
import pandas as pd
import numpy as np

from scripts.clean_data import (
    clean_text,
    clean_department,
    clean_sector,
    clean_job_title,
    clean_salary_band,
    calculate_salary_midpoint,
    calculate_tenure_midpoint,
    clean_dataset
)


def test_clean_text():
    raw = "  Hello\xa0World   "
    assert clean_text(raw) == "Hello World"
    assert pd.isna(clean_text(np.nan))


def test_clean_department():
    assert clean_department(" Administration") == "Administration"
    assert clean_department("HR") == "Human Resources"
    assert clean_department("technical support") == "Technical Support"
    assert clean_department("Customers service") == "Customer Service"
    assert clean_department("patient Affairs") == "Patient Affairs"


def test_clean_sector():
    assert clean_sector("Medical sector") == "Medical"
    assert clean_sector("education sector") == "Education"
    assert clean_sector(" Energy sector") == "Energy"


def test_clean_job_title():
    assert clean_job_title("Manger assistant") == "Manager Assistant"
    assert clean_job_title("  accountant  ") == "Accountant"
    assert clean_job_title("IT specialist") == "IT Specialist"


def test_salary_band_and_midpoint():
    raw_band = " From 5000 to 10000 S.R\xa0"
    cleaned = clean_salary_band(raw_band)
    assert cleaned == "5,000 to 10,000 SAR"
    midpoint = calculate_salary_midpoint(cleaned)
    assert midpoint == 7500.0


def test_tenure_midpoint():
    assert calculate_tenure_midpoint("Less than 5 years") == 2.5
    assert calculate_tenure_midpoint("From 5 to 10 years") == 7.5
    assert calculate_tenure_midpoint("From 11 to 15 years") == 13.0


def test_full_dataset_pipeline():
    raw_path = os.path.join("data", "raw", "Original Dataset of Employee Attrition.xlsx")
    if not os.path.exists(raw_path):
        pytest.skip("Raw file not found in test environment")
        
    df = clean_dataset(raw_path)
    
    # 1. Exact record count preservation
    assert len(df) == 1191, "Row count must strictly remain 1,191"
    
    # 2. No nulls allowed
    assert df.isnull().sum().sum() == 0, "No null values allowed in cleaned dataset"
    
    # 3. Primary key integrity
    assert df['employee_id'].nunique() == 1191, "employee_id must be strictly unique"
    
    # 4. Attrition count preservation
    assert df['is_attrition'].sum() == 515, "Attrition count must remain exactly 515"
    assert pytest.approx(df['is_attrition'].mean(), 0.001) == 0.4324
    
    # 5. Check duplicate profile flagging
    assert df['is_potential_duplicate_profile'].sum() == 2
