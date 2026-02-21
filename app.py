import streamlit as st
import sqlite3
import pandas as pd

st.title("Inbound Data Monitoring Dashboard")

conn = sqlite3.connect("data_quality.db")
df = pd.read_sql_query("SELECT * FROM audit_log", conn)
conn.close()

st.subheader("Ingestion Runs")
st.dataframe(df)

pending = df[df["status"] == "Review Pending"]

if not pending.empty:
    st.subheader("Files Pending Human Review")

    selected = st.selectbox("Select File", pending["file_name"])

    if st.button("Approve"):
        conn = sqlite3.connect("data_quality.db")
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE audit_log SET status='Approved' WHERE file_name=?
        """, (selected,))
        conn.commit()
        conn.close()
        st.success("File Approved")

    if st.button("Reject"):
        conn = sqlite3.connect("data_quality.db")
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE audit_log SET status='Rejected' WHERE file_name=?
        """, (selected,))
        conn.commit()
        conn.close()
        st.error("File Rejected")