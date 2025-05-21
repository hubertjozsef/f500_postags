import pandas as pd
import streamlit as st
import plotly.express as px

@st.cache_data
def load_data():
    df = pd.read_parquet("pos_tag_dist_by_domain.parquet")
    return df

df = load_data()

st.title("POS Tag Trends")

all_tags = sorted({tag for d in df['pos_tag_distribution'] for tag in d})
selected_tags = st.sidebar.multiselect("POS tags", all_tags, default=['NUM'])

sectors = sorted(df['sector'].dropna().unique())
selected_sectors = st.sidebar.multiselect("Sectors", sectors, default=sectors[:4])

df = df[df['sector'].isin(selected_sectors)]

for tag in selected_tags:
    df[tag] = df['pos_tag_distribution'].apply(lambda d: d.get(tag, 0))

agg = (
    df.groupby(['year_month', 'sector'])[selected_tags]
    .mean()
    .reset_index()
)

plot_df = agg.melt(id_vars=['year_month', 'sector'], var_name='pos_tag', value_name='pct')

fig = px.line(
    plot_df,
    x='year_month',
    y='pct',
    color='pos_tag',
    line_group='sector',
    facet_col='sector',
    facet_col_wrap=2,
    title="% of POS Tag by Sector"
)
fig.update_layout(yaxis_tickformat=".0%", height=600)

st.plotly_chart(fig, use_container_width=True)

