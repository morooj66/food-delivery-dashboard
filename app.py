# ===============================
# Saudi Food Delivery Dashboard
# ===============================

import streamlit as st
import pandas as pd
import plotly.express as px

# -------------------------------
# Page Configuration
# -------------------------------

st.set_page_config(
    page_title="Saudi Food Delivery Dashboard",
    page_icon="📊",
    layout="wide"
)

# -------------------------------
# Load Dataset
# -------------------------------

@st.cache_data
def load_data():
    df = pd.read_csv("/saudi_food_delivery_market_2023_2025.csv")
    df["Date"] = pd.to_datetime(df["Date"])
    return df

df = load_data()

# -------------------------------
# Sidebar Filters
# -------------------------------

st.sidebar.title("Filters")

platform_options = ["All"] + list(df["Platform"].unique())

selected_platform = st.sidebar.selectbox(
    "Select Platform",
    platform_options
)

if selected_platform != "All":
    df = df[df["Platform"] == selected_platform]

# -------------------------------
# Header
# -------------------------------

st.title("🇸🇦 Saudi Food Delivery Market Dashboard")
st.markdown("### Market Analysis for Major Delivery Platforms")

st.markdown("---")

# -------------------------------
# KPI Calculations
# -------------------------------

total_orders = int(df["Monthly_Orders"].sum())
total_revenue = int(df["Revenue"].sum())
avg_delivery_time = round(df["Average_Order_Value_SAR"].mean(), 2)
avg_rating = round(df["Customer_Retention_Rate"].mean(), 2)

# -------------------------------
# KPI Cards
# -------------------------------

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Orders", f"{total_orders:,}")
col2.metric("Total Revenue (SAR)", f"{total_revenue:,}")
col3.metric("Average Order Value", f"{avg_delivery_time}")
col4.metric("Customer Retention Rate", f"{avg_rating}")

st.markdown("---")

# -------------------------------
# Monthly Orders Trend
# -------------------------------

orders_trend = df.groupby("Date")["Monthly_Orders"].sum().reset_index()

fig_orders = px.line(
    orders_trend,
    x="Date",
    y="Monthly_Orders",
    title="Monthly Orders Trend",
    markers=True
)

st.plotly_chart(fig_orders, use_container_width=True)

# -------------------------------
# Revenue by Platform
# -------------------------------

revenue_platform = df.groupby("Platform")["Revenue"].sum().reset_index()

fig_revenue = px.bar(
    revenue_platform,
    x="Platform",
    y="Revenue",
    title="Revenue by Platform"
)

st.plotly_chart(fig_revenue, use_container_width=True)

# -------------------------------
# Market Share Pie Chart
# -------------------------------

market_share = df.groupby("Platform")["Monthly_Orders"].sum().reset_index()

fig_market = px.pie(
    market_share,
    names="Platform",
    values="Monthly_Orders",
    title="Market Share by Platform"
)

st.plotly_chart(fig_market, use_container_width=True)

# -------------------------------
# Average Delivery Value Comparison
# -------------------------------

delivery_compare = df.groupby("Platform")["Average_Order_Value_SAR"].mean().reset_index()

fig_delivery = px.bar(
    delivery_compare,
    x="Platform",
    y="Average_Order_Value_SAR",
    title="Average Order Value Comparison"
)

st.plotly_chart(fig_delivery, use_container_width=True)

st.markdown("---")

# -------------------------------
# Data Table
# -------------------------------

st.subheader("Dataset Overview")

st.dataframe(df, use_container_width=True)
