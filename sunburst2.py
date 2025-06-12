import streamlit as st
import pandas as pd
import plotly.express as px

# Load Excel file
df = pd.read_excel("education_career_success.xlsx", sheet_name="education_career_success")

# Tạo Salary_Group theo phần ba lương
df_sunburst = df[['Entrepreneurship', 'Field_of_Study', 'Starting_Salary']].copy()
df_sunburst.dropna(subset=['Field_of_Study', 'Starting_Salary', 'Entrepreneurship'], inplace=True)

# Phân nhóm lương
df_sunburst['Salary_Group'] = pd.qcut(df_sunburst['Starting_Salary'], q=3, labels=['Low', 'Medium', 'High'])

# Tạo cột đếm (số lượng sinh viên theo nhóm)
df_sunburst['Count'] = 1

# UI
st.title("🌟 Sunburst Chart: Filter by Field of Study and Salary Group")

# Dropdown chọn ngành học
selected_fields = st.multiselect(
    "🎓 Select Field(s) of Study:",
    options=sorted(df_sunburst['Field_of_Study'].unique()),
    default=sorted(df_sunburst['Field_of_Study'].unique())
)

# Dropdown chọn mức lương
selected_salaries = st.multiselect(
    "💰 Select Salary Group(s):",
    options=['Low', 'Medium', 'High'],
    default=['Low', 'Medium', 'High']
)

# Lọc dữ liệu theo chọn lọc
filtered_df = df_sunburst[
    df_sunburst['Field_of_Study'].isin(selected_fields) &
    df_sunburst['Salary_Group'].isin(selected_salaries)
]

# Tạo biểu đồ sunburst
fig = px.sunburst(
    filtered_df,
    path=['Entrepreneurship', 'Field_of_Study', 'Salary_Group'],
    values='Count',
    color='Salary_Group',
    color_discrete_map={'Low': '#FF6961', 'Medium': '#FFD700', 'High': '#77DD77'}
)

fig.update_traces(
    insidetextorientation='radial',
    hovertemplate="<b>%{label}</b><br>Count: %{value}<br>"
)

st.plotly_chart(fig, use_container_width=True)
