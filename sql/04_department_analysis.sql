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
-- Uses a Common Table Expression (CTE) to compute an Attrition Risk Index:
-- (Department Attrition Rate / Company Average Attrition Rate).
-- ------------------------------------------------------------------------------
WITH company_avg AS (
    SELECT AVG(is_attrition) * 100.0 AS avg_attrition_rate FROM employees
),
dept_metrics AS (
    SELECT 
        department,
        COUNT(*) AS headcount,
        SUM(is_attrition) AS leavers,
        ROUND(AVG(is_attrition) * 100.0, 2) AS dept_attrition_rate,
        ROUND(AVG(estimated_salary_sar), 0) AS avg_salary,
        ROUND(AVG(job_satisfaction_score), 2) AS avg_satisfaction
    FROM employees
    GROUP BY department
    HAVING COUNT(*) >= 15 -- Focus on significant departments for statistical relevance
)
SELECT 
    d.department,
    d.headcount,
    d.leavers,
    d.dept_attrition_rate,
    ROUND(c.avg_attrition_rate, 2) AS company_avg_rate,
    ROUND(d.dept_attrition_rate - c.avg_attrition_rate, 2) AS variance_vs_company_pct,
    ROUND(d.dept_attrition_rate / c.avg_attrition_rate, 2) AS attrition_risk_index,
    CASE 
        WHEN d.dept_attrition_rate > c.avg_attrition_rate + 5.0 THEN 'High Risk (>5% above avg)'
        WHEN d.dept_attrition_rate < c.avg_attrition_rate - 5.0 THEN 'Low Risk (>5% below avg)'
        ELSE 'Moderate Risk (Near avg)'
    END AS risk_tier,
    d.avg_salary,
    d.avg_satisfaction
FROM dept_metrics d
CROSS JOIN company_avg c
ORDER BY d.dept_attrition_rate DESC;


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
