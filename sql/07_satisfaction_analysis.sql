-- ==============================================================================
-- 07_satisfaction_analysis.sql
-- Employee Sentiment, Organizational Climate & Retention Interactions
-- Database: SQLite (Target Table: employees)
-- Note: Descriptive statistical relationships demonstrate correlation, NOT direct causation.
-- ==============================================================================

-- ------------------------------------------------------------------------------
-- QUERY 1: Overall Job Satisfaction vs. Attrition Rate
-- Baseline sentiment gradient demonstrating retention elasticity by satisfaction level.
-- ------------------------------------------------------------------------------
SELECT 
    job_satisfaction,
    COUNT(*) AS total_employees,
    SUM(is_attrition) AS leavers_count,
    ROUND(AVG(is_attrition) * 100.0, 2) AS attrition_rate_pct,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM employees), 2) AS workforce_share_pct,
    ROUND(AVG(estimated_salary_sar), 0) AS estimated_avg_salary_sar
FROM employees
GROUP BY job_satisfaction
ORDER BY job_satisfaction_score ASC;


-- ------------------------------------------------------------------------------
-- QUERY 2: The Triad of Engagement: Support, Recognition & Emotional Commitment
-- Evaluates how leadership support and recognition correlate with organizational commitment.
-- ------------------------------------------------------------------------------
SELECT 
    job_support,
    recognition,
    emotional_commitment,
    COUNT(*) AS headcount,
    SUM(is_attrition) AS leavers_count,
    ROUND(AVG(is_attrition) * 100.0, 2) AS attrition_rate_pct
FROM employees
GROUP BY job_support, recognition, emotional_commitment
HAVING COUNT(*) >= 15
ORDER BY attrition_rate_pct DESC;


-- ------------------------------------------------------------------------------
-- QUERY 3: Work-Life Balance & Burnout Factors (Physical & Mental Strain)
-- Evaluates attrition across combinations of work-life balance difficulty and exhaustion.
-- ------------------------------------------------------------------------------
SELECT 
    work_life_balance,
    psychological_exhaustion,
    COUNT(*) AS total_employees,
    SUM(is_attrition) AS leavers_count,
    ROUND(AVG(is_attrition) * 100.0, 2) AS attrition_rate_pct,
    ROUND(AVG(job_satisfaction_score), 2) AS avg_job_satisfaction
FROM employees
GROUP BY work_life_balance, psychological_exhaustion
ORDER BY attrition_rate_pct DESC;


-- ------------------------------------------------------------------------------
-- QUERY 4: Professional Development ROI: Training Volume vs. Training Utility
-- Examines whether providing training programs reduces turnover only when deemed useful.
-- ------------------------------------------------------------------------------
SELECT 
    training_programs_last_3yrs,
    useful_training_programs,
    COUNT(*) AS total_employees,
    SUM(is_attrition) AS leavers_count,
    ROUND(AVG(is_attrition) * 100.0, 2) AS attrition_rate_pct
FROM employees
GROUP BY training_programs_last_3yrs, useful_training_programs
ORDER BY training_programs_last_3yrs ASC, useful_training_programs DESC;
