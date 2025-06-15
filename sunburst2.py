import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from scipy.stats import gaussian_kde
import numpy as np

st.set_page_config(page_title="Entrepreneurship Insights", layout="wide")

# --- GLOBAL STYLES: nền pastel + toàn bộ chữ màu đen ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif !important;
        color: #000000 !important;
        font-size: 15px;
        background: linear-gradient(to right, #fde2e4, #fad6a5);
        background-attachment: fixed;
    }

    .main-title {
        font-size: 32px;
        font-weight: 700;
        margin-bottom: 20px;
        color: #000000 !important;
    }

    h1, h2, h3, h4, h5, h6, p, div, span {
        color: #000000 !important;
    }
    </style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    return pd.read_excel("education_career_success.xlsx")

df = load_data()

# --- SIDEBAR FILTERS ---
st.sidebar.title("Filters")

gender_options = sorted(df['Gender'].dropna().unique())
selected_genders = st.sidebar.multiselect("Select Gender(s)", gender_options, default=gender_options)

if not selected_genders:
    st.sidebar.warning("⚠️ No gender selected. Using full data.")
    gender_filtered = df
elif 'All' in selected_genders:
    gender_filtered = df
else:
    gender_filtered = df[df['Gender'].isin(selected_genders)]

job_levels = sorted(df['Current_Job_Level'].dropna().unique())
selected_level = st.sidebar.selectbox("Select Job Level", job_levels)

min_age, max_age = int(df['Age'].min()), int(df['Age'].max())
age_range = st.sidebar.slider("Select Age Range", min_value=min_age, max_value=max_age, value=(min_age, max_age))

if age_range[0] == age_range[1]:
    st.sidebar.warning(f"⚠️ Only one age ({age_range[0]}) selected. Using full range.")
    age_range = (min_age, max_age)

st.sidebar.markdown("**Entrepreneurship Status**")
show_yes = st.sidebar.checkbox("Yes", value=True)
show_no = st.sidebar.checkbox("No", value=True)

selected_statuses = []
if show_yes: selected_statuses.append("Yes")
if show_no: selected_statuses.append("No")
if not selected_statuses:
    st.sidebar.warning("⚠️ No status selected. Using all data.")
    selected_statuses = ['Yes', 'No']

color_map = {'Yes': '#FFD700', 'No': '#004080'}

# --- TABS ---
tab1, tab2 = st.tabs(["📈 Demographics", "📊 Job Offers"])

