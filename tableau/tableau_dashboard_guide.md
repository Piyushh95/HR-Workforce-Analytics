# Tableau Public Dashboard Implementation Guide

**Project:** HR Workforce Analytics & Attrition Intelligence  
**Target Environment:** Tableau Desktop / Tableau Public  
**Primary Data Source:** `output/tableau/hr_workforce_master.csv` (1,191 rows, 60 columns)  

---

## 1. Data Connection Setup

1. Open **Tableau Public** or **Tableau Desktop**.
2. Under **Connect to a File**, select **Text File**.
3. Browse to and select `output/tableau/hr_workforce_master.csv`.
4. Verify that all 1,191 rows load cleanly with appropriate data types:
   - `employee_id`: Number (Whole) / Dimension
   - `is_attrition`: Number (Whole) / Measure
   - `estimated_salary_sar`: Number (Decimal) / Measure
   - `estimated_tenure_years`: Number (Decimal) / Measure
   - `job_satisfaction_score`: Number (Whole) / Measure
   - `department`, `sector`, `job_title`, `monthly_salary_band`: String / Dimension

---

## 2. Calculated Fields Specifications

Create the following calculated fields in Tableau to ensure consistent business metric definitions:

### Metric 1: Headcount
* **Field Name:** `Total Headcount`
* **Formula:**
  ```tableau
  COUNT([employee_id])
  ```
* **Format:** Number (Standard), e.g., `1,191`

### Metric 2: Attrition Count
* **Field Name:** `Attrition Count`
* **Formula:**
  ```tableau
  SUM([is_attrition])
  ```
* **Format:** Number (Standard), e.g., `515`

### Metric 3: Attrition Rate (%)
* **Field Name:** `Attrition Rate`
* **Formula:**
  ```tableau
  SUM([is_attrition]) / COUNT([employee_id])
  ```
* **Format:** Percentage (1 decimal place), e.g., `43.2%`

### Metric 4: Estimated Average Tenure
* **Field Name:** `Estimated Avg Tenure (Years)`
* **Formula:**
  ```tableau
  AVG([estimated_tenure_years])
  ```
* **Format:** Number (Decimal, 1 place), e.g., `4.8 Years`

### Metric 5: Estimated Average Monthly Salary
* **Field Name:** `Estimated Avg Salary (SAR)`
* **Formula:**
  ```tableau
  AVG([estimated_salary_sar])
  ```
* **Format:** Currency (Custom), Prefix `SAR `, 0 decimal places, e.g., `SAR 7,853`

### Metric 6: Department Risk Tier (Color Dimension)
* **Field Name:** `Department Risk Tier`
* **Formula:**
  ```tableau
  IF [Attrition Rate] > 0.482 THEN 'High Risk (>5% Above Avg)'
  ELSEIF [Attrition Rate] < 0.382 THEN 'Low Risk (>5% Below Avg)'
  ELSE 'Moderate Risk'
  END
  ```

---

## 3. Worksheet Build Instructions

### Worksheet 1: KPI Summary Cards (Executive Banner)
* **Type:** KPI Text Cards (4 separate small sheets or single card row).
* **Measures:**
  - Card 1: `Total Headcount` (`1,191`)
  - Card 2: `Attrition Count` (`515`)
  - Card 3: `Attrition Rate` (`43.2%`)
  - Card 4: `Estimated Avg Tenure` (`4.8 yrs`)
* **Styling:** Large font (24pt bold, deep navy `#1A365D`), subtle grey subtext label (10pt `#718096`).

### Worksheet 2: Attrition Rate by Department (Bar Chart)
* **Rows:** `department` (Sorted by `Attrition Rate` Descending)
* **Columns:** `Attrition Rate`
* **Color:** `Department Risk Tier` (Red: `#E53E3E`, Blue/Grey: `#718096`, Teal: `#319795`)
* **Marks:** Add Reference Line at `0.432` labeled `"Company Benchmark: 43.2%"`.
* **Tooltip:** Department Name, Total Headcount, Leavers Count, Attrition Rate.

