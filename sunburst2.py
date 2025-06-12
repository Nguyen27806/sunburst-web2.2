import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Cấu hình trang
st.set_page_config(page_title="Dashboard: Education & Career", layout="wide")
st.title("📊 Dashboard Phân tích Giáo dục và Thành công Nghề nghiệp")

# Load dữ liệu
@st.cache_data
def load_data():
    df = pd.read_excel("education_career_success.xlsx")
    df['Ranking_Group'] = pd.cut(df['University_Ranking'], bins=[0, 200, 500, 1000],
                                 labels=['Top 200', '201–500', '501–1000'])
    df['Internship_Level'] = pd.cut(df['Internships_Completed'], bins=[-1, 1, 3, 10],
                                    labels=['Ít', 'Trung bình', 'Nhiều'])
    return df

df = load_data()

# Sidebar Filters
st.sidebar.header("🔧 Bộ lọc dữ liệu")

# Giới tính
genders = df['Gender'].dropna().unique().tolist()
selected_gender = st.sidebar.selectbox("Chọn giới tính:", ["Tất cả"] + genders)
if selected_gender != "Tất cả":
    df = df[df['Gender'] == selected_gender]

# Ngành học
fields = df['Field_of_Study'].dropna().unique().tolist()
selected_fields = st.sidebar.multiselect("Chọn ngành học:", fields, default=fields)
df = df[df['Field_of_Study'].isin(selected_fields)]

# University GPA filter
min_gpa, max_gpa = df['University_GPA'].min(), df['University_GPA'].max()
gpa_range = st.sidebar.slider("Khoảng điểm GPA đại học:", float(min_gpa), float(max_gpa),
                              (float(min_gpa), float(max_gpa)))
df = df[(df['University_GPA'] >= gpa_range[0]) & (df['University_GPA'] <= gpa_range[1])]

# Kiểm tra dữ liệu sau lọc
if df.empty:
    st.warning("⚠️ Không có dữ liệu phù hợp với bộ lọc.")
    st.stop()

# --- Biểu đồ 1: Scatter plot ---
st.subheader("📍 Biểu đồ 1: SAT Score vs University GPA")
fig1, ax1 = plt.subplots(figsize=(6, 4))
sns.scatterplot(data=df, x="SAT_Score", y="University_GPA", hue="Field_of_Study", ax=ax1)
ax1.set_xlabel("SAT Score")
ax1.set_ylabel("University GPA")
ax1.legend(title="Ngành học", bbox_to_anchor=(1.05, 1), loc='upper left')
st.pyplot(fig1)

# --- Biểu đồ 2: Bar chart ---
st.subheader("💼 Biểu đồ 2: Lương khởi điểm theo Ngành và Giới tính")
salary_group = df.groupby(['Field_of_Study', 'Gender'])['Starting_Salary'].mean().reset_index()
fig2, ax2 = plt.subplots(figsize=(6, 4))
sns.barplot(data=salary_group, x="Field_of_Study", y="Starting_Salary", hue="Gender", ax=ax2)
ax2.set_xticklabels(ax2.get_xticklabels(), rotation=45)
ax2.set_ylabel("Lương khởi điểm (VND)")
st.pyplot(fig2)

# --- Biểu đồ 3: Boxplot ---
st.subheader("📦 Biểu đồ 3: Job Offers theo Thứ hạng Trường và Thực tập")
fig3, ax3 = plt.subplots(figsize=(6, 4))
sns.boxplot(data=df, x='Ranking_Group', y='Job_Offers', hue='Internship_Level', ax=ax3)
ax3.set_xlabel("Thứ hạng Đại học")
ax3.set_ylabel("Số lời mời làm việc")
st.pyplot(fig3)
