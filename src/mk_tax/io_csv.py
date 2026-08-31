# INGEST - Reads CSV and gives structured data (DataFrame or list of Expense objects).

from __future__ import annotations
from pathlib import Path
import pandas as pd

REQUIRED = {"date", "vendor", "amount", "category"}

def project_root() -> Path:
    # io_csv.py is at mk_tax_helper/src/mk_tax/io_csv.py
    return Path(__file__).resolve().parents[2]  # mk_tax_helper/

def load_expenses_csv(csv_path: str = "2025_expenses.csv") -> pd.DataFrame:
    path = Path(csv_path)

    # If user passed a real path (relative or absolute), use it.
    # Otherwise, assume it's a filename inside the project's data/folder.
    if path.is_absolute() or path.exists():
        resolved = path
    else:
        resolved = project_root() / "data" / csv_path

    df = pd.read_csv(resolved)

    # Normalize headers
    df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]

    missing = REQUIRED - set(df.columns)
    if missing:
        raise ValueError(f"CSV missing required columns: {missing}. Found: {list(df.columns)}")

    # Parse date to YYYY-MM-DD
    df["date"] = pd.to_datetime(df["date"], errors="raise").dt.strftime("%Y-%m-%d")

    # Clean/parse amount
    df["amount"] = (
        df["amount"]
        .astype(str)
        .str.replace("$", "", regex=False)
        .str.replace(",", "", regex=False)
        .str.strip()
    )
    df["amount"] = pd.to_numeric(df["amount"], errors="raise")

    # You said ALL are expenses → enforce negative
    df["amount"] = -df["amount"].abs()

    # Optional columns: ensure present
    for col in ["description", "business", "payment_method"]:
        if col not in df.columns:
            df[col] = ""

    # Trim text fields
    for col in ["vendor", "category", "description", "business", "payment_method"]:
        df[col] = df[col].astype(str).str.strip()

    return df

