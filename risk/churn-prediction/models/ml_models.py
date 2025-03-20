import numpy as np
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier, VotingClassifier
from sklearn.svm import SVC
from sklearn.neural_networks import MLPClassifier
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import make_scorer, f1_score
import tensorflow as tf
from tensorflow.keras import layers, models
from sklearn.preprocessing import StandardScaler

class EnsembleChurnPredictor:
    def __init__(self):
        self.models = self._build_models()
        self.scaler = StandardScaler()
        self.best_model = None
        
    def _build_models(self):
        # Neural Network
        nn_model = models.Sequential([
            layers.Dense(128, activation='relu', input_shape=(10,)),
            layers.BatchNormalization(),
            layers.Dropout(0.4),
            layers.Dense(64, activation='relu'),
            layers.BatchNormalization(),
            layers.Dropout(0.4),
            layers.Dense(32, activation='relu'),
            layers.BatchNormalization(),
            layers.Dropout(0.4),
            layers.Dense(1, activation='sigmoid')
        ])
        
        nn_model.compile(
            optimizer='adam',
            loss='binary_crossentropy',
            metrics=['accuracy', tf.keras.metrics.AUC()]
        )
        
        # Traditional ML Models
        rf_model = RandomForestClassifier(
            n_estimators=100,
            max_depth=10,
            random_state=42
        )
        
        gb_model = GradientBoostingClassifier(
            n_estimators=100,
            learning_rate=0.1,
            max_depth=5,
            random_state=42
        )
        
        svm_model = SVC(
            kernel='rbf',
            probability=True,
            random_state=42
        )
        
        mlp_model = MLPClassifier(
            hidden_layer_sizes=(100, 50),
            max_iter=1000,
            random_state=42
        )
        
        # Create voting classifier
        voting_clf = VotingClassifier(
            estimators=[
                ('rf', rf_model),
                ('gb', gb_model),
                ('svm', svm_model),
                ('mlp', mlp_model)
            ],
            voting='soft'
        )
        
        return {
            'neural_network': nn_model,
            'random_forest': rf_model,
            'gradient_boosting': gb_model,
            'svm': svm_model,
            'mlp': mlp_model,
            'voting': voting_clf
        }
    
    def _hyperparameter_tuning(self, X, y):
        # Define parameter grid for Random Forest
        rf_param_grid = {
            'n_estimators': [100, 200, 300],
            'max_depth': [5, 10, 15, None],
            'min_samples_split': [2, 5, 10],
            'min_samples_leaf': [1, 2, 4]
        }
        
        # Define parameter grid for Gradient Boosting
        gb_param_grid = {
            'n_estimators': [100, 200, 300],
            'learning_rate': [0.01, 0.1, 0.3],
            'max_depth': [3, 5, 7]
        }
        
        # Perform Grid Search for Random Forest
        rf_grid = GridSearchCV(
            self.models['random_forest'],
            rf_param_grid,
            cv=5,
            scoring=make_scorer(f1_score),
            n_jobs=-1
        )
        rf_grid.fit(X, y)
        
        # Perform Grid Search for Gradient Boosting
        gb_grid = GridSearchCV(
            self.models['gradient_boosting'],
            gb_param_grid,
            cv=5,
            scoring=make_scorer(f1_score),
            n_jobs=-1
        )
        gb_grid.fit(X, y)
        
        # Update models with best parameters
        self.models['random_forest'] = rf_grid.best_estimator_
        self.models['gradient_boosting'] = gb_grid.best_estimator_
        
        # Train voting classifier
        self.models['voting'].fit(X, y)
    
    def fit(self, X, y):
        # Scale the features
        X_scaled = self.scaler.fit_transform(X)
        
        # Perform hyperparameter tuning
        self._hyperparameter_tuning(X_scaled, y)
        
        # Train neural network
        self.models['neural_network'].fit(
            X_scaled, y,
            epochs=100,
            batch_size=32,
            validation_split=0.2,
            callbacks=[
                tf.keras.callbacks.EarlyStopping(
                    monitor='val_loss',
                    patience=10,
                    restore_best_weights=True
                )
            ],
            verbose=0
        )
        
        # Train individual models
        for name, model in self.models.items():
            if name not in ['neural_network', 'voting']:
                model.fit(X_scaled, y)
    
    def predict(self, X):
        # Scale the features
        X_scaled = self.scaler.transform(X)
        
        # Get predictions from all models
        predictions = {}
        for name, model in self.models.items():
            if name == 'neural_network':
                pred = (model.predict(X_scaled) > 0.5).astype(int)
            else:
                pred = model.predict(X_scaled)
            predictions[name] = pred
        
        # Ensemble predictions (majority voting)
        ensemble_pred = np.mean([pred for pred in predictions.values()], axis=0)
        return (ensemble_pred > 0.5).astype(int)
    
    def predict_proba(self, X):
        # Scale the features
        X_scaled = self.scaler.transform(X)
        
        # Get probability predictions from all models
        probabilities = {}
        for name, model in self.models.items():
            if name == 'neural_network':
                prob = model.predict(X_scaled)
            else:
                prob = model.predict_proba(X_scaled)[:, 1]
            probabilities[name] = prob
        
        # Ensemble probabilities (average)
        return np.mean([prob for prob in probabilities.values()], axis=0)
    
    def get_feature_importance(self, X):
        # Get feature importance from Random Forest
        rf_importance = self.models['random_forest'].feature_importances_
        
        # Get feature importance from Gradient Boosting
        gb_importance = self.models['gradient_boosting'].feature_importances_
        
        # Average feature importance
        return np.mean([rf_importance, gb_importance], axis=0)
    
    def get_model_performance(self, X, y):
        """Get performance metrics for each model"""
        X_scaled = self.scaler.transform(X)
        performance = {}
        
        for name, model in self.models.items():
            if name == 'neural_network':
                pred = (model.predict(X_scaled) > 0.5).astype(int)
            else:
                pred = model.predict(X_scaled)
            
            # Calculate metrics
            accuracy = np.mean(pred == y)
            f1 = f1_score(y, pred)
            
            performance[name] = {
                'accuracy': accuracy,
                'f1_score': f1
            }
        
        return performance 