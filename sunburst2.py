import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Scatter: SAT vs GPA", layout="centered")
st.title("📍 Biểu đồ Scatter: SAT Score vs University GPA")

@st.cache_data
def load_data():
    return pd.read_excel("education_career_success.xlsx")

df = load_data()

# Bộ lọc ngành học
fields = df['Field_of_Study'].unique().tolist()
selected_fields = st.multiselect("Chọn ngành để hiển thị:", fields, default=fields)

filtered_df = df[df['Field_of_Study'].isin(selected_fields)]

fig, ax = plt.subplots(figsize=(8, 6))
sns.scatterplot(data=filtered_df, x="SAT_Score", y="University_GPA", hue="Field_of_Study", ax=ax)
ax.set_title("Mối quan hệ giữa SAT Score và University GPA")
ax.set_xlabel("SAT Score")
ax.set_ylabel("University GPA")
st.pyplot(fig)
