import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Load dữ liệu
@st.cache_data
def load_data():
    return pd.read_csv("education_career_success.csv")

df = load_data()

# Sidebar: chọn Job Level
job_levels_order = ['Entry', 'Mid', 'Senior', 'Executive']
selected_levels = st.sidebar.multiselect(
    "Select Job Levels to Display",
    options=job_levels_order + ["All"],
    default=["All"]
)

# Sidebar: slicer Age
min_age = int(df["Age"].min())
max_age = int(df["Age"].max())
age_range = st.sidebar.slider(
    "Select Age Range",
    min_value=min_age,
    max_value=max_age,
    value=(min_age, max_age)
)

# Lọc dữ liệu theo Age
df_filtered = df[df["Age"].between(age_range[0], age_range[1])]

# Tính trung bình Work-Life Balance theo Job Level và Age
avg_balance = (
    df_filtered.groupby(['Current_Job_Level', 'Age'])['Work_Life_Balance']
    .mean()
    .reset_index()
)

# Gán thứ tự Job Level để sắp xếp
avg_balance['Current_Job_Level'] = pd.Categorical(
    avg_balance['Current_Job_Level'],
    categories=job_levels_order,
    ordered=True
)

# Lọc theo Job Level nếu cần
if "All" not in selected_levels:
    avg_balance = avg_balance[avg_balance["Current_Job_Level"].isin(selected_levels)]

# Tạo biểu đồ
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

# Layout
fig.update_layout(
    title="Average Work-Life Balance by Age",
    xaxis_title="Age",
    yaxis_title="Average Work-Life Balance",
    height=600,
    width=900,
    title_x=0.5,
    legend_title_text="Job Level",
    hovermode="x unified",
    xaxis=dict(
        showspikes=True,
        spikemode="across",
        spikesnap="cursor",
        spikedash="dot",
        spikethickness=1,
        spikecolor="gray"
    ),
    yaxis=dict(
        showspikes=True,
        spikemode="across",
        spikesnap="cursor",
        spikethickness=1,
        spikecolor="gray"
    )
)

# Hiển thị biểu đồ
st.plotly_chart(fig, use_container_width=True)
