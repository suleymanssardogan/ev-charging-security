import joblib
import pandas as pd
import numpy as np

def test_exact_row():
    # Row 2 from test_20_feature.csv
    # 20,1,0,230.5,16.0,35.0,10.5,5.2,0
    row_csv = [20, 1, 0, 230.5, 16.0, 35.0, 10.5, 5.2, 0]
    feat_vector = np.array(row_csv).reshape(1, -1)

    print("--- Testing against rf_clean_final.pkl (Currently Used) ---")
    try:
        data = joblib.load('rf_clean_final.pkl')
        model = data.get('model') if isinstance(data, dict) else data
        pred = model.predict(feat_vector)[0]
        probs = model.predict_proba(feat_vector)[0] if hasattr(model, "predict_proba") else "N/A"
        print(f"Prediction: {pred} ({'ANOMALY' if pred==1 else 'NORMAL'}) Prob: {probs}")
    except Exception as e:
        print(f"Error: {e}")

    print("\n--- Testing against backend/model.pkl (Alternative) ---")
    try:
        data = joblib.load('backend/model.pkl')
        model = data.get('model') if isinstance(data, dict) else data
        pred = model.predict(feat_vector)[0]
        probs = model.predict_proba(feat_vector)[0] if hasattr(model, "predict_proba") else "N/A"
        print(f"Prediction: {pred} ({'ANOMALY' if pred==1 else 'NORMAL'}) Prob: {probs}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_exact_row()
