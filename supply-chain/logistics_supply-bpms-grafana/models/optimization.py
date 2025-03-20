import pandas as pd
import numpy as np
from typing import List, Dict, Any, Tuple
from pulp import *
from ortools.linear_solver import pywraplp
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM, Dropout
from tensorflow.keras.optimizers import Adam
import xgboost as xgb
from sklearn.metrics import mean_squared_error, mean_absolute_error
import cvxopt

class LogisticsOptimizer:
    def __init__(self):
        self.models = {
            'inventory_optimization': None,
            'route_optimization': None,
            'demand_forecast': None,
            'cluster_analysis': None
        }
        self.scaler = StandardScaler()
        
    def optimize_inventory(self, 
                         demand_data: pd.DataFrame,
                         holding_cost: float,
                         ordering_cost: float,
                         lead_time: int) -> Dict[str, Any]:
        """Optimize inventory levels using EOQ model"""
        # Calculate average demand
        avg_demand = demand_data['demand'].mean()
        
        # Calculate EOQ
        eoq = np.sqrt((2 * avg_demand * ordering_cost) / holding_cost)
        
        # Calculate reorder point
        reorder_point = avg_demand * lead_time
        
        # Calculate safety stock (assuming normal distribution)
        std_demand = demand_data['demand'].std()
        safety_stock = 1.96 * std_demand * np.sqrt(lead_time)
        
        return {
            'eoq': eoq,
            'reorder_point': reorder_point,
            'safety_stock': safety_stock,
            'max_inventory': eoq + safety_stock
        }
    
    def optimize_routes(self, 
                       locations: List[Tuple[float, float]],
                       demands: List[float],
                       vehicle_capacity: float) -> Dict[str, Any]:
        """Optimize delivery routes using VRP"""
        # Create solver
        solver = pywraplp.Solver.CreateSolver('SCIP')
        
        # Create variables
        num_locations = len(locations)
        x = {}
        for i in range(num_locations):
            for j in range(num_locations):
                x[i, j] = solver.IntVar(0, 1, f'x_{i}_{j}')
        
        # Add constraints
        # Each location must be visited exactly once
        for i in range(num_locations):
            solver.Add(sum(x[i, j] for j in range(num_locations)) == 1)
            solver.Add(sum(x[j, i] for j in range(num_locations)) == 1)
        
        # Vehicle capacity constraint
        for i in range(num_locations):
            solver.Add(sum(demands[j] * x[i, j] for j in range(num_locations)) <= vehicle_capacity)
        
        # Objective: minimize total distance
        distances = np.zeros((num_locations, num_locations))
        for i in range(num_locations):
            for j in range(num_locations):
                distances[i, j] = np.sqrt(
                    (locations[i][0] - locations[j][0])**2 +
                    (locations[i][1] - locations[j][1])**2
                )
        
        objective = solver.Objective()
        objective.SetMinimization()
        for i in range(num_locations):
            for j in range(num_locations):
                objective.SetCoefficient(x[i, j], distances[i, j])
        
        # Solve
        status = solver.Solve()
        
        if status == pywraplp.Solver.OPTIMAL:
            # Extract solution
            route = []
            current = 0
            while True:
                for j in range(num_locations):
                    if x[current, j].solution_value() == 1:
                        route.append(j)
                        current = j
                        break
                if current == 0:
                    break
            
            return {
                'route': route,
                'total_distance': objective.Value(),
                'status': 'optimal'
            }
        else:
            return {
                'status': 'infeasible',
                'message': 'No feasible solution found'
            }
    
    def train_demand_forecast(self, 
                            data: pd.DataFrame,
                            target_col: str,
                            sequence_length: int = 10) -> None:
        """Train LSTM model for demand forecasting"""
        # Prepare sequences
        X, y = [], []
        for i in range(len(data) - sequence_length):
            X.append(data[target_col].values[i:(i + sequence_length)])
            y.append(data[target_col].values[i + sequence_length])
        
        X = np.array(X)
        y = np.array(y)
        
        # Build model
        model = Sequential([
            LSTM(50, return_sequences=True, input_shape=(sequence_length, 1)),
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
        
        # Train model
        model.fit(
            X, y,
            epochs=50,
            batch_size=32,
            validation_split=0.2,
            verbose=0
        )
        
        self.models['demand_forecast'] = model
    
    def cluster_locations(self, 
                         locations: List[Tuple[float, float]],
                         num_clusters: int) -> Dict[str, Any]:
        """Cluster locations for better distribution planning"""
        # Convert locations to numpy array
        X = np.array(locations)
        
        # Perform K-means clustering
        kmeans = KMeans(n_clusters=num_clusters, random_state=42)
        clusters = kmeans.fit_predict(X)
        
        # Calculate cluster statistics
        cluster_stats = {}
        for i in range(num_clusters):
            cluster_points = X[clusters == i]
            cluster_stats[i] = {
                'center': kmeans.cluster_centers_[i],
                'size': len(cluster_points),
                'points': cluster_points
            }
        
        return {
            'clusters': clusters,
            'centers': kmeans.cluster_centers_,
            'stats': cluster_stats
        }
    
    def optimize_warehouse_location(self,
                                  locations: List[Tuple[float, float]],
                                  demands: List[float]) -> Dict[str, Any]:
        """Optimize warehouse location using weighted center of gravity"""
        # Convert to numpy arrays
        X = np.array(locations)
        w = np.array(demands)
        
        # Calculate weighted center
        weighted_center = np.average(X, axis=0, weights=w)
        
        # Calculate total weighted distance
        distances = np.sqrt(np.sum((X - weighted_center)**2, axis=1))
        total_weighted_distance = np.sum(distances * w)
        
        return {
            'optimal_location': weighted_center,
            'total_weighted_distance': total_weighted_distance
        }
    
    def optimize_transportation(self,
                              origins: List[Tuple[float, float]],
                              destinations: List[Tuple[float, float]],
                              supplies: List[float],
                              demands: List[float],
                              costs: List[List[float]]) -> Dict[str, Any]:
        """Optimize transportation using linear programming"""
        # Create solver
        solver = pywraplp.Solver.CreateSolver('SCIP')
        
        # Create variables
        num_origins = len(origins)
        num_destinations = len(destinations)
        x = {}
        for i in range(num_origins):
            for j in range(num_destinations):
                x[i, j] = solver.DoubleVar(0, solver.infinity(), f'x_{i}_{j}')
        
        # Add constraints
        # Supply constraints
        for i in range(num_origins):
            solver.Add(sum(x[i, j] for j in range(num_destinations)) <= supplies[i])
        
        # Demand constraints
        for j in range(num_destinations):
            solver.Add(sum(x[i, j] for i in range(num_origins)) >= demands[j])
        
        # Objective: minimize total cost
        objective = solver.Objective()
        objective.SetMinimization()
        for i in range(num_origins):
            for j in range(num_destinations):
                objective.SetCoefficient(x[i, j], costs[i][j])
        
        # Solve
        status = solver.Solve()
        
        if status == pywraplp.Solver.OPTIMAL:
            # Extract solution
            solution = np.zeros((num_origins, num_destinations))
            for i in range(num_origins):
                for j in range(num_destinations):
                    solution[i, j] = x[i, j].solution_value()
            
            return {
                'solution': solution,
                'total_cost': objective.Value(),
                'status': 'optimal'
            }
        else:
            return {
                'status': 'infeasible',
                'message': 'No feasible solution found'
            } 