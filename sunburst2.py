import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Boxplot: Job Offers", layout="wide")
st.title("📦 Biểu đồ Hộp: Job Offers theo Thứ hạng và Thực tập")

@st.cache_data
def load_data():
    return pd.read_excel("education_career_success.xlsx")

df = load_data()

# Nhóm thứ hạng và số thực tập
df['Ranking_Group'] = pd.cut(df['University_Ranking'], bins=[0, 200, 500, 1000],
                             labels=['Top 200', '201–500', '501–1000'])
df['Internship_Level'] = pd.cut(df['Internships_Completed'], bins=[-1, 1, 3, 10],
                                labels=['Ít', 'Trung bình', 'Nhiều'])

# Chọn nhóm thực tập
internship_levels = df['Internship_Level'].unique().tolist()
selected_levels = st.multiselect("Chọn cấp độ thực tập:", internship_levels, default=internship_levels)

filtered_df = df[df['Internship_Level'].isin(selected_levels)]

fig, ax = plt.subplots(figsize=(10, 6))
sns.boxplot(data=filtered_df, x='Ranking_Group', y='Job_Offers', hue='Internship_Level', ax=ax)
ax.set_title("Số lời mời làm việc theo Thứ hạng trường và số lần thực tập")
ax.set_xlabel("Nhóm Thứ hạng Đại học")
ax.set_ylabel("Số lời mời làm việc")
st.pyplot(fig)