# === TAB 1 ===
with tab1:
    st.markdown("<h1 class='main-title'>📊 Demographics</h1>", unsafe_allow_html=True)
    chart_option = st.selectbox("Select Variable for Visualization", ['Gender Distribution', 'Field of Study'])

    df_demo = gender_filtered[
        (gender_filtered['Current_Job_Level'] == selected_level) &
        (gender_filtered['Age'].between(age_range[0], age_range[1])) &
        (gender_filtered['Entrepreneurship'].isin(selected_statuses))
    ]

    if df_demo.empty:
        st.warning("⚠️ No data to show.")
    else:
        if chart_option == 'Gender Distribution':
            female_percent = (df_demo['Gender'] == 'Female').mean() * 100
            st.markdown(f"""
                <div style="border: 2px solid #cf5a2e; border-radius: 12px; padding: 20px; margin-bottom: 30px;">
                    <div style="display: flex; justify-content: space-around; text-align: center;">
                        <div><div>Total Records</div><div style="font-size: 28px;">{len(df_demo)}</div></div>
                        <div><div>Median Age</div><div style="font-size: 28px;">{df_demo['Age'].median():.1f}</div></div>
                        <div><div>% Female</div><div style="font-size: 28px;">{female_percent:.1f}%</div></div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
        else:
            top_fields = df_demo['Field_of_Study'].value_counts().head(3).index.tolist()
            st.markdown(f"""
                <div style="border: 2px solid #cf5a2e; border-radius: 12px; padding: 20px; margin-bottom: 30px;">
                    <div style="display: flex; justify-content: space-around; text-align: center;">
                        <div><div>Total Records</div><div style="font-size: 28px;">{len(df_demo)}</div></div>
                        <div><div>Top 3 Fields</div><div style="font-size: 20px;">{", ".join(top_fields) if top_fields else "N/A"}</div></div>
                    </div>
                </div>
            """, unsafe_allow_html=True)

        col1, col2 = st.columns(2)

        with col1:
            group_col = 'Gender' if chart_option == 'Gender Distribution' else 'Field_of_Study'
            fig_density = go.Figure()
            for cat in df_demo[group_col].dropna().unique():
                age_data = df_demo[df_demo[group_col] == cat]['Age']
                if len(age_data) > 1:
                    kde = gaussian_kde(age_data)
                    x_vals = np.linspace(age_range[0], age_range[1], 100)
                    y_vals = kde(x_vals)
                    fig_density.add_trace(go.Scatter(x=x_vals, y=y_vals, mode='lines', name=cat, fill='tozeroy'))
            fig_density.update_layout(
                title=f"Age Distribution by {group_col}",
                xaxis_title="Age",
                yaxis_title="Density",
                height=500,
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)'
            )
            st.plotly_chart(fig_density, use_container_width=True)

        with col2:
            counts = df_demo[group_col].value_counts().reset_index()
            counts.columns = [group_col, 'Count']
            fig_donut = go.Figure(data=[go.Pie(labels=counts[group_col], values=counts['Count'], hole=0.5)])
            fig_donut.update_layout(
                title=f"{chart_option} Distribution",
                height=350,
                paper_bgcolor='rgba(0,0,0,0)'
            )
            st.plotly_chart(fig_donut, use_container_width=True)

# === TAB 2 ===
with tab2:
    st.markdown("<h1 class='main-title'>📊 Job Offers</h1>", unsafe_allow_html=True)

    df_filtered = gender_filtered[
        (gender_filtered['Current_Job_Level'] == selected_level) &
        (gender_filtered['Age'].between(age_range[0], age_range[1])) &
        (gender_filtered['Entrepreneurship'].isin(selected_statuses))
    ]

    if df_filtered.empty:
        st.warning("⚠️ No data to show.")
    else:
        df_grouped = (
            df.groupby(['Current_Job_Level', 'Age', 'Entrepreneurship'])
            .size().reset_index(name='Count')
        )
        df_grouped['Percentage'] = df_grouped.groupby(['Current_Job_Level', 'Age'])['Count'].transform(lambda x: x / x.sum())

        df_bar = df_grouped[
            (df_grouped['Current_Job_Level'] == selected_level) &
            (df_grouped['Age'].between(age_range[0], age_range[1])) &
            (df_grouped['Entrepreneurship'].isin(selected_statuses))
        ]

        df_avg = df_filtered.groupby(['Age', 'Entrepreneurship'])['Job_Offers'].mean().reset_index()

        fig_bar = px.bar(df_bar, x='Age', y='Percentage', color='Entrepreneurship', barmode='stack',
                         color_discrete_map=color_map, height=400,
                         title=f"Entrepreneurship by Age – {selected_level}")
        fig_bar.update_layout(yaxis_tickformat=".0%")

        fig_line = go.Figure()
        for status in selected_statuses:
            data = df_avg[df_avg['Entrepreneurship'] == status]
            fig_line.add_trace(go.Scatter(x=data['Age'], y=data['Job_Offers'],
                                          mode='lines+markers', name=status,
                                          line=dict(color=color_map[status], width=2)))
        fig_line.update_layout(title="Average Job Offers by Age", height=400,
                               yaxis_title="Avg Offers", xaxis_title="Age")

        col1, col2 = st.columns(2)
        col1.plotly_chart(fig_bar, use_container_width=True)
        col2.plotly_chart(fig_line, use_container_width=True)
