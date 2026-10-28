# Power BI Implementation Plan & DAX Measure Specifications

**Project:** HR Workforce Analytics & Attrition Intelligence  
**Target Environment:** Power BI Desktop / Power BI Service  
**Primary Data Source:** `data/processed/cleaned_employee_attrition.csv` (or SQLite `data/hr_analytics.db`)  

---

## 1. Recommended Data Model

### Architecture: Star Schema (or High-Performance Analytic Flat Fact)
For enterprise scalability, the model is structured into a central fact table and supporting dimension tables:

```
┌──────────────────────┐              ┌───────────────────────────┐
│    Dim_Department    │              │        Dim_Sector         │
├──────────────────────┤              ├───────────────────────────┤
│ Department (PK)      │1            1│ Sector (PK)               │
│ Division / Category  │──┐        ┌──│ Industry Group            │
└──────────────────────┘  │        │  └───────────────────────────┘
                          │        │
                          ▼*       ▼*
               ┌─────────────────────────────────┐
               │         Fact_Employees          │
               ├─────────────────────────────────┤
               │ employee_id (PK)                │
               │ department (FK)                 │
               │ sector (FK)                     │
               │ is_attrition                    │
               │ monthly_salary_band             │
               │ estimated_salary_sar            │
               │ tenure_last_org_band            │
               │ estimated_tenure_years          │
               │ job_satisfaction                │
               │ job_satisfaction_score          │
               │ work_life_balance               │
               │ ...                             │
               └─────────────────────────────────┘
```

*Note: In local Desktop deployments, loading `hr_workforce_master.csv` directly as `Fact_Employees` provides full functionality with zero relational overhead.*

---

## 2. Core DAX Measure Definitions

Enter these measures into a dedicated `_Measures` table:

### Base Headcount
```dax
Total Headcount = 
COUNTROWS(Fact_Employees)
```

### Leavers Count
```dax
Total Leavers = 
CALCULATE(
    COUNTROWS(Fact_Employees),
    Fact_Employees[attrition] = "Yes"
)
```

### Retained Headcount
```dax
Total Retained = 
CALCULATE(
    COUNTROWS(Fact_Employees),
    Fact_Employees[attrition] = "No"
)
```

### Attrition Rate (%)
```dax
Attrition Rate = 
DIVIDE([Total Leavers], [Total Headcount], 0)
```
*Format: Percentage (`0.0%`)*

### Organization Attrition Benchmark (Ignores Department Filter)
```dax
Company Benchmark Attrition Rate = 
CALCULATE(
    [Attrition Rate],
    ALL(Fact_Employees[department])
)
```

### Attrition Rate Variance vs. Benchmark
```dax
Attrition Variance vs Benchmark = 
[Attrition Rate] - [Company Benchmark Attrition Rate]
```
*Format: Percentage with sign (`+0.0%;-0.0%`)*

### Estimated Average Monthly Salary
```dax
Avg Monthly Salary (SAR) = 
AVERAGE(Fact_Employees[estimated_salary_sar])
```
*Format: Currency (`$#,##0` or `SAR #,##0`)*

### Estimated Average Tenure
```dax
Avg Tenure (Years) = 
AVERAGE(Fact_Employees[estimated_tenure_years])
```
*Format: Decimal (`0.0`)*

### Department Risk Tier (Dynamic DAX Measure)
```dax
Department Risk Tier = 
VAR AttrRate = [Attrition Rate]
VAR CompRate = [Company Benchmark Attrition Rate]
RETURN
    SWITCH(
        TRUE(),
        AttrRate > CompRate + 0.05, "High Risk (>5% Above Avg)",
        AttrRate < CompRate - 0.05, "Low Risk (>5% Below Avg)",
        "Moderate Risk"
    )
```

### Dynamic Hex Color for Conditional Formatting
```dax
Risk Color Code = 
VAR AttrRate = [Attrition Rate]
VAR CompRate = [Company Benchmark Attrition Rate]
RETURN
    SWITCH(
        TRUE(),
        AttrRate > CompRate + 0.05, "#DC2626", -- Crimson Red
        AttrRate < CompRate - 0.05, "#0D9488", -- Teal
        "#64748B" -- Slate Grey
    )
```

---

## 3. Power BI Visual Report Layout

* **Report Page Canvas:** 16:9 Widescreen (1280 × 720 px or 1920 × 1080 px).
* **Theme:** Corporate Deep Navy (`#0F172A`) & Crisp Slate (`#F1F5F9`).

### Page 1: Executive Workforce Retention Overview
1. **Header Banner:**
   - Visual: Text Box & Card.
   - Text: **HR Workforce Analytics — Executive Retention Report**
   - Subtitle: *Empirical Workforce Insights (Saudi Arabia Survey Sample, N = 1,191)*
2. **Top Row KPI Cards (4 New Card Visuals):**
   - Card 1: `Total Headcount` (1,191)
   - Card 2: `Total Leavers` (515)
   - Card 3: `Attrition Rate` (43.2%)
   - Card 4: `Avg Tenure (Years)` (4.8 Yrs)
3. **Mid-Left Visual: Department Attrition Rate vs. Company Benchmark**
   - Visual: Clustered Bar Chart.
   - Y-Axis: `department`
   - X-Axis: `Attrition Rate`
   - Constant Line: `43.2%` (Labeled: Company Benchmark)
   - Data Bar Color: Conditional formatting using field `[Risk Color Code]`.
4. **Mid-Right Visual: Headcount Volume by Department**
   - Visual: Treemap or Horizontal Bar Chart.
   - Category: `department`
   - Values: `Total Headcount`
5. **Bottom-Left Visual: Attrition by Career Stage (Tenure Band)**
   - Visual: Column Chart.
   - X-Axis: `tenure_last_org_band` (Sorted chronologically by `estimated_tenure_years`)
   - Y-Axis: `Attrition Rate`
6. **Bottom-Right Visual: Attrition Rate by Overall Job Satisfaction**
   - Visual: 100% Stacked Column Chart or Donut Chart.
   - Legend: `job_satisfaction` (`Not satisfied`, `Satisfied`, `Very satisfied`)
   - Values: `Total Headcount`
7. **Slicers Panel (Top Right / Collapsible Bookmark Panel):**
   - Department (`department`)
   - Industry Sector (`sector`)
   - Monthly Salary Tier (`monthly_salary_band`)
   - Gender (`gender`)

---

## 4. Data Refresh & Production Governance

* **Scheduled Refresh:** Configure automated scheduled refresh in Power BI Service via Personal or Enterprise On-Premises Data Gateway if connecting to the local SQLite database.
* **CSV Alternative:** In Web or SharePoint deployments, host `hr_workforce_master.csv` on SharePoint Online / OneDrive for Business to enable direct cloud-to-cloud automated scheduled refreshes without a gateway.
* **Security & Row-Level Security (RLS):**
  If role-based departmental filtering is required:
  ```dax
  [department] = USERNAME()
  ```
