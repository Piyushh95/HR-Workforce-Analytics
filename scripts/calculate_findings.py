"""
calculate_findings.py
Extracts verified empirical findings from data/hr_analytics.db.
Demonstrates multi-dimensional retention analysis, explicit denominators,
methodological caveats, and non-causal descriptive interpretations.
"""

import os
import sqlite3
import pandas as pd

# Handle dynamic execution path
db_path = "data/hr_analytics.db" if os.path.exists("data/hr_analytics.db") else "HR-Workforce-Analytics/data/hr_analytics.db"
conn = sqlite3.connect(db_path)

print("=" * 80)
print("VERIFIED EMPIRICAL WORKFORCE FINDINGS & RETENTION DIAGNOSTICS")
print("=" * 80)

# ------------------------------------------------------------------------------
# FINDING 1: OVERTIME & COMPENSATION PARITY
# ------------------------------------------------------------------------------
print("\n=== FINDING 1: OVERTIME & PAYMENT STATUS ===")
df_ot = pd.read_sql_query("""
SELECT 
    payment_overtime,
    COUNT(*) as headcount,
    SUM(is_attrition) as leavers,
    COUNT(*) - SUM(is_attrition) as retained,
    ROUND(AVG(is_attrition) * 100.0, 2) as attrition_rate_pct
FROM employees
GROUP BY payment_overtime
ORDER BY attrition_rate_pct DESC;
""", conn)
print(df_ot.to_string(index=False))
print("\nInterpretation: Employees working uncompensated overtime exhibit a 51.77% attrition rate,")
print("compared to 39.42% for employees receiving paid overtime (a 12.35 percentage-point spread).")
print("Note: Descriptive correlation does not prove overtime causes turnover; uncompensated hours")
print("may co-occur with broader operational understaffing.")

# ------------------------------------------------------------------------------
# FINDING 2: TENURE LIFECYCLE & COMPARATIVE CONCENTRATION ANALYSIS
# ------------------------------------------------------------------------------
print("\n=== FINDING 2: TENURE LIFECYCLE (COMPARATIVE THREE-METRIC ANALYSIS) ===")
df_tenure = pd.read_sql_query("""
WITH tenure_summary AS (
    SELECT 
        tenure_last_org_band,
        estimated_tenure_years,
        COUNT(*) AS group_respondents,
        SUM(is_attrition) AS group_leavers
    FROM employees
    GROUP BY tenure_last_org_band, estimated_tenure_years
),
totals AS (
    SELECT 
        COUNT(*) AS total_respondents,
        SUM(is_attrition) AS total_leavers
    FROM employees
)
SELECT 
    t.tenure_last_org_band,
    t.estimated_tenure_years,
    t.group_respondents,
    t.group_leavers,
    -- Metric A: Attrition rate within each tenure group
    -- Denominator: All respondents within the specific tenure group
    ROUND(t.group_leavers * 100.0 / t.group_respondents, 2) AS group_attrition_rate_pct,
    -- Metric B: Share of all recorded leavers
    -- Denominator: Total recorded leavers across the entire dataset (515)
    ROUND(t.group_leavers * 100.0 / tot.total_leavers, 2) AS share_of_all_leavers_pct,
    -- Metric C: Share of all respondents
    -- Denominator: Total respondents across the entire dataset (1,191)
    ROUND(t.group_respondents * 100.0 / tot.total_respondents, 2) AS share_of_all_respondents_pct
FROM tenure_summary t
CROSS JOIN totals tot
ORDER BY t.estimated_tenure_years ASC;
""", conn)
print(df_tenure.to_string(index=False))

print("\n--- Detailed Breakdown for '<5 Years' Tenure Cohort ---")
u5 = df_tenure[df_tenure['tenure_last_org_band'] == 'Less than 5 years'].iloc[0]
print(f"1. Group Attrition Rate:     {u5['group_attrition_rate_pct']:.2f}% (Denominator: {int(u5['group_respondents']):,} respondents in <5 yrs group)")
print(f"2. Share of All Leavers:     {u5['share_of_all_leavers_pct']:.2f}% (Denominator: 515 total leavers dataset-wide)")
print(f"3. Share of All Respondents: {u5['share_of_all_respondents_pct']:.2f}% (Denominator: 1,191 total respondents dataset-wide)")

