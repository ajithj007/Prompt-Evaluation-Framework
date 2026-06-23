import plotly.express as px
import pandas as pd
from dash import Dash, dcc, html
import plotly.express as px
import pandas as pd

app = Dash(__name__)

data = {
    'prompt_type': ['Creative', 'Technical', 'Creative', 'Technical'],
    'score': [8.5, 7.2, 9.1, 6.8]
}
df = pd.DataFrame(data)
fig = px.bar(df, x='prompt_type', y='score', title='Prompt Scores')

app.layout = html.Div([
    html.H1('Prompt Evaluation Dashboard'),
    dcc.Graph(figure=fig)
])

if __name__ == '__main__':
    app.run(debug=True)
