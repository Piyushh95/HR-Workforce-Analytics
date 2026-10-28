-- ==============================================================================
-- 02_workforce_kpis.sql
-- Executive Workforce Overview & Core Human Capital KPIs
-- Database: SQLite (Target Table: employees)
-- Grain: High-level organizational aggregate and departmental benchmarking
-- ==============================================================================

-- ------------------------------------------------------------------------------
-- QUERY 1: Organizational Macro Workforce KPIs
-- Computes core HR metrics: Headcount, Leavers, Attrition %, and Estimated Midpoints.
-- ------------------------------------------------------------------------------
SELECT
    COUNT(*) AS total_headcount,
    SUM(is_attrition) AS total_leavers,
    COUNT(*) - SUM(is_attrition) AS total_retained,
    ROUND(AVG(is_attrition) * 100.0, 2) AS attrition_rate_pct,
    ROUND(AVG(estimated_age_years), 1) AS estimated_avg_age_years,
    ROUND(AVG(estimated_tenure_years), 1) AS estimated_avg_tenure_years,
    ROUND(AVG(estimated_salary_sar), 2) AS estimated_avg_salary_sar,
    ROUND(AVG(allowance_count), 2) AS avg_benefits_allowance_count,
    ROUND(AVG(job_satisfaction_score), 2) AS avg_job_satisfaction_score
FROM employees;


-- ------------------------------------------------------------------------------
-- QUERY 2: Workforce Distribution Across Demographics (Gender & Age Brackets)
-- Breaks down headcount and attrition rates across gender and generational bands.
-- ------------------------------------------------------------------------------
SELECT 
    age_band,
    gender,
    COUNT(*) AS headcount,
    SUM(is_attrition) AS attrition_count,
    ROUND(AVG(is_attrition) * 100.0, 2) AS attrition_rate_pct,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM employees), 2) AS pct_of_total_workforce,
    ROUND(AVG(estimated_salary_sar), 0) AS estimated_avg_salary_sar
FROM employees
GROUP BY age_band, gender
ORDER BY age_band ASC, gender ASC;


-- ------------------------------------------------------------------------------
-- QUERY 3: Executive Summary KPI Card Formulation
-- Formats KPIs into a normalized reporting key-value structure ready for BI consumption.
-- ------------------------------------------------------------------------------
WITH kpi_base AS (
    SELECT
        COUNT(*) AS total_headcount,
        SUM(is_attrition) AS total_leavers,
        ROUND(AVG(is_attrition) * 100.0, 2) AS attrition_rate,
        ROUND(AVG(estimated_tenure_years), 1) AS avg_tenure,
        ROUND(AVG(estimated_salary_sar), 0) AS avg_salary,
        ROUND(AVG(job_satisfaction_score), 2) AS avg_satisfaction
    FROM employees
)
SELECT 'Total Headcount' AS kpi_metric, CAST(total_headcount AS TEXT) AS kpi_value, 'Employees (Respondents)' AS metric_unit FROM kpi_base
UNION ALL
SELECT 'Attrition Count', CAST(total_leavers AS TEXT), 'Leavers' FROM kpi_base
UNION ALL
SELECT 'Attrition Rate', CAST(attrition_rate AS TEXT) || '%', 'Percentage' FROM kpi_base
UNION ALL
SELECT 'Estimated Avg Tenure', CAST(avg_tenure AS TEXT), 'Years' FROM kpi_base
UNION ALL
SELECT 'Estimated Avg Monthly Salary', 'SAR ' || CAST(avg_salary AS TEXT), 'SAR / Month' FROM kpi_base
UNION ALL
SELECT 'Avg Job Satisfaction Index', CAST(avg_satisfaction AS TEXT) || ' / 3.00', 'Likert Scale (1-3)' FROM kpi_base;
