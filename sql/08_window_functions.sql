-- ==============================================================================
-- 08_window_functions.sql
-- Advanced Analytical SQL: Window Functions, Partitioning & Cohort Ranking
-- Database: SQLite (Target Table: employees)
-- Techniques: RANK(), DENSE_RANK(), ROW_NUMBER(), AVG() OVER(), NTILE()
-- ==============================================================================

-- ------------------------------------------------------------------------------
-- QUERY 1: Departmental Salary Benchmarking & Variance from Department Average
-- Computes departmental salary averages using window partitions and measures
-- each employee's salary spread from their department's mean.
-- ------------------------------------------------------------------------------
WITH dept_salary_benchmark AS (
    SELECT 
        employee_id,
        department,
        job_title,
        monthly_salary_band,
        estimated_salary_sar,
        is_attrition,
        ROUND(AVG(estimated_salary_sar) OVER (PARTITION BY department), 2) AS dept_avg_salary,
        COUNT(*) OVER (PARTITION BY department) AS dept_total_employees
    FROM employees
)
SELECT 
    employee_id,
    department,
    job_title,
    monthly_salary_band,
    estimated_salary_sar,
    dept_avg_salary,
    ROUND(estimated_salary_sar - dept_avg_salary, 2) AS diff_from_dept_avg_sar,
    CASE 
        WHEN estimated_salary_sar < dept_avg_salary - 2000 THEN 'Below Dept Benchmark'
        WHEN estimated_salary_sar > dept_avg_salary + 2000 THEN 'Above Dept Benchmark'
        ELSE 'At Dept Benchmark'
    END AS pay_position_category,
    is_attrition
FROM dept_salary_benchmark
ORDER BY department ASC, diff_from_dept_avg_sar ASC
LIMIT 30;


-- ------------------------------------------------------------------------------
-- QUERY 2: Intra-Department Job Role Ranking via DENSE_RANK()
-- Ranks job roles within each major department based on headcount and turnover.
-- ------------------------------------------------------------------------------
WITH role_aggregation AS (
    SELECT 
        department,
        job_title,
        COUNT(*) AS role_headcount,
        SUM(is_attrition) AS role_leavers,
        ROUND(AVG(is_attrition) * 100.0, 2) AS role_attrition_rate,
        ROUND(AVG(estimated_salary_sar), 0) AS role_avg_salary
    FROM employees
    GROUP BY department, job_title
)
SELECT 
    department,
    job_title,
    role_headcount,
    role_avg_salary,
    role_leavers,
    role_attrition_rate,
    DENSE_RANK() OVER (PARTITION BY department ORDER BY role_headcount DESC) AS headcount_rank_in_dept,
    DENSE_RANK() OVER (PARTITION BY department ORDER BY role_attrition_rate DESC) AS attrition_rank_in_dept
FROM role_aggregation
WHERE department IN ('Administration', 'Teaching', 'Customer Service', 'Patient Affairs', 'Sales')
ORDER BY department ASC, headcount_rank_in_dept ASC;


-- ------------------------------------------------------------------------------
-- QUERY 3: Cumulative Workforce Headcount & Running Total Attrition
-- Uses cumulative window frames to compute progressive running totals by tenure band.
-- ------------------------------------------------------------------------------
WITH tenure_summary AS (
    SELECT 
        tenure_last_org_band,
        estimated_tenure_years,
        COUNT(*) AS band_headcount,
        SUM(is_attrition) AS band_leavers
    FROM employees
    GROUP BY tenure_last_org_band, estimated_tenure_years
)
SELECT 
    tenure_last_org_band,
    band_headcount,
    band_leavers,
    ROUND(band_leavers * 100.0 / band_headcount, 2) AS band_attrition_rate,
    SUM(band_headcount) OVER (ORDER BY estimated_tenure_years ASC) AS cumulative_headcount,
    SUM(band_leavers) OVER (ORDER BY estimated_tenure_years ASC) AS cumulative_leavers,
    ROUND(
        SUM(band_leavers) OVER (ORDER BY estimated_tenure_years ASC) * 100.0 /
        SUM(band_headcount) OVER (ORDER BY estimated_tenure_years ASC),
        2
    ) AS cumulative_attrition_rate_pct
FROM tenure_summary
ORDER BY estimated_tenure_years ASC;


-- ------------------------------------------------------------------------------
-- QUERY 4: Salary Quartiles via NTILE(4) & Attrition Sensitivity Across Quartiles
-- Divides the workforce into four equal compensation quartiles and measures turnover.
-- ------------------------------------------------------------------------------
WITH salary_quartiles AS (
    SELECT 
        employee_id,
        department,
        estimated_salary_sar,
        is_attrition,
        job_satisfaction_score,
        NTILE(4) OVER (ORDER BY estimated_salary_sar ASC) AS salary_quartile
    FROM employees
)
SELECT 
    'Q' || CAST(salary_quartile AS TEXT) AS compensation_tier,
    CASE 
        WHEN salary_quartile = 1 THEN 'Quartile 1: Lowest 25% Pay'
        WHEN salary_quartile = 2 THEN 'Quartile 2: Lower-Mid Pay'
        WHEN salary_quartile = 3 THEN 'Quartile 3: Upper-Mid Pay'
        WHEN salary_quartile = 4 THEN 'Quartile 4: Top 25% Pay'
    END AS tier_description,
    MIN(estimated_salary_sar) AS min_tier_salary,
    MAX(estimated_salary_sar) AS max_tier_salary,
    COUNT(*) AS employee_count,
    SUM(is_attrition) AS leavers_count,
    ROUND(AVG(is_attrition) * 100.0, 2) AS quartile_attrition_rate_pct,
    ROUND(AVG(job_satisfaction_score), 2) AS avg_job_satisfaction
FROM salary_quartiles
GROUP BY salary_quartile
ORDER BY salary_quartile ASC;
