# HR Workforce Analytics & Talent Retention Intelligence

A comprehensive, end-to-end business intelligence and workforce analytics project evaluating employee turnover dynamics, compensation equity, and workplace sentiment in Saudi Arabia. Built for Data Analyst and BI Specialist portfolios (aligned with standards for institutions such as Standard Chartered).

---

## 1. Project Overview

This project provides an end-to-end empirical workforce analytics solution. Moving beyond predictive machine learning, this project demonstrates real-world data engineering, rigorous data hygiene, SQL database architecture, business KPI formulation, and multi-platform BI design (Tableau Public and Power BI).

### Core Highlights
* **Data Engineering & Hygiene:** Resolved a critical 17-record dataset discrepancy, eliminating selection bias and avoiding target leakage present in third-party ML files.
* **Relational SQL Database:** Designed and indexed an SQLite database table (`employees`) and built 8 advanced SQL analytical scripts demonstrating CTEs, window functions (`RANK()`, `DENSE_RANK()`, `AVG() OVER()`, `NTILE()`), and conditional aggregations.
* **Multi-Platform BI Architecture:** Prepared clean, documented data extracts and implementation blueprints for both Tableau Public and Power BI.
* **Evidence-Based Business Storytelling:** Synthesized 5 verified findings highlighting retention drivers across tenure, compensation, and leadership recognition.

---

## 2. Business Problem & Analytical Objectives

Employee attrition imposes significant organizational costs, including recruitment expenses, institutional knowledge loss, and operational disruption. The primary business objectives of this study are:
1. **Baseline Workforce Health:** Establish baseline human capital KPIs (Headcount, Leavers, Attrition Rate %, Average Tenure, Average Salary).
2. **Departmental Risk Diagnostics:** Identify high-risk business units and quantify their variance against company-wide retention benchmarks.
3. **Career Lifecycle Sensitivity:** Determine at which career and organizational tenure stages flight risk concentrates.
4. **Compensation & Perception Parity:** Evaluate the interaction between base salary tiers, overtime compensation, and pay satisfaction on turnover.
5. **Workplace Sentiment & Retention ROI:** Measure the protective impact of professional development utility, management recognition, and promotion fairness.

---

## 3. Dataset Source & Provenance

* **Instrument & Origin:** The dataset was collected via a bilingual (Arabic/English) cross-sectional survey administered to working professionals across various economic sectors in the Kingdom of Saudi Arabia.
* **Core Framing Question (Q1):** *"Have you ever left a previous organization before your current job?"* (`Yes` / `No`).
* **Operational Definition of Attrition:** `Attrition = 'Yes'` identifies respondents who reported turnover history from a prior organization. Subsequent survey items evaluate work conditions, salary bands, and managerial support at their last employer.
* **HRIS vs. Survey Distinction:** This dataset is **not** an internal corporate HRIS payroll extract from a single enterprise. In reporting, "Headcount" denotes survey respondents, and "Attrition Rate" measures historical turnover prevalence. Salaries are denominated in Saudi Riyals (`SAR`).
* **Provenance Limitations:** The exact collection window, publication date, and sampling frame were not documented in the source metadata. These boundaries are documented in accordance with data governance best practices.

---

## 4. The 17-Record Discrepancy & Dataset Selection

The source project archive contained three Excel workbooks:
1. `Original Dataset of Employee Attrition.xlsx` (1,191 rows, 35 columns)
2. `Employee attrition dataset for tree-based models.xlsx` (1,174 rows, 34 columns)
3. `Employee attrition dataset for non-tree-based models.xlsx` (1,174 rows, 44 columns)

### Investigation Findings
* **Sequential Mapping:** A custom validation script (`scripts/compare_datasets.py`) mapped each row between the cleaned Original and transformed files. Exactly 1,174 rows matched 1-to-1 in sequential order.
* **Dropped Records Identification:** Exactly 17 rows were removed from the transformed files (IDs: `227, 228, 248, 263, 311, 321, 323, 328, 347, 413, 522, 894, 896, 1141, 1166, 1173, 1176`).
* **Severe Selection Bias:** **All 17 dropped records were leavers (`Attrition = 'Yes'`)**. Discarding them reduced leavers from 515 to 498, artificially deflating the attrition rate from **43.24%** down to **42.42%**.
* **Target Leakage:** The transformed files stripped the primary key (`ID`) and target-encoded `Department`, `Sector`, and `JobTitle` using `MEstimateEncoder` based on the target `Attrition`.
* **Governance Decision:** The **Original Dataset (1,191 rows)** was established as the single source of truth. All 17 valid records were retained, ensuring zero selection bias.

