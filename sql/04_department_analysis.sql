-- ==============================================================================
-- 04_department_analysis.sql
-- Departmental Workforce Distribution & Retention Diagnostics
-- Database: SQLite (Target Table: employees)
-- Grain: Department-level aggregation and comparative benchmarking
-- ==============================================================================

-- ------------------------------------------------------------------------------
-- QUERY 1: Departmental Headcount, Turnover Volume, and Attrition Rate
-- Comprehensive breakdown of all departments sorted by headcount volume.
-- ------------------------------------------------------------------------------
SELECT 
    department,
    COUNT(*) AS total_headcount,
    SUM(is_attrition) AS leavers_count,
    COUNT(*) - SUM(is_attrition) AS retained_count,
    ROUND(AVG(is_attrition) * 100.0, 2) AS attrition_rate_pct,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM employees), 2) AS workforce_share_pct,
    ROUND(AVG(estimated_salary_sar), 0) AS estimated_avg_salary_sar,
    ROUND(AVG(job_satisfaction_score), 2) AS avg_satisfaction_score
FROM employees
GROUP BY department
ORDER BY total_headcount DESC;


-- ------------------------------------------------------------------------------
-- QUERY 2: Department Attrition Risk Benchmarking Against Company Average
-- Uses Common Table Expressions (CTEs) to compute an Attrition Risk Index:
-- (Department Attrition Rate / Company Average Attrition Rate).
-- Departments with <20 employees are flagged with small_sample = 1 and assigned
-- NULL for risk_tier to prevent statistical distortion from small sample sizes.
-- ------------------------------------------------------------------------------
WITH company_avg AS (
    SELECT AVG(is_attrition) * 100.0 AS avg_attrition_rate FROM employees
),
all_dept_metrics AS (
    SELECT 
        department,
        COUNT(*) AS headcount,
        SUM(is_attrition) AS leavers,
        ROUND(AVG(is_attrition) * 100.0, 2) AS dept_attrition_rate,
        ROUND(AVG(estimated_salary_sar), 0) AS avg_salary,
        ROUND(AVG(job_satisfaction_score), 2) AS avg_satisfaction
    FROM employees
    GROUP BY department
),
eligible_depts AS (
    SELECT 
        department,
        dept_attrition_rate,
        ROUND(dept_attrition_rate - c.avg_attrition_rate, 2) AS variance_vs_company_pct,
        ROUND(dept_attrition_rate / c.avg_attrition_rate, 2) AS attrition_risk_index,
        CASE 
            WHEN dept_attrition_rate > c.avg_attrition_rate + 5.0 THEN 'High Risk (>5% above avg)'
            WHEN dept_attrition_rate < c.avg_attrition_rate - 5.0 THEN 'Low Risk (>5% below avg)'
            ELSE 'Moderate Risk (Near avg)'
        END AS risk_tier
    FROM all_dept_metrics
    CROSS JOIN company_avg c
    GROUP BY department
    HAVING headcount >= 20 -- Minimum sample size threshold for risk classification
)
SELECT 
    d.department,
    d.headcount,
    d.leavers,
    d.dept_attrition_rate,
    ROUND(c.avg_attrition_rate, 2) AS company_avg_rate,
    e.variance_vs_company_pct,
    e.attrition_risk_index,
    CASE WHEN d.headcount < 20 THEN 1 ELSE 0 END AS small_sample,
    e.risk_tier,
    d.avg_salary,
    d.avg_satisfaction
FROM all_dept_metrics d
CROSS JOIN company_avg c
LEFT JOIN eligible_depts e ON d.department = e.department
ORDER BY small_sample ASC, d.dept_attrition_rate DESC, d.headcount DESC;


-- ------------------------------------------------------------------------------
-- QUERY 3: Cross-Tabulation: Department by Sector Attrition Patterns
-- Analyzes how specific departments behave across broader economic sectors.
-- ------------------------------------------------------------------------------
SELECT 
    sector,
    department,
    COUNT(*) AS headcount,
    SUM(is_attrition) AS leavers,
    ROUND(AVG(is_attrition) * 100.0, 2) AS attrition_rate_pct
FROM employees
GROUP BY sector, department
HAVING COUNT(*) >= 10
ORDER BY sector ASC, headcount DESC;
