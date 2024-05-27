# src/data_preprocessing.py
import pandas as pd
from sklearn.preprocessing import StandardScaler, OneHotEncoder

def preprocess_data(df):
    print("Preprocessing data")
    # Example preprocessing steps
    scaler = StandardScaler()
    df[['age', 'blood_pressure']] = scaler.fit_transform(df[['age', 'blood_pressure']])
    
    encoder = OneHotEncoder()
    encoded_features = encoder.fit_transform(df[['gender']]).toarray()
    df = df.join(pd.DataFrame(encoded_features, columns=encoder.categories_[0]))
    
    return df.drop('gender', axis=1)

if __name__ == "__main__":
    data = pd.read_csv('data/processed/processed_HTN.csv')
    preprocessed_data = preprocess_data(data)
    preprocessed_data.to_csv('data/processed/preprocessed_HTN.csv', index=False)
    print("Data preprocessed and saved to data/processed/preprocessed_HTN.csv")
