import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px
from utils import calculate_revenue

st.set_page_config(page_title="RetailSense Analytics Dashboard", layout="wide")

@st.cache_data
def load_data():
    conn = sqlite3.connect("outputs/retailsense.db")
    customers = pd.read_sql("SELECT * FROM customers", conn)
    orders = pd.read_sql("SELECT * FROM orders", conn)
    products = pd.read_sql("SELECT * FROM products", conn)
    conn.close()
    
    # Merge for full_df
    orders_cust = pd.merge(orders, customers, on="customer_id", how="inner")
    full_df = pd.merge(orders_cust, products, on="product_id", how="inner")
    
    # Calculate revenue
    full_df["revenue"] = full_df.apply(lambda row: calculate_revenue(row["price"], row["quantity"], row["discount_pct"]), axis=1)
    
    return full_df, products

try:
    full_df, products = load_data()
except Exception as e:
    st.error(f"Error loading data: {e}")
    st.stop()

st.title("🛒 RetailSense Analytics Dashboard")

# Sidebar
st.sidebar.header("Filters")
categories = ["All"] + list(products["category"].unique())
selected_category = st.sidebar.selectbox("Choose Category", categories)

min_rating = st.sidebar.slider("Minimum Product Rating", min_value=1.0, max_value=5.0, value=1.0, step=0.1)

# Apply filters
filtered_df = full_df[full_df["rating"] >= min_rating]
if selected_category != "All":
    filtered_df = filtered_df[filtered_df["category"] == selected_category]
else:
    # If "All" is selected, we still want to show prices across all categories
    pass

# Section 1 - Overview Metrics
st.header("1. Overview Metrics")
col1, col2, col3 = st.columns(3)
col1.metric("Total Revenue", f"₹{filtered_df['revenue'].sum():,.2f}")
col2.metric("Total Orders", f"{len(filtered_df)}")
col3.metric("Avg Product Rating", f"{filtered_df['rating'].mean():.2f}" if not filtered_df.empty else "0.00")

# Section 2 - Data Table
st.header("2. Data Table")
st.dataframe(filtered_df.head(50))

# Section 3 - Charts
st.header("3. Charts")
chart_col1, chart_col2 = st.columns(2)

with chart_col1:
    st.subheader("Revenue by Age Group")
    if not filtered_df.empty:
        rev_by_age = filtered_df.groupby("age_group")["revenue"].sum().reset_index()
        fig_bar = px.bar(rev_by_age, x="age_group", y="revenue", color="age_group")
        st.plotly_chart(fig_bar, use_container_width=True)
    else:
        st.write("No data available for the selected filters.")

with chart_col2:
    st.subheader(f"Price Distribution: {selected_category}")
    if not filtered_df.empty:
        fig_box = px.box(filtered_df, x="category", y="price", color="category")
        st.plotly_chart(fig_box, use_container_width=True)
    else:
        st.write("No data available for the selected filters.")

# Section 4 - Upload & Inspect
st.header("4. Upload & Inspect CSV")
uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])
if uploaded_file is not None:
    df_uploaded = pd.read_csv(uploaded_file)
    st.write("**Preview (first 10 rows):**")
    st.dataframe(df_uploaded.head(10))
    st.write("**Basic Stats (.describe):**")
    st.dataframe(df_uploaded.describe())
