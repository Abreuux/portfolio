import pandas as pd
import numpy as np
from typing import List, Dict, Any
from datetime import datetime, timedelta
import psycopg2
from sqlalchemy import create_engine
import os
import json
import requests
from prefect import task, flow
from prefect.tasks import task_input_hash
from datetime import timedelta

class LogisticsETL:
    def __init__(self):
        self.db_params = {
            'host': os.getenv('DB_HOST', 'localhost'),
            'database': os.getenv('DB_NAME', 'logistics_db'),
            'user': os.getenv('DB_USER', 'postgres'),
            'password': os.getenv('DB_PASSWORD', 'postgres')
        }
        self.engine = create_engine(
            f"postgresql://{self.db_params['user']}:{self.db_params['password']}@"
            f"{self.db_params['host']}/{self.db_params['database']}"
        )

    @task(cache_key_fn=task_input_hash, cache_expiration=timedelta(hours=1))
    def extract_orders(self, start_date: datetime, end_date: datetime) -> pd.DataFrame:
        """Extract order data from source system"""
        query = """
        SELECT 
            order_id,
            customer_id,
            order_date,
            delivery_date,
            origin_location,
            destination_location,
            product_id,
            quantity,
            weight,
            volume
        FROM orders
        WHERE order_date BETWEEN %s AND %s
        """
        
        with psycopg2.connect(**self.db_params) as conn:
            df = pd.read_sql(query, conn, params=[start_date, end_date])
        
        return df

    @task(cache_key_fn=task_input_hash, cache_expiration=timedelta(hours=1))
    def extract_inventory(self, date: datetime) -> pd.DataFrame:
        """Extract inventory data from source system"""
        query = """
        SELECT 
            product_id,
            warehouse_id,
            quantity,
            last_updated
        FROM inventory
        WHERE DATE(last_updated) = %s
        """
        
        with psycopg2.connect(**self.db_params) as conn:
            df = pd.read_sql(query, conn, params=[date])
        
        return df

    @task(cache_key_fn=task_input_hash, cache_expiration=timedelta(hours=1))
    def extract_transportation(self, start_date: datetime, end_date: datetime) -> pd.DataFrame:
        """Extract transportation data from source system"""
        query = """
        SELECT 
            shipment_id,
            vehicle_id,
            route_id,
            departure_time,
            arrival_time,
            distance,
            fuel_consumption,
            cost
        FROM shipments
        WHERE departure_time BETWEEN %s AND %s
        """
        
        with psycopg2.connect(**self.db_params) as conn:
            df = pd.read_sql(query, conn, params=[start_date, end_date])
        
        return df

    @task
    def transform_orders(self, orders_df: pd.DataFrame) -> pd.DataFrame:
        """Transform order data"""
        # Calculate delivery time
        orders_df['delivery_time'] = (
            pd.to_datetime(orders_df['delivery_date']) - 
            pd.to_datetime(orders_df['order_date'])
        ).dt.total_seconds() / 3600  # Convert to hours
        
        # Calculate order density
        orders_df['density'] = orders_df['weight'] / orders_df['volume']
        
        # Calculate order value (mock calculation)
        orders_df['order_value'] = orders_df['quantity'] * np.random.uniform(10, 100, len(orders_df))
        
        return orders_df

    @task
    def transform_inventory(self, inventory_df: pd.DataFrame) -> pd.DataFrame:
        """Transform inventory data"""
        # Calculate days of supply (mock calculation)
        inventory_df['daily_demand'] = np.random.uniform(1, 10, len(inventory_df))
        inventory_df['days_of_supply'] = inventory_df['quantity'] / inventory_df['daily_demand']
        
        # Calculate inventory value (mock calculation)
        inventory_df['unit_cost'] = np.random.uniform(5, 50, len(inventory_df))
        inventory_df['inventory_value'] = inventory_df['quantity'] * inventory_df['unit_cost']
        
        return inventory_df

    @task
    def transform_transportation(self, transportation_df: pd.DataFrame) -> pd.DataFrame:
        """Transform transportation data"""
        # Calculate efficiency metrics
        transportation_df['fuel_efficiency'] = transportation_df['distance'] / transportation_df['fuel_consumption']
        transportation_df['cost_per_km'] = transportation_df['cost'] / transportation_df['distance']
        
        # Calculate duration
        transportation_df['duration'] = (
            pd.to_datetime(transportation_df['arrival_time']) - 
            pd.to_datetime(transportation_df['departure_time'])
        ).dt.total_seconds() / 3600  # Convert to hours
        
        # Calculate average speed
        transportation_df['avg_speed'] = transportation_df['distance'] / transportation_df['duration']
        
        return transportation_df

    @task
    def load_transformed_data(self, 
                            orders_df: pd.DataFrame,
                            inventory_df: pd.DataFrame,
                            transportation_df: pd.DataFrame) -> None:
        """Load transformed data into data warehouse"""
        # Load orders
        orders_df.to_sql(
            'fact_orders',
            self.engine,
            if_exists='append',
            index=False
        )
        
        # Load inventory
        inventory_df.to_sql(
            'fact_inventory',
            self.engine,
            if_exists='append',
            index=False
        )
        
        # Load transportation
        transportation_df.to_sql(
            'fact_transportation',
            self.engine,
            if_exists='append',
            index=False
        )

    @flow
    def run_etl_pipeline(self, start_date: datetime, end_date: datetime):
        """Execute the complete ETL pipeline"""
        try:
            # Extract data
            orders_df = self.extract_orders(start_date, end_date)
            inventory_df = self.extract_inventory(end_date)
            transportation_df = self.extract_transportation(start_date, end_date)
            
            # Transform data
            transformed_orders = self.transform_orders(orders_df)
            transformed_inventory = self.transform_inventory(inventory_df)
            transformed_transportation = self.transform_transportation(transportation_df)
            
            # Load data
            self.load_transformed_data(
                transformed_orders,
                transformed_inventory,
                transformed_transportation
            )
            
            return {
                'status': 'success',
                'message': 'ETL pipeline completed successfully',
                'stats': {
                    'orders_processed': len(transformed_orders),
                    'inventory_records': len(transformed_inventory),
                    'shipments_processed': len(transformed_transportation)
                }
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'message': str(e)
            }

if __name__ == "__main__":
    # Example usage
    etl = LogisticsETL()
    start_date = datetime.now() - timedelta(days=1)
    end_date = datetime.now()
    
    result = etl.run_etl_pipeline(start_date, end_date)
    print(json.dumps(result, indent=2)) 