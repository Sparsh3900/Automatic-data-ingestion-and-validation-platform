import sqlite3

DB_NAME = "data_quality.db"

# --------------------------------------------------
# Initialize Database
# --------------------------------------------------
def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Audit Log Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS audit_log (
            run_id INTEGER PRIMARY KEY AUTOINCREMENT,
            file_name TEXT,
            total_rows INTEGER,
            failed_rows INTEGER,
            quality_score REAL,
            risk_level TEXT,
            status TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()


# --------------------------------------------------
# Insert Audit Log Entry
# --------------------------------------------------
def insert_audit_log(file_name, total, failed, score, risk, status):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO audit_log 
        (file_name, total_rows, failed_rows, quality_score, risk_level, status)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (file_name, total, failed, score, risk, status))

    conn.commit()
    conn.close()