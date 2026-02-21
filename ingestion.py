import os
import shutil
import pandas as pd
from validation import validate_data
from database import init_db, insert_audit_log

# --------------------------------------------------
# Folder structure
# --------------------------------------------------
INCOMING_FOLDER = "incoming"
PROCESSING_FOLDER = "processing"
REVIEW_FOLDER = "review"
REJECTED_FOLDER = "rejected"

# Ensure folders exist
for folder in [INCOMING_FOLDER, PROCESSING_FOLDER, REVIEW_FOLDER, REJECTED_FOLDER]:
    os.makedirs(folder, exist_ok=True)

# --------------------------------------------------
# Main Ingestion Logic
# --------------------------------------------------
def run_ingestion():
    files = os.listdir(INCOMING_FOLDER)
    init_db()

    if not files:
        print("No files found in incoming folder.")
        return

    for file in files:
        file_path = os.path.join(INCOMING_FOLDER, file)
        print(f"\nProcessing file: {file}")

        # Default values (safe initialization)
        total = 0
        failed = 0
        score = 0
        risk = "HIGH"
        status = "SYSTEM_ERROR"

        try:
            df = pd.read_csv(file_path)

            errors, total, failed, score, risk = validate_data(df)

            print(f"Validation Score: {score}% | Risk Level: {risk}")

            if errors:
                print("Errors Found:")
                for err in errors:
                    print("-", err)

            # -------------------------------
            # Routing Logic
            # -------------------------------
            if risk == "LOW":
                destination = PROCESSING_FOLDER
                status = "AUTO_PROCESSED"

            elif risk == "MEDIUM":
                destination = REVIEW_FOLDER
                status = "REVIEW_REQUIRED"

            else:
                destination = REJECTED_FOLDER
                status = "REJECTED"

            shutil.move(file_path, os.path.join(destination, file))
            print(f"File moved to {destination}")

        except Exception as e:
            print(f"System error while processing {file}: {e}")
            destination = REJECTED_FOLDER
            status = "SYSTEM_ERROR"
            shutil.move(file_path, os.path.join(destination, file))

        # Always log audit (even if error happens)
        insert_audit_log(file, total, failed, score, risk, status)

# --------------------------------------------------
# Run
# --------------------------------------------------
if __name__ == "__main__":
    run_ingestion()