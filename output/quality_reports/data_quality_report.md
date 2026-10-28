# HR Workforce Analytics — Data Quality & Validation Report

**Generated Date:** 2026-10-29  
**Source Dataset:** `Original Dataset of Employee Attrition.xlsx`  
**Target Table:** `employees`  

---

## 1. Executive Summary & Verification Metrics

| Metric | Raw Value | Cleaned Value | Validation Status | Notes |
| :--- | :---: | :---: | :---: | :--- |
| **Total Employee Records (Rows)** | 1,191 | 1,191 | Verified | 100% record retention; zero rows discarded |
| **Total Features (Columns)** | 35 | 53 | Enhanced | 35 core survey fields + 18 engineered BI/SQL metrics |
| **Missing Values (Nulls)** | 0 | 0 | Clean | Complete survey dataset; no imputation needed |
| **Primary Key (`employee_id`)** | 1,191 unique | 1,191 unique | Verified | Range: 11 to 1213; 12 unassigned ID gaps |
| **Attribute Duplicates (Excl. ID)** | 2 rows | 2 rows | Flagged | IDs [261, 268] flagged via `is_potential_duplicate_profile` |
| **Total Attrition Count** | 515 | 515 | Preserved | Exact headcount preserved |
| **Overall Attrition Rate** | 43.24% | 43.24% | Preserved | Avoided downward bias present in 1,174-row ML files (42.42%) |

---

## 2. Transformations Applied

1. **Whitespace & Non-Breaking Space Removal:**
   - 5 raw column names contained whitespace/`\xa0` (`'Gender '`, `' Maritalstatus'`, `'\xa0Academic_degree '`, `'Get_ Deserved_Promotion'`, `'Training_programs_ During_last_three_years'`).
   - Cleaned across all text features, eliminating category splitting (e.g., `' Married'` merged into `'Married'`).
2. **Schema & Naming Harmonization:**
   - Transformed all 35 original column headers into descriptive, standardized `snake_case`.
   - Renamed `Allowances` to `allowance_count` to reflect that values (0–4) represent the count of benefits, not monetary SAR amounts.
3. **Categorical Normalization:**
   - Standardized `department` into 21 distinct business entities, merging case and spacing variants.
   - Standardized `sector` into 15 business sectors.
   - Corrected prominent job title typo: `'Manger assistant'` -> `'Manager Assistant'`.
   - Standardized `academic_degree` titles.
4. **Salary & Tenure Midpoint Approximations:**
   - Source data records `monthly_salary_band`, `tenure_last_org_band`, `total_experience_band`, and `age_band` as interval bins.
   - Calculated defensible interval midpoints (`estimated_salary_sar`, `estimated_tenure_years`, `estimated_age_years`) to facilitate descriptive aggregate calculations in SQL and BI cards.
5. **Engineered Flags & Scores:**
   - Created 0/1 binary flags for KPI aggregations (`is_attrition`, `is_female`, `has_overtime`, etc.).
   - Standardized 1–3 ordinal rating scores for survey Likert scales.

---

## 3. Unresolved Data Quality Observations & Limitations

1. **Missing ID Sequence:** IDs range from 11 to 1213. Exactly 12 IDs are absent: `[19, 49, 136, 221, 267, 294, 406, 832, 866, 1052, 1057, 1060]`. These represent unassigned survey responses or pre-collection deletions.
2. **Identical Response Profile:** IDs 261 and 268 share identical responses across all 34 survey questions. Because the respondent pool is large and responses are coarse ordinal bands, this profile is retained and flagged rather than arbitrarily deleted.
3. **Cross-Sectional Survey Nature:** This dataset represents self-reported survey responses from Saudi professionals regarding their turnover history and last employer, not an active corporate HRIS payroll extract.

---
