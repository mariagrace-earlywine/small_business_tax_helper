import argparse #argparse = standard library tool for reading command-line arguments like --csv and --out
from pathlib import Path
from .io_csv import load_expenses_csv
from .validate import validate_expenses_df
from .reports import run_reports

#path = moder, cross-platform way to work with file paths (create, read, write)

def run_pipeline(csv_path: str, month: str | None, out_path_str: str) -> int:
    """
    Pipeline runner (DE style):
    ingest -> validate -> (optional filter) -> report -> save output
    """
    print(">>> run_pipeline started")

    df = load_expenses_csv(csv_path)

    result = validate_expenses_df(df)
    if not result.ok:
        print("❌ Validation failed:")
        for e in result.errors:
            print("-", e)
        if result.warnings:
            print("\nWarnings:")
            for w in result.warnings:
                print("-", w)
        return 1  # non-zero exit code

    if result.warnings:
        print("⚠️ Warnings:")
        for w in result.warnings:
            print("-", w)

    print(f"✅ Valid file, {result.row_count} transactions")

    if month:
        df = df[df["date"].astype(str).str.startswith(month).copy()]

    run_reports(df, None)

    out_path = Path(out_path_str)
    if out_path_str == "report.txt":
        suffix = month or "ALL"
        out_path = Path(f"report_{suffix}.txt")

    out_path.write_text(
        f"Pipeline ran successfully.\n"
        f"CSV: {csv_path}\n"
        f"Month filter: {month or 'ALL'}\n"
        f"Transactions processed: {len(df)}\n",
        encoding="utf-8"
    )

    print(f"\nSaved report to {out_path.resolve()}")
    return 0


def main() -> int:

    parser = argparse.ArgumentParser(description="Mary Kay Tax Helper (starter)")
    parser.add_argument("--csv", required=True, help="Path to expenses CSV")
    parser.add_argument("--out", default="report.txt", help="Output report file")
    parser.add_argument("--month", help="Filter by month in YYYY-MM format (example: 2026-01)")
    args = parser.parse_args()

    return run_pipeline(args.csv, args.month, args.out)


if __name__ == "__main__":
    raise SystemExit(main())

