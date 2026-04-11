# 文件名：app.py
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(page_title="Meiwo Realty Dashboard", layout="wide")

st.title("🏠 Meiwo Realty · Rental Data Analytics Dashboard")

# 加载模拟数据
@st.cache_data
def load_data():
    np.random.seed(42)
    areas = ["Downtown", "Midtown", "Brooklyn", "Queens", "Jersey City"]
    data = {
        "区域": np.random.choice(areas, 200),
        "租金": np.random.randint(1500, 5000, 200),
        "面积": np.random.randint(400, 1500, 200),
        "卧室": np.random.choice([0, 1, 2, 3], 200),
        "状态": np.random.choice(["已租", "未租"], 200, p=[0.6, 0.4]),
    }
    return pd.DataFrame(data)

df = load_data()

# 侧边栏筛选
st.sidebar.header("🔍 Filter")
selected_areas = st.sidebar.multiselect(
    "Select Area", df["区域"].unique(), default=df["区域"].unique()
)
min_price, max_price = st.sidebar.slider(
    "Rent Range", int(df["租金"].min()), int(df["租金"].max()), (2000, 4000)
)

# 筛选数据
filtered_df = df[
    (df["区域"].isin(selected_areas)) &
    (df["租金"] >= min_price) &
    (df["租金"] <= max_price)
]

# KPI 卡片
col1, col2, col3, col4 = st.columns(4)
col1.metric("🏘️ Total Properties", len(filtered_df))
col2.metric("💰 Average Rent", f"${filtered_df['租金'].mean():,.0f}")
col3.metric("📐 Average Area", f"{filtered_df['面积'].mean():,.0f} sqft")
col4.metric("🔑 Leased Rate", f"{(filtered_df['状态'] == '已租').mean() * 100:.1f}%")

# 三个图表并排
col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("Average Rent by Area")
    st.bar_chart(filtered_df.groupby("区域")["租金"].mean(), height=400)

with col2:
    st.subheader("Rent Distribution")
    # 用 Streamlit 的 area_chart 模拟分布（或者用 line_chart）
    rent_counts = filtered_df["租金"].value_counts().sort_index()
    st.line_chart(rent_counts, height=400)

with col3:
    st.subheader("Property Share by Area")
    # 饼图只能用 plotly，但统一高度
    area_counts = filtered_df["区域"].value_counts().reset_index()
    area_counts.columns = ["区域", "count"]
    fig = px.pie(area_counts, values="count", names="区域", title="")
    fig.update_layout(height=400, margin=dict(t=0, b=0, l=0, r=0))
    st.plotly_chart(fig, use_container_width=True)

# 数据表格
st.subheader("📋 Property Details")
st.dataframe(filtered_df, use_container_width=True)

# 下载按钮
csv = filtered_df.to_csv(index=False)
st.download_button("⬇️ Download Filtered Data", csv, "rental_data.csv", "text/csv")
