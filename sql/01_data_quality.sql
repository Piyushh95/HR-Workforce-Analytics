-- ==============================================================================
-- 01_data_quality.sql
-- HR Workforce Analytics: Data Quality & Schema Integrity Validation Checks
-- Database: SQLite (Target Table: employees)
-- ==============================================================================

-- ------------------------------------------------------------------------------
-- CHECK 1: Total Record Count & Headcount Baseline
-- Expected Result: Exactly 1,191 employee records.
-- ------------------------------------------------------------------------------
SELECT 
    COUNT(*) AS total_records,
    COUNT(DISTINCT employee_id) AS distinct_employee_ids,
    CASE 
        WHEN COUNT(*) = 1191 AND COUNT(DISTINCT employee_id) = 1191 THEN 'PASS: Headcount intact and PK unique'
        ELSE 'FAIL: Unexpected record count or duplicate primary keys'
    END AS check_status
FROM employees;


-- ------------------------------------------------------------------------------
-- CHECK 2: Null and Missing Value Audit Across Critical Reporting Fields
-- Verifies zero nulls exist in core demographic, departmental, and metric fields.
-- ------------------------------------------------------------------------------
SELECT
    SUM(CASE WHEN employee_id IS NULL THEN 1 ELSE 0 END) AS null_employee_id,
    SUM(CASE WHEN attrition IS NULL THEN 1 ELSE 0 END) AS null_attrition,
    SUM(CASE WHEN department IS NULL THEN 1 ELSE 0 END) AS null_department,
    SUM(CASE WHEN sector IS NULL THEN 1 ELSE 0 END) AS null_sector,
    SUM(CASE WHEN job_title IS NULL THEN 1 ELSE 0 END) AS null_job_title,
    SUM(CASE WHEN monthly_salary_band IS NULL THEN 1 ELSE 0 END) AS null_salary_band,
    SUM(CASE WHEN tenure_last_org_band IS NULL THEN 1 ELSE 0 END) AS null_tenure_band,
    SUM(CASE WHEN job_satisfaction IS NULL THEN 1 ELSE 0 END) AS null_job_satisfaction,
    SUM(CASE WHEN estimated_salary_sar IS NULL THEN 1 ELSE 0 END) AS null_estimated_salary
FROM employees;


-- ------------------------------------------------------------------------------
-- CHECK 3: Domain Validity of Categorical Values
-- Verifies all categorical fields conform strictly to expected business labels.
-- ------------------------------------------------------------------------------
SELECT 
    'attrition' AS field_name,
    attrition AS value_found,
    COUNT(*) AS record_count,
    CASE WHEN attrition IN ('Yes', 'No') THEN 'VALID' ELSE 'INVALID' END AS validation_status
FROM employees
GROUP BY attrition

UNION ALL

SELECT 
    'gender',
    gender,
    COUNT(*),
    CASE WHEN gender IN ('Male', 'Female') THEN 'VALID' ELSE 'INVALID' END
FROM employees
GROUP BY gender

UNION ALL

SELECT 
    'job_satisfaction',
    job_satisfaction,
    COUNT(*),
    CASE WHEN job_satisfaction IN ('Not satisfied', 'Satisfied', 'Very satisfied') THEN 'VALID' ELSE 'INVALID' END
FROM employees
GROUP BY job_satisfaction;


-- ------------------------------------------------------------------------------
-- CHECK 4: Boundary & Range Checks for Numerical and Ordinal Fields
-- Verifies allowance count (0-4), Likert rating scores (1-3), and salary midpoints.
-- ------------------------------------------------------------------------------
SELECT 
    MIN(allowance_count) AS min_allowances,
    MAX(allowance_count) AS max_allowances,
    MIN(job_satisfaction_score) AS min_satisfaction_score,
    MAX(job_satisfaction_score) AS max_satisfaction_score,
    MIN(estimated_salary_sar) AS min_salary_midpoint,
    MAX(estimated_salary_sar) AS max_salary_midpoint,
    CASE 
        WHEN MIN(allowance_count) >= 0 AND MAX(allowance_count) <= 4
         AND MIN(job_satisfaction_score) = 1 AND MAX(job_satisfaction_score) = 3
         AND MIN(estimated_salary_sar) >= 3500 AND MAX(estimated_salary_sar) <= 35000
        THEN 'PASS: All numerical values within expected boundaries'
        ELSE 'FAIL: Numerical values out of range'
    END AS check_status
FROM employees;


-- ------------------------------------------------------------------------------
-- CHECK 5: Attribute-Level Duplicate Inspection (Ignoring Primary Key)
-- Identifies records sharing identical survey profiles across all dimensions.
-- ------------------------------------------------------------------------------
WITH duplicate_profiles AS (
    SELECT 
        gender, age_band, marital_status, academic_degree, sector, department,
        job_title, monthly_salary_band, tenure_last_org_band, job_satisfaction,
        COUNT(*) AS profile_frequency,
        GROUP_CONCAT(employee_id) AS associated_employee_ids
    FROM employees
    GROUP BY 
        gender, age_band, marital_status, academic_degree, sector, department,
        job_title, monthly_salary_band, tenure_last_org_band, job_satisfaction
    HAVING COUNT(*) > 1
)
SELECT 
    associated_employee_ids,
    profile_frequency,
    department,
    job_title,
    monthly_salary_band,
    tenure_last_org_band,
    'FLAGGED: Identical response profile (Retained per data governance protocol)' AS status_note
FROM duplicate_profiles;
