import pandas as pd
import time
import os
import joblib 
import numpy as np
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict, Any

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

MODEL_FILE = "backend/model.pkl"
loaded_objects = {}

class MultiFeatureData(BaseModel):
    features: List[float] 

def load_system():
    global loaded_objects
    loaded_objects = {'solutions': {}}
    
    # 1. Load MAIN Binary Model (High Confidence)
    try:
        binary_data = joblib.load('rf_clean_final.pkl') # Updated path
        loaded_objects['binary_model'] = binary_data.get('model') if isinstance(binary_data, dict) else binary_data
        print("Loaded Binary Model (rf_clean_final.pkl)")
    except Exception as e:
        print(f"Error loading binary model: {e}")

    # 2. Load AUXILIARY Multiclass Model (For Naming)
    try:
        multi_data = joblib.load('backend/model_multiclass.pkl')
        if isinstance(multi_data, dict):
            loaded_objects['multiclass_model'] = multi_data.get('model')
            loaded_objects['solutions'] = multi_data.get('solutions', {})
        else:
            loaded_objects['multiclass_model'] = multi_data
        print("Loaded Multiclass Model (model_multiclass.pkl)")
    except Exception as e:
        print(f"Error loading multiclass model: {e}")

@app.on_event("startup")
async def startup_event():
    load_system()

@app.post("/predict_multifeature")
def predict_multifeature(data: MultiFeatureData):
    binary_model = loaded_objects.get('binary_model')
    multiclass_model = loaded_objects.get('multiclass_model')
    solutions = loaded_objects.get('solutions', {})
    
    # Prepare Inputs
    # Binary model needs first 9 features
    features_binary = np.array(data.features[:9]).reshape(1, -1)
    # Multiclass model needs 12 features (pad if necessary)
    features_multi = np.array(data.features).reshape(1, -1)
    if features_multi.shape[1] < 12:
        # Pad with zeros if input is short (e.g. only 9 feats sent)
        padding = np.zeros((1, 12 - features_multi.shape[1]))
        features_multi = np.hstack([features_multi, padding])
    elif features_multi.shape[1] > 12:
         features_multi = features_multi[:, :12]
    
    if binary_model:
        try:
            # 1. DETECT (Binary Model)
            pred_bin = binary_model.predict(features_binary)[0]
            
            # Get Binary Confidence
            confidence = 0.0
            if hasattr(binary_model, "predict_proba"):
                probs = binary_model.predict_proba(features_binary)
                confidence = float(max(probs[0]))
            
            is_anomaly = bool(pred_bin == 1)
            
            # 2. IDENTIFY (Multiclass Model) - Only if anomaly
            pred_type = "NORMAL"
            solution_text = None
            
            if is_anomaly:
                pred_type = "SECURITY_ANOMALY" # Default fallback
                if multiclass_model:
                    try:
                        multi_label = multiclass_model.predict(features_multi)[0]
                        if str(multi_label) != "NORMAL":
                            pred_type = str(multi_label)
                            solution_text = solutions.get(pred_type, "Detected anomaly pattern matching known attack signature.")
                    except Exception as e:
                        print(f"Multiclass prediction failed: {e}")
                
                if not solution_text:
                     solution_text = "Anomalous behavior detected. Exact type could not be classified."

            return {
                "is_anomaly": is_anomaly,
                "type": pred_type,
                "solution": solution_text,
                "confidence": confidence,
                "source": "hybrid_model"
            }
        except Exception as e:
            return {"is_anomaly": False, "error": str(e)}
    else:
        return {"is_anomaly": False, "source": "no_model"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
