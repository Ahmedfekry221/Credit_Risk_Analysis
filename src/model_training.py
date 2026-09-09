import os
import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, precision_score, recall_score, f1_score

def train_and_evaluate_models(X_train, X_test, y_train, y_test):
    print(" Initializing and Training Models...")
    
    # Initialize models with 'balanced' class_weight to handle imbalanced data
    models = {
        "Logistic Regression": LogisticRegression(max_iter=1000, random_state=42, class_weight='balanced'),
        "Random Forest": RandomForestClassifier(random_state=42, class_weight='balanced')
    }
    
    trained_models = {}
    
    for name, model in models.items():
        print(f"\n{'='*40}")
        print(f" Model: {name}")
        print(f"{'='*40}")
        
        # 1. Train the model
        model.fit(X_train, y_train)
        trained_models[name] = model
        
        # 2. Make predictions on the test set
        y_pred = model.predict(X_test)
        
        # 3. Calculate evaluation metrics focusing on the minority class (pos_label=0 for bad credit)
        accuracy = accuracy_score(y_test, y_pred)
        precision = precision_score(y_test, y_pred, pos_label=0)
        recall = recall_score(y_test, y_pred, pos_label=0)
        f1 = f1_score(y_test, y_pred, pos_label=0)
        
        # Print the metrics
        print(f" Accuracy : {accuracy * 100:.2f}%")
        print(f" Recall   : {recall:.2f}")
        print(f" Precision: {precision:.2f}")
        print(f" F1-Score : {f1:.2f}")
        
        # ---> Save the best performing model (Logistic Regression) for deployment <---
        if name == "Logistic Regression":
            os.makedirs('models', exist_ok=True)
            joblib.dump(model, 'models/logistic_model.pkl')
            print(f" {name} model saved successfully to 'models/logistic_model.pkl'")
            
    return trained_models