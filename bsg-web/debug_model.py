import joblib
import pandas as pd
import numpy as np

def test_model():
    print("Loading model...")
    try:
        model_data = joblib.load('rf_clean_final.pkl')
        model = model_data.get('model') if isinstance(model_data, dict) else model_data
        print("Model loaded.")
    except Exception as e:
        print(f"Failed to load model: {e}")
        return

    # Create a dummy dataframe matching the structure of clean scenario
    # Columns matching prep_scenarios.py feature list (first 9 used by binary model in server.py)
    columns = ['latency_ms', 'integrity_flag', 'token_visible', 'voltage_v', 'current_a', 
               'temperature_c', 'meter_kwh', 'cost', 'ip_changed', 
               'command_code', 'user_role_code', 'status_code']
    
    # Test Case 1: What I currently generated (Integrity 0)
    row_integrity_0 = [20, 0, 0, 230.0, 16.0, 35.0, 10.0, 5.0, 0, 1, 1, 1]
    
    # Test Case 2: Integrity 1 (Like in test_20_feature.csv normal rows)
    row_integrity_1 = [20, 1, 0, 230.0, 16.0, 35.0, 10.0, 5.0, 0, 1, 1, 1]
    
    # Test Case 3: Idle (Integrity 0)
    row_idle_0 = [10, 0, 0, 230.0, 0.0, 25.0, 0.0, 0.0, 0, 1, 1, 1]
    
    # Test Case 4: Idle (Integrity 1)
    row_idle_1 = [10, 1, 0, 230.0, 0.0, 25.0, 0.0, 0.0, 0, 1, 1, 1]

    data = pd.DataFrame([row_integrity_0, row_integrity_1, row_idle_0, row_idle_1], columns=columns)
    
    # Server.py slices first 9 columns for binary model
    # features_binary = np.array(data.features[:9]).reshape(1, -1)
    
    print("\n--- Predictions ---")
    for i, row in data.iterrows():
        # Select first 9 features as per server.py
        # Actually server.py takes a list of features. 
        # features_binary = np.array(data.features[:9]).reshape(1, -1)
        feat_vector = row.values[:9].reshape(1, -1)
        
        pred = model.predict(feat_vector)[0]
        probs = model.predict_proba(feat_vector)[0] if hasattr(model, "predict_proba") else "N/A"
        
        status = "ANOMALY" if pred == 1 else "NORMAL"
        desc = ""
        if i == 0: desc = "Current Clean (Integrity 0, Charging)"
        if i == 1: desc = "Test Clean (Integrity 1, Charging)"
        if i == 2: desc = "Current Clean (Integrity 0, Idle)"
        if i == 3: desc = "Test Clean (Integrity 1, Idle)"
        
        print(f"Case {i}: {desc} -> {status} (Prob: {probs})")

if __name__ == "__main__":
    test_model()
