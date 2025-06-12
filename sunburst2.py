import streamlit as st
import pandas as pd
import plotly.express as px
import os

# Thiết lập giao diện
st.set_page_config(page_title="Entrepreneurship Heatmap", layout="centered")
st.title("🔥 Tỷ lệ Khởi nghiệp theo Tuổi và Giới tính")

# ===== Tải và xử lý dữ liệu =====
@st.cache_data
def load_data():
    file_path = "education_career_success.xlsx"
    if not os.path.exists(file_path):
        st.error(f"❌ Không tìm thấy file '{file_path}'. Vui lòng kiểm tra lại.")
        st.stop()
    df = pd.read_excel(file_path)
    df = df[df['Entrepreneurship'].isin(['Yes', 'No'])]
    df = df[df['Gender'].notna()]
    df['Age'] = df['Age'].round()  # gom nhóm tuổi cho heatmap dễ nhìn
    return df

df = load_data()

# ===== Sidebar chọn Entrepreneurship status =====
st.sidebar.header("🎯 Bộ lọc")
entre_choices = ['Yes', 'No']
selected_status = st.sidebar.selectbox("Chọn Trạng thái Khởi nghiệp", entre_choices, index=0)

# ===== Lọc dữ liệu theo Entrepreneurship =====
df_filtered = df[df['Entrepreneurship'] == selected_status]

# ===== Tính tỷ lệ giới tính theo Age trong nhóm Entrepreneurship =====
# (vẫn dùng cột Entrepreneurship là điều kiện lọc, còn heatmap sẽ phân bố theo Age & Gender)
heat_df = (
    df_filtered.groupby(['Age', 'Gender'])
    .size()
    .reset_index(name='Count')
)

# Tính tổng theo Age để lấy tỷ lệ từng giới trong từng nhóm tuổi
heat_df['Total'] = heat_df.groupby('Age')['Count'].transform('sum')
heat_df['Rate'] = heat_df['Count'] / heat_df['Total']

# ===== Vẽ biểu đồ heatmap =====
fig = px.density_heatmap(
    heat_df,
    x='Age',
    y='Gender',
    z='Rate',
    color_continuous_scale='Viridis',
    title=f"🔥 Tỷ lệ giới tính trong nhóm '{selected_status}' – theo Tuổi",
    labels={'Rate': 'Tỷ lệ'},
    height=400,
    width=600
)

fig.update_layout(
    margin=dict(t=50, l=40, r=40, b=40),
    xaxis_title="Tuổi",
    yaxis_title="Giới tính",
    coloraxis_colorbar=dict(title="Tỷ lệ", tickformat=".0%")
)

# ===== Hiển thị biểu đồ =====
st.plotly_chart(fig, use_container_width=True)
