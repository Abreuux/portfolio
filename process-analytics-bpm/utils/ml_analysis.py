import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.metrics import mean_squared_error, r2_score
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
import joblib
import os
import logging
from datetime import datetime, timedelta

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ProcessMLAnalyzer:
    def __init__(self, model_path=None):
        self.model_path = model_path
        self.next_activity_model = None
        self.duration_model = None
        self.risk_model = None
        self.scaler = StandardScaler()
        self.label_encoder = LabelEncoder()
        self.feature_columns = None
        self.target_column = None

    def prepare_data(self, log_data):
        """Prepara os dados para treinamento"""
        try:
            # Converte log para DataFrame
            df = pd.DataFrame(log_data)
            
            # Extrai features
            self.feature_columns = [
                'case_id', 'activity', 'resource', 'timestamp',
                'duration', 'weekday', 'hour'
            ]
            
            # Adiciona features temporais
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            df['weekday'] = df['timestamp'].dt.weekday
            df['hour'] = df['timestamp'].dt.hour
            
            # Codifica variáveis categóricas
            df['activity_encoded'] = self.label_encoder.fit_transform(df['activity'])
            df['resource_encoded'] = self.label_encoder.fit_transform(df['resource'])
            
            return df
        except Exception as e:
            logger.error(f"Erro ao preparar dados: {str(e)}")
            return None

    def train_next_activity_model(self, data):
        """Treina modelo para prever próxima atividade"""
        try:
            # Prepara dados
            X = data[self.feature_columns]
            y = data['activity'].shift(-1).dropna()
            X = X[:-1]  # Remove última linha para alinhar com y
            
            # Divide dados
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=0.2, random_state=42
            )
            
            # Treina modelo
            self.next_activity_model = RandomForestClassifier(
                n_estimators=100,
                random_state=42
            )
            self.next_activity_model.fit(X_train, y_train)
            
            # Avalia modelo
            y_pred = self.next_activity_model.predict(X_test)
            accuracy = accuracy_score(y_test, y_pred)
            precision = precision_score(y_test, y_pred, average='weighted')
            
            logger.info(f"Modelo de próxima atividade treinado. Acurácia: {accuracy:.2f}")
            return {
                'accuracy': accuracy,
                'precision': precision
            }
        except Exception as e:
            logger.error(f"Erro ao treinar modelo de próxima atividade: {str(e)}")
            return None

    def train_duration_model(self, data):
        """Treina modelo para prever duração"""
        try:
            # Prepara dados
            X = data[self.feature_columns]
            y = data['duration']
            
            # Divide dados
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=0.2, random_state=42
            )
            
            # Treina modelo
            self.duration_model = RandomForestRegressor(
                n_estimators=100,
                random_state=42
            )
            self.duration_model.fit(X_train, y_train)
            
            # Avalia modelo
            y_pred = self.duration_model.predict(X_test)
            mse = mean_squared_error(y_test, y_pred)
            r2 = r2_score(y_test, y_pred)
            
            logger.info(f"Modelo de duração treinado. R²: {r2:.2f}")
            return {
                'mse': mse,
                'r2': r2
            }
        except Exception as e:
            logger.error(f"Erro ao treinar modelo de duração: {str(e)}")
            return None

    def train_risk_model(self, data):
        """Treina modelo para análise de risco"""
        try:
            # Define critérios de risco
            data['risk'] = np.where(
                (data['duration'] > data['duration'].mean() + 2*data['duration'].std()) |
                (data['activity'] == 'Rejeição'),
                1, 0
            )
            
            # Prepara dados
            X = data[self.feature_columns]
            y = data['risk']
            
            # Divide dados
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=0.2, random_state=42
            )
            
            # Treina modelo
            self.risk_model = RandomForestClassifier(
                n_estimators=100,
                random_state=42
            )
            self.risk_model.fit(X_train, y_train)
            
            # Avalia modelo
            y_pred = self.risk_model.predict(X_test)
            f1 = f1_score(y_test, y_pred)
            
            logger.info(f"Modelo de risco treinado. F1-score: {f1:.2f}")
            return {
                'f1_score': f1
            }
        except Exception as e:
            logger.error(f"Erro ao treinar modelo de risco: {str(e)}")
            return None

    def predict_next_activity(self, current_state):
        """Preve a próxima atividade"""
        try:
            if not self.next_activity_model:
                raise ValueError("Modelo de próxima atividade não treinado")
            
            # Prepara dados
            X = pd.DataFrame([current_state])
            
            # Faz previsão
            prediction = self.next_activity_model.predict(X)
            probabilities = self.next_activity_model.predict_proba(X)
            
            return {
                'next_activity': prediction[0],
                'probability': max(probabilities[0])
            }
        except Exception as e:
            logger.error(f"Erro ao prever próxima atividade: {str(e)}")
            return None

    def predict_duration(self, current_state):
        """Preve a duração da próxima atividade"""
        try:
            if not self.duration_model:
                raise ValueError("Modelo de duração não treinado")
            
            # Prepara dados
            X = pd.DataFrame([current_state])
            
            # Faz previsão
            prediction = self.duration_model.predict(X)
            
            return {
                'estimated_duration': prediction[0]
            }
        except Exception as e:
            logger.error(f"Erro ao prever duração: {str(e)}")
            return None

    def assess_risk(self, current_state):
        """Avalia o risco da próxima atividade"""
        try:
            if not self.risk_model:
                raise ValueError("Modelo de risco não treinado")
            
            # Prepara dados
            X = pd.DataFrame([current_state])
            
            # Faz previsão
            prediction = self.risk_model.predict(X)
            probabilities = self.risk_model.predict_proba(X)
            
            return {
                'risk_level': 'Alto' if prediction[0] == 1 else 'Baixo',
                'risk_probability': probabilities[0][1]
            }
        except Exception as e:
            logger.error(f"Erro ao avaliar risco: {str(e)}")
            return None

    def save_models(self, output_dir):
        """Salva os modelos treinados"""
        try:
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
            
            if self.next_activity_model:
                joblib.dump(
                    self.next_activity_model,
                    os.path.join(output_dir, 'next_activity_model.pkl')
                )
            
            if self.duration_model:
                joblib.dump(
                    self.duration_model,
                    os.path.join(output_dir, 'duration_model.pkl')
                )
            
            if self.risk_model:
                joblib.dump(
                    self.risk_model,
                    os.path.join(output_dir, 'risk_model.pkl')
                )
            
            logger.info(f"Modelos salvos em: {output_dir}")
            return True
        except Exception as e:
            logger.error(f"Erro ao salvar modelos: {str(e)}")
            return False

    def load_models(self, input_dir):
        """Carrega os modelos salvos"""
        try:
            self.next_activity_model = joblib.load(
                os.path.join(input_dir, 'next_activity_model.pkl')
            )
            self.duration_model = joblib.load(
                os.path.join(input_dir, 'duration_model.pkl')
            )
            self.risk_model = joblib.load(
                os.path.join(input_dir, 'risk_model.pkl')
            )
            
            logger.info("Modelos carregados com sucesso")
            return True
        except Exception as e:
            logger.error(f"Erro ao carregar modelos: {str(e)}")
            return False

