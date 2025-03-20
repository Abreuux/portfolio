import dash
from dash import html, dcc, callback, Input, Output, State
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize the Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Layout
app.layout = dbc.Container([
    # Header
    dbc.Row([
        dbc.Col([
            html.H1("Painel Corporativo", className="text-center mb-4"),
            html.Hr()
        ])
    ]),

    # Date Range Selector
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H5("Período", className="card-title"),
                    dcc.DatePickerRange(
                        id='date-range',
                        start_date=datetime.now() - timedelta(days=30),
                        end_date=datetime.now(),
                        display_format='DD/MM/YYYY'
                    )
                ])
            ])
        ], width=12)
    ], className="mb-4"),

    # KPI Cards
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H5("Receita Total", className="card-title"),
                    html.H2(id="total-revenue", className="text-success"),
                    html.P("+12.5% vs mês anterior", className="text-success")
                ])
            ])
        ], width=3),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H5("Novos Clientes", className="card-title"),
                    html.H2(id="new-customers", className="text-primary"),
                    html.P("+8.2% vs mês anterior", className="text-success")
                ])
            ])
        ], width=3),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H5("Tickets Suporte", className="card-title"),
                    html.H2(id="support-tickets", className="text-warning"),
                    html.P("-5.1% vs mês anterior", className="text-danger")
                ])
            ])
        ], width=3),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H5("Leads Ativos", className="card-title"),
                    html.H2(id="active-leads", className="text-info"),
                    html.P("+15.3% vs mês anterior", className="text-success")
                ])
            ])
        ], width=3)
    ], className="mb-4"),

    # Charts Row 1
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H5("Receita por Canal", className="card-title"),
                    dcc.Graph(id="revenue-by-channel")
                ])
            ])
        ], width=6),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H5("Desempenho de Campanhas", className="card-title"),
                    dcc.Graph(id="campaign-performance")
                ])
            ])
        ], width=6)
    ], className="mb-4"),

    # Charts Row 2
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H5("Tickets por Status", className="card-title"),
                    dcc.Graph(id="tickets-by-status")
                ])
            ])
        ], width=6),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H5("Leads por Origem", className="card-title"),
                    dcc.Graph(id="leads-by-source")
                ])
            ])
        ], width=6)
    ], className="mb-4"),

    # Data Table
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H5("Últimas Atividades", className="card-title"),
                    html.Div(id="recent-activities")
                ])
            ])
        ], width=12)
    ])
], fluid=True)

# Callbacks
@callback(
    [Output("revenue-by-channel", "figure"),
     Output("campaign-performance", "figure"),
     Output("tickets-by-status", "figure"),
     Output("leads-by-source", "figure")],
    [Input("date-range", "start_date"),
     Input("date-range", "end_date")]
)
def update_charts(start_date, end_date):
    # Sample data - Replace with actual data from your database
    revenue_data = pd.DataFrame({
        'channel': ['Stripe', 'Protheus', 'CRM', 'Intercom'],
        'revenue': [50000, 30000, 20000, 10000]
    })
    
    campaign_data = pd.DataFrame({
        'campaign': ['Facebook Ads', 'Google Ads', 'Email Marketing', 'Social Media'],
        'performance': [85, 92, 78, 88]
    })
    
    tickets_data = pd.DataFrame({
        'status': ['Aberto', 'Em Andamento', 'Resolvido', 'Fechado'],
        'count': [25, 15, 45, 10]
    })
    
    leads_data = pd.DataFrame({
        'source': ['Facebook', 'Google', 'CRM', 'Intercom'],
        'count': [150, 200, 100, 50]
    })

    # Create figures
    revenue_fig = px.pie(revenue_data, values='revenue', names='channel',
                        title='Receita por Canal')
    
    campaign_fig = px.bar(campaign_data, x='campaign', y='performance',
                         title='Desempenho de Campanhas')
    
    tickets_fig = px.pie(tickets_data, values='count', names='status',
                        title='Tickets por Status')
    
    leads_fig = px.bar(leads_data, x='source', y='count',
                      title='Leads por Origem')

    return revenue_fig, campaign_fig, tickets_fig, leads_fig

if __name__ == '__main__':
    app.run_server(debug=True) 