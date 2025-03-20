import pandas as pd
import numpy as np
from typing import List, Dict, Any, Tuple
from sklearn.preprocessing import StandardScaler
from prophet import Prophet
from statsmodels.tsa.holtwinters import ExponentialSmoothing
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
from tensorflow.keras.optimizers import Adam
import xgboost as xgb
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

class DemandForecaster:
    def __init__(self):
        self.models = {
            'prophet': None,
            'holt_winters': None,
            'lstm': None,
            'xgboost': None
        }
        self.scaler = StandardScaler()
        
    def prepare_data(self, data: pd.DataFrame, target_col: str, date_col: str) -> Tuple[np.ndarray, np.ndarray]:
        """Prepare data for forecasting"""
        # Sort data by date
        data = data.sort_values(date_col)
        
        # Create features
        data['year'] = data[date_col].dt.year
        data['month'] = data[date_col].dt.month
        data['day_of_week'] = data[date_col].dt.dayofweek
        data['is_holiday'] = data[date_col].dt.dayofweek.isin([5, 6]).astype(int)
        
        # Scale target variable
        scaled_target = self.scaler.fit_transform(data[[target_col]])
        
        return data, scaled_target
    
    def train_prophet(self, data: pd.DataFrame, target_col: str, date_col: str) -> None:
        """Train Prophet model"""
        # Prepare data for Prophet
        prophet_data = data.rename(columns={date_col: 'ds', target_col: 'y'})
        
        # Initialize and train model
        self.models['prophet'] = Prophet(
            yearly_seasonality=True,
            weekly_seasonality=True,
            daily_seasonality=True,
            changepoint_prior_scale=0.05
        )
        self.models['prophet'].fit(prophet_data)
    
    def train_holt_winters(self, data: pd.DataFrame, target_col: str) -> None:
        """Train Holt-Winters model"""
        # Initialize and train model
        self.models['holt_winters'] = ExponentialSmoothing(
            data[target_col],
            seasonal_periods=7,
            trend='add',
            seasonal='add'
        ).fit()
    
    def build_lstm_model(self, input_shape: Tuple[int, int]) -> Sequential:
        """Build LSTM model architecture"""
        model = Sequential([
            LSTM(50, return_sequences=True, input_shape=input_shape),
            Dropout(0.2),
            LSTM(50, return_sequences=False),
            Dropout(0.2),
            Dense(25),
            Dense(1)
        ])
        
        model.compile(
            optimizer=Adam(learning_rate=0.001),
            loss='mse'
        )
        
        return model
    
    def train_lstm(self, data: pd.DataFrame, target_col: str, sequence_length: int = 10) -> None:
        """Train LSTM model"""
        # Prepare sequences
        X, y = [], []
        for i in range(len(data) - sequence_length):
            X.append(data[target_col].values[i:(i + sequence_length)])
            y.append(data[target_col].values[i + sequence_length])
        
        X = np.array(X)
        y = np.array(y)
        
        # Build and train model
        self.models['lstm'] = self.build_lstm_model((sequence_length, 1))
        self.models['lstm'].fit(
            X, y,
            epochs=50,
            batch_size=32,
            validation_split=0.2,
            verbose=0
        )
    
    def train_xgboost(self, data: pd.DataFrame, target_col: str) -> None:
        """Train XGBoost model"""
        # Prepare features
        features = ['year', 'month', 'day_of_week', 'is_holiday']
        X = data[features]
        y = data[target_col]
        
        # Initialize and train model
        self.models['xgboost'] = xgb.XGBRegressor(
            objective='reg:squarederror',
            n_estimators=100,
            learning_rate=0.1,
            max_depth=6
        )
        self.models['xgboost'].fit(X, y)
    
    def forecast(self, model_type: str, periods: int) -> pd.DataFrame:
        """Generate forecasts using specified model"""
        if model_type not in self.models or self.models[model_type] is None:
            raise ValueError(f"Model {model_type} not trained")
        
        if model_type == 'prophet':
            future = self.models['prophet'].make_future_dataframe(periods=periods)
            forecast = self.models['prophet'].predict(future)
            return forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']]
        
        elif model_type == 'holt_winters':
            forecast = self.models['holt_winters'].forecast(periods)
            return pd.DataFrame({
                'date': pd.date_range(start=forecast.index[0], periods=len(forecast)),
                'forecast': forecast.values
            })
        
        elif model_type == 'lstm':
            # TODO: Implement LSTM forecasting
            return pd.DataFrame()
        
        elif model_type == 'xgboost':
            # TODO: Implement XGBoost forecasting
            return pd.DataFrame()
        
        else:
            raise ValueError(f"Unsupported model type: {model_type}")
    
    def evaluate_model(self, model_type: str, actual: pd.Series, predicted: pd.Series) -> Dict[str, float]:
        """Evaluate model performance"""
        metrics = {
            'mse': mean_squared_error(actual, predicted),
            'rmse': np.sqrt(mean_squared_error(actual, predicted)),
            'mae': mean_absolute_error(actual, predicted),
            'r2': r2_score(actual, predicted)
        }
        return metrics
    
    def ensemble_forecast(self, periods: int, weights: Dict[str, float] = None) -> pd.DataFrame:
        """Generate ensemble forecast using all trained models"""
        if weights is None:
            weights = {model: 1.0 for model in self.models if self.models[model] is not None}
        
        forecasts = {}
        for model_type in self.models:
            if self.models[model_type] is not None:
                forecasts[model_type] = self.forecast(model_type, periods)
        
        # TODO: Implement ensemble logic
        return pd.DataFrame() 