def main():
    """Função principal para demonstração"""
    # Exemplo de dados
    data = {
        'case_id': range(1, 101),
        'activity': ['A', 'B', 'C'] * 34,
        'resource': ['R1', 'R2', 'R3'] * 34,
        'timestamp': pd.date_range(start='2024-01-01', periods=100),
        'duration': np.random.normal(5, 2, 100)
    }
    
    analyzer = ProcessMLAnalyzer()
    df = analyzer.prepare_data(data)
    
    if df is not None:
        # Treina modelos
        analyzer.train_next_activity_model(df)
        analyzer.train_duration_model(df)
        analyzer.train_risk_model(df)
        
        # Faz previsões
        current_state = {
            'case_id': 101,
            'activity': 'A',
            'resource': 'R1',
            'timestamp': datetime.now(),
            'duration': 5.0,
            'weekday': datetime.now().weekday(),
            'hour': datetime.now().hour
        }
        
        next_activity = analyzer.predict_next_activity(current_state)
        duration = analyzer.predict_duration(current_state)
        risk = analyzer.assess_risk(current_state)
        
        print("\nPrevisões:")
        print(f"Próxima atividade: {next_activity['next_activity']} ({next_activity['probability']:.2f})")
        print(f"Duração estimada: {duration['estimated_duration']:.2f}h")
        print(f"Nível de risco: {risk['risk_level']} ({risk['risk_probability']:.2f})")
        
        # Salva modelos
        analyzer.save_models('models')

if __name__ == "__main__":
    main() 