---

## 5. Tools & Technologies

* **Data Cleaning & Pipeline:** Python 3.14, Pandas, NumPy, OpenPyXL
* **Unit Testing:** Python `unittest` test suite (`tests/test_cleaning_suite.py`)
* **Relational Database:** SQLite 3 (`data/hr_analytics.db`)
* **SQL Development:** Advanced SQL (CTEs, Window Functions, Conditional Aggregation, Grouping)
* **Business Intelligence:** Tableau Public, Microsoft Power BI Desktop (DAX, Star Schema)
* **Version Control:** Git, GitHub

---

## 6. Project Directory Structure

```
HR-Workforce-Analytics/
│
├── .github/
│   └── workflows/
│       └── ci.yml                           # GitHub Actions CI workflow (Python 3.12, tests, SQL checks)
│
├── data/
│   ├── raw/                                 # Raw Excel workbooks and survey keys
│   ├── processed/                           # Cleaned, standardized CSV dataset
│   ├── METHODOLOGY.md                       # Documented midpoint estimation methodology & limitations
│   └── hr_analytics.db                      # Indexed SQLite database
│
├── sql/
│   ├── 01_data_quality.sql                  # Primary key, null audit, and domain constraints
│   ├── 02_workforce_kpis.sql                # Executive headcount, attrition, and tenure KPIs
│   ├── 03_attrition_analysis.sql            # Overtime, health, promotion, and turnover drivers
│   ├── 04_department_analysis.sql           # Department headcount, risk indexing, and benchmarks (N >= 20)
│   ├── 05_salary_analysis.sql               # Pay band distribution and job role DENSE_RANK()
│   ├── 06_tenure_analysis.sql               # Career stage matrix and early-tenure flight risk
│   ├── 07_satisfaction_analysis.sql         # Likert sentiment, burnout, and training utility ROI
│   └── 08_window_functions.sql              # Partition benchmarks, cumulative totals, NTILE(4)
│
├── scripts/
│   ├── inspect_data.py                      # Verifies raw workbook schemas and record counts
│   ├── compare_datasets.py                  # Identifies 17-record discrepancy and exports audit
│   ├── clean_data.py                        # Centralized MIDPOINTS dictionary, cleans whitespace
│   ├── load_database.py                     # Populates SQLite 'employees' table and creates indexes
│   ├── run_quality_checks.py                # Automated runner testing all 8 SQL files
│   ├── export_dashboard_data.py             # Exports Tableau-ready master and aggregate CSVs
│   └── calculate_findings.py                # Extracts exact empirical metrics for business findings
│
├── output/
│   ├── quality_reports/                     # Markdown and CSV data quality reports
│   └── tableau/                             # Tableau-ready master and aggregated CSV files
│
├── powerbi/                                 # Power BI report deliverables
├── tableau/                                 # Tableau Public workbook deliverables
│
├── tests/
│   ├── test_clean_data.py                   # Data cleaning unit tests
│   ├── test_cleaning_suite.py               # Dataset hygiene and entity resolution test suite
│   └── test_regression.py                   # Regression tests for midpoints, sample flags, tenure metrics
│
├── requirements.txt
├── .gitignore
└── README.md
```

---

## 7. Data Cleaning & Transformation Methodology

Implemented in `scripts/clean_data.py`:
1. **Whitespace & Non-Breaking Space Removal:** Cleaned leading/trailing whitespace and Unicode `\xa0` across all column headers and string observations. Resolved split categories (e.g., `' Married'` and `'Married'` unified to `'Married'`).
2. **Standardized Snake_Case Naming:** Renamed 35 raw survey headers into consistent, self-documenting database field names (e.g., `Allowances` $\rightarrow$ `allowance_count` to reflect that values 0–4 represent benefit counts, not monetary SAR amounts).
3. **Categorical Entity Resolution:** Harmonized 26 raw department variations into 21 standard business units and 16 raw sector variations into 15 industries. Corrected typographical errors (`'Manger assistant'` $\rightarrow$ `'Manager Assistant'`).
4. **Estimated Midpoint Approximations:** Because `Age`, `MonthlySalary`, `Years_Experience`, and `Years_experience_lastorganization` are recorded as interval bands, standardized midpoints were computed (`estimated_salary_sar`, `estimated_tenure_years`, `estimated_age_years`) to facilitate descriptive averages in SQL and BI cards.
5. **Engineered Analytic Flags:** Created binary integer indicators (`is_attrition`, `is_female`, `has_overtime`, etc.) and 1–3 standardized Likert scale ratings.

