# HR Workforce Analytics — Midpoint Estimation Methodology

This document outlines the formal methodology, formulas, documented assumptions, and statistical limitations for converting ordinal and interval survey brackets into continuous metric approximations.

> **Important Analytical Caveat:**  
> All numerical values derived from category midpoints (`estimated_salary_sar`, `estimated_tenure_years`, `estimated_age_years`) are **group-level approximations**, not exact individual-level measurements. They are intended solely for aggregate descriptive metrics (e.g., mean benchmarking in SQL and BI cards) and must not be interpreted as exact continuous measurements of individual employee compensation, tenure, or age.

---

## 1. Midpoint Mapping Specifications

| Variable | Original Category | Mapping/Formula | Estimated Value | Rationale | Limitation |
| :--- | :--- | :--- | :---: | :--- | :--- |
| **Monthly Salary** | `Less than 5000 SAR` | $(0 + 5000) / 2$ | **2,500.0 SAR** | Standard mathematical interval $[0, 5000)$ with natural zero floor. | May underestimate formal full-time compensation if statutory wage floors or living allowances apply. |
| **Monthly Salary** | `From 5000 to 10000 S.R` | $(5000 + 10000) / 2$ | **7,500.0 SAR** | Closed interval $[5000, 10000]$; arithmetic midpoint of range. | Assumes uniform respondent distribution across the 5,000 SAR spread. |
| **Monthly Salary** | `From 11000 to 15000 S.R` | $(11000 + 15000) / 2$ | **13,000.0 SAR** | Closed interval $[11000, 15000]$; arithmetic midpoint of range. | Leaves 10,001–10,999 undefined due to survey questionnaire design. |
| **Monthly Salary** | `From 16000 to 20000 S.R` | $(16000 + 20000) / 2$ | **18,000.0 SAR** | Closed interval $[16000, 20000]$; arithmetic midpoint of range. | Leaves 15,001–15,999 undefined due to survey questionnaire design. |
| **Monthly Salary** | `From 21000 to 25000 S.R` | $(21000 + 25000) / 2$ | **23,000.0 SAR** | Closed interval $[21000, 25000]$; arithmetic midpoint of range. | Small sample size ($N=2$) in dataset. |
| **Monthly Salary** | `From 26000 to 30000 S.R` | $(26000 + 30000) / 2$ | **28,000.0 SAR** | Closed interval $[26000, 30000]$; arithmetic midpoint of range. | Small sample size ($N=5$) in dataset. |
| **Monthly Salary** | `S.R 31000 - and more` | $(31000 + 39000) / 2$ | **35,000.0 SAR** | Open-ended top bracket $[31000, \infty)$. Assumes conservative upper boundary of 39,000 SAR (consistent with preceding 5k–8k bracket spreads). | Cannot capture executive outliers or salaries significantly exceeding 40,000 SAR. |
| **Tenure** | `Less than 5 years` | $(0 + 5) / 2$ | **2.5 Years** | Natural zero floor for new hires; interval $[0, 5)$. | Masks early 90-day vs. 3-year turnover dynamics within the initial 5-year window. |
| **Tenure** | `From 5 to 10 years` | $(5 + 10) / 2$ | **7.5 Years** | Closed interval $[5, 10]$; arithmetic midpoint of range. | Assumes uniform employee distribution across 5-year span. |
| **Tenure** | `From 11 to 15 years` | $(11 + 15) / 2$ | **13.0 Years** | Closed interval $[11, 15]$; arithmetic midpoint of range. | Assumes mid-career stability across 5-year span. |
| **Tenure** | `From 16 to 20 years` | $(16 + 20) / 2$ | **18.0 Years** | Closed interval $[16, 20]$; arithmetic midpoint of range. | Small cohort ($N=26$) in dataset. |
| **Tenure** | `From 21 to 25 years` | $(21 + 25) / 2$ | **23.0 Years** | Closed interval $[21, 25]$; arithmetic midpoint of range. | Small cohort ($N=13$) in dataset. |
| **Tenure** | `From 26 to 30 years` | $(26 + 30) / 2$ | **28.0 Years** | Closed interval $[26, 30]$; arithmetic midpoint of range. | Small cohort ($N=5$) in dataset. |
| **Tenure** | `From 31 to 35 years` | $(31 + 35) / 2$ | **33.0 Years** | Closed interval $[31, 35]$; arithmetic midpoint of range. | Small cohort ($N=4$) in dataset. |
| **Tenure** | `From 36 to 40 years` | $(36 + 40) / 2$ | **38.0 Years** | Closed interval $[36, 40]$; survey option supported in code. | No respondents present in final dataset ($N=0$). |
| **Age** | `21 to 30` | $(21 + 30) / 2$ | **25.5 Years** | Closed interval $[21, 30]$; entry-career bracket midpoint. | Assumes uniform age distribution across 20s. |
| **Age** | `31 to 40` | $(31 + 40) / 2$ | **35.5 Years** | Closed interval $[31, 40]$; mid-career bracket midpoint. | Assumes uniform age distribution across 30s. |
| **Age** | `41 to 50` | $(41 + 50) / 2$ | **45.5 Years** | Closed interval $[41, 50]$; senior professional bracket midpoint. | Assumes uniform age distribution across 40s. |
| **Age** | `51 to 60` | $(51 + 60) / 2$ | **55.5 Years** | Closed interval $[51, 60]$; pre-retirement bracket midpoint. | Small cohort ($N=13$) in dataset. |

---

## 2. Centralized Architecture & Programmatic Governance

* All midpoint mappings are centrally defined in the immutable `MIDPOINTS` dictionary within [`scripts/clean_data.py`](file:///f:/Big4_Project/Hr%20anlyst/Saudi%20Employee%20Attrition%20Dataset/Saudi%20Employee%20Attrition%20Dataset/HR-Workforce-Analytics/scripts/clean_data.py).
* `calculate_salary_midpoint`, `calculate_tenure_midpoint`, and `calculate_age_midpoint` resolve directly through `MIDPOINTS`.
* Unknown, missing, or out-of-range categories strictly resolve to `np.nan` rather than being assigned an arbitrary default value.
* Re-running the pipeline produces 100% deterministic, byte-identical output across runs.
