import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Thiết lập giao diện
st.set_page_config(page_title="Phân tích Hiệu suất & Thăng tiến", layout="wide")
st.title("📈 Dashboard: Hiệu suất cá nhân và Thăng tiến nghề nghiệp")

# Tải dữ liệu
@st.cache_data
def load_data():
    df = pd.read_excel("education_career_success.xlsx")
    return df

df = load_data()

# Sidebar: bộ lọc liên kết
st.sidebar.header("🔎 Bộ lọc dữ liệu")

# Lọc giới tính
genders = df["Gender"].dropna().unique().tolist()
selected_gender = st.sidebar.selectbox("Chọn giới tính:", ["Tất cả"] + genders)
if selected_gender != "Tất cả":
    df = df[df["Gender"] == selected_gender]

# Lọc ngành học
fields = df["Field_of_Study"].dropna().unique().tolist()
selected_fields = st.sidebar.multiselect("Chọn ngành học:", fields, default=fields)
df = df[df["Field_of_Study"].isin(selected_fields)]

# Lọc theo GPA
min_gpa, max_gpa = df["University_GPA"].min(), df["University_GPA"].max()
gpa_range = st.sidebar.slider("Khoảng điểm GPA đại học:", float(min_gpa), float(max_gpa),
                              (float(min_gpa), float(max_gpa)))
df = df[(df["University_GPA"] >= gpa_range[0]) & (df["University_GPA"] <= gpa_range[1])]

if df.empty:
    st.warning("⚠️ Không có dữ liệu phù hợp với bộ lọc.")
    st.stop()

# Biểu đồ 1: Violin plot - Years_to_Promotion theo ngành
st.subheader("🎻 Biểu đồ 1: Phân phối số năm để được thăng chức theo Ngành học")

fig1, ax1 = plt.subplots(figsize=(8, 4))
sns.violinplot(data=df, x="Field_of_Study", y="Years_to_Promotion", ax=ax1, inner="quart")
ax1.set_ylabel("Số năm thăng chức")
ax1.set_xlabel("Ngành học")
ax1.set_xticklabels(ax1.get_xticklabels(), rotation=45)
st.pyplot(fig1)

# Biểu đồ 2: Lineplot - Career Satisfaction theo Soft Skills Score
st.subheader("📈 Biểu đồ 2: Mức độ hài lòng nghề nghiệp theo điểm Kỹ năng mềm")

avg_satisfaction = df.groupby("Soft_Skills_Score")["Career_Satisfaction"].mean().reset_index()
fig2, ax2 = plt.subplots(figsize=(6, 4))
sns.lineplot(data=avg_satisfaction, x="Soft_Skills_Score", y="Career_Satisfaction", marker="o", ax=ax2)
ax2.set_xlabel("Soft Skills Score")
ax2.set_ylabel("Career Satisfaction (trung bình)")
st.pyplot(fig2)

# Biểu đồ 3: Boxplot - Starting Salary theo Job Level
st.subheader("💼 Biểu đồ 3: Lương khởi điểm theo cấp bậc công việc")

fig3, ax3 = plt.subplots(figsize=(6, 4))
sns.boxplot(data=df, x="Current_Job_Level", y="Starting_Salary", ax=ax3)
ax3.set_xlabel("Cấp bậc hiện tại")
ax3.set_ylabel("Lương khởi điểm (VND)")
st.pyplot(fig3)
