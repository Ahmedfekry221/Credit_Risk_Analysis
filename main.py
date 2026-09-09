import os
from src.preprocessing import preprocess_data
from src.model_training import train_and_evaluate_models

def main():
    print(" Starting Professional Credit Risk Pipeline...")
    
    # 1. Define the data path (ensure the file exists at this exact location)
    data_path = os.path.join('data', 'raw', 'german_credit_data.csv')
    
    # 2. Data Preprocessing (Data loading is now handled inside this function)
    X_train, X_test, y_train, y_test = preprocess_data(data_path)
    
    # 3. Model Training, Comparison, and Evaluation
    models = train_and_evaluate_models(X_train, X_test, y_train, y_test)
    
    print("\n Pipeline executed successfully!")

if __name__ == "__main__":
    main()