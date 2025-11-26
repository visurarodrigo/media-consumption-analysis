import dash
from dash import html, dcc
import plotly.express as px
import pandas as pd

# --- Load data ---
df = pd.read_csv("data/raw/netflix_titles.csv")

# Top 10 genres
top_genres = (
    df['listed_in']
    .str.split(',')
    .explode()
    .str.strip()
    .value_counts()
    .head(10)
    .reset_index()
)
top_genres.columns = ['Genre', 'Count']

# Content added over time
yearly = (
    df['date_added']
    .dropna()
    .str.extract(r'(\d{4})')[0]
    .value_counts()
    .sort_index()
    .reset_index()
)
yearly.columns = ['Year', 'Count']

# --- Create figures ---
fig_genres = px.bar(
    top_genres,
    x='Count',
    y='Genre',
    orientation='h',
    title="Top 10 Genres",
    color='Count',
    color_continuous_scale='Blues'
)

fig_years = px.line(
    yearly,
    x='Year',
    y='Count',
    markers=True,
    title="Content Added Over Time"
)
fig_years.update_traces(line_color='#3498db')

# --- Load map HTML ---
with open(
    r"C:\Users\a12u\OneDrive\Desktop\Courses\IBM Data Science\Data Visualization with python\media-consumption-analysis\notebooks\images\netflix_map.html",
    "r",
    encoding="utf-8"
) as f:
    map_html = f.read()

# --- Build app ---
app = dash.Dash(__name__)
app.title = "Media Consumption Dashboard"

app.layout = html.Div([
    html.H1("Netflix Media Consumption Dashboard", style={"textAlign": "center"}),

    html.Div([
        html.H3("Top Genres"),
        dcc.Graph(figure=fig_genres)
    ], style={"width": "48%", "display": "inline-block", "verticalAlign": "top"}),

    html.Div([
        html.H3("Content Added Over Time"),
        dcc.Graph(figure=fig_years)
    ], style={"width": "48%", "display": "inline-block", "verticalAlign": "top"}),

    html.Div([
        html.H3("Geographic Distribution"),
        html.Iframe(srcDoc=map_html, width="100%", height="600")
    ], style={"marginTop": "40px"})
])

if __name__ == "__main__":
    app.run(debug=True)