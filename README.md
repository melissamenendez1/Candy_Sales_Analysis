# Candy Sales Variance & Seasonality Analysis

An end-to-end analysis investigating a **-$14.86K variance** in the Sugar division of a candy sales dataset — combining Python data pipelines, Power BI dashboards, and a Quarto/RStudio seasonal deep-dive to move from "here's a variance" to a data-backed, testable marketing recommendation.

## Project Overview

This project explores why the Sugar division underperformed against budget, and proposes a data-driven solution, by:

1. Breaking down revenue by product within each division.
2. Drilling into geographic sales patterns (state/city).
3. Visualizing how sales trended over time across all four years, which revealed both an overall upward trend and a recurring seasonal pattern.
4. Using that pattern to inform a scoped, measurable holiday marketing pilot.

## Data

- **Source:** Maven Analytics' US Candy Distributor Sales and geospatial data (2021–2024), covering three divisions: Chocolate, Other, and Sugar.
- **Cleaning performed** (see `Candy_Seasonal_Report.qmd`):
  - Corrected a fixed 2,000-day offset error in the `Ship Date` column.
  - Reassigned "Fizzy Lifting Drinks" (Product ID `OTH-FIZ-56000`) from Sugar to Other division, based on its ID naming convention.
- Cleaned dataset: `Candy_Sales_clean.csv`

## Repo Contents

| File | Description |
|---|---|
| `Candy_Sales.csv` | Raw transaction-level sales data. |
| `Candy_Sales_clean.csv` | Cleaned transaction-level sales data used across all analyses. |
| `Candy_Products.csv` | Product reference data (e.g., product names, IDs, division mapping). |
| `Candy_Targets.csv` | Target figures used for variance analysis. |
| `Candy_Variance_Summary.csv` | Summary of actuals vs. target variance by division. |
| `Product_Sales.csv` | Product-level sales aggregated by city and state, used for Power BI import. |
| `candy_variance_pipeline.py` | Python pipeline for cleaning raw sales data and calculating variance. |
| `product_sales.py` | Python pipeline generating product-level sales by city and state. |
| `Candy_Variance_Analysis.pbix` | Power BI dashboard: variance analysis, product sales by division, sales by city/state, and sales by city/product. |
| `Candy_Seasonal_Report.qmd` | Quarto report (Python, developed in RStudio) analyzing sales trends and seasonality across all three divisions, with a pilot recommendation. |


## Key Findings

- **Product concentration:** Chocolate revenue was evenly distributed across products; the Other division was highly concentrated (Lickable Wallpaper = 84.13% of revenue); Sugar was skewed as well, with Nerds generating just 4.18% of division revenue vs. a 19.16% average for other Sugar products.
- **Geographic pattern:** Nerds sales were concentrated in only two markets — New York City and Philadelphia.
- **Seasonality:** Chocolate and Other both show a clear, statistically visible sales lift in the September–December window. Sugar showed little visible seasonal lift, but with only 34 total transactions (~0.3% of total revenue) and just 4 Nerds transactions across four years, the sample is too small to distinguish "no seasonal demand" from "under-marketed relative to existing seasonal demand."

## Recommendation

Rather than committing to a full-scale marketing expansion on limited historical data, the report proposes a **testable pilot**:

- Run two promotion tracks during the same holiday window (September–December): one promoting the full Sugar line in its top-performing markets, and one promoting Nerds specifically in its existing customer base (NYC and Philadelphia).
- Measure success against a data-driven threshold (sales sustained above baseline plus typical variability), rather than a percentage target, which is unstable on such a small base.
- Treat inconclusive results as inconclusive, not failure, since the historical sample is too small to rule out the hypothesis from a single ambiguous result.

## Tools Used

- **Python** (pandas) — data pipeline for cleaning and aggregating sales by city/state
- **Python via Quarto** (pandas, numpy, matplotlib; developed in RStudio) — seasonal trend analysis and reporting
- **Power BI** — interactive dashboards for variance and geographic sales analysis

## How to Reproduce

```bash
# Clone the repo
git clone <github.com/melissamenendez1>
cd <Candy_Variance_Analysis>

# Install dependencies for the data pipeline
pip install pandas

# Install additional dependencies to render the Quarto report
pip install numpy matplotlib

# Render the Quarto report
quarto render Candy_Seasonal_Report.qmd
```

Open `Candy_Variance_Analysis.pbix` in Power BI Desktop to explore the interactive dashboards.
