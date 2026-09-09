import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, precision_score, recall_score, f1_score

def train_and_evaluate_models(X_train, X_test, y_train, y_test):
    """
    Trains Logistic Regression and Random Forest models.
    Evaluates them using Precision, Recall, and F1-Score for imbalanced data.
    """
    print(" Initializing and Training Models...")
    
    # 1. Define models with class_weight='balanced' to handle class imbalance
    models = {
        "Logistic Regression": LogisticRegression(max_iter=1000, random_state=42, class_weight='balanced'),
        "Random Forest": RandomForestClassifier(random_state=42, class_weight='balanced')
    }
    
    trained_models = {}
    
    for name, model in models.items():
        print(f"\n{'='*40}")
        print(f" Model: {name}")
        print(f"{'='*40}")
        
        # 1. training the model
        model.fit(X_train, y_train)
        trained_models[name] = model
        
        # 2. making predictions
        y_pred = model.predict(X_test)
        
        # 3. extracting important metrics (focusing on Class 0 which is Bad Credit / defaulters)
        # we use pos_label=0 because we are interested in detecting defaulters primarily
        accuracy = accuracy_score(y_test, y_pred)
        precision = precision_score(y_test, y_pred, pos_label=0)
        recall = recall_score(y_test, y_pred, pos_label=0)
        f1 = f1_score(y_test, y_pred, pos_label=0)
        
        print(f" Accuracy : {accuracy * 100:.2f}%")
        print(f" Recall (Detecting Bad Credit)   : {recall:.2f} (Sensitivity)")
        print(f" Precision (Correct Bad Credit)  : {precision:.2f}")
        print(f" F1-Score (Balance)             : {f1:.2f}")
        
        print("\n Full Classification Report:")
        print(classification_report(y_test, y_pred))
        
    return trained_models