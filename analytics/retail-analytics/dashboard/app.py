import dash
from dash import html, dcc, Input, Output, State
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

# Initialize the Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Layout components
header = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Dashboard", href="#")),
        dbc.NavItem(dbc.NavLink("Documentação", href="#")),
    ],
    brand="Retail Analytics Dashboard",
    brand_href="#",
    color="primary",
    dark=True,
    className="mb-4",
)

# Sidebar
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
        html.Label("Loja"),
        dcc.Dropdown(
            id='store-dropdown',
            options=[
                {'label': 'Todas as Lojas', 'value': 'all'},
                {'label': 'Loja 1', 'value': 'store1'},
                {'label': 'Loja 2', 'value': 'store2'},
            ],
            value='all',
            className="mb-3"
        ),
        html.Label("Produto"),
        dcc.Dropdown(
            id='product-dropdown',
            options=[
                {'label': 'Todos os Produtos', 'value': 'all'},
                {'label': 'Produto 1', 'value': 'product1'},
                {'label': 'Produto 2', 'value': 'product2'},
            ],
            value='all',
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
                            html.H4("Vendas Totais", className="card-title"),
                            html.H2(id="total-sales", children="R$ 0,00"),
                        ],
                        body=True,
                        className="mb-3",
                    ),
                    width=3,
                ),
                dbc.Col(
                    dbc.Card(
                        [
                            html.H4("Ticket Médio", className="card-title"),
                            html.H2(id="average-ticket", children="R$ 0,00"),
                        ],
                        body=True,
                        className="mb-3",
                    ),
                    width=3,
                ),
                dbc.Col(
                    dbc.Card(
                        [
                            html.H4("Produtos Vendidos", className="card-title"),
                            html.H2(id="total-products", children="0"),
                        ],
                        body=True,
                        className="mb-3",
                    ),
                    width=3,
                ),
                dbc.Col(
                    dbc.Card(
                        [
                            html.H4("Clientes Atendidos", className="card-title"),
                            html.H2(id="total-customers", children="0"),
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
                            html.H4("Vendas por Período", className="card-title"),
                            dcc.Graph(id="sales-trend"),
                        ],
                        body=True,
                        className="mb-3",
                    ),
                    width=8,
                ),
                dbc.Col(
                    dbc.Card(
                        [
                            html.H4("Top Produtos", className="card-title"),
                            dcc.Graph(id="top-products"),
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
                            html.H4("Previsão de Demanda", className="card-title"),
                            dcc.Graph(id="demand-forecast"),
                        ],
                        body=True,
                        className="mb-3",
                    ),
                    width=12,
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
    [Output("total-sales", "children"),
     Output("average-ticket", "children"),
     Output("total-products", "children"),
     Output("total-customers", "children")],
    [Input("date-range", "start_date"),
     Input("date-range", "end_date"),
     Input("store-dropdown", "value"),
     Input("product-dropdown", "value")]
)
def update_summary_cards(start_date, end_date, store, product):
    # TODO: Implement API calls to get real data
    return "R$ 150.000,00", "R$ 150,00", "1.000", "1.000"

@app.callback(
    Output("sales-trend", "figure"),
    [Input("date-range", "start_date"),
     Input("date-range", "end_date"),
     Input("store-dropdown", "value"),
     Input("product-dropdown", "value")]
)
def update_sales_trend(start_date, end_date, store, product):
    # TODO: Implement API calls to get real data
    dates = pd.date_range(start=start_date, end=end_date, freq='D')
    values = np.random.normal(1000, 100, len(dates))
    fig = px.line(x=dates, y=values, title="Vendas por Dia")
    return fig

@app.callback(
    Output("top-products", "figure"),
    [Input("date-range", "start_date"),
     Input("date-range", "end_date"),
     Input("store-dropdown", "value"),
     Input("product-dropdown", "value")]
)
def update_top_products(start_date, end_date, store, product):
    # TODO: Implement API calls to get real data
    products = ['Produto 1', 'Produto 2', 'Produto 3', 'Produto 4', 'Produto 5']
    values = np.random.normal(100, 20, len(products))
    fig = px.bar(x=values, y=products, orientation='h', title="Top 5 Produtos")
    return fig

@app.callback(
    Output("demand-forecast", "figure"),
    [Input("date-range", "start_date"),
     Input("date-range", "end_date"),
     Input("store-dropdown", "value"),
     Input("product-dropdown", "value")]
)
def update_demand_forecast(start_date, end_date, store, product):
    # TODO: Implement API calls to get real data
    dates = pd.date_range(start=start_date, end=end_date, freq='D')
    actual = np.random.normal(1000, 100, len(dates))
    forecast = np.random.normal(1000, 100, len(dates))
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=dates, y=actual, name='Real'))
    fig.add_trace(go.Scatter(x=dates, y=forecast, name='Previsão'))
    fig.update_layout(title="Previsão de Demanda")
    return fig

if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port=8050, debug=True) 