#!/usr/bin/env python3
"""
Helper script to prepare CSV data for GitHub secrets.
This script reads your CSV file and outputs the content in a format
suitable for copying into the CSV_DATA GitHub secret.
"""

import csv
import sys

def prepare_csv_for_secrets(csv_file_path):
    """Read CSV file and output content for GitHub secrets."""
    try:
        with open(csv_file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            
        print("=" * 80)
        print("CSV CONTENT FOR GITHUB SECRET 'CSV_DATA'")
        print("=" * 80)
        print("Copy the content below and paste it into your GitHub secret 'CSV_DATA':")
        print("=" * 80)
        print(content)
        print("=" * 80)
        print(f"\nTotal characters: {len(content)}")
        print("Note: GitHub secrets have a size limit. If this is too large,")
        print("consider splitting your CSV into smaller chunks.")
        
    except FileNotFoundError:
        print(f"Error: File '{csv_file_path}' not found!")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading file: {e}")
        sys.exit(1)

if __name__ == "__main__":
    csv_file = "smykm_emails.csv"
    
    if len(sys.argv) > 1:
        csv_file = sys.argv[1]
    
    print(f"Reading CSV file: {csv_file}")
    prepare_csv_for_secrets(csv_file) 