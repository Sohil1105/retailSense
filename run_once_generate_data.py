import pandas as pd
import numpy as np
import random
import os

np.random.seed(42)
random.seed(42)
os.makedirs("data", exist_ok=True)
os.makedirs("outputs", exist_ok=True)

# --- Customers ---
n_customers = 500
cities = ["Mumbai", "Delhi", "Bengaluru", "Hyderabad", "Chennai", "Pune", "Kolkata"]
genders = ["M", "F", "Other"]

ages = np.random.randint(18, 65, n_customers).astype(float)
ages[np.random.choice(n_customers, 40, replace=False)] = np.nan  # inject nulls

gender_list = [random.choice(genders) for _ in range(n_customers)]
for i in np.random.choice(n_customers, 30, replace=False):
    gender_list[i] = None  # inject nulls

customers = pd.DataFrame({
    "customer_id": [f"C{str(i).zfill(4)}" for i in range(1, n_customers + 1)],
    "name": [f"Customer_{i}" for i in range(1, n_customers + 1)],
    "email": [f"user{i}@example.com" for i in range(1, n_customers + 1)],
    "age": ages,
    "city": [random.choice(cities) for _ in range(n_customers)],
    "gender": gender_list,
    "signup_date": pd.date_range("2022-01-01", periods=n_customers, freq="D").strftime("%Y-%m-%d").tolist()
})

# Add 10 duplicate emails
for i in range(10):
    customers.iloc[-(i+1), customers.columns.get_loc("email")] = customers.iloc[i]["email"]

customers.to_csv("data/customers.csv", index=False)
print("customers.csv created:", customers.shape)

# --- Products ---
categories = ["Electronics", "Clothing", "Food", "Books"]
n_products = 80

prices = np.random.randint(200, 5000, n_products).astype(float)
ratings = np.random.uniform(1.5, 5.0, n_products).round(1)
ratings[np.random.choice(n_products, 12, replace=False)] = np.nan

# Make some prices into dirty strings
price_list = []
for p in prices:
    r = random.random()
    if r < 0.2:
        price_list.append(f"₹{int(p)}")
    elif r < 0.35:
        price_list.append(str(float(p)))
    else:
        price_list.append(p)

products = pd.DataFrame({
    "product_id": [f"P{str(i).zfill(3)}" for i in range(1, n_products + 1)],
    "product_name": [f"Product_{i}" for i in range(1, n_products + 1)],
    "category": [random.choice(categories) for _ in range(n_products)],
    "price": price_list,
    "rating": ratings
})
products.to_csv("data/products.csv", index=False)
print("products.csv created:", products.shape)

# --- Orders ---
n_orders = 1500
orders = pd.DataFrame({
    "order_id": [f"O{str(i).zfill(5)}" for i in range(1, n_orders + 1)],
    "customer_id": [random.choice(customers["customer_id"].tolist()) for _ in range(n_orders)],
    "product_id": [random.choice(products["product_id"].tolist()) for _ in range(n_orders)],
    "order_date": pd.date_range("2024-01-01", periods=n_orders, freq="h").strftime("%Y-%m-%d").tolist(),
    "quantity": np.random.randint(1, 6, n_orders),
    "discount_pct": np.random.choice([0, 5, 10, 15, 20, 25, 30, 40], n_orders)
})
orders.to_csv("data/orders.csv", index=False)
print("orders.csv created:", orders.shape)

print("\n✅ All datasets created in /data folder.")
