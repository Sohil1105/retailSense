import os
import sys
import sqlite3
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import requests
import json
from utils import calculate_revenue, classify_customer, write_summary_report

# Part 2: Data Cleaning
customers = pd.read_csv("data/customers.csv")
orders = pd.read_csv("data/orders.csv")
products = pd.read_csv("data/products.csv")

def null_report(df, name):
    print(f"\n=== Null Report: {name} ===")
    total = len(df)
    nulls = df.isnull().sum()
    for col, count in nulls.items():
        if count > 0:
            pct = count / total * 100
            print(f"{col:<12} → {count} nulls ({pct:.1f}%)")

null_report(customers, "customers")

customers["age"].fillna(customers["age"].median(), inplace=True)
customers["gender"].fillna("Unknown", inplace=True)
customers.drop_duplicates(subset=["email"], keep="first", inplace=True)
customers["gender"] = customers["gender"].astype("category")
customers["age_group"] = customers["age"].apply(classify_customer)
customers.to_csv("outputs/cleaned_customers.csv", index=False)

products["price"] = products["price"].astype(str).str.replace("₹", "").str.strip().astype(float)
products["rating"].fillna(round(products["rating"].mean(), 1), inplace=True)
products["category"] = products["category"].astype("category")

null_report(customers, "customers_cleaned")

# Part 3: NumPy
price_array = products["price"].values
final_price = price_array * 1.18 * 0.90
first_20 = final_price[:20]

# Part 4: SQL Analysis
conn = sqlite3.connect("outputs/retailsense.db")
customers.to_sql("customers", conn, if_exists="replace", index=False)
products.to_sql("products", conn, if_exists="replace", index=False)
orders.to_sql("orders", conn, if_exists="replace", index=False)
conn.close()

# Part 5: Merging
orders_cust = pd.merge(orders, customers, on="customer_id", how="inner")
full_df = pd.merge(orders_cust, products, on="product_id", how="inner")
full_df["revenue"] = full_df.apply(lambda row: calculate_revenue(row["price"], row["quantity"], row["discount_pct"]), axis=1)

# Part 6: Plots (save to verify functionality)
plt.figure()
full_df.groupby("category")["revenue"].sum().plot(kind="bar", color="skyblue")
plt.savefig("outputs/p1.png")
plt.close()

plt.figure()
sns.histplot(customers["age"], bins=15, kde=True, color="purple")
plt.savefig("outputs/p2.png")
plt.close()

plt.figure()
sns.boxplot(data=products, x="category", y="price", palette="Set2")
plt.savefig("outputs/p3.png")
plt.close()

plt.figure()
numeric_cols = full_df.select_dtypes(include=[np.number])
sns.heatmap(numeric_cols.corr(), annot=True, cmap="coolwarm", fmt=".2f")
plt.savefig("outputs/p4.png")
plt.close()

fig = px.scatter(products, x="price", y="rating", color="category")
fig.write_html("outputs/p5.html")

# Part 7: API
resp = requests.get("https://jsonplaceholder.typicode.com/users")
users = resp.json() if resp.status_code == 200 else []
with open("outputs/api_users.json", "w") as f:
    json.dump(users, f)

stats = {
    "Total Customers": len(customers),
    "Total Orders": len(orders),
    "Total Revenue": round(full_df["revenue"].sum(), 2)
}
write_summary_report(stats, "outputs/summary_report.txt")
print("Data generation run successfully.")
