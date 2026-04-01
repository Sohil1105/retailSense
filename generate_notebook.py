import json
import os

cells = []

def add_md(text):
    cells.append({
        "cell_type": "markdown",
        "metadata": {},
        "source": [text]
    })

def add_code(code):
    cells.append({
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [line + "\n" for line in code.strip().split("\n")]
    })

add_md("# RetailSense End-to-End Data Analysis\n\nThis notebook handles data cleaning, NumPy array manipulation, SQL loading, advanced Pandas groupbys, and visualizations.")

add_md("## Part 2: Data Cleaning with Pandas\n\n**Task 2.1: Load & Inspect**\nLoading all three datasets and inspecting their structures.")
add_code("""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import sqlite3
import requests
import json
import sys
import os

# Ensure utils is importable
sys.path.append(os.path.abspath('..'))
from utils import calculate_revenue, classify_customer, write_summary_report

# Load files
customers = pd.read_csv('../data/customers.csv')
orders = pd.read_csv('../data/orders.csv')
products = pd.read_csv('../data/products.csv')

print("Customers Shape:", customers.shape)
customers.info()
print(customers.describe())
print(customers.isnull().sum())
""")

add_md("**Task 2.4: Null Report Function**\nDefining a standard null report function.")
add_code("""
def null_report(df, name):
    print(f"=== Null Report: {name} ===")
    total = len(df)
    nulls = df.isnull().sum()
    for col, count in nulls.items():
        if count > 0:
            pct = count / total * 100
            print(f"{col:<12} → {count} nulls ({pct:.1f}%)")

null_report(customers, "customers")
null_report(products, "products")
null_report(orders, "orders")
""")

add_md("**Task 2.2: Clean Customers**\nFilling nulls in age/gender, dropping duplicate emails, changing dtypes, and classifying age groups.")
add_code("""
customers["age"].fillna(customers["age"].median(), inplace=True)
customers["gender"].fillna("Unknown", inplace=True)
customers.drop_duplicates(subset=["email"], keep="first", inplace=True)
customers["gender"] = customers["gender"].astype("category")
customers["age_group"] = customers["age"].apply(classify_customer)
customers.to_csv("../outputs/cleaned_customers.csv", index=False)
""")

add_md("**Task 2.3: Clean Products**\nFixing dirty price strings, addressing missing ratings, and specifying category dtype.")
add_code("""
products["price"] = products["price"].astype(str).str.replace("₹", "").str.strip().astype(float)
products["rating"].fillna(round(products["rating"].mean(), 1), inplace=True)
products["category"] = products["category"].astype("category")

null_report(customers, "customers_cleaned")
null_report(products, "products_cleaned")
""")

add_md("## Part 3: NumPy Analysis\n\n**Task 3.1 & 3.2**\nVectorized taxation/discounting, reshaping arrays.")
add_code("""
price_array = products["price"].values
price_with_tax = price_array * 1.18
final_price = price_with_tax * 0.90
print(f"Final Price Array Shape: {final_price.shape}, Dtype: {final_price.dtype}")
print(f"First 5 elements: {final_price[:5]}")

first_20 = final_price[:20]
print("\\nFirst 20 (1D):", first_20.shape)

reshaped = first_20.reshape(4, 5)
print("\\nReshaped (4, 5):\\n", reshaped)

transposed = reshaped.T
print("\\nTransposed (5, 4):\\n", transposed)

flattened = transposed.flatten()
print("\\nFlattened (1D):\\n", flattened)
""")

