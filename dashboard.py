import streamlit as st
import sqlite3
import pandas as pd
import os
import shutil

# Folder paths
PROCESSING_FOLDER = "processing"
REVIEW_FOLDER = "review"
REJECTED_FOLDER = "rejected"

# --------------------------------------------------
# Database Connection
# --------------------------------------------------
def get_connection():
    return sqlite3.connect("data_quality.db")

# --------------------------------------------------
# Fetch Audit Logs
# --------------------------------------------------
def fetch_audit_logs():
    conn = get_connection()
    df = pd.read_sql_query("SELECT * FROM audit_log ORDER BY timestamp DESC", conn)
    conn.close()
    return df

# --------------------------------------------------
# Update File Status
# --------------------------------------------------
def update_status(file_name, new_status):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE audit_log
        SET status = ?
        WHERE file_name = ?
    """, (new_status, file_name))

    conn.commit()
    conn.close()

# --------------------------------------------------
# Move File
# --------------------------------------------------
def move_file(file_name, destination_folder):
    source_path = os.path.join(REVIEW_FOLDER, file_name)
    destination_path = os.path.join(destination_folder, file_name)

    if os.path.exists(source_path):
        shutil.move(source_path, destination_path)

# --------------------------------------------------
# Streamlit UI
# --------------------------------------------------
st.set_page_config(page_title="Financial Data Quality Dashboard", layout="wide")

st.title("Financial Data Quality Monitoring System")

tabs = st.tabs(["📈 Audit Logs", "🕵️ Review Queue"])

# --------------------------------------------------
# Audit Logs Tab
# --------------------------------------------------
with tabs[0]:
    st.subheader("Audit Log Overview")
    logs = fetch_audit_logs()

    if logs.empty:
        st.info("No records found.")
    else:
        st.dataframe(logs, use_container_width=True)

# --------------------------------------------------
# Review Queue Tab
# --------------------------------------------------
with tabs[1]:
    st.subheader("Files Awaiting Human Review")

    review_files = os.listdir(REVIEW_FOLDER)

    if not review_files:
        st.success("No files pending review 🎉")
    else:
        for file in review_files:
            st.write(f"📄 **{file}**")

            col1, col2 = st.columns(2)

            with col1:
                if st.button(f"Approve {file}"):
                    move_file(file, PROCESSING_FOLDER)
                    update_status(file, "MANUALLY_APPROVED")
                    st.success(f"{file} moved to Processing")
                    st.rerun()

            with col2:
                if st.button(f"Reject {file}"):
                    move_file(file, REJECTED_FOLDER)
                    update_status(file, "MANUALLY_REJECTED")
                    st.error(f"{file} moved to Rejected")
                    st.rerun()