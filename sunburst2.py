import streamlit as st
import pandas as pd
import plotly.express as px

# Sample data
data = {
    'Entrepreneurship': ['Yes', 'Yes', 'Yes', 'No', 'No', 'No'],
    'Field_of_Study': ['Engineering', 'Business', 'Arts', 'Engineering', 'Business', 'Arts'],
    'Salary_Group': ['High', 'Medium', 'Low', 'Medium', 'Low', 'Low'],
    'Count': [100, 80, 30, 60, 50, 40]
}

df = pd.DataFrame(data)

# Title
st.title("Sunburst Chart with Customizable Rings")

# Two dropdowns
include_field = st.selectbox(
    "Include Field of Study?",
    options=["Yes", "No"],
    index=0
)

include_salary = st.selectbox(
    "Include Salary Group?",
    options=["Yes", "No"],
    index=0
)

# Construct path based on choices
path = ['Entrepreneurship']
if include_field == "Yes":
    path.append('Field_of_Study')
if include_salary == "Yes":
    path.append('Salary_Group')

# Create sunburst chart
fig = px.sunburst(
    df,
    path=path,
    values='Count'
)

fig.update_traces(
    insidetextorientation='radial',
    branchvalues="total",
    textinfo='label+percent entry',
    hovertemplate="<b>%{label}</b><br>Value: %{value}<br>"
)

# Show chart
st.plotly_chart(fig, use_container_width=True)
