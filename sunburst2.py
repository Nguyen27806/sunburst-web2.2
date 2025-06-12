import streamlit as st
import pandas as pd
import plotly.express as px

# Load and preprocess data
df = pd.read_excel("education_career_success.xlsx", sheet_name=0)
df = df[df['Entrepreneurship'].isin(['Yes', 'No'])]

# Sidebar filters
st.sidebar.title("Filters")

# Gender filter
genders = sorted(df['Gender'].dropna().unique())
selected_genders = st.sidebar.multiselect("Select Gender", genders, default=genders)

# Filter data based on selected genders first
df = df[df['Gender'].isin(selected_genders)]

# Continue processing
df_grouped = (
    df.groupby(['Current_Job_Level', 'Age', 'Entrepreneurship'])
      .size()
      .reset_index(name='Count')
)
df_grouped['Percentage'] = df_grouped.groupby(['Current_Job_Level', 'Age'])['Count'].transform(lambda x: x / x.sum())

# Job level filter
job_levels = sorted(df_grouped['Current_Job_Level'].unique())
selected_level = st.sidebar.selectbox("Select Job Level (Bar/Area Charts)", job_levels)

# Age filter
min_age, max_age = int(df_grouped['Age'].min()), int(df_grouped['Age'].max())
age_range = st.sidebar.slider("Select Age Range", min_value=min_age, max_value=max_age, value=(min_age, max_age))

# Entrepreneurship filter
selected_statuses = st.sidebar.multiselect("Select Entrepreneurship Status", ['Yes', 'No'], default=['Yes', 'No'])

# Final filtered dataset
filtered = df_grouped[
    (df_grouped['Current_Job_Level'] == selected_level) &
    (df_grouped['Entrepreneurship'].isin(selected_statuses)) &
    (df_grouped['Age'].between(age_range[0], age_range[1]))
]

def font_size_by_count(n):
    return {1: 20, 2: 18, 3: 16, 4: 14, 5: 12, 6: 11, 7: 10, 8: 9, 9: 8, 10: 7}.get(n, 6)

color_map = {'Yes': '#FFD700', 'No': '#004080'}

if filtered.empty:
    st.write(f"### No data available for {selected_level} level.")
else:
    ages = sorted(filtered['Age'].unique())
    font_size = font_size_by_count(len(ages))
    chart_width = max(400, min(1200, 50 * len(ages) + 100))

    # Bar chart: Percentage
    fig_bar = px.bar(
        filtered,
        x='Age',
        y='Percentage',
        color='Entrepreneurship',
        barmode='stack',
        color_discrete_map=color_map,
        category_orders={'Entrepreneurship': ['No', 'Yes'], 'Age': ages},
        labels={'Age': 'Age', 'Percentage': 'Percentage'},
        height=400,
        width=chart_width,
        title=f"{selected_level} Level – Entrepreneurship by Age (%)"
    )

    for status in ['No', 'Yes']:
        for _, row in filtered[filtered['Entrepreneurship'] == status].iterrows():
            if row['Percentage'] > 0:
                y_pos = 0.2 if status == 'No' else 0.9
                fig_bar.add_annotation(
                    x=row['Age'],
                    y=y_pos,
                    text=f"{row['Percentage']:.0%}",
                    showarrow=False,
                    font=dict(color="white", size=font_size),
                    xanchor="center",
                    yanchor="middle"
                )

    fig_bar.update_layout(
        margin=dict(t=40, l=40, r=40, b=40),
        legend_title_text='Entrepreneurship',
        xaxis_tickangle=90,
        bargap=0.1
    )
    fig_bar.update_yaxes(tickformat=".0%", title="Percentage")

    # Area chart: Count
    fig_area = px.area(
        filtered,
        x='Age',
        y='Count',
        color='Entrepreneurship',
        markers=True,
        color_discrete_map=color_map,
        category_orders={'Entrepreneurship': ['No', 'Yes'], 'Age': ages},
        labels={'Age': 'Age', 'Count': 'Count'},
        height=400,
        width=chart_width,
        title=f"{selected_level} Level – Entrepreneurship by Age (Count)"
    )
    fig_area.update_traces(line=dict(width=2), marker=dict(size=8))
    fig_area.update_layout(
        margin=dict(t=40, l=40, r=40, b=40),
        legend_title_text='Entrepreneurship',
        xaxis_tickangle=90
    )
    fig_area.update_yaxes(title="Count")

    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(fig_bar, use_container_width=True)
    with col2:
        st.plotly_chart(fig_area, use_container_width=True)


