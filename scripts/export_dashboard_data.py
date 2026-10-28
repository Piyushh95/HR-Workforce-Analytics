"""
export_dashboard_data.py
Exports clean, documented, Tableau-ready CSV files from data/hr_analytics.db
and data/processed/cleaned_employee_attrition.csv.
"""

import os
import sqlite3
import pandas as pd


def export_dashboard_data(
    db_path: str = "data/hr_analytics.db",
    csv_src: str = "data/processed/cleaned_employee_attrition.csv",
    output_dir: str = "output/tableau"
):
    print("=" * 70)
    print("EXPORTING TABLEAU & BI DASHBOARD DATASETS")
    print("=" * 70)
    
    os.makedirs(output_dir, exist_ok=True)
    
    # 1. Master Employee-Level Dataset (Primary Tableau Source)
    df_master = pd.read_csv(csv_src)
    master_path = os.path.join(output_dir, "hr_workforce_master.csv")
    df_master.to_csv(master_path, index=False)
    print(f"1. Master Employee Dataset: {master_path} ({len(df_master)} rows)")
    
    conn = sqlite3.connect(db_path)
    
    # 2. Executive KPI Summary Table
    kpi_query = """
    SELECT
        COUNT(*) AS total_headcount,
        SUM(is_attrition) AS total_leavers,
        COUNT(*) - SUM(is_attrition) AS total_retained,
        ROUND(AVG(is_attrition) * 100.0, 2) AS attrition_rate_pct,
        ROUND(AVG(estimated_tenure_years), 1) AS estimated_avg_tenure_years,
        ROUND(AVG(estimated_salary_sar), 0) AS estimated_avg_salary_sar,
        ROUND(AVG(job_satisfaction_score), 2) AS avg_satisfaction_score
    FROM employees;
    """
    df_kpi = pd.read_sql_query(kpi_query, conn)
    kpi_path = os.path.join(output_dir, "kpi_summary.csv")
    df_kpi.to_csv(kpi_path, index=False)
    print(f"2. Executive KPI Summary: {kpi_path}")
    
    # 3. Department Attrition & Benchmark Summary
    dept_query = """
    WITH company AS (SELECT AVG(is_attrition) * 100.0 AS comp_avg FROM employees),
    dept_all AS (
        SELECT 
            department,
            COUNT(*) AS total_headcount,
            SUM(is_attrition) AS leavers_count,
            COUNT(*) - SUM(is_attrition) AS retained_count,
            ROUND(AVG(is_attrition) * 100.0, 2) AS attrition_rate_pct,
            ROUND(AVG(estimated_salary_sar), 0) AS avg_salary_sar,
            ROUND(AVG(job_satisfaction_score), 2) AS avg_satisfaction_score
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
        HAVING total_headcount >= 20 -- Minimum department sample threshold
    )
    SELECT 
        d.department,
        d.total_headcount,
        d.leavers_count,
        d.retained_count,
        d.attrition_rate_pct,
        d.avg_salary_sar,
        d.avg_satisfaction_score,
        e.variance_vs_company_pct,
        e.attrition_risk_index,
        CASE WHEN d.total_headcount < 20 THEN 1 ELSE 0 END AS small_sample,
        e.risk_tier
    FROM dept_all d
    LEFT JOIN dept_eligible e ON d.department = e.department
    ORDER BY small_sample ASC, d.total_headcount DESC;
    """
    df_dept = pd.read_sql_query(dept_query, conn)
    dept_path = os.path.join(output_dir, "department_attrition_benchmark.csv")
    df_dept.to_csv(dept_path, index=False)
    print(f"3. Department Benchmark: {dept_path} ({len(df_dept)} rows, small_sample flagged for N<20)")
    
    # 4. Tenure Cohort & Career Stage Summary
    tenure_query = """
    SELECT 
        tenure_last_org_band,
        estimated_tenure_years,
        COUNT(*) AS headcount,
        SUM(is_attrition) AS leavers_count,
        ROUND(AVG(is_attrition) * 100.0, 2) AS attrition_rate_pct,
        ROUND(AVG(estimated_salary_sar), 0) AS avg_salary_sar,
        ROUND(AVG(job_satisfaction_score), 2) AS avg_satisfaction_score
    FROM employees
    GROUP BY tenure_last_org_band, estimated_tenure_years
    ORDER BY estimated_tenure_years ASC;
    """
    df_tenure = pd.read_sql_query(tenure_query, conn)
    tenure_path = os.path.join(output_dir, "tenure_attrition_summary.csv")
    df_tenure.to_csv(tenure_path, index=False)
    print(f"4. Tenure Summary: {tenure_path} ({len(df_tenure)} rows)")
    
    # 5. Satisfaction & Sentiment Retention Summary
    sat_query = """
    SELECT 
        job_satisfaction,
        job_satisfaction_score,
        work_life_balance,
        COUNT(*) AS headcount,
        SUM(is_attrition) AS leavers_count,
        ROUND(AVG(is_attrition) * 100.0, 2) AS attrition_rate_pct
    FROM employees
    GROUP BY job_satisfaction, job_satisfaction_score, work_life_balance
    ORDER BY job_satisfaction_score ASC;
    """
    df_sat = pd.read_sql_query(sat_query, conn)
    sat_path = os.path.join(output_dir, "satisfaction_retention_summary.csv")
    df_sat.to_csv(sat_path, index=False)
    print(f"5. Satisfaction Summary: {sat_path} ({len(df_sat)} rows)")
    
    # 6. Salary & Role Matrix
    salary_query = """
    SELECT 
        department,
        monthly_salary_band,
        estimated_salary_sar,
        COUNT(*) AS headcount,
        SUM(is_attrition) AS leavers_count,
        ROUND(AVG(is_attrition) * 100.0, 2) AS attrition_rate_pct
    FROM employees
    GROUP BY department, monthly_salary_band, estimated_salary_sar
    ORDER BY department ASC, estimated_salary_sar ASC;
    """
    df_salary = pd.read_sql_query(salary_query, conn)
    salary_path = os.path.join(output_dir, "salary_distribution_matrix.csv")
    df_salary.to_csv(salary_path, index=False)
    print(f"6. Salary Distribution Matrix: {salary_path} ({len(df_salary)} rows)")
    
    conn.close()
    print("=" * 70)
    print(f"All dashboard deliverables successfully exported to {output_dir}/")
    print("=" * 70)


if __name__ == "__main__":
    export_dashboard_data()
