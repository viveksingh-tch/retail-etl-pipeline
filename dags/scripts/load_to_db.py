import duckdb
import pandas as pd
import os

def load_data(csv_path, db_path):
    print(f"Reading from: {csv_path}")
    
    if not os.path.exists(csv_path):
        print(f"ERROR: File {csv_path} not found. Did the extraction task run?")
        return

    # 1. READ (Extract)
    df = pd.read_csv(csv_path)
    
    # 2. TRANSFORM
    # Business Rule: We only want orders greater than $50
    clean_df = df[df['amount'] > 50.0] 
    print(f"Filtered data: Kept {len(clean_df)} rows out of {len(df)}")

    # 3. LOAD
    # Connect to our 'Mini Data Warehouse'
    con = duckdb.connect(db_path)
    
    # Create the table if it doesn't exist yet
    con.execute("CREATE TABLE IF NOT EXISTS sales (transaction_id VARCHAR, date DATE, customer_name VARCHAR, product VARCHAR, amount DECIMAL, store_id VARCHAR)")
    
    # Insert the pandas dataframe directly into SQL (DuckDB magic)
    con.execute("INSERT INTO sales SELECT * FROM clean_df")
    
    # Validation: Count how many rows we have now
    count = con.execute("SELECT COUNT(*) FROM sales").fetchone()[0]
    print(f"SUCCESS: Total rows in Data Warehouse now: {count}")
    con.close()

if __name__ == "__main__":
    # Test run manually
    load_data(
        '/workspaces/retail-etl-pipeline/data/sales_data.csv', 
        '/workspaces/retail-etl-pipeline/data/retail_wh.duckdb'
    )