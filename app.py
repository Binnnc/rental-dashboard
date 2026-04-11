# 文件名：app.py
# 运行方式：在终端执行 streamlit run app.py

import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="房源数据分析", layout="wide")

st.title("🏠 美窝房产 · 房源数据分析看板")

# 加载数据（后面换成你的真实 Excel）
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
st.sidebar.header("🔍 筛选条件")
selected_areas = st.sidebar.multiselect(
    "选择区域", df["区域"].unique(), default=df["区域"].unique()
)
min_price, max_price = st.sidebar.slider(
    "租金范围", int(df["租金"].min()), int(df["租金"].max()), (2000, 4000)
)

# 筛选数据
filtered_df = df[
    (df["区域"].isin(selected_areas)) &
    (df["租金"] >= min_price) &
    (df["租金"] <= max_price)
]

# KPI 卡片
col1, col2, col3, col4 = st.columns(4)
col1.metric("🏘️ 房源总数", len(filtered_df))
col2.metric("💰 平均租金", f"${filtered_df['租金'].mean():,.0f}")
col3.metric("📐 平均面积", f"{filtered_df['面积'].mean():,.0f} sqft")
col4.metric("🔑 已租比例", f"{(filtered_df['状态'] == '已租').mean() * 100:.1f}%")

# 图表
left, right = st.columns(2)

with left:
    st.subheader("各区域平均租金对比")
    st.bar_chart(filtered_df.groupby("区域")["租金"].mean())

with right:
    st.subheader("租金分布")
    st.line_chart(filtered_df["租金"].value_counts().sort_index())

# 数据表格
st.subheader("📋 房源明细")
st.dataframe(filtered_df, use_container_width=True)

# 下载按钮
csv = filtered_df.to_csv(index=True)
st.download_button("⬇️ 下载筛选后的数据", csv, "filtered_rentals.csv", "text/csv")