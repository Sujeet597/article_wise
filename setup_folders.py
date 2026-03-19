"""
Setup script to create required folder structure for MSA Article Stock Analysis
Run this once to create all necessary directories
"""

import os
from pathlib import Path

def create_folder_structure():
    """Create all required directories"""
    
    directories = [
        'MSA_STORENAME',
        'BASE DATA',
        'LIST',
    ]
    
    print("Creating folder structure for MSA Article Stock Analysis...")
    print("=" * 60)
    
    for directory in directories:
        dir_path = Path(directory)
        
        if dir_path.exists():
            print(f"✓ {directory}/ (already exists)")
        else:
            dir_path.mkdir(exist_ok=True)
            print(f"✓ {directory}/ (created)")
    
    print("=" * 60)
    print("\nFolder structure created successfully!")
    print("\nNext steps:")
    print("1. Place your data files in the correct folders:")
    print("   - MSA_STORENAME/Generated_Colors_2026-03-14.csv")
    print("   - MSA_STORENAME/STORE NAME.xlsx")
    print("   - BASE DATA/BASE-DATA-*.csv (4 files)")
    print("   - LIST/[category]-ALL.csv (4 files)")
    print("\n2. Run: python app.py")
    print("\nFor detailed instructions, see QUICK_START.md")

if __name__ == '__main__':
    create_folder_structure()