---

## 8. Database Schema & Architecture

* **Table Name:** `employees` (1,191 rows, 60 columns)
* **Primary Key:** `employee_id` (Unique, range 11 to 1213)
* **Indexes:** `idx_emp_dept`, `idx_emp_attrition`, `idx_emp_salary`, `idx_emp_tenure`, `idx_emp_satisfaction`

```sql
CREATE TABLE employees (
    employee_id INTEGER PRIMARY KEY,
    attrition TEXT NOT NULL,
    gender TEXT NOT NULL,
    age_band TEXT NOT NULL,
    marital_status TEXT NOT NULL,
    academic_degree TEXT NOT NULL,
    sector TEXT NOT NULL,
    department TEXT NOT NULL,
    job_title TEXT NOT NULL,
    monthly_salary_band TEXT NOT NULL,
    tenure_last_org_band TEXT NOT NULL,
    allowance_count INTEGER NOT NULL,
    payment_overtime TEXT NOT NULL,
    job_satisfaction TEXT NOT NULL,
    is_attrition INTEGER NOT NULL,
    estimated_salary_sar REAL,
    estimated_tenure_years REAL,
    job_satisfaction_score INTEGER,
    -- (Additional survey dimensions & engineered metrics)
);
```

---

## 9. Core SQL Analysis & Techniques

The repository includes 8 comprehensive SQL files executing across `data/hr_analytics.db`:

* **`01_data_quality.sql`:** Asserts primary key uniqueness, checks null counts across all critical reporting columns, and validates categorical domain constraints.
* **`02_workforce_kpis.sql`:** Aggregates macro organizational metrics and formats a normalized KPI key-value card table.
* **`03_attrition_analysis.sql`:** Evaluates turnover rates across compensation schemes, career advancement, and work-related health factors.
* **`04_department_analysis.sql`:** Uses CTEs to compute an **Attrition Risk Index** (`Department Attrition Rate / Company Average`) and categorizes units into risk tiers.
* **`05_salary_analysis.sql`:** Uses `DENSE_RANK() OVER (ORDER BY avg_salary DESC)` to rank job roles by pay and investigates the compensation perception gap.
* **`06_tenure_analysis.sql`:** Cross-tabulates career stage against organizational tenure to diagnose retention drop-offs.
* **`07_satisfaction_analysis.sql`:** Analyzes multi-factor sentiment (Support, Recognition, Work-Life Balance) and training program utility ROI.
* **`08_window_functions.sql`:** Employs window partitions to measure individual salary variance from departmental averages, calculates cumulative running total attrition across tenure, and segments the workforce into quartiles via `NTILE(4)`.

---

## 10. Executive KPI Summary

| KPI Metric | Value | Unit | Definition / Business Context |
| :--- | :---: | :---: | :--- |
| **Total Headcount** | **1,191** | Respondents | Total surveyed workforce population |
| **Total Leavers** | **515** | Employees | Respondents reporting having left prior employer |
| **Overall Attrition Rate** | **43.24%** | Percentage | `Total Leavers / Total Headcount` |
| **Estimated Avg Tenure** | **4.8** | Years | Estimated mean duration at last organization |
| **Estimated Avg Salary** | **SAR 7,445** | SAR / Month | Estimated mean monthly compensation across bands (`data/METHODOLOGY.md`) |
| **Avg Job Satisfaction** | **1.97 / 3.00** | Rating | Standardized Likert scale (1=Low, 2=Med, 3=High) |

---

## 11. Key Empirical Findings & Business Storytelling

