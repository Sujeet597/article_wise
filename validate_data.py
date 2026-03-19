"""
Data Validation Script for MSA Article Stock Analysis
Validates that all required data files exist and are accessible before processing
"""

import pandas as pd
from pathlib import Path
import sys

def validate_files():
    """Validate all required data files exist and can be read"""
    
    print("\n" + "=" * 80)
    print("MSA ARTICLE STOCK ANALYSIS - DATA VALIDATION")
    print("=" * 80 + "\n")
    
    issues = []
    warnings = []
    
    # Check MSA files
    print("Checking MSA_STORENAME files...")
    print("-" * 80)
    
    msa_dir = Path('MSA_STORENAME')
    if not msa_dir.exists():
        issues.append(f"Directory not found: {msa_dir}/")
        print(f"✗ MSA_STORENAME/ directory not found")
    else:
        print(f"✓ MSA_STORENAME/ directory exists")
        
        # Check for article file
        article_file = msa_dir / 'Generated_Colors_2026-03-14.csv'
        if not article_file.exists():
            issues.append(f"File not found: {article_file}")
            print(f"✗ Generated_Colors_2026-03-14.csv not found")
        else:
            try:
                df = pd.read_csv(article_file)
                print(f"✓ Generated_Colors_2026-03-14.csv ({len(df):,} rows, {len(df.columns)} columns)")
                
                # Check for required columns
                required_cols = ['STK_QTY', 'MAJ_CAT', 'GEN_ART_NUMBER', 'DATE', 'ST_CD']
                missing = [col for col in required_cols if col not in df.columns]
                if missing:
                    warnings.append(f"Missing columns in article file: {', '.join(missing)}")
                    print(f"  ⚠ Missing columns: {', '.join(missing)}")
                
            except Exception as e:
                issues.append(f"Error reading article file: {str(e)}")
                print(f"✗ Error reading file: {str(e)}")
        
        # Check for store file
        store_file = msa_dir / 'STORE NAME.xlsx'
        if not store_file.exists():
            issues.append(f"File not found: {store_file}")
            print(f"✗ STORE NAME.xlsx not found")
        else:
            try:
                df = pd.read_excel(store_file)
                print(f"✓ STORE NAME.xlsx ({len(df):,} rows, {len(df.columns)} columns)")
            except Exception as e:
                issues.append(f"Error reading store file: {str(e)}")
                print(f"✗ Error reading file: {str(e)}")
    
    # Check BASE DATA files
    print("\nChecking BASE DATA files...")
    print("-" * 80)
    
    base_dir = Path('BASE DATA')
    if not base_dir.exists():
        issues.append(f"Directory not found: {base_dir}/")
        print(f"✗ BASE DATA/ directory not found")
    else:
        print(f"✓ BASE DATA/ directory exists")
        
        categories = ['GM', 'KIDS', 'LADIES', 'MENS']
        found_count = 0
        
        for cat in categories:
            file_path = base_dir / f'BASE-DATA-{cat}.csv'
            if not file_path.exists():
                warnings.append(f"File not found: BASE-DATA-{cat}.csv")
                print(f"⚠ BASE-DATA-{cat}.csv not found")
            else:
                try:
                    df = pd.read_csv(file_path)
                    print(f"✓ BASE-DATA-{cat}.csv ({len(df):,} rows, {len(df.columns)} columns)")
                    found_count += 1
                except Exception as e:
                    warnings.append(f"Error reading BASE-DATA-{cat}.csv: {str(e)}")
                    print(f"✗ BASE-DATA-{cat}.csv: {str(e)}")
        
        if found_count < 4:
            warnings.append(f"Only {found_count}/4 BASE DATA files found")
    
    # Check LIST files
    print("\nChecking LIST files...")
    print("-" * 80)
    
    list_dir = Path('LIST')
    if not list_dir.exists():
        issues.append(f"Directory not found: {list_dir}/")
        print(f"✗ LIST/ directory not found")
    else:
        print(f"✓ LIST/ directory exists")
        
        categories = ['GM', 'KIDS', 'LADIES', 'MENS']
        found_count = 0
        
        for cat in categories:
            file_path = list_dir / f'{cat}-ALL.csv'
            if not file_path.exists():
                warnings.append(f"File not found: {cat}-ALL.csv")
                print(f"⚠ {cat}-ALL.csv not found")
            else:
                try:
                    df = pd.read_csv(file_path)
                    print(f"✓ {cat}-ALL.csv ({len(df):,} rows, {len(df.columns)} columns)")
                    found_count += 1
                except Exception as e:
                    warnings.append(f"Error reading {cat}-ALL.csv: {str(e)}")
                    print(f"✗ {cat}-ALL.csv: {str(e)}")
        
        if found_count < 4:
            warnings.append(f"Only {found_count}/4 LIST files found")
    
    # Summary
    print("\n" + "=" * 80)
    print("VALIDATION SUMMARY")
    print("=" * 80)
    
    if issues:
        print(f"\n❌ CRITICAL ISSUES ({len(issues)}):")
        for i, issue in enumerate(issues, 1):
            print(f"  {i}. {issue}")
    
    if warnings:
        print(f"\n⚠️  WARNINGS ({len(warnings)}):")
        for i, warning in enumerate(warnings, 1):
            print(f"  {i}. {warning}")
    
    if not issues:
        print("\n✅ All critical files are present and valid!")
        if not warnings:
            print("✅ No warnings detected!")
            print("\nYou can now run: python app.py")
        else:
            print(f"\n⚠️  {len(warnings)} warning(s) detected. Processing may have incomplete data.")
            print("Consider fixing warnings before running app.py")
        
        return True
    else:
        print(f"\n❌ {len(issues)} critical issue(s) detected.")
        print("Please fix these issues before running app.py")
        return False
    
    print("=" * 80 + "\n")


if __name__ == '__main__':
    success = validate_files()
    sys.exit(0 if success else 1)
