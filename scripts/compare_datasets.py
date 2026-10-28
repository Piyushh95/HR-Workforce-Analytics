"""
compare_datasets.py
Compares the Original dataset against the Tree-based and Non-tree-based datasets.
Investigates the 17-record discrepancy, validates row-level alignment,
and documents reasons for retaining the 1,191-row Original dataset.
"""

import os
import pandas as pd
import numpy as np


def run_dataset_comparison(data_dir: str = "data/raw", output_dir: str = "output/quality_reports"):
    orig_path = os.path.join(data_dir, "Original Dataset of Employee Attrition.xlsx")
    tree_path = os.path.join(data_dir, "Employee attrition dataset for tree-based models.xlsx")
    nontree_path = os.path.join(data_dir, "Employee attrition dataset for non-tree-based models.xlsx")
    
    os.makedirs(output_dir, exist_ok=True)
    
    print("=" * 70)
    print("DATASET COMPARISON & 17-RECORD DISCREPANCY INVESTIGATION")
    print("=" * 70)
    
    df_orig = pd.read_excel(orig_path)
    df_tree = pd.read_excel(tree_path)
    df_nontree = pd.read_excel(nontree_path)
    
    print(f"Original Dataset Shape:  {df_orig.shape[0]} rows x {df_orig.shape[1]} columns")
    print(f"Tree-based Dataset Shape: {df_tree.shape[0]} rows x {df_tree.shape[1]} columns")
    print(f"Non-tree Dataset Shape:   {df_nontree.shape[0]} rows x {df_nontree.shape[1]} columns")
    
    # 1. Compare Tree vs Non-tree
    shared_cols = [c for c in df_tree.columns if c in df_nontree.columns]
    mismatches = [c for c in shared_cols if not (df_tree[c] == df_nontree[c]).all()]
    print(f"\nTree vs Non-Tree shared columns: {len(shared_cols)} columns")
    print(f"Value mismatches in shared columns: {len(mismatches)}")
    
    # 2. Sequential Row Matching between Original and Tree
    # Clean original strings for mapping
    df_orig_clean = df_orig.copy()
    df_orig_clean.columns = [c.strip().replace('\xa0', '').replace(' ', '_') for c in df_orig_clean.columns]
    for c in df_orig_clean.columns:
        if c not in ['ID', 'Allowances']:
            df_orig_clean[c] = df_orig_clean[c].astype(str).str.strip().str.replace('\xa0', '')
            
    binary_map = {'Yes': 1, 'No': 0, '1': 1, '0': 0}
    df_orig_enc = pd.DataFrame()
    df_orig_enc['ID'] = df_orig_clean['ID']
    df_orig_enc['Attrition'] = df_orig_clean['Attrition'].map(binary_map)
    df_orig_enc['Gender'] = df_orig_clean['Gender'].map({'Male': 1, 'Female': 0})
    df_orig_enc['Age'] = df_orig_clean['Age'].map({'21 to 30': 0, '31 to 40': 1, '41 to 50': 2, '51 to 60': 2})
    df_orig_enc['Academic_degree'] = df_orig_clean['Academic_degree'].map(
        {'Diploma or secondary': 0, "Bachelor's": 1, "Master's": 2, 'Ph.D': 3}
    )
    df_orig_enc['Allowances'] = df_orig_clean['Allowances'].astype(int)
    df_orig_enc['MedicalInsurance'] = df_orig_clean['MedicalInsurance'].map(binary_map)
    df_orig_enc['Bonus'] = df_orig_clean['Bonus'].map(binary_map)
    df_orig_enc['OverTime'] = df_orig_clean['OverTime'].map(binary_map)
    df_orig_enc['Payment_Overtime'] = df_orig_clean['Payment_Overtime'].map(
        {'No Overtime': 0, "I don't have overtime": 0, 'No': 1, 'Yes': 2}
    )
    df_orig_enc['Rewards_Wages_Satisfaction'] = df_orig_clean['Rewards&Wages_Satisfaction'].map(binary_map)
    df_orig_enc['Get_Deserved_Promotion'] = df_orig_clean['Get__Deserved_Promotion'].map(binary_map)
    df_orig_enc['Useful_Training_Programs'] = df_orig_clean['Useful_Training_Programs'].map(binary_map)
    df_orig_enc['Business_Travel'] = df_orig_clean['Business_Travel'].map(
        {'I do not travel for work': 0, 'Travel rarely': 1, 'Travel frequently': 2}
    )
    df_orig_enc['Job_Support'] = df_orig_clean['Job_Support'].map({'Low': 0, 'Medium': 1, 'High': 2})
    df_orig_enc['Recognition'] = df_orig_clean['Recognition'].map(binary_map)
    df_orig_enc['Emotional_Commitment'] = df_orig_clean['Emotional_Commitment'].map({'Low': 0, 'Medium': 1, 'High': 2})
    df_orig_enc['Job_Engagement'] = df_orig_clean['Job_Engagement'].map({'Easy': 0, 'Medium': 1, 'Difficult': 2})
    df_orig_enc['Distance_to_work'] = df_orig_clean['Distance_to_work'].map({'Close': 0, 'Medium': 1, 'Far': 2})
    df_orig_enc['Work_Live_Balance'] = df_orig_clean['Work_Live_Balance'].map({'Easy': 0, 'Medium': 1, 'Difficult': 2})
    df_orig_enc['Physical_Stress'] = df_orig_clean['Physical_Stress'].map({'No': 0, 'Sometimes': 1, 'Yes': 2})
    df_orig_enc['Psychological_Exhaustion'] = df_orig_clean['Psychological_Exhaustion'].map({'No': 0, 'Sometimes': 1, 'Yes': 2})
    df_orig_enc['Job_Stability'] = df_orig_clean['Job_Stability'].map(binary_map)
    df_orig_enc['Health_Issues'] = df_orig_clean['Health_Issues'].map(binary_map)
    df_orig_enc['Environment_Satisfaction'] = df_orig_clean['Environment_Satisfaction'].map({'Low': 0, 'Medium': 1, 'High': 2})
    df_orig_enc['Job_Satisfaction'] = df_orig_clean['Job_Satisfaction'].map(
        {'Not satisfied': 0, 'Satisfied': 1, 'Very satisfied': 2}
    )
    df_orig_enc['Job_Opportunities'] = df_orig_clean['Job_Opportunities'].map(binary_map)
    
    feat_cols = [c for c in df_orig_enc.columns if c != 'ID']
    
    orig_idx = 0
    tree_idx = 0
    dropped_orig_indices = []
    
    while orig_idx < len(df_orig_enc) and tree_idx < len(df_tree):
        orig_vals = tuple(df_orig_enc.iloc[orig_idx][feat_cols].values)
        tree_vals = tuple(df_tree.iloc[tree_idx][feat_cols].values)
        if orig_vals == tree_vals:
            orig_idx += 1
            tree_idx += 1
        else:
            dropped_orig_indices.append(orig_idx)
            orig_idx += 1
            
    while orig_idx < len(df_orig_enc):
        dropped_orig_indices.append(orig_idx)
        orig_idx += 1
        
    dropped_df = df_orig.iloc[dropped_orig_indices].copy()
    dropped_csv_path = os.path.join(output_dir, "dropped_17_records.csv")
    dropped_df.to_csv(dropped_csv_path, index=False)
    
    orig_attr_counts = df_orig['Attrition'].astype(str).str.strip().value_counts()
    orig_rate = (orig_attr_counts.get('Yes', 0) / len(df_orig)) * 100
    tree_attr_counts = df_tree['Attrition'].value_counts()
    tree_rate = (tree_attr_counts.get(1, 0) / len(df_tree)) * 100
    
    print(f"\n--- Discrepancy Findings ---")
    print(f"Total rows matched sequentially: {tree_idx} / {len(df_tree)}")
    print(f"Total dropped rows identified: {len(dropped_df)}")
    print(f"Dropped IDs: {list(dropped_df['ID'])}")
    print(f"Attrition of dropped records: {dropped_df['Attrition'].astype(str).str.strip().value_counts().to_dict()}")
    print(f"Original Attrition Rate: {orig_rate:.2f}% ({orig_attr_counts.get('Yes', 0)} / {len(df_orig)})")
    print(f"Transformed Attrition Rate: {tree_rate:.2f}% ({tree_attr_counts.get(1, 0)} / {len(df_tree)})")
    print(f"Discrepancy impact: Bias reduction of {orig_rate - tree_rate:.2f}% points in attrition rate.")
    print(f"Report exported: {dropped_csv_path}")
    
    return {
        "dropped_count": len(dropped_df),
        "dropped_ids": list(dropped_df['ID']),
        "orig_attrition_rate": orig_rate,
        "transformed_attrition_rate": tree_rate
    }


if __name__ == "__main__":
    run_dataset_comparison()
