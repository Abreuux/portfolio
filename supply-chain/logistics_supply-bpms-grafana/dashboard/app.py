import dash
from dash import html, dcc, Input, Output, State
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import requests
import json
import os

# Initialize the Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# API configuration
API_URL = os.getenv('API_URL', 'http://localhost:8000')

# Layout components
header = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Dashboard", href="#")),
        dbc.NavItem(dbc.NavLink("Documentação", href="#")),
    ],
    brand="SupplyChainOptimizer Dashboard",
    brand_href="#",
    color="primary",
    dark=True,
    className="mb-4",
)

# Sidebar filters
sidebar = dbc.Card(
    [
        html.H4("Filtros", className="card-title"),
        html.Hr(),
        html.Label("Período"),
        dcc.DatePickerRange(
            id='date-range',
            start_date=datetime.now() - timedelta(days=30),
            end_date=datetime.now(),
            className="mb-3"
        ),
        html.Label("Centro de Distribuição"),
        dcc.Dropdown(
            id='warehouse-dropdown',
            options=[
                {'label': 'Todos os CDs', 'value': 'all'},
                {'label': 'CD 1', 'value': 'wh1'},
                {'label': 'CD 2', 'value': 'wh2'},
            ],
            value='all',
            className="mb-3"
        ),
        html.Label("Tipo de Análise"),
        dcc.Dropdown(
            id='analysis-type-dropdown',
            options=[
                {'label': 'Otimização de Rotas', 'value': 'routes'},
                {'label': 'Análise de Estoque', 'value': 'inventory'},
                {'label': 'Análise de Transporte', 'value': 'transportation'},
            ],
            value='routes',
            className="mb-3"
        ),
    ],
    body=True,
    className="mb-3",
)

# Main content
content = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(
                    dbc.Card(
                        [
                            html.H4("Custos Logísticos", className="card-title"),
                            html.H2(id="total-costs", children="R$ 0,00"),
                        ],
                        body=True,
                        className="mb-3",
                    ),
                    width=3,
                ),
                dbc.Col(
                    dbc.Card(
                        [
                            html.H4("Nível de Serviço", className="card-title"),
                            html.H2(id="service-level", children="0%"),
                        ],
                        body=True,
                        className="mb-3",
                    ),
                    width=3,
                ),
                dbc.Col(
                    dbc.Card(
                        [
                            html.H4("Utilização de Frota", className="card-title"),
                            html.H2(id="fleet-utilization", children="0%"),
                        ],
                        body=True,
                        className="mb-3",
                    ),
                    width=3,
                ),
                dbc.Col(
                    dbc.Card(
                        [
                            html.H4("Giro de Estoque", className="card-title"),
                            html.H2(id="inventory-turnover", children="0"),
                        ],
                        body=True,
                        className="mb-3",
                    ),
                    width=3,
                ),
            ],
            className="mb-4",
        ),
        dbc.Row(
            [
                dbc.Col(
                    dbc.Card(
                        [
                            html.H4("Mapa de Rotas", className="card-title"),
                            dcc.Graph(id="routes-map"),
                        ],
                        body=True,
                        className="mb-3",
                    ),
                    width=8,
                ),
                dbc.Col(
                    dbc.Card(
                        [
                            html.H4("Análise de Clusters", className="card-title"),
                            dcc.Graph(id="cluster-analysis"),
                        ],
                        body=True,
                        className="mb-3",
                    ),
                    width=4,
                ),
            ],
            className="mb-4",
        ),
        dbc.Row(
            [
                dbc.Col(
                    dbc.Card(
                        [
                            html.H4("Otimização de Estoque", className="card-title"),
                            dcc.Graph(id="inventory-optimization"),
                        ],
                        body=True,
                        className="mb-3",
                    ),
                    width=6,
                ),
                dbc.Col(
                    dbc.Card(
                        [
                            html.H4("Análise de Transporte", className="card-title"),
                            dcc.Graph(id="transportation-analysis"),
                        ],
                        body=True,
                        className="mb-3",
                    ),
                    width=6,
                ),
            ],
            className="mb-4",
        ),
    ],
    fluid=True,
)

