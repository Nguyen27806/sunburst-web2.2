import streamlit as st
import pandas as pd
import plotly.express as px


st.set_page_config(
    page_title="Career Path Sunburst",
    layout="wide",
    page_icon="🌞"
)
st.title("🌞 Career Path Sunburst")


@st.cache_data
def load_data():
    return pd.read_excel("education_career_success.xlsx", sheet_name=0)

df = load_data()


def categorize_salary(salary):
    if salary < 30000:
        return '<30K'
    elif salary < 50000:
        return '30K–50K'
    elif salary < 70000:
        return '50K–70K'
    else:
        return '70K+'

df['Salary_Group'] = df['Starting_Salary'].apply(categorize_salary)


sunburst_data = df.groupby(['Entrepreneurship', 'Field_of_Study', 'Salary_Group']).size().reset_index(name='Count')
total_count = sunburst_data['Count'].sum()
sunburst_data['Percentage'] = (sunburst_data['Count'] / total_count * 100).round(2)


ent_totals = sunburst_data.groupby('Entrepreneurship')['Count'].sum()
sunburst_data['Ent_Label'] = sunburst_data['Entrepreneurship'].map(
    lambda x: f"{x}<br>{round(ent_totals[x] / total_count * 100, 2)}%"
)

field_totals = sunburst_data.groupby(['Entrepreneurship', 'Field_of_Study'])['Count'].sum()
sunburst_data['Field_Label'] = sunburst_data.apply(
    lambda row: f"{row['Field_of_Study']}<br>{round(field_totals[(row['Entrepreneurship'], row['Field_of_Study'])] / total_count * 100, 2)}%",
    axis=1
)

sunburst_data['Salary_Label'] = sunburst_data['Salary_Group'] + '<br>' + sunburst_data['Percentage'].astype(str) + '%'
sunburst_data['Ent_Field'] = sunburst_data['Entrepreneurship'] + " - " + sunburst_data['Field_of_Study']


yes_colors = {
    'Engineering': '#aedea7',
    'Business': '#dbf1d5',
    'Arts': '#0c7734',
    'Computer Science': '#73c375',
    'Medicine': '#00441b',
    'Law': '#f7fcf5',
    'Mathematics': '#37a055'
}

no_colors = {
    'Engineering': '#005b96',
    'Business': '#03396c',
    'Arts': '#009ac7',
    'Computer Science': '#8ed2ed',
    'Medicine': '#b3cde0',
    'Law': '#5dc4e1',
    'Mathematics': '#0a70a9'
}


color_map = {}
for field, color in yes_colors.items():
    color_map[f"Yes - {field}"] = color
for field, color in no_colors.items():
    color_map[f"No - {field}"] = color

color_map['Yes'] = '#ffd16a'
color_map['No'] = '#ffd16a'


fig = px.sunburst(
    sunburst_data,
    path=['Ent_Label', 'Field_Label', 'Salary_Label'],
    values='Count',
    color='Ent_Field',
    color_discrete_map=color_map,
    custom_data=['Percentage'],
    title='Career Path Insights: Education, Salary & Entrepreneurship'
)

fig.update_traces(
    insidetextorientation='radial',
    maxdepth=2,
    branchvalues="total",
    textinfo='label+text',
    hovertemplate=
            "<b>%{label}</b><br>" +
            "Value: %{value}<br>" 
)

fig.update_layout(
    width=500,
    height=500,
    margin=dict(t=50, l=0, r=0, b=0)
)


col1, col2 = st.columns([3, 1])

with col1:
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.markdown("### 💡 How to use")
    st.markdown(
        """
- The chart displays all three levels:  
    - Entrepreneurship (inner ring)  
    - Field of Study (middle ring)  
    - Salary Group (outer ring)  
- All labels include their percentage share (e.g., Engineering (20.1%))  
- Click on any segment to zoom in and explore deeper insights.
        """
    )
