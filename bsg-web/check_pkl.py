import joblib
import sys

try:
    data = joblib.load('rf_clean_final.pkl')
    if isinstance(data, dict):
        print(f"Keys in pkl: {data.keys()}")
    else:
        print("Loaded object is not a dict, it's a:", type(data))
except Exception as e:
    print(f"Error: {e}")
