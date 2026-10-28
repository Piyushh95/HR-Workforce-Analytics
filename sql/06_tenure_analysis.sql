-- ==============================================================================
-- 06_tenure_analysis.sql
-- Employee Tenure, Career Stage Dynamics & Retention Lifecycle
-- Database: SQLite (Target Table: employees)
-- Analytical Limitation: Tenure is captured as survey interval bands, not continuous dates.
-- ==============================================================================

-- ------------------------------------------------------------------------------
-- QUERY 1: Attrition by Organizational Tenure Band (Last Organization)
-- Investigates voluntary departure propensity across tenure stages at previous employer.
-- ------------------------------------------------------------------------------
SELECT 
    tenure_last_org_band,
    COUNT(*) AS total_employees,
    SUM(is_attrition) AS leavers_count,
    ROUND(AVG(is_attrition) * 100.0, 2) AS attrition_rate_pct,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM employees), 2) AS workforce_share_pct,
    ROUND(AVG(estimated_salary_sar), 0) AS estimated_avg_salary,
    ROUND(AVG(job_satisfaction_score), 2) AS avg_job_satisfaction
FROM employees
GROUP BY tenure_last_org_band
ORDER BY estimated_tenure_years ASC;


-- ------------------------------------------------------------------------------
-- QUERY 2: Total Career Experience vs. Organization Tenure Matrix
-- Evaluates whether early-career professionals leave faster than experienced hires.
-- ------------------------------------------------------------------------------
SELECT 
    total_experience_band,
    tenure_last_org_band,
    COUNT(*) AS employee_count,
    SUM(is_attrition) AS leavers_count,
    ROUND(AVG(is_attrition) * 100.0, 2) AS attrition_rate_pct
FROM employees
GROUP BY total_experience_band, tenure_last_org_band
HAVING COUNT(*) >= 10
ORDER BY estimated_total_exp_years ASC, estimated_tenure_years ASC;


-- ------------------------------------------------------------------------------
-- QUERY 3: Early-Career (<5 Years) vs. Tenured Employee Cohort Comparison
-- Categorizes employees into simplified lifecycle cohorts to assess flight risk.
-- ------------------------------------------------------------------------------
WITH cohort_analysis AS (
    SELECT 
        CASE 
            WHEN tenure_last_org_band = 'Less than 5 years' THEN 'Early Stage (<5 Years)'
            WHEN tenure_last_org_band = 'From 5 to 10 years' THEN 'Mid Stage (5-10 Years)'
            ELSE 'Tenured (>10 Years)'
        END AS tenure_cohort,
        is_attrition,
        job_satisfaction_score,
        estimated_salary_sar,
        has_deserved_promotion
    FROM employees
)
SELECT 
    tenure_cohort,
    COUNT(*) AS cohort_headcount,
    SUM(is_attrition) AS leavers_count,
    ROUND(AVG(is_attrition) * 100.0, 2) AS attrition_rate_pct,
    ROUND(AVG(job_satisfaction_score), 2) AS avg_satisfaction_score,
    ROUND(AVG(estimated_salary_sar), 0) AS avg_salary_sar,
    ROUND(AVG(has_deserved_promotion) * 100.0, 1) AS pct_received_deserved_promotion
FROM cohort_analysis
GROUP BY tenure_cohort
ORDER BY attrition_rate_pct DESC;
