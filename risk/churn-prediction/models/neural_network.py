import tensorflow as tf
from tensorflow.keras import layers, models
import numpy as np
from sklearn.preprocessing import StandardScaler

class ChurnPredictor:
    def __init__(self):
        self.model = self._build_model()
        self.scaler = StandardScaler()
        
    def _build_model(self):
        model = models.Sequential([
            layers.Dense(64, activation='relu', input_shape=(10,)),
            layers.Dropout(0.3),
            layers.Dense(32, activation='relu'),
            layers.Dropout(0.3),
            layers.Dense(16, activation='relu'),
            layers.Dropout(0.3),
            layers.Dense(1, activation='sigmoid')
        ])
        
        model.compile(
            optimizer='adam',
            loss='binary_crossentropy',
            metrics=['accuracy']
        )
        
        return model
    
    def fit(self, X, y):
        # Scale the features
        X_scaled = self.scaler.fit_transform(X)
        
        # Train the model
        self.model.fit(
            X_scaled, y,
            epochs=50,
            batch_size=32,
            validation_split=0.2,
            verbose=0
        )
    
    def predict(self, X):
        # Scale the features
        X_scaled = self.scaler.transform(X)
        
        # Make predictions
        predictions = self.model.predict(X_scaled)
        return (predictions > 0.5).astype(int)
    
    def predict_proba(self, X):
        # Scale the features
        X_scaled = self.scaler.transform(X)
        
        # Get probability predictions
        return self.model.predict(X_scaled)
    
    def get_feature_importance(self, X):
        # This is a simplified feature importance calculation
        # In a real application, you might want to use more sophisticated methods
        base_pred = self.predict_proba(X)
        importance = []
        
        for i in range(X.shape[1]):
            X_modified = X.copy()
            X_modified[:, i] = 0
            modified_pred = self.predict_proba(X_modified)
            importance.append(np.mean(np.abs(base_pred - modified_pred)))
        
        return importance 