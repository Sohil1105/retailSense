# 🛒 RetailSense: End-to-End Data Analysis & Insights Dashboard

Welcome to the **RetailSense** project! This repository contains a fully structured, end-to-end data pipeline built for a fictional retail company. The project covers data generation, cleaning, numerical assessment, SQL database modeling, advanced group-by interactions, and a fully interactive **Streamlit dashboard**.

## 🚀 Project Overview

RetailSense collects critical data on customers, products, and order history. However, this raw data is deeply fragmented with missing values, poorly typed numerical currencies, and duplicates. Our data engineering and analytics pipeline automatically:

1. **Cleans the raw datasets** (Handling demographic nulls, duplicated PII emails, and string manipulations on parsed currencies).
2. **Transforms and Vectors Computations** using `NumPy` to establish final tax pricing efficiently.
3. **Loads Structured Data to SQLite**, serving back complex aggregations across multiple table `JOIN` and `GROUP BY` patterns. 
4. **Pivots & Aggregates** metrics to unveil deep trends across categorical and demographic intersections via `Pandas`.
5. **Serves an Interactive Dashboard UI** built entirely via Python's `Streamlit`, showcasing modern statistical visualizations from `Plotly` and `Seaborn`.

## 🗂️ Project Structure

```bash
retailsense/
├── data/
│   ├── customers.csv         # Raw customer records
│   ├── orders.csv            # Sales transaction logs
│   └── products.csv          # Catalog items with ratings
    ...
├── outputs/
│   ├── api_users.json        # Fetched CRM endpoint mock data
│   ├── cleaned_customers.csv # Cleaned user subset
│   ├── retailsense.db        # Structured SQL database engine
│   └── summary_report.txt    # Fast-glance pipeline KPI summary
├── notebooks/
│   └── analysis.ipynb        # In-depth narrative analytical Jupyter notebook
├── app.py                    # Real-time Streamlit Dashboard application
├── analysis.py               # Background pipeline execution engine
├── config.json               # Environment & Project variable definitions
└── utils.py                  # Module for calculation and IO utilities
```

## 🛠️ Technology Stack
- **Languages:** Python 3.10+
- **Data Engineering:** `Pandas`, `NumPy`
- **Database Architecture:** `SQLite3`
- **Visualizations:** `Matplotlib`, `Seaborn`, `Plotly Express`
- **Dashboard Application:** `Streamlit`
- **API Fetching:** `Requests` library 

## ⚙️ How to Run

1. **Install dependencies:**
    ```bash
    pip install pandas numpy matplotlib seaborn plotly streamlit requests pyarrow
    ```

2. **Generate initial datasets (Run Once):**
   ```bash
   python run_once_generate_data.py
   ```

3. **Execute the core Analytics Pipeline** (Creates DB, fixes types, and saves visualizations):
    ```bash
    python analysis.py
    ```

4. **Boot the Streamlit Dashboard UI:**
    ```bash
    streamlit run app.py
    ```

## 🔐 Ethics & Privacy Note
Data within this pipeline handles mocked attributes that conventionally qualify as Personally Identifiable Information (PII) including emails and un-hashed explicit designations. The notebook contains a brief ethics audit on modern standard handling practices regarding redaction, cryptographic hashing, and categorical blurring for ML data transfers.