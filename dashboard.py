import streamlit as st
import pandas as pd
import json
from datetime import datetime

# Заголовок
st.title("CI/CD Pipeline Usage Dashboard")

# Загрузка данных
with open("pipeline_data.json") as f:
    data = json.load(f)
df = pd.DataFrame(data)

# Преобразуем дату
df["timestamp"] = pd.to_datetime(df["timestamp"])

# Фильтры
st.sidebar.header("Filters")
selected_lz = st.sidebar.multiselect("Caller Landing Zone", df["caller_lz"].unique())
selected_tool = st.sidebar.multiselect("Build Tool", df["build_tool"].unique())
date_range = st.sidebar.date_input("Date Range", [])

filtered_df = df.copy()

if selected_lz:
    filtered_df = filtered_df[filtered_df["caller_lz"].isin(selected_lz)]

if selected_tool:
    filtered_df = filtered_df[filtered_df["build_tool"].isin(selected_tool)]

if date_range and len(date_range) == 2:
    start_date = datetime.combine(date_range[0], datetime.min.time())
    end_date = datetime.combine(date_range[1], datetime.max.time())
    filtered_df = filtered_df[(filtered_df["timestamp"] >= start_date) & (filtered_df["timestamp"] <= end_date)]

# Общая статистика
st.subheader("Summary")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Runs", len(filtered_df))
col2.metric("Unique Repositories", filtered_df["repository"].nunique())
col3.metric("Reusable Workflows Used", filtered_df["called_reusable_workflow"].sum())
col4.metric("Success Rate", f"{(filtered_df['status'] == 'success').mean() * 100:.1f}%")

# График: Запуски по дате
st.subheader("Runs Over Time")
runs_by_date = filtered_df.groupby(filtered_df["timestamp"].dt.date).size()
st.line_chart(runs_by_date)

# График: Используемые билд-системы
st.subheader("Build Tool Usage")
build_tool_counts = filtered_df["build_tool"].value_counts()
st.bar_chart(build_tool_counts)

# Таблица
st.subheader("Detailed Table")
st.dataframe(filtered_df)
