
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

folder_path = r"E:\ADIDAS"
file_path = os.path.join(folder_path, "Adidas US Sales.csv")
output_path = os.path.join(folder_path, "outputs")

os.makedirs(output_path, exist_ok=True)
os.makedirs(os.path.join(output_path, "charts"), exist_ok=True)

df = pd.read_csv(file_path)

df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")

print("FIRST FIVE ROWS")
print(df.head())

print("\nDATASET SHAPE")
print(df.shape)

print("\nCOLUMN NAMES")
print(df.columns.tolist())

print("\nDATASET INFORMATION")
df.info()

print("\nMISSING VALUES")
print(df.isnull().sum())

print("\nDUPLICATE ROWS")
print(df.duplicated().sum())

df = df.drop_duplicates()

if "invoice_date" in df.columns:
    df["invoice_date"] = pd.to_datetime(df["invoice_date"], errors="coerce")
    df["year"] = df["invoice_date"].dt.year
    df["month"] = df["invoice_date"].dt.month
    df["month_name"] = df["invoice_date"].dt.strftime("%b")
    df["year_month"] = df["invoice_date"].dt.to_period("M").astype(str)

numeric_columns = [
    "price_per_unit",
    "units_sold",
    "total_sales",
    "operating_profit",
    "operating_margin"
]

for column in numeric_columns:
    if column in df.columns:
        df[column] = pd.to_numeric(df[column], errors="coerce")

df.to_csv(os.path.join(output_path, "cleaned_adidas_sales.csv"), index=False)

print("\nNUMERICAL SUMMARY")
print(df.describe())

total_sales = df["total_sales"].sum()
total_profit = df["operating_profit"].sum()
total_units = df["units_sold"].sum()
profit_margin = (total_profit / total_sales * 100) if total_sales else 0

print("\nKEY BUSINESS METRICS")
print(f"Total Sales: ${total_sales:,.2f}")
print(f"Total Operating Profit: ${total_profit:,.2f}")
print(f"Total Units Sold: {total_units:,.0f}")
print(f"Overall Operating Profit Margin: {profit_margin:.2f}%")

kpis = pd.DataFrame({
    "Metric": [
        "Total Sales",
        "Total Operating Profit",
        "Total Units Sold",
        "Overall Operating Profit Margin (%)"
    ],
    "Value": [
        total_sales,
        total_profit,
        total_units,
        profit_margin
    ]
})

kpis.to_csv(os.path.join(output_path, "key_metrics.csv"), index=False)

def save_group_summary(column, filename):
    if column in df.columns:
        summary = (
            df.groupby(column, dropna=False)
            .agg(
                total_sales=("total_sales", "sum"),
                total_profit=("operating_profit", "sum"),
                units_sold=("units_sold", "sum")
            )
            .sort_values("total_sales", ascending=False)
        )
        summary.to_csv(os.path.join(output_path, filename))
        print(f"\nSALES BY {column.upper()}")
        print(summary)
        return summary
    return None

product_summary = save_group_summary("product", "sales_by_product.csv")
retailer_summary = save_group_summary("retailer", "sales_by_retailer.csv")
region_summary = save_group_summary("region", "sales_by_region.csv")
state_summary = save_group_summary("state", "sales_by_state.csv")
city_summary = save_group_summary("city", "sales_by_city.csv")
method_summary = save_group_summary("sales_method", "sales_by_method.csv")

sns.set_theme(style="whitegrid")

if product_summary is not None:
    plt.figure(figsize=(12, 6))
    product_summary["total_sales"].sort_values().plot(kind="barh")
    plt.title("Total Sales by Product")
    plt.xlabel("Total Sales ($)")
    plt.ylabel("Product")
    plt.tight_layout()
    plt.savefig(os.path.join(output_path, "charts", "sales_by_product.png"))
    plt.show()
    plt.close()

if region_summary is not None:
    plt.figure(figsize=(10, 6))
    region_summary["total_sales"].sort_values().plot(kind="bar", color="steelblue")
    plt.title("Total Sales by Region")
    plt.xlabel("Region")
    plt.ylabel("Total Sales ($)")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(os.path.join(output_path, "charts", "sales_by_region.png"))
    plt.show()
    plt.close()

if retailer_summary is not None:
    plt.figure(figsize=(12, 6))
    retailer_summary["total_sales"].sort_values().plot(kind="bar", color="orange")
    plt.title("Total Sales by Retailer")
    plt.xlabel("Retailer")
    plt.ylabel("Total Sales ($)")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig(os.path.join(output_path, "charts", "sales_by_retailer.png"))
    plt.show()
    plt.close()

if method_summary is not None:
    plt.figure(figsize=(8, 5))
    method_summary["total_sales"].sort_values().plot(kind="bar", color="seagreen")
    plt.title("Total Sales by Sales Method")
    plt.xlabel("Sales Method")
    plt.ylabel("Total Sales ($)")
    plt.xticks(rotation=0)
    plt.tight_layout()
    plt.savefig(os.path.join(output_path, "charts", "sales_by_method.png"))
    plt.show()
    plt.close()

if "year" in df.columns:
    yearly_sales = df.groupby("year")["total_sales"].sum()
    yearly_sales.to_csv(os.path.join(output_path, "yearly_sales.csv"))

    plt.figure(figsize=(8, 5))
    yearly_sales.plot(kind="bar", color="purple")
    plt.title("Yearly Sales Trend")
    plt.xlabel("Year")
    plt.ylabel("Total Sales ($)")
    plt.xticks(rotation=0)
    plt.tight_layout()
    plt.savefig(os.path.join(output_path, "charts", "yearly_sales.png"))
    plt.show()
    plt.close()

if "year_month" in df.columns:
    monthly_sales = (
        df.groupby("year_month")["total_sales"]
        .sum()
        .sort_index()
    )
    monthly_sales.to_csv(os.path.join(output_path, "monthly_sales.csv"))

    plt.figure(figsize=(14, 6))
    monthly_sales.plot(kind="line", marker="o")
    plt.title("Monthly Sales Trend")
    plt.xlabel("Year-Month")
    plt.ylabel("Total Sales ($)")
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.savefig(os.path.join(output_path, "charts", "monthly_sales.png"))
    plt.show()
    plt.close()

correlation_columns = [
    column for column in [
        "price_per_unit",
        "units_sold",
        "total_sales",
        "operating_profit",
        "operating_margin"
    ]
    if column in df.columns
]

if len(correlation_columns) > 1:
    plt.figure(figsize=(9, 6))
    sns.heatmap(
        df[correlation_columns].corr(),
        annot=True,
        cmap="coolwarm",
        fmt=".2f"
    )
    plt.title("Correlation Between Numerical Variables")
    plt.tight_layout()
    plt.savefig(os.path.join(output_path, "charts", "correlation_heatmap.png"))
    plt.show()
    plt.close()

print("\nEDA COMPLETED SUCCESSFULLY")
print(f"Results and charts saved in: {output_path}")
