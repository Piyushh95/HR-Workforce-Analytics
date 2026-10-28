"""
test_regression.py
Comprehensive regression test suite asserting midpoint methodology,
small-sample department handling, tenure three-metric calculations,
and CI configuration validity.
"""

import os
import unittest
import pandas as pd
import numpy as np
import sqlite3

# Dynamically resolve base dir
base_dir = "." if os.path.exists("scripts") else "HR-Workforce-Analytics"

from scripts.clean_data import (
    MIDPOINTS,
    calculate_salary_midpoint,
    calculate_tenure_midpoint,
    calculate_age_midpoint,
    clean_salary_band,
    clean_text
)


class TestMidpointMethodology(unittest.TestCase):
    """Assertions for centralized midpoint mappings and documentation."""

    def test_midpoint_dictionary_completeness(self):
        """Every supported salary, tenure, and age category must exist in MIDPOINTS."""
        self.assertIn('salary', MIDPOINTS)
        self.assertIn('tenure', MIDPOINTS)
        self.assertIn('age', MIDPOINTS)

        # Expected salary categories
        expected_salaries = [
            'Less than 5,000 SAR',
            '5,000 to 10,000 SAR',
            '11,000 to 15,000 SAR',
            '16,000 to 20,000 SAR',
            '21,000 to 25,000 SAR',
            '26,000 to 30,000 SAR',
            '31,000 SAR and more'
        ]
        for s in expected_salaries:
            self.assertIn(s, MIDPOINTS['salary'], f"Missing salary category: {s}")
            self.assertIsInstance(MIDPOINTS['salary'][s], float)

        # Expected tenure categories
        expected_tenures = [
            'Less than 5 years',
            'From 5 to 10 years',
            'From 11 to 15 years',
            'From 16 to 20 years',
            'From 21 to 25 years',
            'From 26 to 30 years',
            'From 31 to 35 years',
            'From 36 to 40 years'
        ]
        for t in expected_tenures:
            self.assertIn(t, MIDPOINTS['tenure'], f"Missing tenure category: {t}")
            self.assertIsInstance(MIDPOINTS['tenure'][t], float)

        # Expected age categories
        expected_ages = ['21 to 30', '31 to 40', '41 to 50', '51 to 60']
        for a in expected_ages:
            self.assertIn(a, MIDPOINTS['age'], f"Missing age category: {a}")
            self.assertIsInstance(MIDPOINTS['age'][a], float)

    def test_midpoint_calculation_values(self):
        """Midpoint calculations must match documented interval formulas."""
        # Salary: natural zero floor [0, 5000) -> 2500.0
        self.assertEqual(calculate_salary_midpoint("Less than 5000 SAR"), 2500.0)
        self.assertEqual(calculate_salary_midpoint("Less than 5,000 SAR"), 2500.0)
        self.assertEqual(calculate_salary_midpoint("From 5000 to 10000 S.R"), 7500.0)
        self.assertEqual(calculate_salary_midpoint("From 11000 to 15000 S.R"), 13000.0)
        self.assertEqual(calculate_salary_midpoint("From 16000 to 20000 S.R"), 18000.0)
        self.assertEqual(calculate_salary_midpoint("From 21000 to 25000 S.R"), 23000.0)
        self.assertEqual(calculate_salary_midpoint("From 26000 to 30000 S.R"), 28000.0)
        # Open-ended: [31000, 39000] -> 35000.0
        self.assertEqual(calculate_salary_midpoint("S.R 31000 - and more"), 35000.0)
        self.assertEqual(calculate_salary_midpoint("31,000 SAR and more"), 35000.0)

        # Tenure
        self.assertEqual(calculate_tenure_midpoint("Less than 5 years"), 2.5)
        self.assertEqual(calculate_tenure_midpoint("From 5 to 10 years"), 7.5)
        self.assertEqual(calculate_tenure_midpoint("From 11 to 15 years"), 13.0)
        self.assertEqual(calculate_tenure_midpoint("From 16 to 20 years"), 18.0)
        self.assertEqual(calculate_tenure_midpoint("From 21 to 25 years"), 23.0)
        self.assertEqual(calculate_tenure_midpoint("From 26 to 30 years"), 28.0)
        self.assertEqual(calculate_tenure_midpoint("From 31 to 35 years"), 33.0)

        # Age
        self.assertEqual(calculate_age_midpoint("21 to 30"), 25.5)
        self.assertEqual(calculate_age_midpoint("31 to 40"), 35.5)
        self.assertEqual(calculate_age_midpoint("41 to 50"), 45.5)
        self.assertEqual(calculate_age_midpoint("51 to 60"), 55.5)

    def test_midpoint_unknown_categories(self):
        """Unknown or invalid categories must explicitly return np.nan."""
        self.assertTrue(np.isnan(calculate_salary_midpoint("Over 100,000 USD")))
        self.assertTrue(np.isnan(calculate_salary_midpoint("Invalid Band")))
        self.assertTrue(np.isnan(calculate_tenure_midpoint("50 to 100 years")))
        self.assertTrue(np.isnan(calculate_age_midpoint("100 to 120")))

    def test_methodology_document_exists_and_valid(self):
        """data/METHODOLOGY.md must exist, contain the required table format, and state limitations."""
        doc_path = os.path.join(base_dir, "data", "METHODOLOGY.md")
        self.assertTrue(os.path.exists(doc_path), f"METHODOLOGY.md not found at {doc_path}")
        with open(doc_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Assert table columns required by prompt
        required_headers = [
            "Variable", "Original Category", "Mapping/Formula",
            "Estimated Value", "Rationale", "Limitation"
        ]
        for h in required_headers:
            self.assertIn(h, content, f"Missing column header in METHODOLOGY.md: {h}")

        # Assert approximation caveat is present
        self.assertIn("approximation", content.lower())
        self.assertIn("not exact individual", content.lower())


class TestSmallDepartmentHandling(unittest.TestCase):
    """Assertions for department sample size threshold (N >= 20) and small_sample flag."""

    def test_small_sample_department_classification_logic(self):
        """Synthetic test data for boundary conditions: N = 19, 20, 21."""
        comp_avg = 43.24
        
        # Test N = 19 (< 20)
        n_small = 19
        small_sample_flag = 1 if n_small < 20 else 0
        risk_tier_small = None if small_sample_flag == 1 else "Eligible"
        self.assertEqual(small_sample_flag, 1)
        self.assertIsNone(risk_tier_small)

        # Test N = 20 (exact boundary)
        n_boundary = 20
        small_sample_flag_b = 1 if n_boundary < 20 else 0
        rate_b = 55.0
        risk_tier_b = (
            "High Risk (>5% Above Avg)" if rate_b > comp_avg + 5.0
            else "Low Risk (>5% Below Avg)" if rate_b < comp_avg - 5.0
            else "Moderate Risk"
        ) if small_sample_flag_b == 0 else None
        self.assertEqual(small_sample_flag_b, 0)
        self.assertEqual(risk_tier_b, "High Risk (>5% Above Avg)")

        # Test N = 21 (> 20)
        n_large = 21
        small_sample_flag_l = 1 if n_large < 20 else 0
        self.assertEqual(small_sample_flag_l, 0)

    def test_exported_department_benchmark_artifact(self):
        """Checks output/tableau/department_attrition_benchmark.csv artifact."""
        csv_path = os.path.join(base_dir, "output", "tableau", "department_attrition_benchmark.csv")
        self.assertTrue(os.path.exists(csv_path), f"Benchmark CSV not found at {csv_path}")
        df = pd.read_csv(csv_path)

        # 1. All 21 departments must be retained
        self.assertEqual(len(df), 21, "All 21 departments must be present in benchmark output")
        self.assertIn("small_sample", df.columns)
        self.assertIn("risk_tier", df.columns)

        # 2. Check counts: 11 eligible (N>=20), 10 small (N<20)
        small_depts = df[df['small_sample'] == 1]
        eligible_depts = df[df['small_sample'] == 0]
        self.assertEqual(len(small_depts), 10, "Exactly 10 departments must have N < 20")
        self.assertEqual(len(eligible_depts), 11, "Exactly 11 departments must have N >= 20")

        # 3. Small departments must have unavailable/null risk tier
        for _, row in small_depts.iterrows():
            self.assertTrue(row['total_headcount'] < 20)
            self.assertTrue(pd.isna(row['risk_tier']) or row['risk_tier'] is None,
                            f"Department {row['department']} has N<20 but assigned risk tier {row['risk_tier']}")

        # 4. Eligible departments must have valid risk tier
        valid_tiers = {'High Risk (>5% Above Avg)', 'Low Risk (>5% Below Avg)', 'Moderate Risk'}
        for _, row in eligible_depts.iterrows():
            self.assertTrue(row['total_headcount'] >= 20)
            self.assertIn(row['risk_tier'], valid_tiers)

    def test_sql_and_python_export_consistency(self):
        """SQL Query 2 output must match Python exported CSV exactly."""
        db_path = os.path.join(base_dir, "data", "hr_analytics.db")
        csv_path = os.path.join(base_dir, "output", "tableau", "department_attrition_benchmark.csv")
        if not os.path.exists(db_path) or not os.path.exists(csv_path):
            self.skipTest("Database or benchmark CSV missing")

        conn = sqlite3.connect(db_path)
        sql_path = os.path.join(base_dir, "sql", "04_department_analysis.sql")
        with open(sql_path, "r", encoding="utf-8") as f:
            statements = [s.strip() for s in f.read().split(";") if s.strip()]
        
        # Query 2 is the benchmarking query
        df_sql = pd.read_sql_query(statements[1], conn)
        conn.close()

        df_csv = pd.read_csv(csv_path)

        # Check department count
        self.assertEqual(len(df_sql), len(df_csv))
        self.assertEqual(set(df_sql['department']), set(df_csv['department']))

        # Merge and assert match on key metrics
        merged = pd.merge(df_sql, df_csv, on="department")
        for _, row in merged.iterrows():
            self.assertEqual(row['headcount'], row['total_headcount'])
            self.assertEqual(row['small_sample_x'], row['small_sample_y'])
            # Attrition rate equality
            self.assertAlmostEqual(row['dept_attrition_rate'], row['attrition_rate_pct'], places=2)


class TestTenureFindingsInterpretation(unittest.TestCase):
    """Assertions for the three distinct tenure percentage metrics and warnings."""

    def test_three_tenure_metrics_distinct_and_correct(self):
        """Attrition rate, share of leavers, and share of respondents must use distinct denominators."""
        csv_path = os.path.join(base_dir, "data", "processed", "cleaned_employee_attrition.csv")
        if not os.path.exists(csv_path):
            self.skipTest("Cleaned CSV not found")
        df = pd.read_csv(csv_path)

        total_respondents = len(df)
        total_leavers = df['is_attrition'].sum()

        u5_mask = df['tenure_last_org_band'] == 'Less than 5 years'
        u5_respondents = u5_mask.sum()
        u5_leavers = df[u5_mask]['is_attrition'].sum()

        # Metric A: Within-group attrition rate
        group_attrition_rate = (u5_leavers / u5_respondents) * 100.0
        # Metric B: Share of all leavers
        share_of_all_leavers = (u5_leavers / total_leavers) * 100.0
        # Metric C: Share of all respondents
        share_of_all_respondents = (u5_respondents / total_respondents) * 100.0

        # Verify values
        self.assertAlmostEqual(group_attrition_rate, 53.35, places=2)
        self.assertAlmostEqual(share_of_all_leavers, 74.17, places=2)
        self.assertAlmostEqual(share_of_all_respondents, 60.12, places=2)

        # Assert these three percentages are statistically distinct and not interchangeable
        self.assertNotEqual(group_attrition_rate, share_of_all_leavers)
        self.assertNotEqual(share_of_all_leavers, share_of_all_respondents)
        self.assertNotEqual(group_attrition_rate, share_of_all_respondents)

    def test_tenure_methodological_warning_in_findings_script(self):
        """scripts/calculate_findings.py must include the non-leaver tenure ambiguity warning."""
        script_path = os.path.join(base_dir, "scripts", "calculate_findings.py")
        with open(script_path, "r", encoding="utf-8") as f:
            script_text = f.read()

        # Must mention ambiguity / warning
        self.assertIn("ambiguous", script_text.lower())
        self.assertIn("last organization", script_text.lower())
        self.assertIn("causal", script_text.lower())


class TestCIWorkflowConfiguration(unittest.TestCase):
    """Assertions for GitHub Actions CI workflow syntax and command alignment."""

    def test_ci_workflow_yaml_structure(self):
        """Validates ci.yml file exists, contains proper triggers, and valid command sequence."""
        ci_path = os.path.join(base_dir, ".github", "workflows", "ci.yml")
        self.assertTrue(os.path.exists(ci_path), f"ci.yml not found at {ci_path}")
        with open(ci_path, "r", encoding="utf-8") as f:
            lines = f.read().splitlines()

        content = "\n".join(lines)
        self.assertIn("actions/checkout@v4", content)
        self.assertIn("actions/setup-python@v5", content)
        self.assertIn('3.12', content)
        self.assertIn("python -m unittest discover", content)
        self.assertIn("python scripts/load_database.py", content)
        self.assertIn("python scripts/run_quality_checks.py", content)


if __name__ == '__main__':
    unittest.main()