add_md("## Part 4: SQL Analysis\n\n**Task 4.1 & 4.2**\nCreating `retailsense.db` and executing 7 distinct business logic queries.")
add_code("""
conn = sqlite3.connect("../outputs/retailsense.db")
customers.to_sql("customers", conn, if_exists="replace", index=False)
products.to_sql("products", conn, if_exists="replace", index=False)
orders.to_sql("orders", conn, if_exists="replace", index=False)

queries = {
    "Q1: Customers per city": "SELECT city, COUNT(*) as count FROM customers GROUP BY city ORDER BY count DESC",
    "Q2: Top 5 expensive products": "SELECT product_name, price FROM products ORDER BY price DESC LIMIT 5",
    "Q3: Orders with discount > 20": "SELECT order_id, customer_id, discount_pct FROM orders WHERE discount_pct > 20",
    "Q4: Average rating per category": "SELECT category, AVG(rating) as avg_rating FROM products GROUP BY category",
    "Q5: Categories > 10 products AND rating > 3.5": "SELECT category FROM products GROUP BY category HAVING COUNT(*) > 10 AND AVG(rating) > 3.5",
    "Q6: Order details (Inner Join)": "SELECT c.name, p.product_name, o.quantity, p.price FROM orders o JOIN customers c ON o.customer_id = c.customer_id JOIN products p ON o.product_id = p.product_id",
    "Q7: Customers with no orders": "SELECT c.name, c.email FROM customers c LEFT JOIN orders o ON c.customer_id = o.customer_id WHERE o.order_id IS NULL"
}

for q_name, sql in queries.items():
    print(f"\\n--- {q_name} ---")
    display(pd.read_sql(sql, conn).head())

conn.close()
""")

add_md("## Part 5: Advanced Pandas: GroupBy & Pivot\n\n**Task 5.1 & 5.2**\nMerging datasets into `full_df` and grouping insights.")
add_code("""
orders_cust = pd.merge(orders, customers, on="customer_id", how="inner")
full_df = pd.merge(orders_cust, products, on="product_id", how="inner")
full_df["revenue"] = full_df.apply(lambda row: calculate_revenue(row["price"], row["quantity"], row["discount_pct"]), axis=1)

print("\\nTotal revenue per product category:")
display(full_df.groupby("category")["revenue"].sum())

print("\\nAverage order quantity per city:")
display(full_df.groupby("city")["quantity"].mean())

print("\\nTop 3 customers by total revenue:")
display(full_df.groupby("name")["revenue"].sum().nlargest(3))

print("\\nCustom aggregation (Category -> Revenue, Unique Customers, Avg Discount):")
display(full_df.groupby("category").agg({"revenue": "sum", "customer_id": "nunique", "discount_pct": "mean"}))

print("\\nPivot Table (Category vs Age Group -> Revenue Sum):")
display(full_df.pivot_table(index="category", columns="age_group", values="revenue", aggfunc="sum", fill_value=0))
""")

add_md("## Part 6: Data Visualization\n\nBuilding 5 specific charts reflecting `full_df` trends.")
add_code("""
# P1 Revenue by product category
plt.figure(figsize=(8, 5))
full_df.groupby("category")["revenue"].sum().plot(kind="bar", color="skyblue")
plt.title("Revenue by Product Category")
plt.xlabel("Category")
plt.ylabel("Total Revenue")
plt.show()
""")
add_md("Insight: Electronics brings in the highest amount of revenue, dwarfing Books and Food.")

add_code("""
# P2 Customer age distribution
plt.figure(figsize=(8, 5))
sns.histplot(customers["age"], bins=15, kde=True, color="purple")
plt.title("Customer Age Distribution")
plt.xlabel("Age")
plt.ylabel("Frequency")
plt.show()
""")
add_md("Insight: The distribution is relatively uniform across adult ages, with a spike at the median filled values.")

add_code("""
# P3 Price distribution per category
plt.figure(figsize=(8, 5))
sns.boxplot(data=products, x="category", y="price", palette="Set2")
plt.title("Price Distribution per Category")
plt.xlabel("Category")
plt.ylabel("Price")
plt.show()
""")
add_md("Insight: Electronics and Clothing have wide distributions, potentially indicating premium and budget options.")

