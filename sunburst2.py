import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from scipy.stats import gaussian_kde
import numpy as np

st.set_page_config(page_title="Entrepreneurship Insights", layout="wide")

# Global styles (instead of importing from utils)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif !important;
        color: #52504d;
        font-size: 15px;
    }

    .main-title {
        font-size: 32px;
        font-weight: 700;
        margin-bottom: 20px;
        color: #222;
    }

    .stApp {
        background-color: #f9f9f9;
    }
    </style>
""", unsafe_allow_html=True)

def local_css(file_name):
    with open(file_name) as f:
        st.markdown('<style>{}</style>'.format(f.read()), unsafe_allow_html=True)

# Optional: uncomment if you have a style file
# local_css("style/style.css")

@st.cache_data
def load_data():
    return pd.read_excel("education_career_success.xlsx")

df = load_data()

# Sidebar Filters
st.sidebar.title("Filters")
gender_options = sorted(df['Gender'].dropna().unique())
selected_genders = st.sidebar.multiselect("Select Gender(s)", gender_options, default=gender_options)

if not selected_genders:
    st.sidebar.warning("⚠️ No gender selected. Using full data. Please choose at least one option.")
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
    st.sidebar.warning(f"⚠️ Only one age ({age_range[0]}) selected. Using full age range.")
    age_range = (min_age, max_age)

st.sidebar.markdown("**Select Entrepreneurship Status**")
show_yes = st.sidebar.checkbox("Yes", value=True)
show_no = st.sidebar.checkbox("No", value=True)
selected_statuses = []
if show_yes:
    selected_statuses.append("Yes")
if show_no:
    selected_statuses.append("No")
if not selected_statuses:
    st.sidebar.warning("⚠️ No status selected. Using full data. Please choose at least one option.")
    selected_statuses = ['Yes', 'No']

color_map = {'Yes': '#FFD700', 'No': '#004080'}

graph_tab = st.tabs(["📈 Demographics", "📊 Job Offers"])

# === TAB 1: Demographics ===
with graph_tab[0]:
    st.markdown("""<h1 style='font-family: "Inter", sans-serif; color: #cf5a2e; font-size: 40px;'>📊 Demographics</h1>""", unsafe_allow_html=True)
    chart_option = st.selectbox("Select Variable for Visualization", ['Gender Distribution', 'Field of Study'])

    df_demo = gender_filtered[
        (gender_filtered['Current_Job_Level'] == selected_level) &
        (gender_filtered['Age'].between(age_range[0], age_range[1])) &
        (gender_filtered['Entrepreneurship'].isin(selected_statuses))
    ]

    if df_demo.empty:
        st.warning("⚠️ Not enough data to display charts. Please adjust the filters.")
    else:
        if chart_option == 'Gender Distribution':
            st.markdown("""<div style="border: 2px solid #cf5a2e; border-radius: 12px; padding: 20px; margin-bottom: 30px;">
                <div style="display: flex; justify-content: space-around; text-align: center;">
                    <div><div>Total Records</div><div style="font-size: 28px;">{}</div></div>
                    <div><div>Median Age</div><div style="font-size: 28px;">{:.1f}</div></div>
                    <div><div>% Female</div><div style="font-size: 28px;">{:.1f}%</div></div>
                </div></div>
            """.format(len(df_demo), df_demo['Age'].median(),
                       (df_demo['Gender'] == 'Female').mean() * 100),
                       unsafe_allow_html=True)
        else:
            top_fields = df_demo['Field_of_Study'].value_counts().head(3).index.tolist()
            display_fields = ", ".join(top_fields) if top_fields else "N/A"
            st.markdown("""<div style="border: 2px solid #cf5a2e; border-radius: 12px; padding: 20px; margin-bottom: 30px;">
                <div style="display: flex; justify-content: space-around; text-align: center;">
                    <div><div>Total Records</div><div style="font-size: 28px;">{}</div></div>
                    <div><div>Top 3 Fields</div><div style="font-size: 20px;">{}</div></div>
                </div></div>
            """.format(len(df_demo), display_fields),
            unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            fig_density = go.Figure()
            group_col = 'Gender' if chart_option == 'Gender Distribution' else 'Field_of_Study'
            title = f"Age Distribution by {group_col.replace('_', ' ')}"
            for cat in df_demo[group_col].dropna().unique():
                age_data = df_demo[df_demo[group_col] == cat]['Age']
                if len(age_data) > 1:
                    kde = gaussian_kde(age_data)
                    x_vals = np.linspace(age_range[0], age_range[1], 100)
                    y_vals = kde(x_vals)
                    fig_density.add_trace(go.Scatter(x=x_vals, y=y_vals, mode='lines', name=str(cat), fill='tozeroy'))

            fig_density.update_layout(
                title=title,
                xaxis_title="Age",
                yaxis_title="Density",
                height=500,
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)'
            )
            st.plotly_chart(fig_density, use_container_width=True)

        with col2:
            if chart_option == 'Gender Distribution':
                counts = df_demo['Gender'].value_counts().reset_index()
                counts.columns = ['Gender', 'Count']
            else:
                counts = df_demo['Field_of_Study'].value_counts().reset_index()
                counts.columns = ['Field of Study', 'Count']
            fig_donut = go.Figure(data=[go.Pie(labels=counts.iloc[:, 0], values=counts['Count'], hole=0.5)])
            fig_donut.update_layout(
                title=f"{chart_option} Distribution (Donut Chart)",
                height=350,
                paper_bgcolor='rgba(0,0,0,0)'
            )
            st.plotly_chart(fig_donut, use_container_width=True)

# === TAB 2: Job Offers ===
job_level_notes = {
    "Entry": "- Entrepreneurship increases slightly at age 21–23.",
    "Mid": "- Slight increases in participation around 21–23.",
    "Senior": "- Entrepreneurs more common at age 29.",
    "Executive": "- High entrepreneurship at ages 20–22."
}
job_offers_notes = {
    "Entry": "- More offers for entrepreneurs at ages 18, 26, 28.",
    "Mid": "- Peak at age 27 for entrepreneurs.",
    "Senior": "- Spikes at age 29 for entrepreneurs.",
    "Executive": "- Peak offers at age 27 for entrepreneurs."
}

with graph_tab[1]:
    st.markdown("""<h1 style='font-family: "Inter", sans-serif; color: #cf5a2e; font-size: 36px;'>Job Offers</h1>""", unsafe_allow_html=True)
    df_filtered = gender_filtered[
        (gender_filtered['Current_Job_Level'] == selected_level) &
        (gender_filtered['Age'].between(age_range[0], age_range[1])) &
        (gender_filtered['Entrepreneurship'].isin(selected_statuses))
    ]

    if df_filtered.empty:
        st.warning("⚠️ Not enough data to display charts. Please adjust the filters.")
    else:
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

        even_ages = sorted(df_bar['Age'].unique())
        even_ages = [age for age in even_ages if age % 2 == 0]

        fig_bar = px.bar(
            df_bar, x='Age', y='Percentage', color='Entrepreneurship',
            barmode='stack', color_discrete_map=color_map,
            title=f"Entrepreneurship Distribution by Age – {selected_level} Level",
            height=450
        )
        fig_bar.update_layout(
            yaxis=dict(title="Percentage", tickformat=".0%", range=[0, 1]),
            xaxis=dict(tickvals=even_ages),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
        )

        df_avg_offers = (
            df_filtered
            .groupby(['Age', 'Entrepreneurship'])['Job_Offers']
            .mean()
            .reset_index()
        )

        fig_line = go.Figure()
        for status in selected_statuses:
            data_status = df_avg_offers[df_avg_offers["Entrepreneurship"] == status]
            fig_line.add_trace(go.Scatter(
                x=data_status["Age"], y=data_status["Job_Offers"],
                mode="lines+markers", name=status,
                line=dict(color=color_map[status], width=2),
                marker=dict(size=6)
            ))
        fig_line.update_layout(
            title=f"Average Job Offers by Age – {selected_level} Level",
            yaxis_title="Average Job Offers",
            xaxis=dict(tickvals=even_ages),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)'
        )

        col1, col2 = st.columns(2)
        col1.plotly_chart(fig_bar, use_container_width=True)
        col2.plotly_chart(fig_line, use_container_width=True)

        # Notes
        note_style = """
        <div style="background-color:#fff4ec;border-left:6px solid #cf5a2e;padding:15px 20px;margin-top:20px;border-radius:8px;">
            <b>{title}</b><br>{text}
        </div>
        """
        col1.markdown(note_style.format(title="Entrepreneurship Note", text=job_level_notes.get(selected_level, "")), unsafe_allow_html=True)
        col2.markdown(note_style.format(title="Job Offers Note", text=job_offers_notes.get(selected_level, "")), unsafe_allow_html=True)
