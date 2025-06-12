import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import os

# Cài đặt trang
st.set_page_config(page_title="Work-Life Balance by Age", layout="centered")
st.title("💼 Work-Life Balance theo Age và Job Level")

# Tải dữ liệu an toàn
@st.cache_data
def load_data():
    file_path = "education_career_success.xlsx"
    if not os.path.exists(file_path):
        st.error(f"❌ File '{file_path}' không tồn tại. Vui lòng upload đúng file.")
        st.stop()
    return pd.read_excel(file_path)

df = load_data()

# Sidebar: chọn Job Level
job_levels_order = ['Entry', 'Mid', 'Senior', 'Executive']
selected_levels = st.sidebar.multiselect(
    "🎯 Chọn Job Level để hiển thị:",
    options=job_levels_order + ["All"],
    default=["All"]
)

# Sidebar: slicer chọn Age range
min_age = int(df["Age"].min())
max_age = int(df["Age"].max())
age_range = st.sidebar.slider(
    "📊 Chọn khoảng tuổi (Age):",
    min_value=min_age,
    max_value=max_age,
    value=(min_age, max_age)
)

# Lọc dữ liệu theo Age
df_filtered = df[df["Age"].between(age_range[0], age_range[1])]

# Tính trung bình Work-Life Balance theo Age và Job Level
avg_balance = (
    df_filtered.groupby(['Current_Job_Level', 'Age'])['Work_Life_Balance']
    .mean()
    .reset_index()
)

avg_balance['Current_Job_Level'] = pd.Categorical(
    avg_balance['Current_Job_Level'],
    categories=job_levels_order,
    ordered=True
)

# Lọc theo Job Level nếu không chọn All
if "All" not in selected_levels:
    avg_balance = avg_balance[avg_balance["Current_Job_Level"].isin(selected_levels)]

# Vẽ biểu đồ
fig = go.Figure()
colors = {
    "Entry": "#1f77b4",      # blue
    "Mid": "#ff7f0e",        # orange
    "Senior": "#2ca02c",     # green
    "Executive": "#d62728"   # red
}

for level in job_levels_order:
    if "All" in selected_levels or level in selected_levels:
        data_level = avg_balance[avg_balance["Current_Job_Level"] == level]
        if not data_level.empty:
            fig.add_trace(go.Scatter(
                x=data_level["Age"],
                y=data_level["Work_Life_Balance"],
                mode="lines+markers",
                name=level,
                line=dict(color=colors[level]),
                hovertemplate="%{y:.2f}<extra></extra>"
            ))

# Cấu hình layout
fig.update_layout(
    title="📈 Trung bình Work-Life Balance theo Age",
    xaxis_title="Age",
    yaxis_title="Work-Life Balance",
    height=600,
    width=900,
    title_x=0.5,
    legend_title_text="Job Level",
    hovermode="x unified",
    xaxis=dict(
        showspikes=True,
        spikemode="across",
        spikecolor="gray",
        spikedash="dot",
        spikesnap="cursor",
        spikethickness=1
    ),
    yaxis=dict(
        showspikes=True,
        spikemode="across",
        spikecolor="gray",
        spikedash="dot",
        spikesnap="cursor",
        spikethickness=1
    )
)

st.plotly_chart(fig, use_container_width=True)
