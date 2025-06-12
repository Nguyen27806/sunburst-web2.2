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

# Filter data based on selected genders
df = df[df['Gender'].isin(selected_genders)]

# Grouping
df_grouped = (
    df.groupby(['Entrepreneurship', 'Age', 'Current_Job_Level'])
      .size()
      .reset_index(name='Count')
)
df_grouped['Percentage'] = df_grouped.groupby(['Entrepreneurship', 'Age'])['Count'].transform(lambda x: x / x.sum())

# === Replace Job Level Filter with Entrepreneurship Filter ===
entre_options = ['Yes', 'No']
selected_status = st.sidebar.selectbox("Select Entrepreneurship Status", entre_options)

# Age filter
min_age, max_age = int(df_grouped['Age'].min()), int(df_grouped['Age'].max())
age_range = st.sidebar.slider("Select Age Range", min_value=min_age, max_value=max_age, value=(min_age, max_age))

# Final filtered dataset
filtered = df_grouped[
    (df_grouped['Entrepreneurship'] == selected_status) &
    (df_grouped['Age'].between(age_range[0], age_range[1]))
]

def font_size_by_count(n):
    return {1: 20, 2: 18, 3: 16, 4: 14, 5: 12, 6: 11, 7: 10, 8: 9, 9: 8, 10: 7}.get(n, 6)

color_map = {'Yes': '#FFD700', 'No': '#004080'}

if filtered.empty:
    st.write(f"### No data available for entrepreneurship = {selected_status}.")
else:
    ages = sorted(filtered['Age'].unique())
    font_size = font_size_by_count(len(ages))
    chart_width = max(400, min(1200, 50 * len(ages) + 100))

    # ===== Bar chart: Percentage =====
    fig_bar = px.bar(
        filtered,
        x='Age',
        y='Percentage',
        color='Current_Job_Level',
        barmode='stack',
        color_discrete_sequence=px.colors.qualitative.Set2,
        category_orders={'Age': ages},
        labels={'Age': 'Age', 'Percentage': 'Percentage'},
        height=400,
        width=chart_width,
        title=f"Entrepreneurship: {selected_status} – Job Level Distribution by Age (%)"
    )

    for _, row in filtered.iterrows():
        if row['Percentage'] > 0:
            y_pos = 0.9
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
        legend_title_text='Job Level',
        xaxis_tickangle=90,
        bargap=0.1
    )
    fig_bar.update_yaxes(tickformat=".0%", title="Percentage")

    # ===== Area chart: Count =====
    fig_area = px.area(
        filtered,
        x='Age',
        y='Count',
        color='Current_Job_Level',
        markers=True,
        color_discrete_sequence=px.colors.qualitative.Set2,
        category_orders={'Age': ages},
        labels={'Age': 'Age', 'Count': 'Count'},
        height=400,
        width=chart_width,
        title=f"Entrepreneurship: {selected_status} – Job Level Distribution by Age (Count)"
    )
    fig_area.update_traces(line=dict(width=2), marker=dict(size=8))
    fig_area.update_layout(
        margin=dict(t=40, l=40, r=40, b=40),
        legend_title_text='Job Level',
        xaxis_tickangle=90
    )
    fig_area.update_yaxes(title="Count")

    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(fig_bar, use_container_width=True)
    with col2:
        st.plotly_chart(fig_area, use_container_width=True)