print("\n--- Methodological Warning on Tenure Interpretation ---")
print("WARNING: Tenure for non-leavers may be ambiguous because survey Question 7 specifically")
print("measures tenure at 'the last organization you left.' For respondents reporting no previous")
print("turnover (Attrition='No'), the available survey data does not establish whether recorded")
print("tenure represents completed prior tenure or current ongoing employment tenure.")
print("CRITICAL STATISTICAL DISTINCTION: A high share of all leavers (74.17%) in the <5 years cohort")
print("does NOT mean this group automatically has the highest attrition rate. Rather, this volume")
print("is a joint product of both an elevated attrition rate (53.35% vs 43.24% baseline) AND the fact")
print("that the <5 years cohort forms the clear majority of all surveyed respondents (60.12%).")
print("These descriptive comparisons must not be interpreted as causal effects.")

# ------------------------------------------------------------------------------
# FINDING 3: DEPARTMENTAL VARIATION & RISK TIERS (THRESHOLD N >= 20)
# ------------------------------------------------------------------------------
print("\n=== FINDING 3: DEPARTMENTAL VARIATION & RISK TIERS (THRESHOLD N >= 20) ===")
df_dept = pd.read_sql_query("""
WITH company AS (SELECT AVG(is_attrition) * 100.0 AS comp_avg FROM employees),
dept_all AS (
    SELECT 
        department,
        COUNT(*) AS total_headcount,
        SUM(is_attrition) AS leavers_count,
        ROUND(AVG(is_attrition) * 100.0, 2) AS attrition_rate_pct
    FROM employees
    GROUP BY department
),
dept_eligible AS (
    SELECT 
        department,
        ROUND(attrition_rate_pct - c.comp_avg, 2) AS variance_vs_company_pct,
        ROUND(attrition_rate_pct / c.comp_avg, 2) AS attrition_risk_index,
        CASE 
            WHEN attrition_rate_pct > c.comp_avg + 5.0 THEN 'High Risk (>5% Above Avg)'
            WHEN attrition_rate_pct < c.comp_avg - 5.0 THEN 'Low Risk (>5% Below Avg)'
            ELSE 'Moderate Risk'
        END AS risk_tier
    FROM dept_all
    CROSS JOIN company c
    GROUP BY department
    HAVING total_headcount >= 20
)
SELECT 
    d.department,
    d.total_headcount,
    d.leavers_count,
    d.attrition_rate_pct,
    e.variance_vs_company_pct,
    e.attrition_risk_index,
    CASE WHEN d.total_headcount < 20 THEN 1 ELSE 0 END AS small_sample,
    e.risk_tier
FROM dept_all d
LEFT JOIN dept_eligible e ON d.department = e.department
ORDER BY small_sample ASC, d.total_headcount DESC;
""", conn)
print(df_dept.to_string(index=False))
eligible_cnt = len(df_dept[df_dept['small_sample'] == 0])
small_cnt = len(df_dept[df_dept['small_sample'] == 1])
print(f"\nEligible Departments (N >= 20): {eligible_cnt} | Small-Sample Departments (N < 20): {small_cnt}")

# ------------------------------------------------------------------------------
# FINDING 4: JOB SATISFACTION GRADIENT
# ------------------------------------------------------------------------------
print("\n=== FINDING 4: JOB SATISFACTION GRADIENT ===")
df_sat = pd.read_sql_query("""
SELECT 
    job_satisfaction,
    COUNT(*) as headcount,
    SUM(is_attrition) as leavers,
    ROUND(AVG(is_attrition) * 100.0, 2) as attrition_rate_pct
FROM employees
GROUP BY job_satisfaction
ORDER BY job_satisfaction_score ASC;
""", conn)
print(df_sat.to_string(index=False))
print("\nInterpretation: Attrition drops monotonically from 58.36% ('Not satisfied')")
print("to 43.19% ('Satisfied') to 25.79% ('Very satisfied') — a 32.57 percentage-point gradient.")

# ------------------------------------------------------------------------------
# FINDING 5: PROMOTION FAIRNESS & RECOGNITION SYNERGY
# ------------------------------------------------------------------------------
print("\n=== FINDING 5: PROMOTION DESERVEDNESS VS RECOGNITION ===")
df_promo = pd.read_sql_query("""
SELECT 
    deserved_promotion,
    recognition,
    COUNT(*) as headcount,
    SUM(is_attrition) as leavers,
    ROUND(AVG(is_attrition) * 100.0, 2) as attrition_rate_pct
FROM employees
GROUP BY deserved_promotion, recognition
ORDER BY attrition_rate_pct DESC;
""", conn)
print(df_promo.to_string(index=False))
print("\nInterpretation: Staff receiving neither deserved promotion nor recognition experience")
print("55.91% attrition, while those receiving both experience 27.97% attrition (cut in half).")

conn.close()
