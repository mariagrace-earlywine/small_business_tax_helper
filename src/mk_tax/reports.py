from pathlib import Path
import pandas as pd
from .io_csv import load_expenses_csv

def export_mk_category_summary(mk: pd.DataFrame, base_dir: Path) -> None:
    out_dir = base_dir / "out"
    out_dir.mkdir(exist_ok=True)

    summary = (
        mk.groupby("category")["amount_abs"]
        .sum()
        .sort_values(ascending=False)
        .reset_index()
        .rename(columns={"amounts_abs": "total"})
    )

    output_file = out_dir / "2025_mary_kay_by_category.csv"
    summary.to_csv(output_file, index=False)
    print(f"Saved: {output_file}")

def export_mk_month_summary(mk: pd.DataFrame, base_dir: Path) -> None:
    out_dir = base_dir/"out"
    out_dir.mkdir(exist_ok=True)

    summary = (
        mk.groupby("month")["amount_abs"]
        .sum()
        .sort_index()
        .reset_index()
        .rename(columns={"amount_abs": "total"})
    )

    output_file = out_dir / "2025_mary_kay_by_month.csv"
    summary.to_csv(output_file, index=False)
    print(f"Saved: {output_file}")


def export_mk_year_summary(mk: pd.DataFrame, base_dir: Path) -> None:
    out_dir = base_dir/"out"
    out_dir.mkdir(exist_ok=True)

    total = mk["amount_abs"].sum()

    # Top 10 categories
    top_categories = (
        mk.groupby("category")["amount_abs"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
    )

    # Monthly totals
    by_month = (
        mk.groupby("month")["amount_abs"]
        .sum()
        .sort_index()
    )

    # Builds a simple "report-like" table
    rows = []
    rows.append(("TOTAL MARY KAY EXPENSES (2025)", float(total)))

    rows.append(("", "")) # spacer
    rows.append(("TOP CATEGORIES", ""))
    for cat, amt in top_categories.items():
        rows.append((cat, float(amt)))

    rows.append(("", "")) # spacer
    rows.append(("MONTHLY TOTALS", ""))
    for m, amt in by_month.items():
        rows.append((m, float(amt)))

    summary_df = pd.DataFrame(rows, columns=["item", "amount"])
    output_file = out_dir / "2025_mary_kay_year_summary.csv"
    summary_df.to_csv(output_file, index=False)
    print(f"Saved: {output_file}")


def export_cleaned_expenses(df: pd.DataFrame, base_dir: Path) -> None:
    out_dir = base_dir/"out"
    out_dir.mkdir(exist_ok=True)

    output_file = out_dir / "expenses_cleaned.csv"
    df.to_csv(output_file, index=False)
    print(f"Saved: {output_file}")


def export_needs_review(df: pd.DataFrame, base_dir: Path) -> None:
    out_dir = base_dir / "out"
    out_dir.mkdir(exist_ok=True)

    review = df.copy()
    review["review_reason"] = ""

    blank_vendor = review["vendor"].astype(str).str.strip().eq("")
    blank_category = review["category"].astype(str).str.strip().eq("")
    amount_num = pd.to_numeric(review["amount"], errors="coerce")
    positive_amount = amount_num > 0

    review.loc[blank_vendor, "review_reason"] += "blank_vendor" # for every row where blank_vendor is True, append the text "blank_vendor" to the row's review_reason cell.
    review.loc[blank_category, "review_reason"] += "blank_category"
    review.loc[positive_amount, "review_reason"] += "positive_amount"

    review = review[review["review_reason"].ne("")]  # filters rows and keeps rows where review_reason is not empty.

    output_file = out_dir / "needs_review.csv"
    review.to_csv(output_file, index=False)
    print(f"Saved: {output_file} ({len(review)} rows)")



def run_reports(df, month: str | None = None) -> None:
    if month:
        df = df[df["date"].astype(str).str.startswith(month)]

    df = df.copy()
    df["month"] = pd.to_datetime(df["date"]).dt.to_period("M").astype(str)

    mk = df[df["business"].str.lower().eq("mary kay")].copy()
    mk["amount_abs"] = mk["amount"].abs()

    print("\n=== MARY KAY: Total by Category (Positive) ===")
    print(mk.groupby("category")["amount_abs"].sum().sort_values(ascending=False))

    print("\n=== MARY KAY: Total by Month (Positive) ===")
    print(mk.groupby("month")["amount_abs"].sum().sort_index())

    print("\n=== ALL BUSINESSES: Total by Business (Positive) ===")
    df2 = df.copy()
    df2["amount_abs"] = df2["amount"].abs()
    print(df2.groupby("business")["amount_abs"].sum().sort_values(ascending=False))

    base_dir = Path(__file__).resolve().parents[2]
    export_cleaned_expenses(df, base_dir)
    export_needs_review(df, base_dir)
    export_mk_category_summary(mk, base_dir)
    export_mk_month_summary(mk, base_dir)
    export_mk_year_summary(mk, base_dir)



if __name__ == "__main__":
    run_reports()
