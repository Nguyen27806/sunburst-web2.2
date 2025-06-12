import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Entrepreneurship Analysis", layout="wide")

@st.cache_data
def load_data():
    return pd.read_excel("education_career_success.xlsx")

df = load_data()

st.title("📈 Entrepreneurship and Job Offers by Age")
st.markdown("Analyze the relationship between entrepreneurship status, job level, and job offers across age groups.")

# ==== Sidebar ====
st.sidebar.title("Filter Options")

gender_options = ['All'] + sorted(df['Gender'].dropna().unique())
selected_gender = st.sidebar.selectbox("Select Gender", gender_options)
if selected_gender != 'All':
    df = df[df['Gender'] == selected_gender]

job_levels = sorted(df['Current_Job_Level'].dropna().unique())
selected_level = st.sidebar.selectbox("Select Job Level", job_levels)

min_age, max_age = int(df['Age'].min()), int(df['Age'].max())
age_range = st.sidebar.slider("Select Age Range", min_value=min_age, max_value=max_age, value=(min_age, max_age))

entrepreneur_options = ['All', 'Yes', 'No']
selected_status = st.sidebar.selectbox("Select Entrepreneurship Status", entrepreneur_options)
selected_statuses = ['Yes', 'No'] if selected_status == 'All' else [selected_status]

color_map = {'Yes': '#FFD700', 'No': '#004080'}
chart_width = 1000  # tăng chiều ngang

# ==== Bar chart data ====
df_grouped = (
    df.groupby(['Current_Job_Level', 'Age', 'Entrepreneurship'])
    .size()
    .reset_index(name='Count')
)
df_grouped['Percentage'] = df_grouped.groupby(['Current_Job_Level', 'Age'])['Count'].transform(lambda x: x / x.sum())

df_bar = df_grouped[
    (df_grouped['Current_Job_Level'] == selected_level) &
    (df_grouped['Age'].between(age_range[0], age_range[1]))
]
if selected_status != 'All':
    df_bar = df_bar[df_bar['Entrepreneurship'] == selected_status]

sorted_ages = sorted(df_bar['Age'].unique())
even_ages = [x for x in sorted_ages if x % 2 == 0]

# ==== Bar chart ====
fig_bar = px.bar(
    df_bar,
    x='Age',
    y='Percentage',
    color='Entrepreneurship',
    barmode='stack',
    color_discrete_map=color_map,
    category_orders={'Entrepreneurship': ['No', 'Yes'], 'Age': sorted_ages},
    labels={'Age': 'Age', 'Percentage': 'Percentage'},
    height=450,
    width=chart_width,
    title=f"Entrepreneurship Distribution by Age – {selected_level} Level"
)

# ✅ Hiển thị phần trăm trong từng phần màu
for _, row in df_bar.iterrows():
    pct = row['Percentage']
    status = row['Entrepreneurship']
    age = row['Age']

    y_pos = pct * 0.85 if status == 'Yes' else pct / 2  # vàng thì cao hơn
    fig_bar.add_annotation(
        x=age,
        y=y_pos,
        text=f"{pct:.0%}",
        showarrow=False,
        font=dict(color="white", size=10),
        xanchor="center",
        yanchor="middle"
    )

# ✅ Legend cấu hình chung
legend_config = dict(
    orientation="h",
    yanchor="bottom",
    y=-0.3,
    xanchor="center",
    x=0.5,
    font=dict(size=12)
)

# ✅ Gom legend vào line chart, ẩn của bar
fig_bar.update_layout
