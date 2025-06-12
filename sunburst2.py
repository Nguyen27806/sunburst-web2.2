import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Entrepreneurship Analysis", layout="wide")

# ---------- Load data ----------
@st.cache_data
def load_data():
    return pd.read_excel("education_career_success.xlsx")

df = load_data()

# ---------- Sidebar filters ----------
st.sidebar.title("Filters")

gender_opts = ['All'] + sorted(df['Gender'].dropna().unique())
gender = st.sidebar.selectbox("Gender", gender_opts)
if gender != 'All':
    df = df[df['Gender'] == gender]

job_levels = sorted(df['Current_Job_Level'].dropna().unique())
job_level = st.sidebar.selectbox("Job Level", job_levels)

min_age, max_age = int(df['Age'].min()), int(df['Age'].max())
age_low, age_high = st.sidebar.slider("Age Range", min_age, max_age, (min_age, max_age))

entre_opts = ['All', 'Yes', 'No']
entre_status = st.sidebar.selectbox("Entrepreneurship Status", entre_opts)
status_list = ['Yes', 'No'] if entre_status == 'All' else [entre_status]

# ---------- Color / width ----------
color_map = {'Yes': '#FFD700', 'No': '#004080'}
chart_w = 1000

# ---------- Prepare bar-chart data ----------
grouped = (
    df.groupby(['Current_Job_Level', 'Age', 'Entrepreneurship'])
      .size()
      .reset_index(name='Count')
)
grouped['Percentage'] = grouped.groupby(['Current_Job_Level', 'Age'])['Count']\
                               .transform(lambda x: x / x.sum())

bar_df = grouped[
    (grouped['Current_Job_Level'] == job_level) &
    (grouped['Age'].between(age_low, age_high))
]
if entre_status != 'All':
    bar_df = bar_df[bar_df['Entrepreneurship'] == entre_status]

ages_sorted   = sorted(bar_df['Age'].unique())
ages_even     = [a for a in ages_sorted if a % 2 == 0]

# ---------- Bar chart ----------
fig_bar = px.bar(
    bar_df,
    x='Age', y='Percentage', color='Entrepreneurship',
    barmode='stack', color_discrete_map=color_map,
    category_orders={'Entrepreneurship': ['No', 'Yes'], 'Age': ages_sorted},
    width=chart_w, height=450,
    title=f"Entrepreneurship Distribution by Age – {job_level} Level",
    labels={'Percentage': 'Percentage'}
)

# Hide its legend & link legendgroup
fig_bar.update_traces(
    legendgroup=lambda t: t.name,
    showlegend=False
)

# Add % inside each segment
for _, r in bar_df.iterrows():
    pct = r['Percentage']
    if pct == 0:              # skip zero-height
        continue
    y_mid = pct/2 if r['Entrepreneurship'] == 'No' else pct*0.85
    fig_bar.add_annotation(
        x=r['Age'], y=y_mid,
        text=f"{pct:.0%}",
        showarrow=False,
        font=dict(color="white", size=10),
        xanchor="center", yanchor="middle"
    )

fig_bar.update_layout(
    margin=dict(t=45, l=40, r=40, b=80),
    bargap=0.1,
    legend_title_text='Entrepreneurship',
    xaxis=dict(tickmode='array', tickvals=ages_even, title="Age"),
    yaxis=dict(tickformat=".0%", title="Percentage")
)

# ---------- Line chart ----------
avg_offers = (
    df[(df['Current_Job_Level'] == job_level) &
       (df['Entrepreneurship'].isin(status_list)) &
       (df['Age'].between(age_low, age_high))]
    .groupby(['Age', 'Entrepreneurship'])['Job_Offers']
    .mean()
    .reset_index()
)

fig_line = go.Figure()

for status in status_list:
    sub = avg_offers[avg_offers['Entrepreneurship'] == status]
    fig_line.add_trace(go.Scatter(
        x=sub['Age'], y=sub['Job_Offers'],
        mode='lines+markers',
        name=status,
        legendgroup=status,           # 🔗 liên kết với bar
        marker=dict(size=6),
        line=dict(width=2),
        hovertemplate='Age: %{x}<br>Avg Job Offers: %{y:.2f}',
        line_color=color_map[status]
    ))

fig_line.update_layout(
    title="Average Job Offers by Age",
    width=chart_w, height=450,
    margin=dict(t=45, l=40, r=40, b=80),
    legend=dict(                     # legend duy nhất
        orientation="h", yanchor="bottom", xanchor="center",
        y=-0.3, x=0.5, font=dict(size=12)
    ),
    legend_title_text='Entrepreneurship',
    xaxis=dict(
        title="Age",
        tickmode='array',
        tickvals=ages_even,
        showspikes=True, spikemode='across',
        spikesnap='data', spikecolor='gray',
        spikethickness=1.2, spikedash='dot'
    ),
    yaxis=dict(title="Average Job Offers"),
    hovermode="closest",
    hoverlabel=dict(bgcolor="white", font_size=13, font_family="Arial")
)

# ---------- Display ----------
col1, col2 = st.columns(2)
with col1:
    st.plotly_chart(fig_bar, use_container_width=True)
with col2:
    st.plotly_chart(fig_line, use_container_width=True)
