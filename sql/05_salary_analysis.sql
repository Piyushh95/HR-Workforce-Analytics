-- ==============================================================================
-- 05_salary_analysis.sql
-- Compensation Distribution, Pay Equity & Attrition Sensitivity
-- Database: SQLite (Target Table: employees)
-- Grain: Salary band, job role, and department-level compensation structures
-- ==============================================================================

-- ------------------------------------------------------------------------------
-- QUERY 1: Attrition Rate Across Monthly Salary Brackets
-- Tests whether lower compensation brackets exhibit higher turnover rates.
-- ------------------------------------------------------------------------------
SELECT 
    monthly_salary_band,
    COUNT(*) AS total_employees,
    SUM(is_attrition) AS leavers_count,
    ROUND(AVG(is_attrition) * 100.0, 2) AS attrition_rate_pct,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM employees), 2) AS workforce_pct,
    ROUND(AVG(has_compensation_satisfaction) * 100.0, 1) AS pct_satisfied_with_pay,
    ROUND(AVG(job_satisfaction_score), 2) AS avg_job_satisfaction
FROM employees
GROUP BY monthly_salary_band
ORDER BY estimated_salary_sar ASC;


-- ------------------------------------------------------------------------------
-- QUERY 2: Compensation Ranking Across Job Roles using DENSE_RANK()
-- Ranks job titles by estimated average salary and compares against role-level attrition.
-- ------------------------------------------------------------------------------
WITH role_pay AS (
    SELECT 
        department,
        job_title,
        COUNT(*) AS role_headcount,
        ROUND(AVG(estimated_salary_sar), 0) AS estimated_avg_salary,
        SUM(is_attrition) AS role_leavers,
        ROUND(AVG(is_attrition) * 100.0, 2) AS role_attrition_rate
    FROM employees
    GROUP BY department, job_title
    HAVING COUNT(*) >= 10 -- Minimum 10 employees per role for meaningful aggregation
)
SELECT 
    DENSE_RANK() OVER (ORDER BY estimated_avg_salary DESC) AS salary_rank,
    department,
    job_title,
    role_headcount,
    estimated_avg_salary,
    role_leavers,
    role_attrition_rate
FROM role_pay
ORDER BY salary_rank ASC, role_headcount DESC;


-- ------------------------------------------------------------------------------
-- QUERY 3: Pay Perception Gap: Actual Salary Band vs. Compensation Satisfaction
-- Evaluates whether high earners report dissatisfaction and whether dissatisfaction
-- amplifies turnover regardless of actual earnings tier.
-- ------------------------------------------------------------------------------
SELECT 
    monthly_salary_band,
    compensation_satisfaction,
    COUNT(*) AS headcount,
    SUM(is_attrition) AS leavers_count,
    ROUND(AVG(is_attrition) * 100.0, 2) AS attrition_rate_pct
FROM employees
GROUP BY monthly_salary_band, compensation_satisfaction
ORDER BY estimated_salary_sar ASC, compensation_satisfaction DESC;
