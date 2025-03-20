from flask import Flask, render_template, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
import pm4py
import plotly.express as px
import plotly.graph_objects as go
import rpy2.robjects as robjects
import os
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///process_analytics.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Models
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))

class ProcessLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    case_id = db.Column(db.String(50))
    activity = db.Column(db.String(100))
    timestamp = db.Column(db.DateTime)
    resource = db.Column(db.String(100))
    duration = db.Column(db.Float)

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

@app.route('/process-mining')
@login_required
def process_mining():
    return render_template('process_mining.html')

@app.route('/ml-analysis')
@login_required
def ml_analysis():
    return render_template('ml_analysis.html')

@app.route('/six-sigma')
@login_required
def six_sigma():
    return render_template('six_sigma.html')

# API Endpoints
@app.route('/api/process-metrics')
@login_required
def get_process_metrics():
    # Sample data - Replace with actual data from database
    metrics = {
        'throughput_time': 45.2,
        'cycle_time': 38.5,
        'bottleneck': 'Negociação',
        'efficiency': 85.3,
        'sigma_level': 4.2
    }
    return jsonify(metrics)

@app.route('/api/process-flow')
@login_required
def get_process_flow():
    # Generate process flow data using PM4PY
    log = pd.read_csv('data/process_log.csv')
    process_model = pm4py.discover_petri_net_inductive(log)
    return jsonify(process_model)

@app.route('/api/predictions')
@login_required
def get_predictions():
    # Sample ML predictions
    predictions = {
        'next_activity': 'Fechamento',
        'completion_probability': 0.85,
        'estimated_duration': 5.2
    }
    return jsonify(predictions)

@app.route('/api/six-sigma-metrics')
@login_required
def get_six_sigma_metrics():
    # Calculate Six Sigma metrics using R
    r = robjects.r
    r('''
        calculate_sigma <- function(data) {
            mean_val <- mean(data)
            sd_val <- sd(data)
            usl <- mean_val + 3*sd_val
            lsl <- mean_val - 3*sd_val
            cp <- (usl - lsl)/(6*sd_val)
            return(c(cp, mean_val, sd_val))
        }
    ''')
    
    # Sample data - Replace with actual data
    data = [45, 42, 48, 43, 46, 44, 47, 45, 43, 46]
    result = r.calculate_sigma(robjects.FloatVector(data))
    
    return jsonify({
        'cp': result[0],
        'mean': result[1],
        'sd': result[2]
    })

# Error handlers
@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True) 