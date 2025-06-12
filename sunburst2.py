import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# --- Cài đặt Streamlit
st.set_page_config(page_title="Liên kết 3 Biểu đồ", layout="wide")
st.title("📈 Dashboard Phân tích Sinh viên & Sự nghiệp (Liên kết 3 biểu đồ)")

# --- Tải dữ liệu
@st.cache_data
def load_data():
    df = pd.read_excel("education_career_success.xlsx")
    return df

df = load_data()

# --- Sidebar: Bộ lọc dùng chung ---
st.sidebar.header("🎛️ Bộ lọc dữ liệu")

# Giới tính
gender_options = df['Gender'].dropna().unique().tolist()
selected_gender = st.sidebar.selectbox("Chọn giới tính:", ["Tất cả"] + gender_options)
if selected_gender != "Tất cả":
    df = df[df["Gender"] == selected_gender]

# Ngành học
fields = df['Field_of_Study'].dropna().unique().tolist()
selected_fields = st.sidebar.multiselect("Chọn ngành học:", fields, default=fields)
df = df[df["Field_of_Study"].isin(selected_fields)]

# GPA filter
min_gpa, max_gpa = df["University_GPA"].min(), df["University_GPA"].max()
gpa_range = st.sidebar.slider("Chọn khoảng GPA đại học:", float(min_gpa), float(max_gpa),
                              (float(min_gpa), float(max_gpa)))
df = df[(df["University_GPA"] >= gpa_range[0]) & (df["University_GPA"] <= gpa_range[1])]

# Nếu không còn dữ liệu
if df.empty:
    st.warning("⚠️ Không có dữ liệu phù hợp.")
    st.stop()

# --- Plot 1: Pie chart ngành học ---
st.subheader("📊 Biểu đồ 1: Tỷ lệ sinh viên theo Ngành học")

field_counts = df["Field_of_Study"].value_counts()
fig1, ax1 = plt.subplots()
ax1.pie(field_counts, labels=field_counts.index, autopct="%1.1f%%", startangle=90)
ax1.axis("equal")
st.pyplot(fig1)

# --- Plot 2: Histogram điểm kỹ năng mềm ---
st.subheader("🧠 Biểu đồ 2: Phân phối điểm Kỹ năng mềm")

fig2, ax2 = plt.subplots()
sns.histplot(df["Soft_Skills_Score"], bins=10, kde=True, ax=ax2, color="skyblue")
ax2.set_xlabel("Soft Skills Score")
ax2.set_ylabel("Số lượng sinh viên")
st.pyplot(fig2)

# --- Plot 3: Scatter Networking Score vs Job Offers ---
st.subheader("🌐 Biểu đồ 3: Mối quan hệ Networking Score và Số Job Offers")

fig3, ax3 = plt.subplots()
sns.scatterplot(data=df, x="Networking_Score", y="Job_Offers", hue="Field_of_Study", ax=ax3)
ax3.set_xlabel("Networking Score")
ax3.set_ylabel("Số lời mời làm việc")
ax3.set_title("Liên hệ giữa Networking và Cơ hội nghề nghiệp")
st.pyplot(fig3)
