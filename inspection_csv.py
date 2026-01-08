import pandas as pd

# Load the CSV file with correct encoding
df = pd.read_csv("airline_2m.csv", encoding="ISO-8859-1")

# Print basic info
print("\n--- COLUMNS ---")
print(df.columns)

print("\n--- DATA TYPES ---")
print(df.dtypes)

print("\n--- SAMPLE ROWS ---")
print(df.head())

print("\n--- SUMMARY STATISTICS ---")
print(df.describe(include='all'))
