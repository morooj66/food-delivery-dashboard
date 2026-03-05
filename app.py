import streamlit as st
import pandas as pd
import plotly.express as px

# إعداد الصفحة
st.set_page_config(
    page_title="Saudi Food Delivery Dashboard",
    page_icon="🍔",
    layout="wide"
)

# ستايل أزرق وأبيض
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
        df["Year"] = df["Date"].dt.year
        df["Month"] = df["Date"].dt.month
    if "City" not in df.columns:
        df["City"] = "Unknown"
    return df

df = load_data()

# فلترة المنصة
platforms = df["Platform"].unique() if "Platform" in df.columns else []
selected_platform = st.sidebar.selectbox("Select Platform", platforms)

filtered = df[df["Platform"] == selected_platform] if "Platform" in df.columns else df

# فلترة السنة
years = sorted(filtered["Year"].unique()) if "Year" in filtered.columns else []
selected_year = st.sidebar.selectbox("Select Year", years) if years else None

if selected_year:
    filtered = filtered[filtered["Year"] == selected_year]

# فلترة المدينة
cities = filtered["City"].unique() if "City" in filtered.columns else []
selected_city = st.sidebar.selectbox("Select City", cities) if cities else None

if selected_city:
    filtered = filtered[filtered["City"] == selected_city]

# تحديد الأعمدة الصحيحة
orders_col = "Orders" if "Orders" in filtered.columns else "Orders_Count" if "Orders_Count" in filtered.columns else None
revenue_col = "Revenue" if "Revenue" in filtered.columns else None
delivery_col = "Delivery_Time_Min" if "Delivery_Time_Min" in filtered.columns else None

# مؤشرات رئيسية
col1, col2, col3 = st.columns(3)

total_orders = int(filtered[orders_col].sum()) if orders_col else 0
total_revenue = int(filtered[revenue_col].sum()) if revenue_col else 0
avg_delivery = round(filtered[delivery_col].mean(),1) if delivery_col else 0

col1.metric("Total Orders", f"{total_orders:,}")
col2.metric("Total Revenue (SAR)", f"{total_revenue:,}")
col3.metric("Avg Delivery Time (min)", avg_delivery)

st.divider()

# رسومات Orders
st.subheader("📈 Monthly Orders")
if orders_col and "Date" in filtered.columns:
    orders_chart = filtered.groupby("Date")[orders_col].sum().reset_index()
    fig_orders = px.line(orders_chart, x="Date", y=orders_col, markers=True,
                         title="Monthly Orders", template="plotly_white")
    fig_orders.update_layout(title_font_color="#0a3d91")
    st.plotly_chart(fig_orders, use_container_width=True)
else:
    st.info("Orders data not available in dataset.")

# رسومات Revenue
st.subheader("💰 Monthly Revenue")
if revenue_col and "Date" in filtered.columns:
    revenue_chart = filtered.groupby("Date")[revenue_col].sum().reset_index()
    fig_revenue = px.line(revenue_chart, x="Date", y=revenue_col, markers=True,
                          title="Monthly Revenue", template="plotly_white")
    fig_revenue.update_layout(title_font_color="#0a3d91")
    st.plotly_chart(fig_revenue, use_container_width=True)
else:
    st.info("Revenue data not available in dataset.")

# Market Share لكل منصة
st.subheader("📊 Market Share by Platform")
if orders_col:
    market_share = df.groupby("Platform")[orders_col].sum().reset_index()
    fig_share = px.pie(market_share, names="Platform", values=orders_col,
                       color_discrete_sequence=px.colors.sequential.Blues)
    st.plotly_chart(fig_share, use_container_width=True)
else:
    st.info("Orders data not available for Market Share.")

st.divider()

# عرض جدول البيانات
st.subheader("Dataset Preview")
st.dataframe(filtered, use_container_width=True)
