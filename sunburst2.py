import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Bar: Lương theo giới", layout="wide")
st.title("💼 Biểu đồ Cột: Lương Khởi điểm theo Ngành và Giới tính")

@st.cache_data
def load_data():
    return pd.read_excel("education_career_success.xlsx")

df = load_data()

# Chọn giới tính
genders = df['Gender'].unique().tolist()
selected_genders = st.multiselect("Chọn giới tính để so sánh:", genders, default=genders)

filtered_df = df[df['Gender'].isin(selected_genders)]
salary_group = filtered_df.groupby(['Field_of_Study', 'Gender'])['Starting_Salary'].mean().reset_index()

fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(data=salary_group, x="Field_of_Study", y="Starting_Salary", hue="Gender", ax=ax)
ax.set_title("Lương khởi điểm trung bình theo ngành và giới tính")
ax.set_xticklabels(ax.get_xticklabels(), rotation=45)
ax.set_ylabel("Lương khởi điểm (VND)")
st.pyplot(fig)
