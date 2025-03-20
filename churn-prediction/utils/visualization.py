import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from sklearn.metrics import roc_curve, auc, confusion_matrix
import seaborn as sns

def create_churn_distribution(data):
    """Create a pie chart showing the distribution of churn vs non-churn customers."""
    churn_counts = data['churn'].value_counts()
    
    fig = px.pie(
        values=churn_counts.values,
        names=['Retained', 'Churned'],
        title='Customer Churn Distribution',
        color_discrete_sequence=['#2ecc71', '#e74c3c']
    )
    
    fig.update_traces(textinfo='percent+label')
    return fig

def create_feature_importance(data, model):
    """Create a bar chart showing feature importance from multiple models."""
    features = ['tenure', 'monthly_charges', 'contract_type', 'payment_method']
    importance = model.get_feature_importance(data[features])
    
    fig = go.Figure(data=[
        go.Bar(
            x=features,
            y=importance,
            marker_color='#3498db'
        )
    ])
    
    fig.update_layout(
        title='Feature Importance (Ensemble)',
        xaxis_title='Features',
        yaxis_title='Importance Score',
        showlegend=False
    )
    
    return fig

def create_model_performance_comparison(performance):
    """Create a comparison chart of model performances."""
    models = list(performance.keys())
    metrics = ['accuracy', 'f1_score']
    
    fig = go.Figure()
    
    for metric in metrics:
        values = [performance[model][metric] for model in models]
        fig.add_trace(go.Bar(
            name=metric,
            x=models,
            y=values
        ))
    
    fig.update_layout(
        title='Model Performance Comparison',
        xaxis_title='Models',
        yaxis_title='Score',
        barmode='group'
    )
    
    return fig

def create_roc_curves(data, model):
    """Create ROC curves for all models."""
    features = ['tenure', 'monthly_charges', 'contract_type', 'payment_method']
    X = data[features]
    y = data['churn']
    
    fig = go.Figure()
    
    for name, m in model.models.items():
        if name == 'neural_network':
            y_pred_proba = m.predict(X)
        else:
            y_pred_proba = m.predict_proba(X)[:, 1]
        
        fpr, tpr, _ = roc_curve(y, y_pred_proba)
        roc_auc = auc(fpr, tpr)
        
        fig.add_trace(go.Scatter(
            x=fpr,
            y=tpr,
            name=f'{name} (AUC = {roc_auc:.2f})',
            mode='lines'
        ))
    
    fig.add_trace(go.Scatter(
        x=[0, 1],
        y=[0, 1],
        name='Random',
        mode='lines',
        line=dict(dash='dash')
    ))
    
    fig.update_layout(
        title='ROC Curves for All Models',
        xaxis_title='False Positive Rate',
        yaxis_title='True Positive Rate',
        showlegend=True
    )
    
    return fig

def create_confusion_matrix(data, model):
    """Create confusion matrix visualization."""
    features = ['tenure', 'monthly_charges', 'contract_type', 'payment_method']
    X = data[features]
    y = data['churn']
    
    y_pred = model.predict(X)
    cm = confusion_matrix(y, y_pred)
    
    fig = go.Figure(data=go.Heatmap(
        z=cm,
        x=['Predicted No', 'Predicted Yes'],
        y=['Actual No', 'Actual Yes'],
        colorscale='RdBu'
    ))
    
    fig.update_layout(
        title='Confusion Matrix (Ensemble)',
        xaxis_title='Predicted',
        yaxis_title='Actual'
    )
    
    return fig

def create_feature_distributions(data):
    """Create distribution plots for numerical features."""
    numerical_features = ['tenure', 'monthly_charges']
    
    fig = make_subplots(
        rows=1,
        cols=2,
        subplot_titles=[f'{feature} Distribution' for feature in numerical_features]
    )
    
    for i, feature in enumerate(numerical_features, 1):
        fig.add_trace(
            go.Histogram(
                x=data[feature],
                name=feature,
                nbinsx=30,
                showlegend=False
            ),
            row=1,
            col=i
        )
    
    fig.update_layout(
        title='Feature Distributions',
        showlegend=False,
        height=400
    )
    
    return fig

def create_correlation_matrix(data):
    """Create correlation matrix visualization."""
    numerical_features = ['tenure', 'monthly_charges', 'churn']
    corr_matrix = data[numerical_features].corr()
    
    fig = go.Figure(data=go.Heatmap(
        z=corr_matrix,
        x=corr_matrix.columns,
        y=corr_matrix.columns,
        colorscale='RdBu',
        zmid=0
    ))
    
    fig.update_layout(
        title='Feature Correlation Matrix',
        height=500
    )
    
    return fig

def create_tenure_vs_churn(data):
    """Create a box plot showing tenure distribution by churn status."""
    fig = px.box(
        data,
        x='churn',
        y='tenure',
        title='Tenure Distribution by Churn Status',
        color='churn',
        color_discrete_sequence=['#2ecc71', '#e74c3c']
    )
    
    fig.update_layout(
        xaxis_title='Churn Status',
        yaxis_title='Tenure (months)',
        showlegend=False
    )
    
    return fig

def create_monthly_charges_vs_churn(data):
    """Create a violin plot showing monthly charges distribution by churn status."""
    fig = px.violin(
        data,
        x='churn',
        y='monthly_charges',
        title='Monthly Charges Distribution by Churn Status',
        color='churn',
        color_discrete_sequence=['#2ecc71', '#e74c3c']
    )
    
    fig.update_layout(
        xaxis_title='Churn Status',
        yaxis_title='Monthly Charges ($)',
        showlegend=False
    )
    
    return fig 