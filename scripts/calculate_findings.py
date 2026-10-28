"""
calculate_findings.py
Extracts verified empirical findings from data/hr_analytics.db.
"""

import sqlite3
import pandas as pd

conn = sqlite3.connect("data/hr_analytics.db")

print("=== FINDING 1: OVERTIME & PAYMENT STATUS ===")
df_ot = pd.read_sql_query("""
SELECT 
    payment_overtime,
    COUNT(*) as headcount,
    SUM(is_attrition) as leavers,
    ROUND(AVG(is_attrition) * 100.0, 2) as attrition_rate
FROM employees
GROUP BY payment_overtime
ORDER BY attrition_rate DESC;
""", conn)
print(df_ot)

print("\n=== FINDING 2: TENURE LIFECYCLE (EARLY CAREER FLIGHT RISK) ===")
df_tenure = pd.read_sql_query("""
SELECT 
    tenure_last_org_band,
    COUNT(*) as headcount,
    SUM(is_attrition) as leavers,
    ROUND(AVG(is_attrition) * 100.0, 2) as attrition_rate,
    ROUND(SUM(is_attrition) * 100.0 / (SELECT SUM(is_attrition) FROM employees), 2) as pct_of_all_leavers
FROM employees
GROUP BY tenure_last_org_band
ORDER BY estimated_tenure_years ASC;
""", conn)
print(df_tenure)

print("\n=== FINDING 3: DEPARTMENTAL VARIATION & RISK TIERS ===")
df_dept = pd.read_sql_query("""
SELECT 
    department,
    COUNT(*) as headcount,
    SUM(is_attrition) as leavers,
    ROUND(AVG(is_attrition) * 100.0, 2) as attrition_rate
FROM employees
GROUP BY department
HAVING COUNT(*) >= 25
ORDER BY attrition_rate DESC;
""", conn)
print(df_dept)

print("\n=== FINDING 4: JOB SATISFACTION GRADIENT ===")
df_sat = pd.read_sql_query("""
SELECT 
    job_satisfaction,
    COUNT(*) as headcount,
    SUM(is_attrition) as leavers,
    ROUND(AVG(is_attrition) * 100.0, 2) as attrition_rate
FROM employees
GROUP BY job_satisfaction
ORDER BY job_satisfaction_score ASC;
""", conn)
print(df_sat)

print("\n=== FINDING 5: PROMOTION DESERVEDNESS VS RECOGNITION ===")
df_promo = pd.read_sql_query("""
SELECT 
    deserved_promotion,
    recognition,
    COUNT(*) as headcount,
    SUM(is_attrition) as leavers,
    ROUND(AVG(is_attrition) * 100.0, 2) as attrition_rate
FROM employees
GROUP BY deserved_promotion, recognition
ORDER BY attrition_rate DESC;
""", conn)
print(df_promo)

conn.close()
