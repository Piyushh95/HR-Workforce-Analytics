"""
run_quality_checks.py
Executes all SQL scripts in the sql/ folder against data/hr_analytics.db.
Verifies syntax, asserts execution without errors, and prints sample query outputs.
"""

import os
import sqlite3
import glob


def test_sql_scripts(db_path: str = "data/hr_analytics.db", sql_dir: str = "sql"):
    print("=" * 70)
    print("EXECUTING SQL TEST SUITE AGAINST SQLITE DATABASE")
    print("=" * 70)
    
    if not os.path.exists(db_path):
        raise FileNotFoundError(f"Database not found at {db_path}. Run load_database.py first.")
        
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    sql_files = sorted(glob.glob(os.path.join(sql_dir, "*.sql")))
    print(f"Found {len(sql_files)} SQL files in {sql_dir}/\n")
    
    passed = 0
    failed = 0
    
    for filepath in sql_files:
        filename = os.path.basename(filepath)
        print(f"Testing {filename}...")
        
        with open(filepath, 'r', encoding='utf-8') as f:
            full_sql = f.read()
            
        # SQLite executescript or splitting queries by semicolon
        # Clean statements
        statements = [stmt.strip() for stmt in full_sql.split(';') if stmt.strip()]
        
        file_passed = True
        for i, stmt in enumerate(statements, 1):
            try:
                cursor.execute(stmt)
                rows = cursor.fetchall()
                # print first statement output sample
                if i == 1:
                    col_names = [desc[0] for desc in cursor.description] if cursor.description else []
                    print(f"   Query {i} OK ({len(rows)} rows returned, cols: {col_names[:4]})")
            except Exception as e:
                print(f"   [ERROR] in Query {i}: {e}")
                file_passed = False
                
        if file_passed:
            print(f"   [PASS] {filename} (All {len(statements)} queries executed successfully)\n")
            passed += 1
        else:
            print(f"   [FAIL] {filename}\n")
            failed += 1
            
    conn.close()
    
    print("=" * 70)
    print(f"SQL TEST SUMMARY: {passed} PASSED, {failed} FAILED (Total: {len(sql_files)})")
    print("=" * 70)
    
    if failed > 0:
        raise RuntimeError(f"{failed} SQL files failed execution.")


if __name__ == "__main__":
    test_sql_scripts()
