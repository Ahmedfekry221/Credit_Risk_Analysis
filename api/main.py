import joblib
import pandas as pd
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Any

app = FastAPI(
    title="Credit Risk Prediction API",
    description="API for evaluating bank loans using Logistic Regression.",
    version="1.0"
)

# 1. Load the saved model and scaler (Loaded once when server starts)
try:
    scaler = joblib.load('models/scaler.pkl')
    model = joblib.load('models/logistic_model.pkl')
    # Extract the exact 48 feature names the model was trained on
    expected_columns = scaler.feature_names_in_
except Exception as e:
    print(f"Error loading models: {e}")

# 2. Define the expected incoming data structure from React
class CustomerData(BaseModel):
    data: Dict[str, Any]

    # Providing a default example for Swagger UI
    class Config:
        json_schema_extra = {
            "example": {
                "data": {
                    "Age": 30,
                    "Sex": "male",
                    "Job": 2,
                    "Housing": "own",
                    "Saving accounts": "little",
                    "Checking account": "moderate",
                    "Credit amount": 2500,
                    "Duration": 12,
                    "Purpose": "radio/TV"
                }
            }
        }

@app.get("/")
def read_root():
    return {"message": "Welcome to the Credit Risk API! 🚀 Server is running."}

# 3. The Prediction Endpoint
@app.post("/predict")
def predict_risk(customer: CustomerData):
    try:
        # A. Convert incoming JSON from React to a Pandas DataFrame (1 row)
        df = pd.DataFrame([customer.data])
        
        # B. Apply One-Hot Encoding to categorical columns
        categorical_cols = df.select_dtypes(include=['object', 'string']).columns
        df_encoded = pd.get_dummies(df, columns=categorical_cols, drop_first=True)
        
        # C. Align columns with training data (Fill missing dummy columns with 0)
        df_aligned = df_encoded.reindex(columns=expected_columns, fill_value=0)
        
        # D. Scale the features using the saved scaler
        X_scaled = scaler.transform(df_aligned)
        
        # E. Make the Prediction
        prediction = int(model.predict(X_scaled)[0])
        probability = model.predict_proba(X_scaled)[0]
        
        # F. Return the response
        result = "Good Credit Risk ✅" if prediction == 1 else "Bad Credit Risk ❌ (High Default Probability)"
        
        return {
            "status": "success",
            "prediction_label": result,
            "prediction_code": prediction,
            "confidence_good": f"{probability[1] * 100:.2f}%",
            "confidence_bad": f"{probability[0] * 100:.2f}%"
        }
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Prediction Error: {str(e)}")