### Finding 1: The Unpaid Overtime Retention Penalty
* **Observed Pattern:** Employees working **Unpaid Overtime** exhibit an attrition rate of **51.77%** (117 leavers / 226 employees). By comparison, employees receiving **Paid Overtime** show an attrition rate of **39.42%** (164 leavers / 416 employees) — a **12.35 percentage-point spread**. Those with No Overtime had an attrition rate of **42.62%** (234 leavers / 549 employees).
* **Business Interpretation:** Overtime itself is not inherently detrimental to retention; rather, uncompensated extra hours correlate strongly with higher turnover propensity.
* **Analytical Limitation:** Descriptive cross-sectional data cannot prove causality; uncompensated overtime may co-occur with broader operational stressors or understaffing.

### Finding 2: Early-Tenure Retention Dynamics (<5 Years)
* **Observed Metrics (Three-Metric Comparison):**
  * **Attrition Rate Within Group:** **53.35%** (`382 leavers / 716 group respondents`)
  * **Share of Total Recorded Leavers:** **74.17%** (`382 leavers / 515 total leavers`)
  * **Share of Total Survey Respondents:** **60.12%** (`716 respondents / 1,191 total respondents`)
* **Tenure Progression Comparison:** Attrition rate within group drops to **33.52%** (118/352) at 5–10 years, **20.00%** (15/75) at 11–15 years, and **0.00%** (0/48) beyond 16 years.
* **Business Interpretation:** While early-tenure employees account for the vast majority of leavers (74.17%), this is partly driven by their large share of the surveyed workforce (60.12%). Even after accounting for population share, the attrition rate within this group (53.35%) exceeds the organizational average (43.24%). However, a high share of leavers in a cohort does not automatically imply the highest possible attrition rate without comparing group-level denominators.
* **Methodological Warning & Analytical Limitation:** Tenure for non-leavers may be ambiguous because the source instrument measures tenure at the last organization, and the survey data may not establish whether non-leavers' responses represent completed prior employment or current tenure. Descriptive comparisons must not be interpreted as causal effects. Furthermore, tenure is measured in broad survey brackets, masking micro-trends within years 1 through 4.

### Finding 3: Departmental Retention Disparity & Sample Thresholding
* **Observed Pattern:** Applying a minimum reliability threshold of $N \ge 20$ employees separates 11 eligible departments from 10 small-sample departments:
  * **Eligible High-Risk Departments ($N \ge 20$):** **Safety & Security (66.67%, N=27)**, **Human Resources (62.22%, N=45)**, **Accounting (60.94%, N=64)**, **Processes (56.57%, N=99)**, **Public Relations (55.88%, N=34)**, and **Sales (52.17%, N=23)**.
  * **Eligible Low-Risk Departments ($N \ge 20$):** **Teaching (23.24%, N=142)** and **Patient Affairs (26.97%, N=89)**.
  * **Small-Sample Departments ($N < 20$):** 10 departments (IT, Marketing, Banking Operations, Legal Affairs, Production, Training, Treasury, Studies & Design, Engineering, Medical Service) are retained in reporting but flagged (`small_sample = 1`) with risk tiers left unassigned (`NULL`) to avoid small-sample volatility.
* **Business Interpretation:** Among sufficiently sampled departments, administrative and operational support functions experience turnover rates over 2.6 times higher than specialized public-facing roles like Teaching.
* **Analytical Limitation:** Departments with fewer than 20 respondents exhibit high sampling error, requiring suppressed risk classifications until adequate sample size is achieved.

### Finding 4: The Job Satisfaction Retention Gradient
* **Observed Pattern:** Employees reporting they were **"Not satisfied"** show an attrition rate of **58.36%** (171 leavers / 293 employees). Those who were **"Satisfied"** had a **43.19% rate** (279 / 646), and those **"Very satisfied"** had a **25.79% rate** (65 / 252).
* **Business Interpretation:** Job satisfaction demonstrates a strong, monotonic relationship with retention, reflecting a **32.57 percentage-point drop** between dissatisfied and highly satisfied staff.
* **Analytical Limitation:** Survey responses are retrospective; respondents who left may recall past experiences more negatively.

### Finding 5: Deserved Promotion and Recognition Synergy
* **Observed Pattern:** Employees receiving **neither a deserved promotion nor managerial recognition** experienced an attrition rate of **55.91%** (213 / 381). Employees receiving **both deserved promotion and recognition** experienced an attrition rate of **27.97%** (127 / 454) — cutting turnover in half.
* **Business Interpretation:** Financial compensation must be paired with career progression and moral recognition to maximize retention efficacy.
* **Analytical Limitation:** Survey questions on "deserved promotion" are self-reported and reflect subjective perception.

