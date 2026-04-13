# 文件名：app.py
# 美窝房产 - 真实数据看板

import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Meiwo Realty Dashboard", layout="wide")

st.title("🏠 美窝房产 · 成交数据分析看板")

# 加载清洗后的数据
@st.cache_data
def load_data():
    df = pd.read_csv("cleaned_rental_data.csv", encoding="gbk")
    # 转换日期列
    df["开始日期"] = pd.to_datetime(df["开始日期"])
    df["结束日期"] = pd.to_datetime(df["结束日期"])
    return df

try:
    df = load_data()
    st.success(f"✅ 数据加载成功！共 {len(df)} 条成交记录")
except FileNotFoundError:
    st.error("❌ 找不到 cleaned_rental_data.csv，请先运行 Jupyter 清洗数据")
    st.stop()

# 侧边栏筛选
st.sidebar.header("🔍 筛选条件")

# 区域筛选（如果有区域列的话，目前没有，可以后续补充）
# 学校筛选
schools = ["全部"] + sorted(df["学校"].dropna().unique().tolist())
selected_school = st.sidebar.selectbox("🎓 客户身份", schools)

# 来源筛选
sources = ["全部"] + sorted(df["来源"].dropna().unique().tolist())
selected_source = st.sidebar.selectbox("📢 客户来源", sources)

# 户型筛选
unit_types = ["全部"] + sorted(df["户型"].dropna().unique().tolist())
selected_unit = st.sidebar.selectbox("🏠 户型", unit_types)

# 筛选数据
filtered_df = df.copy()
if selected_school != "全部":
    filtered_df = filtered_df[filtered_df["学校"] == selected_school]
if selected_source != "全部":
    filtered_df = filtered_df[filtered_df["来源"] == selected_source]
if selected_unit != "全部":
    filtered_df = filtered_df[filtered_df["户型"] == selected_unit]

# KPI 卡片
col1, col2, col3, col4 = st.columns(4)
col1.metric("🏘️ 总成交单数", len(filtered_df))
col2.metric("💰 Source", f"${filtered_df['价格1'].mean():,.0f}")
col3.metric("💰 B&B", f"${filtered_df['价格2'].mean():,.0f}")
col4.metric("🎓 身份数量", filtered_df["学校"].nunique())

# 图表1：各学校成交数量（Top 10）
st.subheader("🎓 各身份成交数量（Top 10）")
school_counts = filtered_df["学校"].value_counts().head(10).reset_index()
school_counts.columns = ["身份", "数量"]
fig1 = px.bar(school_counts, x="学校", y="数量", text="数量", color="数量")
fig1.update_traces(textposition='outside')
fig1.update_layout(height=450)
st.plotly_chart(fig1, use_container_width=True)

# 图表2：客户来源分布
st.subheader("📢 客户来源分布")
source_counts = filtered_df["来源"].value_counts().reset_index()
source_counts.columns = ["来源", "数量"]
fig2 = px.pie(source_counts, values="数量", names="来源", hole=0.3)
fig2.update_traces(textposition='inside', textinfo='percent+label')
fig2.update_layout(height=500)
st.plotly_chart(fig2, use_container_width=True)

# 图表3：户型分布
col1, col2 = st.columns(2)
with col1:
    st.subheader("🏠 户型分布")
    unit_counts = filtered_df["户型"].value_counts().reset_index()
    unit_counts.columns = ["户型", "数量"]
    fig3 = px.bar(unit_counts, x="户型", y="数量", text="数量", color="数量")
    fig3.update_traces(textposition='outside')
    fig3.update_layout(height=400)
    st.plotly_chart(fig3, use_container_width=True)

with col2:
    st.subheader("🏢 热门大楼（Top 8）")
    building_counts = filtered_df["大楼"].value_counts().head(8).reset_index()
    building_counts.columns = ["大楼", "数量"]
    fig4 = px.bar(building_counts, x="数量", y="大楼", text="数量", orientation='h')
    fig4.update_traces(textposition='outside')
    fig4.update_layout(height=400)
    st.plotly_chart(fig4, use_container_width=True)

# 图表4：成交趋势（按开始日期）
st.subheader("📅 成交趋势（按开始日期）")
daily_trend = filtered_df.groupby("开始日期").size().reset_index(name="数量")
fig5 = px.line(daily_trend, x="开始日期", y="数量", markers=True, title="每日成交数量")
fig5.update_layout(height=400)
st.plotly_chart(fig5, use_container_width=True)

# 数据表格
st.subheader("📋 成交明细")
st.dataframe(filtered_df, use_container_width=True)

# 下载按钮
csv = filtered_df.to_csv(index=False).encode('utf-8-sig')
st.download_button("⬇️ 下载筛选后的数据", csv, "filtered_data.csv", "text/csv")
