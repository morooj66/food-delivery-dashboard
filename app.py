# ==========================================
# Saudi Food Delivery Market Dashboard
# ==========================================

import streamlit as st
import pandas as pd
import plotly.express as px
import os

# ------------------------------------------
# Page Config
# ------------------------------------------

st.set_page_config(
    page_title="Saudi Food Delivery Dashboard",
    page_icon="📊",
    layout="wide"
)

# ------------------------------------------
# Load Dataset (Safe Loader)
# ------------------------------------------

@st.cache_data
def load_data():

    possible_paths = [
        "saudi_food_delivery_market_2023_2025.csv",
        "food_delivery_data.csv",
        "data/saudi_food_delivery_market_2023_2025.csv",
        "data/food_delivery_data.csv"
    ]

    for path in possible_paths:
        if os.path.exists(path):
            df = pd.read_csv(path)
            df["Date"] = pd.to_datetime(df["Date"])
            return df

    st.error("Dataset file not found. Please upload the CSV file to the repository.")
    st.write("Files currently in the project folder:")
    st.write(os.listdir())
    st.stop()

df = load_data()

# ------------------------------------------
# Sidebar Filter
# ------------------------------------------

st.sidebar.title("Filter Platform")

platforms = ["All"] + list(df["Platform"].unique())

selected_platform = st.sidebar.selectbox(
    "Choose Platform",
    platforms
)

if selected_platform != "All":
    df = df[df["Platform"] == selected_platform]

# ------------------------------------------
# Header
# ------------------------------------------

st.title("🇸🇦 Saudi Food Delivery Market Dashboard")
st.markdown("Food Delivery Platforms Analysis (HungerStation, Jahez, Keeta, Ninja)")

st.divider()

# ------------------------------------------
# KPI Calculations
# ------------------------------------------

total_orders = int(df["Monthly_Orders"].sum())
total_revenue = int(df["Revenue"].sum())
avg_order_value = round(df["Average_Order_Value_SAR"].mean(), 2)
avg_retention = round(df["Customer_Retention_Rate"].mean(), 2)

# ------------------------------------------
# KPI Cards
# ------------------------------------------

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Orders", f"{total_orders:,}")
col2.metric("Total Revenue (SAR)", f"{total_revenue:,}")
col3.metric("Average Order Value (SAR)", avg_order_value)
col4.metric("Customer Retention Rate", avg_retention)

st.divider()

# ------------------------------------------
# Monthly Orders Trend
# ------------------------------------------

orders_trend = df.groupby("Date")["Monthly_Orders"].sum().reset_index()

fig_orders = px.line(
    orders_trend,
    x="Date",
    y="Monthly_Orders",
    title="Monthly Orders Trend",
    markers=True
)

st.plotly_chart(fig_orders, use_container_width=True)

# ------------------------------------------
# Revenue by Platform
# ------------------------------------------

revenue_platform = df.groupby("Platform")["Revenue"].sum().reset_index()

fig_revenue = px.bar(
    revenue_platform,
    x="Platform",
    y="Revenue",
    title="Revenue by Platform"
)

st.plotly_chart(fig_revenue, use_container_width=True)

# ------------------------------------------
# Market Share Pie Chart
# ------------------------------------------

market_share = df.groupby("Platform")["Monthly_Orders"].sum().reset_index()

fig_market = px.pie(
    market_share,
    names="Platform",
    values="Monthly_Orders",
    title="Market Share by Platform"
)

st.plotly_chart(fig_market, use_container_width=True)

# ------------------------------------------
# Average Order Value Comparison
# ------------------------------------------

order_value = df.groupby("Platform")["Average_Order_Value_SAR"].mean().reset_index()

fig_order_value = px.bar(
    order_value,
    x="Platform",
    y="Average_Order_Value_SAR",
    title="Average Order Value Comparison"
)

st.plotly_chart(fig_order_value, use_container_width=True)

st.divider()

# ------------------------------------------
# Dataset Table
# ------------------------------------------

st.subheader("Dataset")

st.dataframe(df, use_container_width=True)
