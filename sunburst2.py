import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Cấu hình trang
st.set_page_config(page_title="SAT vs University GPA", layout="centered")
st.title("📍 Biểu đồ Scatter: SAT Score vs University GPA theo Ngành học")

# Tải dữ liệu từ file Excel
@st.cache_data
def load_data():
    return pd.read_excel("education_career_success.xlsx")

df = load_data()

# Danh sách các ngành học để chọn
fields = df['Field_of_Study'].dropna().unique().tolist()
fields.sort()

# Widget multiselect để người dùng chọn ngành hiển thị
selected_fields = st.multiselect("🎓 Chọn ngành học để hiển thị:", fields, default=fields[:5])

# Lọc dữ liệu theo lựa chọn
filtered_df = df[df['Field_of_Study'].isin(selected_fields)]

# Kiểm tra nếu không có ngành nào được chọn
if filtered_df.empty:
    st.warning("⚠️ Vui lòng chọn ít nhất một ngành để hiển thị biểu đồ.")
else:
    # Vẽ biểu đồ scatter
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.scatterplot(data=filtered_df, x="SAT_Score", y="University_GPA", hue="Field_of_Study", ax=ax)
    ax.set_title("Mối quan hệ giữa SAT Score và University GPA")
    ax.set_xlabel("SAT Score")
    ax.set_ylabel("University GPA")
    ax.legend(title="Ngành học", bbox_to_anchor=(1.05, 1), loc='upper left')
    st.pyplot(fig)