# App layout
app.layout = dbc.Container(
    [
        header,
        dbc.Row(
            [
                dbc.Col(sidebar, width=3),
                dbc.Col(content, width=9),
            ],
        ),
    ],
    fluid=True,
)

# Callbacks
@app.callback(
    [Output("total-costs", "children"),
     Output("service-level", "children"),
     Output("fleet-utilization", "children"),
     Output("inventory-turnover", "children")],
    [Input("date-range", "start_date"),
     Input("date-range", "end_date"),
     Input("warehouse-dropdown", "value"),
     Input("analysis-type-dropdown", "value")]
)
def update_metrics(start_date, end_date, warehouse, analysis_type):
    # TODO: Implement API calls to get real metrics
    return "R$ 1.500.000,00", "95%", "85%", "4.5"

@app.callback(
    Output("routes-map", "figure"),
    [Input("date-range", "start_date"),
     Input("date-range", "end_date"),
     Input("warehouse-dropdown", "value")]
)
def update_routes_map(start_date, end_date, warehouse):
    # TODO: Implement API calls to get real route data
    # Sample data for demonstration
    locations = pd.DataFrame({
        'latitude': np.random.uniform(-23.5, -23.6, 10),
        'longitude': np.random.uniform(-46.6, -46.7, 10),
        'type': ['warehouse', 'customer', 'customer', 'customer', 'customer',
                'customer', 'customer', 'customer', 'customer', 'customer']
    })
    
    fig = px.scatter_mapbox(
        locations,
        lat='latitude',
        lon='longitude',
        color='type',
        mapbox_style="carto-positron",
        zoom=10
    )
    
    return fig

@app.callback(
    Output("cluster-analysis", "figure"),
    [Input("date-range", "start_date"),
     Input("date-range", "end_date"),
     Input("warehouse-dropdown", "value")]
)
def update_cluster_analysis(start_date, end_date, warehouse):
    # TODO: Implement API calls to get real cluster data
    # Sample data for demonstration
    data = pd.DataFrame({
        'x': np.random.normal(0, 1, 100),
        'y': np.random.normal(0, 1, 100),
        'cluster': np.random.choice(['A', 'B', 'C'], 100)
    })
    
    fig = px.scatter(data, x='x', y='y', color='cluster')
    return fig

@app.callback(
    Output("inventory-optimization", "figure"),
    [Input("date-range", "start_date"),
     Input("date-range", "end_date"),
     Input("warehouse-dropdown", "value")]
)
def update_inventory_optimization(start_date, end_date, warehouse):
    # TODO: Implement API calls to get real inventory data
    # Sample data for demonstration
    dates = pd.date_range(start=start_date, end=end_date, freq='D')
    data = pd.DataFrame({
        'date': dates,
        'inventory': np.random.normal(1000, 100, len(dates)),
        'optimal': np.random.normal(900, 50, len(dates))
    })
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data['date'], y=data['inventory'], name='Atual'))
    fig.add_trace(go.Scatter(x=data['date'], y=data['optimal'], name='Ótimo'))
    return fig

@app.callback(
    Output("transportation-analysis", "figure"),
    [Input("date-range", "start_date"),
     Input("date-range", "end_date"),
     Input("warehouse-dropdown", "value")]
)
def update_transportation_analysis(start_date, end_date, warehouse):
    # TODO: Implement API calls to get real transportation data
    # Sample data for demonstration
    routes = ['Rota 1', 'Rota 2', 'Rota 3', 'Rota 4', 'Rota 5']
    data = pd.DataFrame({
        'route': routes,
        'cost': np.random.uniform(1000, 5000, len(routes)),
        'distance': np.random.uniform(100, 500, len(routes))
    })
    
    fig = px.bar(data, x='route', y=['cost', 'distance'], barmode='group')
    return fig

if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port=8050, debug=True) 