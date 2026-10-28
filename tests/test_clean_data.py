"""
test_clean_data.py
Unit tests for data cleaning, category normalization, and dataset validation.
Uses standard library unittest for seamless CI execution.
"""

import os
import unittest
import pandas as pd
import numpy as np

# Dynamically resolve base dir
base_dir = "." if os.path.exists("scripts") else "HR-Workforce-Analytics"

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


class TestCleanDataFunctions(unittest.TestCase):

    def test_clean_text(self):
        raw = "  Hello\xa0World   "
        self.assertEqual(clean_text(raw), "Hello World")
        self.assertTrue(pd.isna(clean_text(np.nan)))

    def test_clean_department(self):
        self.assertEqual(clean_department(" Administration"), "Administration")
        self.assertEqual(clean_department("HR"), "Human Resources")
        self.assertEqual(clean_department("technical support"), "Technical Support")
        self.assertEqual(clean_department("Customers service"), "Customer Service")
        self.assertEqual(clean_department("patient Affairs"), "Patient Affairs")

    def test_clean_sector(self):
        self.assertEqual(clean_sector("Medical sector"), "Medical")
        self.assertEqual(clean_sector("education sector"), "Education")
        self.assertEqual(clean_sector(" Energy sector"), "Energy")

    def test_clean_job_title(self):
        self.assertEqual(clean_job_title("Manger assistant"), "Manager Assistant")
        self.assertEqual(clean_job_title("  accountant  "), "Accountant")
        self.assertEqual(clean_job_title("IT specialist"), "IT Specialist")

    def test_salary_band_and_midpoint(self):
        raw_band = " From 5000 to 10000 S.R\xa0"
        cleaned = clean_salary_band(raw_band)
        self.assertEqual(cleaned, "5,000 to 10,000 SAR")
        midpoint = calculate_salary_midpoint(cleaned)
        self.assertEqual(midpoint, 7500.0)

        cleaned_low = clean_salary_band("Less than 5000 SAR")
        self.assertEqual(calculate_salary_midpoint(cleaned_low), 2500.0)

    def test_tenure_midpoint(self):
        self.assertEqual(calculate_tenure_midpoint("Less than 5 years"), 2.5)
        self.assertEqual(calculate_tenure_midpoint("From 5 to 10 years"), 7.5)
        self.assertEqual(calculate_tenure_midpoint("From 11 to 15 years"), 13.0)

    def test_full_dataset_pipeline(self):
        raw_path = os.path.join(base_dir, "data", "raw", "Original Dataset of Employee Attrition.xlsx")
        processed_path = os.path.join(base_dir, "data", "processed", "cleaned_employee_attrition.csv")
        
        if os.path.exists(raw_path):
            df = clean_dataset(raw_path)
        elif os.path.exists(processed_path):
            df = pd.read_csv(processed_path)
        else:
            self.skipTest("Neither raw dataset nor processed dataset found")
            
        # 1. Exact record count preservation
        self.assertEqual(len(df), 1191, "Row count must strictly remain 1,191")
        
        # 2. No nulls allowed
        self.assertEqual(df.isnull().sum().sum(), 0, "No null values allowed in cleaned dataset")
        
        # 3. Primary key integrity
        self.assertEqual(df['employee_id'].nunique(), 1191, "employee_id must be strictly unique")
        
        # 4. Attrition count preservation
        self.assertEqual(df['is_attrition'].sum(), 515, "Attrition count must remain exactly 515")
        self.assertAlmostEqual(df['is_attrition'].mean(), 0.4324, places=3)
        
        # 5. Check duplicate profile flagging
        self.assertEqual(df['is_potential_duplicate_profile'].sum(), 2)


if __name__ == '__main__':
    unittest.main()
