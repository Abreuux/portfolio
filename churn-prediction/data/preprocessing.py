import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
from sklearn.compose import ColumnTransformer

class DataPreprocessor:
    def __init__(self):
        self.label_encoders = {}
        self.one_hot_encoder = None
        self.categorical_features = ['contract_type', 'payment_method']
        self.numerical_features = ['tenure', 'monthly_charges']
        
    def fit(self, X):
        # Fit label encoders for categorical variables
        for feature in self.categorical_features:
            self.label_encoders[feature] = LabelEncoder()
            self.label_encoders[feature].fit(X[feature])
        
        # Create and fit one-hot encoder
        categorical_data = np.column_stack([
            self.label_encoders[feature].transform(X[feature])
            for feature in self.categorical_features
        ])
        
        self.one_hot_encoder = OneHotEncoder(sparse=False)
        self.one_hot_encoder.fit(categorical_data)
        
    def transform(self, X):
        # Transform categorical variables
        categorical_data = np.column_stack([
            self.label_encoders[feature].transform(X[feature])
            for feature in self.categorical_features
        ])
        
        # One-hot encode categorical variables
        categorical_encoded = self.one_hot_encoder.transform(categorical_data)
        
        # Get numerical features
        numerical_data = X[self.numerical_features].values
        
        # Combine numerical and categorical features
        return np.hstack([numerical_data, categorical_encoded])
    
    def fit_transform(self, X):
        self.fit(X)
        return self.transform(X) 