# ==========================================
# Saudi Food Delivery Market Dashboard (No Orders)
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
# Load Dataset
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
selected_platform = st.sidebar.selectbox("Choose Platform", platforms)
if selected_platform != "All":
    df = df[df["Platform"] == selected_platform]

# ------------------------------------------
# Header
# ------------------------------------------
st.title("🇸🇦 Saudi Food Delivery Market Dashboard")
st.markdown("Platform Performance Analysis (HungerStation, Jahez, Keeta, Ninja)")

st.divider()

# ------------------------------------------
# KPI Calculations
# ------------------------------------------
total_revenue = int(df["Revenue"].sum())
avg_order_value = round(df["Average_Order_Value_SAR"].mean(), 2)
avg_retention = round(df["Customer_Retention_Rate"].mean(), 2)
total_active_users = int(df["Active_Users"].sum())
total_marketing_spend = int(df["Marketing_Spend_SAR"].sum())

# ------------------------------------------
# KPI Cards
# ------------------------------------------
col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("Total Revenue (SAR)", f"{total_revenue:,}")
col2.metric("Average Order Value (SAR)", avg_order_value)
col3.metric("Customer Retention Rate", avg_retention)
col4.metric("Total Active Users", f"{total_active_users:,}")
col5.metric("Marketing Spend (SAR)", f"{total_marketing_spend:,}")

st.divider()

# ------------------------------------------
# Revenue by Platform
# ------------------------------------------
revenue_platform = df.groupby("Platform")["Revenue"].sum().reset_index()
fig_revenue = px.bar(
    revenue_platform,
    x="Platform",
    y="Revenue",
    title="Revenue by Platform",
    color="Platform"
)
st.plotly_chart(fig_revenue, use_container_width=True)

# ------------------------------------------
# Average Order Value by Platform
# ------------------------------------------
avg_order_value_platform = df.groupby("Platform")["Average_Order_Value_SAR"].mean().reset_index()
fig_avg_value = px.bar(
    avg_order_value_platform,
    x="Platform",
    y="Average_Order_Value_SAR",
    title="Average Order Value by Platform",
    color="Platform"
)
st.plotly_chart(fig_avg_value, use_container_width=True)

# ------------------------------------------
# Active Users by Platform
# ------------------------------------------
active_users_platform = df.groupby("Platform")["Active_Users"].sum().reset_index()
fig_users = px.bar(
    active_users_platform,
    x="Platform",
    y="Active_Users",
    title="Active Users by Platform",
    color="Platform"
)
st.plotly_chart(fig_users, use_container_width=True)

# ------------------------------------------
# Market Share Pie Chart
# ------------------------------------------
market_share = df.groupby("Platform")["Market_Share"].sum().reset_index()
fig_market = px.pie(
    market_share,
    names="Platform",
    values="Market_Share",
    title="Market Share by Platform"
)
st.plotly_chart(fig_market, use_container_width=True)

# ------------------------------------------
# Marketing Spend by Platform
# ------------------------------------------
marketing_platform = df.groupby("Platform")["Marketing_Spend_SAR"].sum().reset_index()
fig_marketing = px.bar(
    marketing_platform,
    x="Platform",
    y="Marketing_Spend_SAR",
    title="Marketing Spend by Platform",
    color="Platform"
)
st.plotly_chart(fig_marketing, use_container_width=True)

st.divider()

# ------------------------------------------
# Dataset Table
# ------------------------------------------
st.subheader("Dataset Overview")
st.dataframe(df, use_container_width=True)
