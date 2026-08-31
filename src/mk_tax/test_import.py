from .io_csv import load_expenses_csv

def main() -> None:
    df = load_expenses_csv("2025_expenses.csv")
    print(df.head(5))
    print("Rows:", len(df))
    print("Columns:", df.columns.tolist())

if __name__ == "__main__":
    main()






