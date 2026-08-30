import pandas as pd

# Set variable constants
ORDER_DATE_COL = "Order Date"
SHIP_DATE_COL = "Ship Date"
PRODUCT_ID_COL = "Product ID"
DIVISION_COL = "Division"
REGION_COL = "Region"
SALES_COL = "Sales"
ACTUAL_SALES_COL = "Actual_Sales"
TARGET_COL = "Target"

# Load the files
sales_df = pd.read_csv("Candy_Sales.csv")
products_df = pd.read_csv("Candy_Products.csv")
targets_df = pd.read_csv("Candy_Targets.csv")

# Print the actual column names
print("Sales Columns:", sales_df.columns.tolist())
print("Products Columns:", products_df.columns.tolist())
print("Targets Columns:", targets_df.columns.tolist())

# Convert both date columns into standard Python datetime format
sales_df[ORDER_DATE_COL] = pd.to_datetime(sales_df[ORDER_DATE_COL])
sales_df[SHIP_DATE_COL] = pd.to_datetime(sales_df[SHIP_DATE_COL])

# Filter the table to only keep rows where the order year matches 2024
sales_df = sales_df[sales_df[ORDER_DATE_COL].dt.year == 2024]

# Clean up hidden spaces
sales_df[PRODUCT_ID_COL] = sales_df[PRODUCT_ID_COL].astype(str).str.strip()
sales_df[DIVISION_COL] = sales_df[DIVISION_COL].astype(str).str.strip()
sales_df[REGION_COL] = sales_df[REGION_COL].astype(str).str.strip()
products_df[PRODUCT_ID_COL] = products_df[PRODUCT_ID_COL].astype(str).str.strip()
products_df[DIVISION_COL] = products_df[DIVISION_COL].astype(str).str.strip()
targets_df[DIVISION_COL] = targets_df[DIVISION_COL].astype(str).str.strip()

# Correct Fizzy Lifting Drinks division (mislabeled as "Sugar"; product ID
# prefix "OTH-" and Candy_Products.csv both indicate it belongs to "Other")
sales_df.loc[sales_df[PRODUCT_ID_COL] == "OTH-FIZ-56000", DIVISION_COL] = "Other"

# Verify every single product code found in the sales files
unmatched_products = sales_df[
    ~sales_df[PRODUCT_ID_COL].isin(products_df[PRODUCT_ID_COL])
][PRODUCT_ID_COL].nunique()

# Check for blank or null values
print("\nBlank fields in Sales fields:\n")
print(sales_df.isna().sum())

# Sum the actual total sales revenue for each division
actuals_by_division = sales_df.groupby(DIVISION_COL, as_index=False)[SALES_COL].sum()
actuals_by_division.rename(columns={SALES_COL: ACTUAL_SALES_COL}, inplace=True)

# Combine the targets and actuals into a single summary table
variance_summary = pd.merge(
    targets_df, actuals_by_division, on=DIVISION_COL, how="left", validate="one_to_one"
)

print(variance_summary)

# Calculate the dollar variance and percentage variance
TARGET_COL = "Target"

variance_summary["Dollar_Variance"] = (
    variance_summary[ACTUAL_SALES_COL].fillna(0) - variance_summary[TARGET_COL]
)

variance_summary["Percentage_Variance"] = (
    variance_summary["Dollar_Variance"] / variance_summary[TARGET_COL].replace(0, pd.NA)
) * 100

print("\nVariance Summary:\n")
print(variance_summary)

# Export the table to a new CSV file
OUTPUT_FILE = "Candy_Variance_Summary.csv"
variance_summary.to_csv(OUTPUT_FILE, index=False)
print(f"\nExport complete: {OUTPUT_FILE}")
