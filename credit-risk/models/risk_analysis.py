import pandas as pd
import numpy as np
from typing import List, Dict, Any, Tuple
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import roc_auc_score, precision_score, recall_score, f1_score
import xgboost as xgb
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.optimizers import Adam
from lifelines import CoxPHFitter
from sklearn.ensemble import IsolationForest
from sklearn.decomposition import PCA
import tensorflow as tf

class RiskAnalyzer:
    def __init__(self):
        self.models = {
            'random_forest': None,
            'gradient_boosting': None,
            'xgboost': None,
            'neural_network': None,
            'survival_analysis': None,
            'fraud_detection': None
        }
        self.scaler = StandardScaler()
        self.pca = PCA(n_components=0.95)
        
    def prepare_data(self, data: pd.DataFrame) -> Tuple[np.ndarray, np.ndarray]:
        """Prepare data for risk analysis"""
        # Handle missing values
        data = data.fillna(data.mean())
        
        # Scale features
        scaled_features = self.scaler.fit_transform(data)
        
        # Apply PCA for dimensionality reduction
        reduced_features = self.pca.fit_transform(scaled_features)
        
        return reduced_features
    
    def train_random_forest(self, X: np.ndarray, y: np.ndarray) -> None:
        """Train Random Forest model for credit scoring"""
        self.models['random_forest'] = RandomForestClassifier(
            n_estimators=100,
            max_depth=10,
            random_state=42
        )
        self.models['random_forest'].fit(X, y)
    
    def train_gradient_boosting(self, X: np.ndarray, y: np.ndarray) -> None:
        """Train Gradient Boosting model for credit scoring"""
        self.models['gradient_boosting'] = GradientBoostingClassifier(
            n_estimators=100,
            learning_rate=0.1,
            max_depth=5,
            random_state=42
        )
        self.models['gradient_boosting'].fit(X, y)
    
    def train_xgboost(self, X: np.ndarray, y: np.ndarray) -> None:
        """Train XGBoost model for credit scoring"""
        self.models['xgboost'] = xgb.XGBClassifier(
            objective='binary:logistic',
            n_estimators=100,
            learning_rate=0.1,
            max_depth=6,
            random_state=42
        )
        self.models['xgboost'].fit(X, y)
    
    def build_neural_network(self, input_shape: int) -> Sequential:
        """Build Neural Network model architecture"""
        model = Sequential([
            Dense(64, activation='relu', input_shape=(input_shape,)),
            Dropout(0.3),
            Dense(32, activation='relu'),
            Dropout(0.3),
            Dense(16, activation='relu'),
            Dense(1, activation='sigmoid')
        ])
        
        model.compile(
            optimizer=Adam(learning_rate=0.001),
            loss='binary_crossentropy',
            metrics=['accuracy']
        )
        
        return model
    
    def train_neural_network(self, X: np.ndarray, y: np.ndarray) -> None:
        """Train Neural Network model for credit scoring"""
        # Split data
        X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)
        
        # Build and train model
        self.models['neural_network'] = self.build_neural_network(X.shape[1])
        self.models['neural_network'].fit(
            X_train, y_train,
            validation_data=(X_val, y_val),
            epochs=50,
            batch_size=32,
            verbose=0
        )
    
    def train_survival_analysis(self, data: pd.DataFrame, duration_col: str, event_col: str) -> None:
        """Train Survival Analysis model for default prediction"""
        self.models['survival_analysis'] = CoxPHFitter()
        self.models['survival_analysis'].fit(
            data,
            duration_col=duration_col,
            event_col=event_col
        )
    
    def train_fraud_detection(self, X: np.ndarray) -> None:
        """Train Isolation Forest model for fraud detection"""
        self.models['fraud_detection'] = IsolationForest(
            contamination=0.1,
            random_state=42
        )
        self.models['fraud_detection'].fit(X)
    
    def predict_risk_score(self, model_type: str, X: np.ndarray) -> np.ndarray:
        """Generate risk scores using specified model"""
        if model_type not in self.models or self.models[model_type] is None:
            raise ValueError(f"Model {model_type} not trained")
        
        if model_type == 'neural_network':
            return self.models[model_type].predict(X)
        else:
            return self.models[model_type].predict_proba(X)[:, 1]
    
    def detect_fraud(self, X: np.ndarray) -> np.ndarray:
        """Detect fraudulent transactions"""
        if self.models['fraud_detection'] is None:
            raise ValueError("Fraud detection model not trained")
        
        return self.models['fraud_detection'].predict(X)
    
    def predict_survival(self, data: pd.DataFrame, duration: int) -> pd.DataFrame:
        """Predict survival probabilities"""
        if self.models['survival_analysis'] is None:
            raise ValueError("Survival analysis model not trained")
        
        return self.models['survival_analysis'].predict_survival_function(data, duration)
    
    def evaluate_model(self, model_type: str, X: np.ndarray, y: np.ndarray) -> Dict[str, float]:
        """Evaluate model performance"""
        if model_type not in self.models or self.models[model_type] is None:
            raise ValueError(f"Model {model_type} not trained")
        
        y_pred = self.predict_risk_score(model_type, X)
        
        metrics = {
            'roc_auc': roc_auc_score(y, y_pred),
            'precision': precision_score(y, y_pred > 0.5),
            'recall': recall_score(y, y_pred > 0.5),
            'f1': f1_score(y, y_pred > 0.5)
        }
        
        return metrics
    
    def ensemble_prediction(self, X: np.ndarray, weights: Dict[str, float] = None) -> np.ndarray:
        """Generate ensemble predictions using all trained models"""
        if weights is None:
            weights = {model: 1.0 for model in self.models if self.models[model] is not None}
        
        predictions = {}
        for model_type in self.models:
            if self.models[model_type] is not None:
                predictions[model_type] = self.predict_risk_score(model_type, X)
        
        # Weighted average of predictions
        ensemble_pred = np.zeros(X.shape[0])
        total_weight = sum(weights.values())
        
        for model_type, pred in predictions.items():
            ensemble_pred += weights[model_type] * pred
        
        return ensemble_pred / total_weight 