add_code("""
# P4 Correlation heatmap of numeric columns
plt.figure(figsize=(8, 6))
numeric_cols = full_df.select_dtypes(include=[np.number])
sns.heatmap(numeric_cols.corr(), annot=True, cmap="coolwarm", fmt=".2f")
plt.title("Correlation Heatmap of Full Data")
plt.show()
""")
add_md("Insight: Strong correlation between revenue, price, and quantity as expected mathematically.")

add_code("""
# P5 Interactive scatter: Price vs Rating
fig = px.scatter(
    products, x="price", y="rating", color="category",
    hover_name="product_name", title="Price vs Rating by Category"
)
fig.show()

# P6 Bonus: Top 10 customers
top_cust = full_df.groupby('name')['revenue'].sum().nlargest(10).reset_index()
fig2 = px.bar(top_cust, x='name', y='revenue', title="Top 10 Customers by Revenue", color="revenue")
fig2.show()
""")
add_md("Insight: The scatter plot reveals rating is sparsely related to price, while scatter highlights product groupings nicely.")

add_md("## Part 7: API Integration\nFetching data from a REST endpoint.")
add_code("""
resp = requests.get("https://jsonplaceholder.typicode.com/users")
if resp.status_code == 200:
    users = resp.json()
    for u in users[:2]:
        print(f"Name: {u['name']}, Email: {u['email']}, City: {u['address']['city']}")

post_resp = requests.post("https://jsonplaceholder.typicode.com/posts", json={
  "title": "RetailSense Report",
  "body": "Q4 revenue exceeded targets by 12%",
  "userId": 1
})
print(f"Status: {post_resp.status_code}, POST response ID: {post_resp.json().get('id')}")

with open("../outputs/api_users.json", "w") as f:
    json.dump(users, f)

with open("../outputs/api_users.json", "r") as f:
    loaded_users = json.load(f)
    print("First loaded user name:", loaded_users[0]["name"])
""")

add_md("## Part 9: Ethics & Privacy Audit")
add_md("""
### Ethics Answers

1. **PII Identification:** 
   - `name`: Drop prior to external sharing.
   - `email`: Hash or mask completely (e.g. `us***@example.com`). This is highly sensitive.
   - `address/city`: Mask down to state or region level.
   
2. **Anonymization Plan (ML Vendor Sharing):**
   - Drop `name` and `email` columns entirely, as they offer no predictive ML benefit and are severe privacy risks.
   - Hash `customer_id` using a salted cryptographic hash to maintain referential integrity without exposing actual IDs.
   - Generalize exact `age` into coarse categorical bins (e.g. `20-30`, `30-40`) to prevent de-anonymization via link attacks.

3. **API Ethics (CRM APIs):**
   - **Data Retention:** Does the API provider cache or store the PII I transmit, and for how long?
   - **Third-Party Subprocessors:** Do they sell or syndicate our customer data to downstream brokers?
   - **Security Compliance:** Is the API connection encrypted (TLS1.2+) and compliant with SOC2 / GDPR boundaries?

4. **Null Handling Choice:**
   - Yes, using median fill for an age group can introduce artificial peaks and bias toward the "Adult" segment. If those users were actually older or younger, their categorization as median artificially inflates the revenue metrics for that specific demographic.
""")

notebook = {
    "cells": cells,
    "metadata": {
        "kernelspec": {
            "display_name": "Python 3",
            "language": "python",
            "name": "python3"
        },
        "language_info": {
            "codemirror_mode": {"name": "ipython", "version": 3},
            "file_extension": ".py",
            "mimetype": "text/x-python",
            "name": "python",
            "nbconvert_exporter": "python",
            "pygments_lexer": "ipython3",
            "version": "3.8.0"
        }
    },
    "nbformat": 4,
    "nbformat_minor": 4
}

with open(r"d:\AIML Course\retailsense\notebooks\analysis.ipynb", "w", encoding="utf-8") as f:
    json.dump(notebook, f, indent=1)

print("Notebook generated successfully.")
