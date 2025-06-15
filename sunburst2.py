import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from scipy.stats import gaussian_kde
import numpy as np

st.set_page_config(page_title="Education Career Success", layout="wide")

# Custom background gradient & font
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif !important;
        color: #333;
        font-size: 15px;
    }

    .stApp {
        background: linear-gradient(to right, #fde2e4, #fad6a5);
        background-attachment: fixed;
    }

    .main-title {
        font-size: 40px;
        font-weight: 700;
        text-align: center;
        color: #a3471d;
        margin-bottom: 10px;
    }
    </style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    return pd.read_excel("education_career_success.xlsx")

df = load_data()

# Sidebar
st.sidebar.title("📊 Filters")

# Gender
gender_options = sorted(df['Gender'].dropna().unique())
selected_genders = st.sidebar.multiselect("Gender", gender_options, default=gender_options)

# Job Level
job_levels = sorted(df['Current_Job_Level'].dropna().unique())
selected_level = st.sidebar.selectbox("Job Level", job_levels)

# Age
min_age, max_age = int(df['Age'].min()), int(df['Age'].max())
age_range = st.sidebar.slider("Age Range", min_value=min_age, max_value=max_age, value=(min_age, max_age))

# Entrepreneurship
st.sidebar.markdown("Entrepreneurship")
show_yes = st.sidebar.checkbox("Yes", value=True)
show_no = st.sidebar.checkbox("No", value=True)
selected_statuses = []
if show_yes: selected_statuses.append("Yes")
if show_no: selected_statuses.append("No")
if not selected_statuses:
    selected_statuses = ['Yes', 'No']
    st.sidebar.warning("⚠️ No status selected. Using all data.")

# Apply filters
filtered_df = df[
    (df['Gender'].isin(selected_genders)) &
    (df['Current_Job_Level'] == selected_level) &
    (df['Age'].between(age_range[0], age_range[1])) &
    (df['Entrepreneurship'].isin(selected_statuses))
]

# Tabs
tab1, tab2 = st.tabs(["📈 Demographics", "📊 Job Offers"])

# =====================
# TAB 1: Demographics
# =====================
with tab1:
    st.markdown("<div class='main-title'>EDUCATION CAREER SUCCESS</div>", unsafe_allow_html=True)
    st.subheader("Insight into success, powered by data.")
    st.write("Discover how different factors shape career paths—through interactive analytics.")

    chart_option = st.selectbox("Choose Visualization", ['Gender Distribution', 'Field of Study'])

    if filtered_df.empty:
        st.warning("⚠️ No data available with current filters.")
    else:
        col1, col2 = st.columns(2)

        with col1:
            # KDE plot
            fig_density = go.Figure()
            group_col = 'Gender' if chart_option == 'Gender Distribution' else 'Field_of_Study'
            for cat in filtered_df[group_col].dropna().unique():
                age_data = filtered_df[filtered_df[group_col] == cat]['Age']
                if len(age_data) > 1:
                    kde = gaussian_kde(age_data)
                    x_vals = np.linspace(age_range[0], age_range[1], 100)
                    y_vals = kde(x_vals)
                    fig_density.add_trace(go.Scatter(
                        x=x_vals, y=y_vals, mode='lines', name=str(cat), fill='tozeroy'
                    ))
            fig_density.update_layout(
                title=f"Age Distribution by {group_col}",
                xaxis_title="Age", yaxis_title="Density",
                paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)'
            )
            st.plotly_chart(fig_density, use_container_width=True)

        with col2:
            # Donut chart
            if chart_option == 'Gender Distribution':
                counts = filtered_df['Gender'].value_counts().reset_index()
                counts.columns = ['Gender', 'Count']
            else:
                counts = filtered_df['Field_of_Study'].value_counts().reset_index()
                counts.columns = ['Field of Study', 'Count']
            fig_donut = go.Figure(data=[go.Pie(labels=counts.iloc[:, 0], values=counts['Count'], hole=0.5)])
            fig_donut.update_layout(
                title=f"{chart_option} Distribution",
                paper_bgcolor='rgba(0,0,0,0)'
            )
            st.plotly_chart(fig_donut, use_container_width=True)

# =====================
# TAB 2: Job Offers
# =====================
with tab2:
    st.markdown("<div class='main-title'>📊 Job Offers</div>", unsafe_allow_html=True)

    if filtered_df.empty:
        st.warning("⚠️ No data to show.")
    else:
        color_map = {'Yes': '#FFD700', 'No': '#004080'}

        # Bar chart
        df_grouped = (
            df.groupby(['Current_Job_Level', 'Age', 'Entrepreneurship'])
            .size()
            .reset_index(name='Count')
        )
        df_grouped['Percentage'] = df_grouped.groupby(['Current_Job_Level', 'Age'])['Count'].transform(lambda x: x / x.sum())

        df_bar = df_grouped[
            (df_grouped['Current_Job_Level'] == selected_level) &
            (df_grouped['Age'].between(age_range[0], age_range[1])) &
            (df_grouped['Entrepreneurship'].isin(selected_statuses))
        ]

        fig_bar = px.bar(
            df_bar, x='Age', y='Percentage', color='Entrepreneurship',
            barmode='stack', color_discrete_map=color_map,
            title=f"Entrepreneurship by Age – {selected_level}"
        )
        fig_bar.update_layout(yaxis_tickformat=".0%", height=450)

        # Line chart
        df_avg_offers = (
            filtered_df.groupby(['Age', 'Entrepreneurship'])['Job_Offers']
            .mean().reset_index()
        )

        fig_line = go.Figure()
        for status in selected_statuses:
            data = df_avg_offers[df_avg_offers['Entrepreneurship'] == status]
            fig_line.add_trace(go.Scatter(
                x=data['Age'], y=data['Job_Offers'],
                mode='lines+markers', name=status,
                line=dict(color=color_map[status], width=2),
                marker=dict(size=6)
            ))
        fig_line.update_layout(
            title=f"Avg Job Offers by Age – {selected_level}",
            yaxis_title="Avg Offers", xaxis_title="Age", height=450
        )

        col1, col2 = st.columns(2)
        col1.plotly_chart(fig_bar, use_container_width=True)
        col2.plotly_chart(fig_line, use_container_width=True)
