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

# Gender filter (with 'All')
gender_options = ['All'] + sorted(df['Gender'].dropna().unique())
selected_gender = st.sidebar.selectbox("Select Gender", gender_options)
if selected_gender != 'All':
    df = df[df['Gender'] == selected_gender]

# Job level filter
job_levels = sorted(df['Current_Job_Level'].dropna().unique())
selected_level = st.sidebar.selectbox("Select Job Level", job_levels)

# Age filter
min_age, max_age = int(df['Age'].min()), int(df['Age'].max())
age_range = st.sidebar.slider("Select Age Range", min_value=min_age, max_value=max_age, value=(min_age, max_age))

# Entrepreneurship filter (with 'All')
entrepreneur_options = ['All', 'Yes', 'No']
selected_status = st.sidebar.selectbox("Select Entrepreneurship Status", entrepreneur_options)

# Convert to list for filtering
selected_statuses = ['Yes', 'No'] if selected_status == 'All' else [selected_status]

# Color mapping
color_map = {'Yes': '#FFD700', 'No': '#004080'}

# Grouped data for percentage bar chart
df_grouped = (
    df.groupby(['Current_Job_Level', 'Age', 'Entrepreneurship'])
    .size()
    .reset_index(name='Count')
)
df_grouped['Percentage'] = df_grouped.groupby(['Current_Job_Level', 'Age'])['Count'].transform(lambda x: x / x.sum())

# Filter bar data
df_bar = df_grouped[
    (df_grouped['Current_Job_Level'] == selected_level) &
    (df_grouped['Age'].between(age_range[0], age_range[1]))
]
if selected_status != 'All':
    df_bar = df_bar[df_bar['Entrepreneurship'] == selected_status]

# Filter only even ages for ticks
even_ages = sorted(df_bar['Age'].unique())
even_ages = [age for age in even_ages if age % 2 == 0]

# Bar chart
fig_bar = px.bar(
    df_bar,
    x='Age',
    y='Percentage',
    color='Entrepreneurship',
    barmode='stack',
    color_discrete_map=color_map,
    category_orders={'Entrepreneurship': ['No', 'Yes'], 'Age': sorted(df_bar['Age'].unique())},
    labels={'Age': 'Age', 'Percentage': 'Percentage'},
    height=450,
    width=1250,
    title=f"Entrepreneurship Distribution by Age – {selected_level} Level"
)



fig_bar.update_traces(
    hovertemplate="Entrepreneurship=%{customdata[0]}<br>Age=%{x}<br>Percentage=%{y:.0%}<extra></extra>",
    customdata=df_bar[['Entrepreneurship']].values,
    hoverinfo="skip"
)

fig_bar.update_layout(
    margin=dict(t=40, l=40, r=40, b=40),
    legend_title_text='Entrepreneurship',
    xaxis_tickangle=0,
    bargap=0.1,
    xaxis=dict(tickvals=even_ages),
    yaxis=dict(title="Percentage", range=[0, 1], tickformat=".0%"),
    
    legend=dict(orientation='h', yanchor='bottom', y=-0.3, xanchor='center', x=0.5)
)

# Line chart: Average Job Offers
df_avg_offers = (
    df[(df['Current_Job_Level'] == selected_level) &
       (df['Entrepreneurship'].isin(selected_statuses)) &
       (df['Age'].between(age_range[0], age_range[1]))]
    .groupby(['Age', 'Entrepreneurship'])['Job_Offers']
    .mean()
    .reset_index()
)

fig_line = go.Figure()

for status in selected_statuses:  # ['Yes', 'No'] hoặc ['Yes'] hoặc ['No']
    data_status = df_avg_offers[df_avg_offers["Entrepreneurship"] == status]
    fig_line.add_trace(go.Scatter(
        x=data_status["Age"],
        y=data_status["Job_Offers"],
        mode="lines+markers",
        name=status,
        line=dict(color=color_map[status], width=2),
        marker=dict(size=6),
        hovertemplate="%{y:.2f}"  # chỉ hiện giá trị, tên và màu line sẽ auto hiện
    ))

fig_line.update_layout(
    margin=dict(t=40, l=40, r=40, b=40),
    legend_title_text='Entrepreneurship',
    xaxis_tickangle=0,
    hovermode="x unified",
    width=1250,
    xaxis=dict(
        showspikes=True,
        spikemode='across',  # vertical dash only
        spikesnap='cursor',
        spikethickness=1.2,
        spikedash='dot',
        tickvals=even_ages
    ),
    yaxis=dict(
        title="Average Job Offers",
        showspikes=True,
        spikemode='across',
        spikesnap='cursor',
        spikethickness=1.2,
        spikedash='dot'
    ),
    legend=dict(orientation='h', yanchor='bottom', y=-0.3, xanchor='center', x=0.5)
)

# Display charts
col1, col2 = st.columns(2)
with col1:
    st.plotly_chart(fig_bar, use_container_width=True)
with col2:
    st.plotly_chart(fig_line, use_container_width=True)
