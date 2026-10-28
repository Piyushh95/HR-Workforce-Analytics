"""
load_database.py
Loads the cleaned HR dataset from data/processed/cleaned_employee_attrition.csv
into an SQLite database table named 'employees'.
Creates indexes for efficient querying and verifies data integrity.
"""

import os
import sqlite3
import pandas as pd


def load_database(
    csv_path: str = "data/processed/cleaned_employee_attrition.csv",
    db_path: str = "data/hr_analytics.db"
) -> sqlite3.Connection:
    print("=" * 70)
    print("LOADING CLEANED HR DATASET INTO SQLITE DATABASE")
    print("=" * 70)
    
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"Cleaned CSV not found at {csv_path}. Run clean_data.py first.")
        
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    
    df = pd.read_csv(csv_path)
    print(f"Loaded {len(df)} rows from {csv_path}")
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Drop table if exists to ensure idempotent re-runs
    cursor.execute("DROP TABLE IF EXISTS employees;")
    
    # Write to SQLite
    df.to_sql('employees', conn, if_exists='replace', index=False)
    
    # Create indexes for high-frequency filter and group columns
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_emp_dept ON employees(department);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_emp_attrition ON employees(attrition);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_emp_salary ON employees(monthly_salary_band);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_emp_tenure ON employees(tenure_last_org_band);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_emp_satisfaction ON employees(job_satisfaction);")
    
    conn.commit()
    
    # Verification query
    cursor.execute("SELECT COUNT(*) FROM employees;")
    row_count = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(DISTINCT employee_id) FROM employees;")
    distinct_ids = cursor.fetchone()[0]
    
    cursor.execute("SELECT SUM(is_attrition), ROUND(AVG(is_attrition) * 100.0, 2) FROM employees;")
    attr_count, attr_rate = cursor.fetchone()
    
    print(f"\n--- SQLite Database Verification (`{db_path}`) ---")
    print(f"Target Table: 'employees'")
    print(f"Total Rows: {row_count}")
    print(f"Distinct Primary Keys (employee_id): {distinct_ids}")
    print(f"Attrition Count: {attr_count}")
    print(f"Attrition Rate: {attr_rate}%")
    print("Indexes created: department, attrition, monthly_salary_band, tenure_last_org_band, job_satisfaction")
    print("=" * 70)
    
    return conn


if __name__ == "__main__":
    conn = load_database()
    conn.close()