---

## 12. Tableau Public & Power BI Implementation

The master dataset extract and aggregated reporting tables are prepared for Tableau Public and Power BI integration:
* **Primary Reporting Extract:** [`output/tableau/hr_workforce_master.csv`](file:///f:/Big4_Project/Hr%20anlyst/Saudi%20Employee%20Attrition%20Dataset/Saudi%20Employee%20Attrition%20Dataset/HR-Workforce-Analytics/output/tableau/hr_workforce_master.csv) (1,191 rows, 60 features)
* **Pre-Aggregated Benchmarks:** [`output/tableau/department_attrition_benchmark.csv`](file:///f:/Big4_Project/Hr%20anlyst/Saudi%20Employee%20Attrition%20Dataset/Saudi%20Employee%20Attrition%20Dataset/HR-Workforce-Analytics/output/tableau/department_attrition_benchmark.csv)

### Visual Architecture:
1. **Executive KPI Header:** Total Headcount (1,191), Leavers (515), Attrition Rate (43.2%), Estimated Avg Tenure (4.8 yrs).
2. **Department Benchmark:** Bar chart comparing departmental attrition rates against the 43.2% benchmark line, conditionally formatted by risk tier.
3. **Headcount Volume:** Departmental scale distribution.
4. **Tenure Lifecycle Curve:** Column chart highlighting the 74.2% leaver concentration in the <5 years tenure band.
5. **Satisfaction Gradient:** Attrition elasticity across satisfaction levels.
6. **Interactive Slicers:** Dynamic filtering by Department, Industry Sector, Salary Tier, and Gender.

---

## 13. How to Reproduce the Analysis

### 1. Clone the Repository
```bash
git clone https://github.com/Piyushh95/HR-Workforce-Analytics.git
cd HR-Workforce-Analytics
```

### 2. Set Up Environment
```bash
python -m venv venv
# Windows:
venv\Scripts\activate
# Mac/Linux:
# source venv/bin/activate
pip install -r requirements.txt
```

### 3. Run Pipeline Scripts
```bash
# Step 1: Inspect raw files
python scripts/inspect_data.py

# Step 2: Verify 17-record discrepancy
python scripts/compare_datasets.py

# Step 3: Clean and validate dataset
python scripts/clean_data.py

# Step 4: Run test suite (unit & regression tests)
python -m unittest discover tests

# Step 5: Load SQLite database
python scripts/load_database.py

# Step 6: Test all 8 SQL files
python scripts/run_quality_checks.py

# Step 7: Export Tableau / Power BI extracts
python scripts/export_dashboard_data.py
```

---

## 14. Continuous Integration & Quality Assurance

Automated testing is configured via GitHub Actions in [`.github/workflows/ci.yml`](file:///.github/workflows/ci.yml):
* **Environment:** Python 3.12 runner
* **Test Stages:**
  1. `python -m unittest discover tests` — Executes data cleaning, entity resolution, and regression tests (verifying midpoints, boundary conditions $N=19, 20, 21$, and tenure metric definitions).
  2. `python scripts/load_database.py` — Builds indexed SQLite database.
  3. `python scripts/run_quality_checks.py` — Executes and validates all 29 SQL queries across 8 analytical files.

---

## 15. Project Limitations

1. **Retrospective Survey Design:** The data captures self-reported employee sentiment rather than objective, continuous transactional logs from an enterprise HRIS.
2. **Grouped Ordinal Fields:** Age, tenure, and monthly compensation are measured in categorical brackets rather than exact numbers, requiring midpoint approximations (`data/METHODOLOGY.md`) for aggregate mathematical averages.
3. **Non-Leaver Tenure Ambiguity:** The source instrument measures tenure at the last organization; survey data may not establish whether non-leavers' responses represent completed prior employment or current tenure.
4. **Provenance Boundaries:** Specific collection dates and institutional affiliations were not stated in the source documentation.
5. **Descriptive Nature:** All analyses demonstrate observed statistical correlations; direct causality cannot be inferred without controlled experimental or longitudinal data.

---

## 16. Future Enhancements

* **Time-to-Event Survival Analysis:** Implement Kaplan-Meier survival curves and Cox proportional hazards modeling if longitudinal date timestamps become available.
* **Exit Interview Natural Language Processing (NLP):** Incorporate qualitative open-text survey fields using sentiment analysis.
