-- ==============================================================================
-- 03_attrition_analysis.sql
-- Comprehensive Employee Turnover Driver & Segmentation Analysis
-- Database: SQLite (Target Table: employees)
-- Business Objective: Identify key workplace factors correlating with employee attrition.
-- ==============================================================================

-- ------------------------------------------------------------------------------
-- QUERY 1: Overtime Status & Compensation Impact on Attrition
-- Compares attrition rates between employees with Paid Overtime, Unpaid Overtime, and No Overtime.
-- ------------------------------------------------------------------------------
SELECT 
    payment_overtime,
    COUNT(*) AS total_employees,
    SUM(is_attrition) AS leavers_count,
    COUNT(*) - SUM(is_attrition) AS retained_count,
    ROUND(AVG(is_attrition) * 100.0, 2) AS attrition_rate_pct,
    ROUND(AVG(job_satisfaction_score), 2) AS avg_job_satisfaction,
    ROUND(AVG(psychological_exhaustion_score), 2) AS avg_psych_exhaustion
FROM employees
GROUP BY payment_overtime
ORDER BY attrition_rate_pct DESC;


-- ------------------------------------------------------------------------------
-- QUERY 2: Career Mobility — Deserved Promotion & Recognition Impact
-- Evaluates retention differences among employees who felt they received deserved promotions.
-- ------------------------------------------------------------------------------
SELECT 
    deserved_promotion,
    recognition,
    COUNT(*) AS total_employees,
    SUM(is_attrition) AS leavers_count,
    ROUND(AVG(is_attrition) * 100.0, 2) AS attrition_rate_pct,
    ROUND(AVG(estimated_salary_sar), 0) AS estimated_avg_salary
FROM employees
GROUP BY deserved_promotion, recognition
ORDER BY attrition_rate_pct DESC;


-- ------------------------------------------------------------------------------
-- QUERY 3: Job Opportunities & External Pull vs. Internal Push Factors
-- Examines whether external job alternatives interact with job satisfaction to drive turnover.
-- ------------------------------------------------------------------------------
SELECT 
    job_opportunities AS external_opportunities,
    job_satisfaction,
    COUNT(*) AS total_employees,
    SUM(is_attrition) AS leavers_count,
    ROUND(AVG(is_attrition) * 100.0, 2) AS attrition_rate_pct
FROM employees
GROUP BY job_opportunities, job_satisfaction
ORDER BY job_opportunities DESC, job_satisfaction ASC;


-- ------------------------------------------------------------------------------
-- QUERY 4: Health & Workplace Stress Factors in Voluntary Turnover
-- Tests the correlation between health issues, physical stress, and attrition.
-- ------------------------------------------------------------------------------
SELECT 
    health_issues,
    physical_stress,
    COUNT(*) AS total_employees,
    SUM(is_attrition) AS leavers_count,
    ROUND(AVG(is_attrition) * 100.0, 2) AS attrition_rate_pct
FROM employees
GROUP BY health_issues, physical_stress
ORDER BY attrition_rate_pct DESC;
