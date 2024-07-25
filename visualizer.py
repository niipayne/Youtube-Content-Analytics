import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

from dash.dependencies import Input, Output
from dash import Dash,html,dcc


def display():
    # Creating the app
    app = Dash(__name__)

    # Reading the data 
    df = pd.read_json('data.json')

    # Creating the chart
    fig = px.bar(df, x='published', 
                 y ='views',
                 hover_data=['title','duration'],
                 )
    
    fig.update_layout(
        xaxis_title= 'Published At',
        yaxis_title = 'Views',
        bargap = 0,
        clickmode = 'event+select'
         )

    app.layout = html.Div(
            dcc.Graph(
            id='graph',
            figure=fig
        )
    )


    app.run(debug = True)

