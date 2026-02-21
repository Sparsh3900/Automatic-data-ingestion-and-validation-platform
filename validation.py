def validate_data(df):
    errors = []
    required_columns = ["transaction_id", "customer_id", "amount", "date"]

    # -------------------------------------------------
    # Schema Validation (CRITICAL)
    # --------------------------------------------------
    for col in required_columns:
        if col not in df.columns:
            errors.append(f"Missing column: {col}")

    if errors:
        return errors, 0, 0, 0, "HIGH"

    total = len(df)
    failed = 0

    # --------------------------------------------------
    # Missing Required Field Values → MEDIUM RISK
    # --------------------------------------------------
    missing_cells = df[required_columns].isnull().sum().sum()

    if missing_cells > 0:
        errors.append("Missing values found in required fields")
        failed = missing_cells

        # We STOP scoring here
        return errors, total, failed, None, "MEDIUM"

    # --------------------------------------------------
    # Invalid Amount → HIGH RISK
    # --------------------------------------------------
    invalid_amount = (df["amount"] <= 0).sum()

    if invalid_amount > 0:
        errors.append("Invalid transaction amount")
        failed = invalid_amount
        return errors, total, failed, None, "HIGH"

    # --------------------------------------------------
    # If All Good → LOW RISK
    # --------------------------------------------------
    score = 100
    return [], total, 0, score, "LOW"