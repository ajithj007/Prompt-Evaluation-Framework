from dash import Dash, dcc, html
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

df = pd.read_csv('../data/results.csv')
app = Dash(__name__)

# Chart 1 - Overall comparison
avg_data = pd.DataFrame({
    'Prompt': ['Prompt A (Simple)', 'Prompt B (Detailed)'],
    'Average Score': [df['average_a'].mean(), df['average_b'].mean()]
})
fig_overall = px.bar(avg_data, x='Prompt', y='Average Score',
                     title='Overall Average Scores',
                     color='Prompt',
                     color_discrete_map={
                         'Prompt A (Simple)': '#3498db',
                         'Prompt B (Detailed)': '#e74c3c'
                     })
fig_overall.update_layout(yaxis_range=[0, 10])

# Chart 2 - Winner pie
winner_counts = df['winner'].value_counts().reset_index()
winner_counts.columns = ['Winner', 'Count']
winner_counts['Winner'] = winner_counts['Winner'].map({
    'A': 'Prompt A', 'B': 'Prompt B'
})
fig_winners = px.pie(winner_counts, values='Count', names='Winner',
                     title='Win Distribution',
                     color_discrete_sequence=['#3498db', '#e74c3c'])

# Chart 3 - Category comparison
cat_scores = df.groupby('category')[
    ['average_a', 'average_b']].mean().reset_index()
fig_category = go.Figure()
fig_category.add_trace(go.Bar(
    name='Prompt A', x=cat_scores['category'],
    y=cat_scores['average_a'], marker_color='#3498db'
))
fig_category.add_trace(go.Bar(
    name='Prompt B', x=cat_scores['category'],
    y=cat_scores['average_b'], marker_color='#e74c3c'
))
fig_category.update_layout(
    title='Scores by Category',
    barmode='group',
    yaxis_range=[0, 10]
)

# Chart 4 - Radar criteria
criteria = ['Relevance', 'Clarity', 'Completeness', 'Conciseness']
fig_criteria = go.Figure()
fig_criteria.add_trace(go.Scatterpolar(
    r=[df['relevance_a'].mean(), df['clarity_a'].mean(),
       df['completeness_a'].mean(), df['conciseness_a'].mean()],
    theta=criteria, fill='toself',
    name='Prompt A', line_color='#3498db'
))
fig_criteria.add_trace(go.Scatterpolar(
    r=[df['relevance_b'].mean(), df['clarity_b'].mean(),
       df['completeness_b'].mean(), df['conciseness_b'].mean()],
    theta=criteria, fill='toself',
    name='Prompt B', line_color='#e74c3c'
))
fig_criteria.update_layout(title='Criteria Comparison (Radar)')

# ── Layout ───────────────────────────────────────────
app.layout = html.Div([

    html.H1('Prompt Evaluation Framework',
            style={'textAlign': 'center', 'color': '#2c3e50',
                   'fontFamily': 'Arial'}),
    html.P('Automated A/B testing of AI prompts using Claude API',
           style={'textAlign': 'center', 'color': '#7f8c8d',
                  'fontFamily': 'Arial'}),
    html.Hr(),

    # Stat cards
    html.Div([
        html.Div([
            html.H3(f"{len(df)}",
                    style={'color': '#3498db', 'margin': 0}),
            html.P("Total Evaluations", style={'margin': 0})
        ], style={'textAlign': 'center', 'padding': '20px',
                  'background': '#ecf0f1', 'borderRadius': '10px',
                  'width': '22%'}),
        html.Div([
            html.H3(f"{df['average_a'].mean():.2f}",
                    style={'color': '#3498db', 'margin': 0}),
            html.P("Prompt A Avg Score", style={'margin': 0})
        ], style={'textAlign': 'center', 'padding': '20px',
                  'background': '#ecf0f1', 'borderRadius': '10px',
                  'width': '22%'}),
        html.Div([
            html.H3(f"{df['average_b'].mean():.2f}",
                    style={'color': '#e74c3c', 'margin': 0}),
            html.P("Prompt B Avg Score", style={'margin': 0})
        ], style={'textAlign': 'center', 'padding': '20px',
                  'background': '#ecf0f1', 'borderRadius': '10px',
                  'width': '22%'}),
        html.Div([
            html.H3(f"{(df['winner']=='B').sum()}/{len(df)}",
                    style={'color': '#27ae60', 'margin': 0}),
            html.P("Detailed Prompt Wins", style={'margin': 0})
        ], style={'textAlign': 'center', 'padding': '20px',
                  'background': '#ecf0f1', 'borderRadius': '10px',
                  'width': '22%'}),
    ], style={'display': 'flex', 'justifyContent': 'space-around',
              'margin': '20px'}),

    # Charts row 1
    html.Div([
        dcc.Graph(figure=fig_overall, style={'width': '48%'}),
        dcc.Graph(figure=fig_winners, style={'width': '48%'})
    ], style={'display': 'flex', 'justifyContent': 'space-between',
              'margin': '20px'}),

    # Charts row 2
    html.Div([
        dcc.Graph(figure=fig_category, style={'width': '48%'}),
        dcc.Graph(figure=fig_criteria, style={'width': '48%'})
    ], style={'display': 'flex', 'justifyContent': 'space-between',
              'margin': '20px'}),

    html.Hr(),
    html.P('Built with Claude API + Plotly Dash | Prompt Evaluation Framework',
           style={'textAlign': 'center', 'color': '#bdc3c7',
                  'fontFamily': 'Arial'})
])

if __name__ == '__main__':
    app.run(debug=True)