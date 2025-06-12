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

st.title("Sunburst Chart: Filter by Field and Salary Group")

# Dropdown 1: Filter Field_of_Study
selected_fields = st.multiselect(
    "Select Field(s) of Study:",
    options=df['Field_of_Study'].unique(),
    default=df['Field_of_Study'].unique()
)

# Dropdown 2: Filter Salary_Group
selected_salaries = st.multiselect(
    "Select Salary Group(s):",
    options=df['Salary_Group'].unique(),
    default=df['Salary_Group'].unique()
)

# Filter dataframe based on selection
filtered_df = df[
    df['Field_of_Study'].isin(selected_fields) &
    df['Salary_Group'].isin(selected_salaries)
]

# Create sunburst chart
fig = px.sunburst(
    filtered_df,
    path=['Entrepreneurship', 'Field_of_Study', 'Salary_Group'],
    values='Count'
)

fig.update_traces(
    insidetextorientation='radial',
    branchvalues="total",
    textinfo='label+percent entry',
    hovertemplate="<b>%{label}</b><br>Value: %{value}<br>"
)

st.plotly_chart(fig, use_container_width=True)
