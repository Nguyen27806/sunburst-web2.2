import pandas as pd
import plotly.express as px
import streamlit as st

st.title("Sunburst: Field of Study by Current Job Level")

uploaded_file = st.file_uploader("Upload Excel File", type=["xlsx"])
if uploaded_file is not None:
    df = pd.read_excel(uploaded_file, sheet_name="education_career_success")

    # Đếm số lượng theo cấp độ công việc và ngành học
    grouped = df.groupby(['Current_Job_Level', 'Field_of_Study']).size().reset_index(name='Count')

    # Tính tổng theo cấp độ công việc
    total_by_job_level = grouped.groupby('Current_Job_Level')['Count'].transform('sum')

    # Tính phần trăm ngành học trong mỗi cấp độ công việc
    grouped['Proportion'] = grouped['Count'] / total_by_job_level

    # Vẽ biểu đồ sunburst
    fig = px.sunburst(
        grouped,
        path=['Current_Job_Level', 'Field_of_Study'],
        values='Proportion',
        title='Tỉ lệ ngành học trong từng cấp độ công việc',
        color='Proportion',
        color_continuous_scale='Agsunset'
    )

    st.plotly_chart(fig)
