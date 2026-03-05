import streamlit as st
import pandas as pd

# إعداد الصفحة
st.set_page_config(
    page_title="Saudi Food Delivery Dashboard",
    page_icon="🍔",
    layout="wide"
)

# تصميم أزرق وأبيض بسيط
st.markdown("""
<style>
h1,h2,h3{
color:#0a3d91;
}
[data-testid="metric-container"]{
background-color:#f0f6ff;
border:1px solid #d0e2ff;
padding:15px;
border-radius:10px;
}
</style>
""", unsafe_allow_html=True)

st.title("🇸🇦 Saudi Food Delivery Market Dashboard (2023–2025)")

# تحميل البيانات
@st.cache_data
def load_data():
    df = pd.read_csv("saudi_food_delivery_market_2023_2025.csv")
    df.columns = df.columns.str.strip()
    
    if "Date" in df.columns:
        df["Date"] = pd.to_datetime(df["Date"])
        
    return df

df = load_data()

# فلتر المنصة
platform = st.sidebar.selectbox(
    "Select Platform",
    df["Platform"].unique()
)

filtered = df[df["Platform"] == platform]

# المؤشرات
col1, col2, col3 = st.columns(3)

orders_total = int(filtered["Orders"].sum()) if "Orders" in filtered.columns else 0
revenue_total = int(filtered["Revenue"].sum()) if "Revenue" in filtered.columns else 0
avg_delivery = round(filtered["Delivery_Time_Min"].mean(),1) if "Delivery_Time_Min" in filtered.columns else 0

col1.metric("Total Orders", f"{orders_total:,}")
col2.metric("Total Revenue (SAR)", f"{revenue_total:,}")
col3.metric("Avg Delivery Time (min)", avg_delivery)

st.divider()

# الرسم الأول
st.subheader("📈 Monthly Orders")

if "Orders" in filtered.columns and "Date" in filtered.columns:
    orders_chart = filtered.groupby("Date")["Orders"].sum()
    st.line_chart(orders_chart)
else:
    st.info("Orders data not available in dataset.")

# الرسم الثاني
st.subheader("💰 Monthly Revenue")

if "Revenue" in filtered.columns and "Date" in filtered.columns:
    revenue_chart = filtered.groupby("Date")["Revenue"].sum()
    st.line_chart(revenue_chart)
else:
    st.info("Revenue data not available in dataset.")

st.divider()

# عرض البيانات
st.subheader("Dataset Preview")
st.dataframe(filtered, use_container_width=True)
