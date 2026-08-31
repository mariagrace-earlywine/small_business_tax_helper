import os
import pandas as pd

CSV_PATH = "2025_expenses.csv"  # change to "data/2025_expenses.csv" if needed

print("CWD:", os.getcwd())
print("CSV exists?", os.path.exists(CSV_PATH))

df = pd.read_csv(CSV_PATH)
print("\nRAW columns:", list(df.columns))
print("Row count:", len(df))

print("\nFirst 5 rows:")
print(df.head(5))

# Show amount examples
if "amount" in [c.lower().strip() for c in df.columns]:
    # find the actual column name case
    amt_col = [c for c in df.columns if c.lower().strip() == "amount"][0]
    print("\nAmount sample types:", df[amt_col].head(10).map(type).tolist())
    print("Amount sample values:", df[amt_col].head(10).tolist())

# Show date examples
if "date" in [c.lower().strip() for c in df.columns]:
    date_col = [c for c in df.columns if c.lower().strip() == "date"][0]
    print("\nDate sample values:", df[date_col].head(10).tolist())
