import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Sunburst Chart", layout="centered")

st.title("📊 Sunburst Chart: Field → SAT → GPA → Job Offers")

# Đọc dữ liệu
df = pd.read_excel("education_career_success.xlsx")

# Nhóm điểm SAT
sat_bins = [0, 1000, 1200, 1400, 1600]
sat_labels = ["<1000", "1000–1199", "1200–1399", "1400+"]
df["SAT_Band"] = pd.cut(df["SAT_Score"], bins=sat_bins, labels=sat_labels)

# Nhóm GPA
gpa_bins = [0, 2.5, 3.0, 3.5, 4.0]
gpa_labels = ["<2.5", "2.5–3.0", "3.0–3.5", "3.5–4.0"]
df["GPA_Band"] = pd.cut(df["University_GPA"], bins=gpa_bins, labels=gpa_labels)

# Tạo biểu đồ sunburst
fig = px.sunburst(
    df,
    path=["Field_of_Study", "SAT_Band", "GPA_Band"],
    values="Job_Offers",
    title="Field of Study → SAT Band → GPA Band → Job Offers"
)
fig.update_traces(textinfo="label+percent parent")

st.plotly_chart(fig, use_container_width=True)