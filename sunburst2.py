import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Entrepreneurship Analysis", layout="wide")

@st.cache_data
def load_data():
    return pd.read_excel("education_career_success.xlsx")

df = load_data()

st.title("\U0001F4C8 Entrepreneurship and Job Offers by Age")
st.markdown("Analyze the relationship between entrepreneurship status, job level, and job offers across age groups.")

st.sidebar.title("Filter Options")

# Sidebar filters
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

# Grouped data for bar chart
df_grouped = (
    df.groupby(['Current_Job_Level', 'Age', 'Entrepreneurship'])
    .size().reset_index(name='Count')
)
df_grouped['Percentage'] = df_grouped.groupby(['Current_Job_Level', 'Age'])['Count'].transform(lambda x: x / x.sum())

# Filtered for bar chart
df_bar = df_grouped[(df_grouped['Current_Job_Level'] == selected_level) &
                    (df_grouped['Age'].between(age_range[0], age_range[1]))]
if selected_status != 'All':
    df_bar = df_bar[df_bar['Entrepreneurship'] == selected_status]

# Bar chart (stacked)
fig_bar = px.bar(
    df_bar,
    x='Age',
    y='Percentage',
    color='Entrepreneurship',
    barmode='stack',
    color_discrete_map=color_map,
    category_orders={'Entrepreneurship': ['No', 'Yes'], 'Age': sorted(df_bar['Age'].unique())},
    height=500,
    width=800,
    title=f"Entrepreneurship Distribution by Age – {selected_level} Level"
)
# (Không dùng update_traces ở đây)

# Line chart
avg_offer_df = df[(df['Current_Job_Level'] == selected_level) &
                  (df['Entrepreneurship'].isin(selected_statuses)) &
                  (df['Age'].between(age_range[0], age_range[1]))]
df_avg_offers = avg_offer_df.groupby(['Age', 'Entrepreneurship'])['Job_Offers'].mean().reset_index()

fig_line = go.Figure()
for status in selected_statuses:
    df_line = df_avg_offers[df_avg_offers['Entrepreneurship'] == status]
    fig_line.add_trace(go.Scatter(
        x=df_line['Age'],
        y=df_line['Job_Offers'],
        mode='lines+markers',
        name=status,
        line=dict(color=color_map[status], width=2),
        hovertemplate='Age: %{x}<br>Avg Job Offers: %{y:.2f}<extra></extra>',
        legendgroup="Entrepreneurship"
    ))

fig_line.update_layout(
    height=500,
    width=800,
    title="Average Job Offers by Age",
    xaxis_title="Age",
    yaxis_title="Avg Job Offers",
    hovermode="x unified",
    showlegend=True,
    legend_title_text="Entrepreneurship"
)

col1, col2 = st.columns(2)
with col1:
    st.plotly_chart(fig_bar, use_container_width=True)
with col2:
    st.plotly_chart(fig_line, use_container_width=True)
