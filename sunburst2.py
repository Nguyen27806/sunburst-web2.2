import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.title("📊 Phân tích Giáo dục và Thành công Nghề nghiệp")

# Tải dữ liệu
@st.cache_data
def load_data():
    df = pd.read_excel("education_career_success.xlsx")
    return df

df = load_data()

# Biểu đồ 1: Scatter plot SAT vs University GPA, màu theo ngành học
st.header("Biểu đồ 1: SAT Score vs University GPA theo Ngành học")

fig1, ax1 = plt.subplots()
sns.scatterplot(data=df, x="SAT_Score", y="University_GPA", hue="Field_of_Study", ax=ax1)
ax1.set_xlabel("SAT Score")
ax1.set_ylabel("University GPA")
st.pyplot(fig1)

# Biểu đồ 2: Biểu đồ cột Starting Salary trung bình theo ngành và giới tính
st.header("Biểu đồ 2: Mức lương khởi điểm trung bình theo Ngành và Giới tính")

salary_group = df.groupby(['Field_of_Study', 'Gender'])['Starting_Salary'].mean().reset_index()
fig2, ax2 = plt.subplots(figsize=(10, 6))
sns.barplot(data=salary_group, x="Field_of_Study", y="Starting_Salary", hue="Gender", ax=ax2)
ax2.set_xticklabels(ax2.get_xticklabels(), rotation=45)
st.pyplot(fig2)

# Biểu đồ 3: Boxplot số Job Offers theo University Ranking nhóm và số Internship
st.header("Biểu đồ 3: Số lời mời làm việc theo Thứ hạng Trường và Số lần Thực tập")

# Nhóm University Ranking
df['Ranking_Group'] = pd.cut(df['University_Ranking'],
                             bins=[0, 200, 500, 1000],
                             labels=['Top 200', '201–500', '501–1000'])

# Nhóm số thực tập
df['Internship_Level'] = pd.cut(df['Internships_Completed'],
                                bins=[-1, 1, 3, 10],
                                labels=['Ít', 'Trung bình', 'Nhiều'])

fig3, ax3 = plt.subplots(figsize=(8, 6))
sns.boxplot(data=df, x='Ranking_Group', y='Job_Offers', hue='Internship_Level', ax=ax3)
ax3.set_xlabel("Nhóm Thứ hạng Đại học")
ax3.set_ylabel("Số lời mời làm việc")
st.pyplot(fig3)
