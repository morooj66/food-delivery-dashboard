import streamlit as st
import pandas as pd

st.set_page_config(page_title="Saudi Food Delivery Dashboard", layout="wide")

st.title("Saudi Food Delivery Market Dashboard (2023–2025)")

# تحميل البيانات
@st.cache_data
def load_data():
    df = pd.read_csv("saudi_food_delivery_market_2023_2025.csv")
    df.columns = df.columns.str.strip()
    df["Date"] = pd.to_datetime(df["Date"])
    return df

df = load_data()

# اختيار المنصة
platform = st.sidebar.selectbox(
    "Choose Platform",
    df["Platform"].unique()
)

filtered = df[df["Platform"] == platform]

# مؤشرات سريعة
col1, col2, col3 = st.columns(3)

orders_total = int(filtered["Orders"].sum()) if "Orders" in filtered.columns else 0
revenue_total = int(filtered["Revenue"].sum()) if "Revenue" in filtered.columns else 0
avg_delivery = round(filtered["Delivery_Time_Min"].mean(),1) if "Delivery_Time_Min" in filtered.columns else 0

col1.metric("Total Orders", orders_total)
col2.metric("Total Revenue (SAR)", revenue_total)
col3.metric("Average Delivery Time", avg_delivery)
st.subheader("Monthly Orders")

orders_chart = filtered.groupby("Date")["Orders"].sum()
st.line_chart(orders_chart)

st.subheader("Monthly Revenue")

revenue_chart = filtered.groupby("Date")["Revenue"].sum()
st.line_chart(revenue_chart)

st.subheader("Dataset Preview")

st.dataframe(filtered)
