"""
inspect_data.py
Performs initial structural inspection of raw HR datasets in data/raw.
Reports row/column counts, sheets, data types, nulls, and duplicates.
"""

import os
import openpyxl
import pandas as pd


def inspect_raw_files(data_dir: str = "data/raw") -> dict:
    files = [
        "Original Dataset of Employee Attrition.xlsx",
        "Employee attrition dataset for tree-based models.xlsx",
        "Employee attrition dataset for non-tree-based models.xlsx"
    ]
    
    results = {}
    print("=" * 70)
    print("RAW DATASET STRUCTURAL INSPECTION REPORT")
    print("=" * 70)
    
    for filename in files:
        filepath = os.path.join(data_dir, filename)
        if not os.path.exists(filepath):
            print(f"[ERROR] File not found: {filepath}")
            continue
            
        wb = openpyxl.load_workbook(filepath, read_only=True)
        sheets = wb.sheetnames
        wb.close()
        
        df = pd.read_excel(filepath)
        null_total = int(df.isnull().sum().sum())
        dup_rows = int(df.duplicated().sum())
        
        id_col = "ID" if "ID" in df.columns else None
        dup_no_id = int(df.drop(columns=[id_col]).duplicated().sum()) if id_col else None
        
        results[filename] = {
            "sheets": sheets,
            "rows": len(df),
            "columns": len(df.columns),
            "null_total": null_total,
            "duplicate_rows": dup_rows,
            "has_id": id_col is not None,
            "duplicate_ignoring_id": dup_no_id,
            "column_names": list(df.columns)
        }
        
        print(f"\n--- {filename} ---")
        print(f"Sheets: {sheets}")
        print(f"Shape: {len(df)} rows x {len(df.columns)} columns")
        print(f"Missing Values (Nulls): {null_total}")
        print(f"Full Row Duplicates: {dup_rows}")
        if id_col:
            print(f"Identifier: {id_col} present (Min: {df[id_col].min()}, Max: {df[id_col].max()}, Unique: {df[id_col].nunique()})")
            print(f"Duplicates ignoring ID: {dup_no_id}")
        else:
            print("Identifier: None (ID dropped in transformed file)")
            
    return results


if __name__ == "__main__":
    inspect_raw_files()
