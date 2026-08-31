from __future__ import annotations
from dataclasses import dataclass
import pandas as pd


@dataclass
class ValidationResult:
    ok: bool
    row_count: int
    errors: list[str]
    warnings: list[str]


def validate_expenses_df(df: pd.DataFrame) -> ValidationResult:
    """
    Validate a normalized expenses DataFrame.
    Inputs: df with columns like date/vendor/amount/category (already normalized by io_csv)
    Outputs: ValidationResult with errors (must-fix) and warnings (review).
    """
    errors: list[str] = []
    warnings: list[str] = []

    required = {"date", "vendor", "amount", "category"}
    missing = required - set(df.columns)
    if missing:
        errors.append(f"Missing required columns: {sorted(missing)}")
        return ValidationResult(False, len(df), errors, warnings)

    # Date format check (expects YYYY-MM-DD after io_csv standardization)
    bad_date_mask = ~df["date"].astype(str).str.match(r"^\d{4}-\d{2}-\d{2}$")
    if bad_date_mask.any():
        errors.append(f"{int(bad_date_mask.sum())} row(s) have invalid date format (expected YYYY-MM-DD).")

    # Amount numeric check
    amt = pd.to_numeric(df["amount"], errors="coerce")
    if amt.isna().any():
        errors.append(f"{int(amt.isna().sum())} row(s) have non-numeric amount.")

    # Vendor not blank
    blank_vendor = df["vendor"].astype(str).str.strip().eq("")
    if blank_vendor.any():
        errors.append(f"{int(blank_vendor.sum())} row(s) have blank vendor.")

    # Category blank = warning (you may allow "Needs Review" later)
    blank_cat = df["category"].astype(str).str.strip().eq("")
    if blank_cat.any():
        warnings.append(f"{int(blank_cat.sum())} row(s) have blank category (consider Needs Review).")

    # Positive amount warning (only if you later allow refunds, but helpful anyway)
    if (amt > 0).any():
        warnings.append(f"{int((amt > 0).sum())} row(s) have positive amounts (refunds?).")

    ok = len(errors) == 0
    return ValidationResult(ok, len(df), errors, warnings)





