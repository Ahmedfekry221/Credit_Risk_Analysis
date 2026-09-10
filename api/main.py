import joblib
import pandas as pd
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Any

app = FastAPI(
    title="Credit Risk Prediction API",
    description="API for evaluating bank loans using Logistic Regression trained on UCI German Credit Data.",
    version="2.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load saved artifacts
scaler = joblib.load('models/scaler.pkl')
model = joblib.load('models/logistic_model.pkl')
expected_columns = list(scaler.feature_names_in_)

class CustomerData(BaseModel):
    data: Dict[str, Any]

@app.get("/")
def read_root():
    return {"message": "Server is running smoothly! 🚀"}

@app.post("/predict")
def predict_risk(customer: CustomerData):
    try:
        raw_data = customer.data
        
        # 1. Start with a zeroed dataframe matching EXACT training columns
        df_aligned = pd.DataFrame(0, index=[0], columns=expected_columns)

        # 2. Map Numerical Features (Case-sensitive matching)
        # Note: Handling lower/upper case potential variations
        num_mapping = {
            'duration': ['duration', 'Duration', 'duration_in_month'],
            'credit_amount': ['credit_amount', 'Credit amount', 'credit_amount_val'],
            'installment_commitment': ['installment_commitment', 'installment_rate'],
            'present_residence': ['present_residence', 'residence_since'],
            'age': ['age', 'Age'],
            'existing_credits': ['existing_credits', 'number_credits'],
            'num_dependents': ['num_dependents', 'people_liable']
        }

        for model_col, possible_keys in num_mapping.items():
            for key in possible_keys:
                if key in raw_data:
                    if model_col in df_aligned.columns:
                        df_aligned[model_col] = float(raw_data[key])
                    break

        # 3. Map Categorical Features to One-Hot Columns manually
        # Format in train: FeatureName_Value (e.g. checking_status_<0, housing_own)
        for feature, val in raw_data.items():
            if isinstance(val, str):
                column_name = f"{feature}_{val}"
                if column_name in df_aligned.columns:
                    df_aligned[column_name] = 1

        # 4. Scale features
        X_scaled = scaler.transform(df_aligned)

        # 5. Model Inference
        prediction = int(model.predict(X_scaled)[0])
        probability = model.predict_proba(X_scaled)[0]

        result = "Good Credit Risk " if prediction == 1 else "Bad Credit Risk ❌"

        return {
            "status": "success",
            "prediction_label": result,
            "prediction_code": prediction,
            "confidence_good": f"{probability[1] * 100:.2f}%",
            "confidence_bad": f"{probability[0] * 100:.2f}%"
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Prediction Error: {str(e)}")