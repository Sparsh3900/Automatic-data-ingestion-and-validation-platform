import os
import shutil
import pandas as pd
from database import get_audit_logs, update_review_status

REVIEW_FOLDER = "review"
PROCESSING_FOLDER = "processing"
REJECTED_FOLDER = "rejected"

def show_review_files():
    files = os.listdir(REVIEW_FOLDER)
    
    if not files:
        print("No files pending review.")
        return None
    
    print("\nFiles Pending Review:")
    for idx, file in enumerate(files):
        print(f"{idx + 1}. {file}")
    
    choice = int(input("\nSelect file number to review: "))
    
    if choice < 1 or choice > len(files):
        print("Invalid choice")
        return None
    
    return files[choice - 1]

def review_file(file):
    file_path = os.path.join(REVIEW_FOLDER, file)
    
    print(f"\nOpening {file}...\n")
    
    df = pd.read_csv(file_path)
    print(df.head())
    
    decision = input("\nApprove or Reject? (A/R): ").upper()
    
    if decision == "A":
        destination = PROCESSING_FOLDER
        status = "APPROVED_BY_REVIEWER"
    elif decision == "R":
        destination = REJECTED_FOLDER
        status = "REJECTED_BY_REVIEWER"
    else:
        print("Invalid decision")
        return
    
    shutil.move(file_path, os.path.join(destination, file))
    
    update_review_status(file, status)
    
    print(f"\nFile moved to {destination} and audit log updated.")

def run_dashboard():
    file = show_review_files()
    
    if file:
        review_file(file)

if __name__ == "__main__":
    run_dashboard()