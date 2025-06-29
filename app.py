import pandas as pd
import numpy as np
import plotly.graph_objects as go
import dash
from dash import html, dcc
from dash.dependencies import Input, Output

# External Bootstrap stylesheet
external_stylesheets = [
    {
        'href': 'https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css',
        'rel': 'stylesheet',
        'integrity': 'sha384-MCw98/SFnGE8fJT3GXwEOngsV7Zt27NXFoaoApmYr81iuXoPkFOJwJ8ERdknLPMO',
        'crossorigin': 'anonymous'
    }
]

patient=pd.read_csv('IndividualDetails.csv')
Total_Cases=patient.shape[0]
active=patient[patient['current_status']=='Hospitalized'].shape[0]
recovered=patient[patient['current_status']=='Recovered'].shape[0]
Death=patient[patient['current_status']=='Deceased'].shape[0]


options = [
    {'label': 'All', 'value': 'All'},
    {'label': 'Hospitalized', 'value': 'Hospitalized'},
    {'label': 'Recovered', 'value': 'Recovered'},
    {'label': 'Deceased', 'value': 'Deceased'}
]



app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

box_style = {
    'border': '3px solid #007BFF',
    'margin': '15px',
    'width': '320px',
    'float': 'left',  # Aligns each box to the left
    'display': 'block',  # Ensures the box behaves like a block-level element
    'textAlign': 'center',
    'padding': '10px'  # Optional padding inside the box
}



app.layout = html.Div([
    html.H1("COVID-19 Monitoring and Analysis Tool", style={'color': '#8B0000', 'textAlign': 'center'}),

    # Row of cards
    html.Div([
        html.Div([
            html.Div([
                html.Div([
                    html.H2('Total Cases', className='card-title'),
                    html.H3(Total_Cases, className='card-text')
                ], className='card-body')
            ], className='card text-white bg-primary mb-3', style={'maxWidth': '250px'})
        ], className='col-md-3',style=box_style),

        html.Div([
            html.Div([
                html.Div([
                    html.H2('Recovered', className='card-title'),
                    html.H3(recovered, className='card-text')
                ], className='card-body')
            ], className='card text-white bg-success mb-3', style={'maxWidth': '18rem'})
        ], className='col-md-3',style=box_style),

        html.Div([
            html.Div([
                html.Div([
                    html.H2('Deaths', className='card-title'),
                    html.H3(Death, className='card-text')
                ], className='card-body')
            ], className='card text-white bg-danger mb-3', style={'maxWidth': '18rem'})
        ], className='col-md-3',style=box_style),

        html.Div([
            html.Div([
                html.Div([
                    html.H2('Active_Cases', className='card-title'),
                    html.H3(active, className='card-text')
                ], className='card-body')
            ], className='card text-white bg-warning mb-3', style={'maxWidth': '18rem'})
        ], className='col-md-3',style=box_style)
    ], className='d-flex flex-row flex-nowrap justify-content-center'),

    html.Div([]),
    html.Div([
        html.Div([
            html.Div([
                html.Div([
                    dcc.Dropdown(id='click',options=options,value='All'),
                    dcc.Graph(id='bar')
                ],className='card-body')
            ],className='card')
        ],className='col-md-12')
    ], className='row')
], className='container')

@app.callback(Output('bar','figure'),[Input('click','value')])
def Draw_graph(type):
    if type=='All':
        pbar=patient['detected_state'].value_counts().reset_index()
        return {
            'data':[go.Bar(x=pbar['detected_state'],y=pbar['count'])],
            'layout':go.Layout(title='State Total Count')
        }
    else:
        nplt=patient[patient['current_status']==type]
        pbar=nplt['detected_state'].value_counts().reset_index()
        return {
            'data':[go.Bar(x=pbar['detected_state'],y=pbar['count'])],
            'layout':go.Layout(title='State Total Count')
        }
    


if __name__ == '__main__':
    app.run(debug=True)