### Worksheet 3: Headcount Volume by Department (Horizontal Bar)
* **Rows:** `department` (Sorted by `Total Headcount` Descending)
* **Columns:** `Total Headcount`
* **Color:** `gender` or `#2B6CB0` (Subtle corporate navy)
* **Label:** `Total Headcount` at bar end.

### Worksheet 4: Attrition Across Tenure Groups (Column Chart)
* **Columns:** `tenure_last_org_band` (Ordered manually: `<5 years`, `5 to 10 years`, `11 to 15 years`, `16 to 20 years`, `21 to 25 years`, `26 to 30 years`, `31 to 35 years`)
* **Rows:** `Attrition Rate`
* **Marks:** Line or Bar with Data Labels. Dual-axis: add Bar for `Total Headcount` (grey background) and Line for `Attrition Rate` (coral red).

### Worksheet 5: Attrition by Job Satisfaction Level (Donut or Heatmap)
* **Columns:** `job_satisfaction` (`Not satisfied`, `Satisfied`, `Very satisfied`)
* **Rows:** `Attrition Rate`
* **Bar Color:** Color gradient from Dark Red (`Not satisfied`: ~58.2%) to Slate (`Satisfied`: ~41.1%) to Vibrant Teal (`Very satisfied`: ~30.8%).

### Worksheet 6: Monthly Salary Distribution & Pay Equity (Boxplot / Stacked Bar)
* **Columns:** `monthly_salary_band` (Ordered by salary magnitude)
* **Rows:** `Total Headcount`
* **Color:** `attrition` (`Yes`: Leavers, `No`: Retained)
* **Insight Annotation:** Over 82% of workforce concentrated under 10,000 SAR/month.

---

## 4. Dashboard Assembly & Layout Guidelines

* **Target Canvas Size:** Fixed Size, **1366 × 768 px** or **1440 × 900 px** (Standard Modern Widescreen).
* **Color Palette:**
  - Executive Navy: `#0F172A` (Headers / Titles)
  - Card Background: `#F8FAFC` (Clean light off-white)
  - Attrition Alert Red: `#DC2626`
  - Retained / Neutral Slate: `#475569`
  - Accent Blue: `#2563EB`
* **Top Header (Height ~80px):**
  - Title: **HR Workforce Analytics & Talent Retention Dashboard**
  - Subtitle: *Empirical workforce study on turnover patterns and employee sentiment in Saudi Arabia (N = 1,191)*
  - Source Note: *Retrospective cross-sectional survey data; SAR currency.*
* **Row 1 (Height ~100px):** 4 Horizontal KPI Cards.
* **Row 2 (Height ~300px):**
  - Left: *Worksheet 2 (Attrition Rate by Department)* (55% width).
  - Right: *Worksheet 3 (Headcount Volume by Department)* (45% width).
* **Row 3 (Height ~280px):**
  - Left: *Worksheet 4 (Attrition by Tenure Group)* (50% width).
  - Right: *Worksheet 5 (Attrition by Job Satisfaction)* (50% width).
* **Right/Top Slicer Panel:**
  - Slicer 1: `Department` (Multiple Values Dropdown)
  - Slicer 2: `Sector` (Dropdown)
  - Slicer 3: `Monthly Salary Band` (Dropdown)
  - Slicer 4: `Gender` (Radio button / List)

---

## 5. Screenshot Checklist & Verification

When publishing to Tableau Public or capturing desktop screenshots, verify:
- [ ] Header title and data provenance caveat are clearly legible.
- [ ] All 4 KPI card values match exact verified totals: Headcount = 1,191, Attrition = 515, Rate = 43.2%, Avg Tenure = 4.8 yrs.
- [ ] No chart labels are truncated or overlapping.
- [ ] Interactive filters cross-filter all 4 charts properly.
- [ ] Color legends clearly distinguish between Retained and Leavers.
- [ ] Evidence-based callout annotation highlights key retention findings.
