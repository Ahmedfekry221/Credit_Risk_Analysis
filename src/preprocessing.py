import os
import joblib
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from imblearn.over_sampling import SMOTE

def preprocess_data(file_path):
    print(" Starting Preprocessing, Scaling & SMOTE...")
    
    # 1. Load the dataset
    df = pd.read_csv(file_path)
    
    # 2. Map the target variable 'class' to binary values (good: 1, bad: 0)
    if 'class' in df.columns:
        df['class'] = df['class'].map({'good': 1, 'bad': 0})
        
    # 3. Apply One-Hot Encoding to categorical features, dropping the first column to avoid multicollinearity
    categorical_cols = df.select_dtypes(include=['object']).columns
    df_encoded = pd.get_dummies(df, columns=categorical_cols, drop_first=True)
    
    # 4. Separate features (X) and target variable (y)
    X = df_encoded.drop('class', axis=1)
    y = df_encoded['class']
    
    # 5. Split the data into training (80%) and testing (20%) sets with stratification
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    # 6. Initialize and apply StandardScaler
    scaler = StandardScaler()
    # Fit the scaler ONLY on the training data to prevent data leakage
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test) # Only transform the test data
    
    # Convert the scaled NumPy arrays back to Pandas DataFrames to retain column names
    X_train_scaled = pd.DataFrame(X_train_scaled, columns=X_train.columns)
    X_test_scaled = pd.DataFrame(X_test_scaled, columns=X_test.columns)
    
    # ---> Save the fitted scaler for future use in production (API/Frontend) <---
    os.makedirs('models', exist_ok=True) # Create 'models' directory if it doesn't exist
    joblib.dump(scaler, 'models/scaler.pkl')
    print(" Scaler saved successfully to 'models/scaler.pkl'")
    
    # 7. Apply SMOTE to handle the class imbalance (ONLY on the training set)
    smote = SMOTE(random_state=42)
    X_train_balanced, y_train_balanced = smote.fit_resample(X_train_scaled, y_train)
    
    print(" Preprocessing and SMOTE completed successfully!")
    
    return X_train_balanced, X_test_scaled, y_train_balanced, y_test