import joblib
import pandas as pd
import numpy as np

def brute_force_normal():
    print("Loading model...")
    try:
        model_data = joblib.load('rf_clean_final.pkl')
        model = model_data.get('model') if isinstance(model_data, dict) else model_data
    except Exception as e:
        print(f"Failed to load model: {e}")
        return

    # Base "Charging" row
    # columns matching vector indices 0-8
    
    attempts = []
    
    # Try different Integrity flags
    for integrity in [0, 1]:
        # Try different Costs (ratio check)
        # Assuming kwh=10
        for cost_multiplier in [0.1, 0.2, 0.5, 0.8, 1.0, 2.0]:
            # Try different Latencies
            for latency in [10, 20, 50, 100]:
                kwh = 10.0
                cost = kwh * cost_multiplier
                
                # Try different Voltages
                for voltage in [220, 230, 240]:
                    
                     # [latency, integrity, token_vis, voltage, current, temp, kwh, cost, ip_chg]
                    row = [latency, integrity, 0, voltage, 16.0, 35.0, kwh, cost, 0]
                    
                    attempts.append(row)

    print(f"Testing {len(attempts)} combinations...")
    
    matches = []
    for row in attempts:
        feat_vector = np.array(row).reshape(1, -1)
        pred = model.predict(feat_vector)[0]
        probs = model.predict_proba(feat_vector)[0]
        
        # If Normal (0) and Confidence > 0.6 (to be safe)
        if pred == 0:
            matches.append((row, probs[0])) # probs[0] is prob of class 0 (Normal)

    # Sort by confidence
    matches.sort(key=lambda x: x[1], reverse=True)
    
    print("\n--- TOP 5 NORMAL CONFIGURATIONS ---")
    for m in matches[:10]:
        r = m[0]
        # [latency, integrity, token_vis, voltage, current, temp, kwh, cost, ip_chg]
        print(f"Conf: {m[1]:.4f} | Integ: {r[1]}, Lat: {r[0]}, Volt: {r[3]}, Rate: {r[7]/r[6] if r[6]!=0 else 0}")

    if not matches:
        print("No normal configurations found for Charging state!")

if __name__ == "__main__":
    brute_force_normal()
