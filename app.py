import streamlit as st
import pandas as pd

# إعداد الصفحة
st.set_page_config(
    page_title="Saudi Food Delivery Dashboard",
    page_icon="🍔",
    layout="wide"
)

# ستايل بسيط (أزرق وأبيض)
st.markdown("""
<style>
.metric-card {
    background-color:#f0f6ff;
    padding:20px;
    border-radius:10px;
    border:1px solid #d0e2ff;
}
h1,h2,h3{
    color:#0a3d91;
}
</style>
""", unsafe_allow_html=True)

st.title("🇸🇦 Saudi Food Delivery Market Dashboard (2023–2025)")

# تحميل البيانات
@st.cache_data
def load_data():
    df = pd.read_csv("saudi_food_delivery_market_2023_2025.csv")
    df.columns = df.columns.str.strip()
    df["Date"] = pd.to_datetime(df["Date"])
    return df

df = load_data()

# فلترة المنصة
platform = st.sidebar.selectbox(
    "Select Platform",
    df["Platform"].unique()
)

filtered = df[df["Platform"] == platform]

# مؤشرات
col1, col2, col3 = st.columns(3)

total_orders = int(filtered["Orders"].sum()) if "Orders" in filtered.columns else 0
total_revenue = int(filtered["Revenue"].sum()) if "Revenue" in filtered.columns else 0
avg_delivery = round(filtered["Delivery_Time_Min"].mean(),1) if "Delivery_Time_Min" in filtered.columns else 0

col1.metric("Total Orders", f"{total_orders:,}")
col2.metric("Total Revenue (SAR)", f"{total_revenue:,}")
col3.metric("Avg Delivery Time (min)", avg_delivery)

st.divider()

# الرسم الأول
st.subheader("📈 Monthly Orders")

orders_chart = filtered.groupby("Date")["Orders"].sum()
st.line_chart(orders_chart)

# الرسم الثاني
st.subheader("💰 Monthly Revenue")

revenue_chart = filtered.groupby("Date")["Revenue"].sum()
st.line_chart(revenue_chart)

st.divider()

# عرض البيانات
st.subheader("Dataset Preview")

st.dataframe(filtered, use_container_width=True)
