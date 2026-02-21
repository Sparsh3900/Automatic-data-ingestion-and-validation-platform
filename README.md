# Automatic-data-ingestion-and-validation-platform
Project Overview
This project simulates a real-world regulatory data ingestion and validation pipeline used by financial institutions to process inbound transaction files.
The system automatically validates incoming CSV files, assigns risk scores, routes files based on data quality, and enables human-in-the-loop review through a dashboard interface.

Problem Statement
Financial institutions receive transaction files from multiple external sources. Poor data quality can lead to:
Regulatory reporting errors
Compliance breaches
Financial penalties
Operational delays

This project demonstrates how automated validation and risk-based routing can improve governance and reliability.

System Architecture
Incoming CSV Files → Validation Engine → Risk Classification →
Auto Processing / Human Review / Rejection → Audit Logging → Dashboard Monitoring

Key Features
schema Validation
Ensures required columns exist before processing.
Data Quality Checks
Missing values detection
Negative/invalid transaction amounts
Row-level error tracking
Risk-Based Routing
LOW → Auto processed
MEDIUM → Human review required
HIGH → Rejected
Audit Logging

Stores:
File name
Total rows
Failed rows
Quality score
Risk level
Processing status
Timestamp
Human-in-the-Loop Dashboard

Built using Streamlit:
View review files
Approve / Reject files
Monitor audit logs

Tech Stack
Python
Pandas
SQLite
Streamlit
Modular ETL Architecture
