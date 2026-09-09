import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from imblearn.over_sampling import SMOTE

def preprocess_data(file_path):
    print(" Starting Preprocessing, Scaling & SMOTE...")
    
    # 1. Load data
    df = pd.read_csv(file_path)
    
    # 2. Map target variable (class) to binary: good -> 1, bad -> 0
    if 'class' in df.columns:
        df['class'] = df['class'].map({'good': 1, 'bad': 0})
        
    # 3. Handle categorical columns using One-Hot Encoding
    categorical_cols = df.select_dtypes(include=['object']).columns
    df_encoded = pd.get_dummies(df, columns=categorical_cols, drop_first=True)
    
    # 4. Separate features (X) and target (y)
    X = df_encoded.drop('class', axis=1)
    y = df_encoded['class']
    
    # 5. Split data into training and testing sets (80% train, 20% test)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    # 6. Feature Scaling (Standardization)
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    X_train_scaled = pd.DataFrame(X_train_scaled, columns=X_train.columns)
    X_test_scaled = pd.DataFrame(X_test_scaled, columns=X_test.columns)
    
    # 7. Apply SMOTE to handle class imbalance (ONLY on training data)
    print(f" Before SMOTE: Good (1): {sum(y_train==1)}, Bad (0): {sum(y_train==0)}")
    smote = SMOTE(random_state=42)
    X_train_balanced, y_train_balanced = smote.fit_resample(X_train_scaled, y_train)
    print(f" After SMOTE : Good (1): {sum(y_train_balanced==1)}, Bad (0): {sum(y_train_balanced==0)}")
    
    print(" Preprocessing and SMOTE completed successfully!")
    
    return X_train_balanced, X_test_scaled, y_train_balanced, y_test