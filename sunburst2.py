import pandas as pd
import plotly.express as px
import streamlit as st

st.title("Sunburst: Field of Study by Current Job Level")

uploaded_file = st.file_uploader("Upload Excel File", type=["xlsx"])
if uploaded_file is not None:
    df = pd.read_excel(uploaded_file, sheet_name="education_career_success")

    # Bỏ các dòng thiếu dữ liệu
    df = df.dropna(subset=['Current_Job_Level', 'Field_of_Study'])

    # Đếm số lượng theo cấp độ công việc và ngành học
    grouped = df.groupby(['Current_Job_Level', 'Field_of_Study']).size().reset_index(name='Count')

    # Tính tổng trong mỗi cấp độ
    total_by_job_level = grouped.groupby('Current_Job_Level')['Count'].transform('sum')

    # Tính phần trăm
    grouped['Proportion'] = grouped['Count'] / total_by_job_level
    grouped['Percent_Label'] = (grouped['Proportion'] * 100).round(1).astype(str) + '%'

    # Tạo custom label để hiển thị rõ
    grouped['Label'] = grouped['Field_of_Study'] + ' (' + grouped['Percent_Label'] + ')'

    # Vẽ sunburst
    fig = px.sunburst(
        grouped,
        path=['Current_Job_Level', 'Label'],  # dùng label hiển thị phần trăm
        values='Proportion',
        title='Tỉ lệ ngành học trong từng cấp độ công việc',
        color='Proportion',
        color_continuous_scale='Blues'
    )

    fig.update_traces(insidetextorientation='radial')

    st.plotly_chart(fig)
