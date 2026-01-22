import joblib
import numpy as np
import pandas as pd

def find_normal_points():
    print("Loading model...")
    try:
        data = joblib.load('rf_clean_final.pkl')
        model = data.get('model') if isinstance(data, dict) else data
    except Exception as e:
        print(f"Error: {e}")
        return

    n_samples = 100000
    
    # Generate random data
    # 0: latency (0-200)
    latency = np.random.uniform(0, 100, n_samples)
    # 1: integrity (0 or 1)
    integrity = np.random.choice([0, 1], n_samples)
    # 2: token_visible (0 usually)
    token = np.random.choice([0, 1], n_samples, p=[0.9, 0.1])
    # 3: voltage (210-250 for normal usually)
    voltage = np.random.uniform(210, 250, n_samples)
    # 4: current (0-20)
    current = np.random.uniform(0, 20, n_samples)
    # 5: temp (20-50)
    temp = np.random.uniform(20, 50, n_samples)
    # 6: meter (0-20)
    meter = np.random.uniform(0, 20, n_samples)
    # 7: cost (0-10)
    cost = np.random.uniform(0, 10, n_samples)
    # 8: ip_changed (0)
    ip = np.random.choice([0, 1], n_samples, p=[0.9, 0.1])
    
    dataset = np.column_stack((latency, integrity, token, voltage, current, temp, meter, cost, ip))
    
    print(f"Predicting on {n_samples} samples...")
    preds = model.predict(dataset)
    
    normals = dataset[preds == 0]
    print(f"Found {len(normals)} Normal samples out of {n_samples}")
    
    if len(normals) > 0:
        # Check specific rows to understand patterns
        df_norm = pd.DataFrame(normals, columns=['latency','integrity','token','voltage','current','temp','meter','cost','ip'])
        print("\nMean values of Normal samples:")
        print(df_norm.mean())
        
        print("\nSample Normal Row:")
        print(df_norm.iloc[0].values)
        
        # Save a few for me to use in the clean scenario
        df_norm.head(50).to_csv('found_normals.csv', index=False)
    else:
        print("No normal samples found. The model is extremely restrictive.")

if __name__ == "__main__":
    find_normal_points()
