import csv
import random
from faker import Faker
from datetime import datetime

# Initialize Faker to generate real-looking names
fake = Faker()

def generate_daily_sales(file_path, num_records=100):
    print(f"Generating data at: {file_path}") # Log for debugging
    with open(file_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        # Header: The column names
        writer.writerow(['transaction_id', 'date', 'customer_name', 'product', 'amount', 'store_id'])
        
        # Loop 100 times to create 100 fake sales
        for _ in range(num_records):
            writer.writerow([
                fake.uuid4(), # Random ID like 'a1b2-c3d4...'
                datetime.today().strftime('%Y-%m-%d'),
                fake.name(), # Fake name like 'John Doe'
                random.choice(['Laptop', 'Mouse', 'Monitor', 'Keyboard', 'Webcam']),
                round(random.uniform(20.0, 1500.0), 2), # Random price between $20 and $1500
                random.choice(['STORE_A', 'STORE_B', 'STORE_C'])
            ])
    print(f"Successfully generated {num_records} records.")

if __name__ == "__main__":
    # This allows us to test the script manually without Airflow
    generate_daily_sales('/workspaces/retail-etl-pipeline/data/sales_data.csv')