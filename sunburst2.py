import streamlit as st
import pandas as pd
import plotly.express as px

# Sample Data
data = {
    'Entrepreneurship': ['Yes', 'Yes', 'Yes', 'No', 'No', 'No'],
    'Field_of_Study': ['Engineering', 'Business', 'Arts', 'Engineering', 'Business', 'Arts'],
    'Salary_Group': ['High', 'Medium', 'Low', 'Medium', 'Low', 'Low'],
    'Count': [100, 80, 30, 60, 50, 40]
}

df = pd.DataFrame(data)

# Streamlit App
st.title("Sunburst Chart with Selectable Depth")

# Dropdown to choose level of depth
depth_option = st.selectbox(
    "Select depth level (how many rings to show):",
    options=[1, 2, 3],
    index=2,
    help="1 = Entrepreneurship only, 2 = +Field of Study, 3 = +Salary Group"
)

# Define levels dynamically based on selection
levels = ['Entrepreneurship', 'Field_of_Study', 'Salary_Group'][:depth_option]

# Create sunburst chart
fig = px.sunburst(
    df,
    path=levels,
    values='Count'
)

# Update trace settings
fig.update_traces(
    insidetextorientation='radial',
    maxdepth=depth_option,
    branchvalues="total",
    textinfo='label+percent entry',
    hovertemplate="<b>%{label}</b><br>Value: %{value}<br>"
)

# Show chart
st.plotly_chart(fig, use_container_width=True)
