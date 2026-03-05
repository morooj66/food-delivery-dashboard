import streamlit as st

import pandas as pd



st.title("Saudi Food Delivery Market Dashboard")



df = pd.read_csv("saudi_food_delivery_market_2023_2025.csv")



df["Date"] = pd.to_datetime(df["Date"])



st.subheader("Dataset Preview")

st.dataframe(df)



platform = st.selectbox("Choose Platform", df["Platform"].unique())



filtered = df[df["Platform"] == platform]



st.subheader("Revenue Over Time")

st.line_chart(filtered.set_index("Date")["Revenue"])



st.subheader("Market Share")

st.line_chart(filtered.set_index("Date")["Market_Share"])



st.subheader("Marketing Spend vs New Users")

st.scatter_chart(filtered[["Marketing_Spend_SAR","New_Users"]])

