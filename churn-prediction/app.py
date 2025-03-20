from flask import Flask, render_template, request, jsonify
import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from models.ml_models import EnsembleChurnPredictor
from data.preprocessing import DataPreprocessor
from utils.visualization import (
    create_churn_distribution, create_feature_importance,
    create_model_performance_comparison, create_roc_curves,
    create_confusion_matrix, create_feature_distributions,
    create_correlation_matrix
)
import os

app = Flask(__name__)
dash_app = dash.Dash(__name__, server=app, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Initialize the model and preprocessor
model = EnsembleChurnPredictor()
preprocessor = DataPreprocessor()

# Load sample data (replace with your actual data loading logic)
sample_data = pd.DataFrame({
    'customer_id': range(1, 1001),
    'tenure': np.random.randint(0, 72, 1000),
    'monthly_charges': np.random.uniform(20, 100, 1000),
    'total_charges': np.random.uniform(100, 5000, 1000),
    'contract_type': np.random.choice(['Month-to-month', 'One year', 'Two year'], 1000),
    'payment_method': np.random.choice(['Electronic check', 'Mailed check', 'Bank transfer', 'Credit card'], 1000),
    'churn': np.random.choice([0, 1], 1000, p=[0.7, 0.3])
})

# Train the model
features = ['tenure', 'monthly_charges', 'contract_type', 'payment_method']
X = sample_data[features]
y = sample_data['churn']
model.fit(X, y)

# Dash layout
dash_app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.H1("Advanced Churn Prediction Dashboard", className="text-center my-4"), width=12)
    ]),
    
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Churn Distribution"),
                dbc.CardBody([
                    dcc.Graph(id='churn-distribution')
                ])
            ])
        ], width=6),
        
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Feature Importance"),
                dbc.CardBody([
                    dcc.Graph(id='feature-importance')
                ])
            ])
        ], width=6)
    ], className="mb-4"),
    
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Model Performance"),
                dbc.CardBody([
                    dcc.Graph(id='model-performance')
                ])
            ])
        ], width=6),
        
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("ROC Curves"),
                dbc.CardBody([
                    dcc.Graph(id='roc-curves')
                ])
            ])
        ], width=6)
    ], className="mb-4"),
    
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Confusion Matrix"),
                dbc.CardBody([
                    dcc.Graph(id='confusion-matrix')
                ])
            ])
        ], width=6),
        
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Feature Distributions"),
                dbc.CardBody([
                    dcc.Graph(id='feature-distributions')
                ])
            ])
        ], width=6)
    ], className="mb-4"),
    
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Feature Correlations"),
                dbc.CardBody([
                    dcc.Graph(id='correlation-matrix')
                ])
            ])
        ], width=12)
    ], className="mb-4"),
    
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Predict Churn"),
                dbc.CardBody([
                    dbc.Form([
                        dbc.Row([
                            dbc.Col([
                                dbc.Label("Tenure (months)"),
                                dbc.Input(id="tenure-input", type="number", value=12)
                            ], width=6),
                            dbc.Col([
                                dbc.Label("Monthly Charges"),
                                dbc.Input(id="monthly-charges-input", type="number", value=50)
                            ], width=6)
                        ]),
                        dbc.Row([
                            dbc.Col([
                                dbc.Label("Contract Type"),
                                dbc.Select(
                                    id="contract-type-input",
                                    options=[
                                        {"label": "Month-to-month", "value": "Month-to-month"},
                                        {"label": "One year", "value": "One year"},
                                        {"label": "Two year", "value": "Two year"}
                                    ],
                                    value="Month-to-month"
                                )
                            ], width=6),
                            dbc.Col([
                                dbc.Label("Payment Method"),
                                dbc.Select(
                                    id="payment-method-input",
                                    options=[
                                        {"label": "Electronic check", "value": "Electronic check"},
                                        {"label": "Mailed check", "value": "Mailed check"},
                                        {"label": "Bank transfer", "value": "Bank transfer"},
                                        {"label": "Credit card", "value": "Credit card"}
                                    ],
                                    value="Electronic check"
                                )
                            ], width=6)
                        ]),
                        dbc.Button("Predict", id="predict-button", color="primary", className="mt-3"),
                        html.Div(id="prediction-result", className="mt-3")
                    ])
                ])
            ])
        ], width=12)
    ])
], fluid=True)

# Dash callbacks
@dash_app.callback(
    Output('churn-distribution', 'figure'),
    Input('predict-button', 'n_clicks')
)
def update_churn_distribution(n_clicks):
    return create_churn_distribution(sample_data)

@dash_app.callback(
    Output('feature-importance', 'figure'),
    Input('predict-button', 'n_clicks')
)
def update_feature_importance(n_clicks):
    return create_feature_importance(sample_data, model)

@dash_app.callback(
    Output('model-performance', 'figure'),
    Input('predict-button', 'n_clicks')
)
def update_model_performance(n_clicks):
    performance = model.get_model_performance(X, y)
    return create_model_performance_comparison(performance)

@dash_app.callback(
    Output('roc-curves', 'figure'),
    Input('predict-button', 'n_clicks')
)
def update_roc_curves(n_clicks):
    return create_roc_curves(sample_data, model)

@dash_app.callback(
    Output('confusion-matrix', 'figure'),
    Input('predict-button', 'n_clicks')
)
def update_confusion_matrix(n_clicks):
    return create_confusion_matrix(sample_data, model)

@dash_app.callback(
    Output('feature-distributions', 'figure'),
    Input('predict-button', 'n_clicks')
)
def update_feature_distributions(n_clicks):
    return create_feature_distributions(sample_data)

@dash_app.callback(
    Output('correlation-matrix', 'figure'),
    Input('predict-button', 'n_clicks')
)
def update_correlation_matrix(n_clicks):
    return create_correlation_matrix(sample_data)

@dash_app.callback(
    Output('prediction-result', 'children'),
    Input('predict-button', 'n_clicks'),
    [Input('tenure-input', 'value'),
     Input('monthly-charges-input', 'value'),
     Input('contract-type-input', 'value'),
     Input('payment-method-input', 'value')]
)
def predict_churn(n_clicks, tenure, monthly_charges, contract_type, payment_method):
    if n_clicks is None:
        return ""
    
    # Create input data
    input_data = pd.DataFrame({
        'tenure': [tenure],
        'monthly_charges': [monthly_charges],
        'contract_type': [contract_type],
        'payment_method': [payment_method]
    })
    
    # Make prediction
    prediction = model.predict(input_data)
    probability = model.predict_proba(input_data)
    
    # Get individual model predictions
    model_predictions = {}
    for name, m in model.models.items():
        if name == 'neural_network':
            pred = (m.predict(input_data) > 0.5).astype(int)
        else:
            pred = m.predict(input_data)
        model_predictions[name] = pred[0]
    
    # Create detailed prediction result
    result = dbc.Card([
        dbc.CardHeader("Prediction Results"),
        dbc.CardBody([
            dbc.Alert(
                f"Ensemble Prediction: {'Likely to Churn' if prediction[0] == 1 else 'Likely to Stay'}\n"
                f"Probability: {probability[0]:.2%}",
                color="danger" if prediction[0] == 1 else "success",
                className="mb-3"
            ),
            html.H5("Individual Model Predictions:", className="mt-3"),
            html.Ul([
                html.Li(f"{name}: {'Churn' if pred == 1 else 'Stay'}")
                for name, pred in model_predictions.items()
            ])
        ])
    ])
    
    return result

# Flask routes
@app.route('/')
def index():
    return dash_app.index()

if __name__ == '__main__':
    app.run(debug=True) 