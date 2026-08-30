# Import pandas
import pandas as pd

# Set variable constants
PRODUCT_COL = "Product Name"
CUSTOMER_ID_COL = "Customer ID"
STATE_COL = "State/Province"
CITY_COL = "City"
SALES_COL = "Sales"
ORDER_DATE_COL = "Order Date"
SHIP_DATE_COL = "Ship Date"
PRODUCT_ID_COL = "Product ID"

# Load the file
sales_df = pd.read_csv("Candy_Sales.csv")

# Convert both date columns into standard Python datetime format
sales_df[ORDER_DATE_COL] = pd.to_datetime(sales_df[ORDER_DATE_COL])
sales_df[SHIP_DATE_COL] = pd.to_datetime(sales_df[SHIP_DATE_COL])

# Filter the table to only keep rows where the order year matches 2024
sales_df = sales_df[sales_df[ORDER_DATE_COL].dt.year == 2024]

# Clean up accidental, hidden spaces
sales_df.columns = sales_df.columns.str.replace("\u00a0", " ", regex=False).str.strip()

columns_to_clean = [
    PRODUCT_COL,
    CUSTOMER_ID_COL,
    STATE_COL,
    CITY_COL,
    SALES_COL,
    ORDER_DATE_COL,
    SHIP_DATE_COL,
]

for col in columns_to_clean:
    if col in sales_df.columns and (
        sales_df[col].dtype == "object" or pd.api.types.is_string_dtype(sales_df[col])
    ):
        sales_df[col] = sales_df[col].apply(
            lambda value: (
                " ".join(str(value).replace("\u00a0", " ").replace("\t", " ").split())
                if pd.notna(value)
                else value
            )
        )

# Verify every single product code found in the sales files
missing_product_ids = sales_df[PRODUCT_ID_COL].isna().sum()
blank_product_ids = sales_df[PRODUCT_ID_COL].astype(str).str.strip().eq("").sum()
unique_product_ids = sales_df[PRODUCT_ID_COL].nunique()

print(f"Missing Product IDs: {missing_product_ids}")
print(f"Blank Product IDs: {blank_product_ids}")
print(f"Unique Product IDs: {unique_product_ids}")

# Check for blank or null values
print("\nBlank fields in Sales fields:\n")
print(sales_df.isna().sum())

# Sum the total sales revenue for each product
sales_by_product = sales_df.groupby("Product Name", as_index=False)["Sales"].sum()
print(sales_by_product)

# Aggregate transactional data into a single, flat fact table
product_sales_df = sales_df.groupby(
    ["Division", PRODUCT_COL, STATE_COL, CITY_COL], as_index=False
)[SALES_COL].sum()

# Export the table to a new CSV file
OUTPUT_FILE = "Product_Sales.csv"
product_sales_df.to_csv(OUTPUT_FILE, index=False)
print(f"\nExport complete: {OUTPUT_FILE}")
