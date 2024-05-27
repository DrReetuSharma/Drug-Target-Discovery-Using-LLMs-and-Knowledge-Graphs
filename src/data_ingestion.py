# src/data_ingestion.py
import pandas as pd

def load_data(file_path):
    print(f"Loading data from {file_path}")
    return pd.read_csv(file_path)

def clean_data(df):
    print("Cleaning data")
    # Example cleaning steps
    df.dropna(inplace=True)  # Drop missing values
    df.rename(columns=lambda x: x.strip().lower().replace(' ', '_'), inplace=True)  # Normalize column names
    return df

if __name__ == "__main__":
    raw_data = load_data('data/raw/dataset_HTN.csv')
    cleaned_data = clean_data(raw_data)
    cleaned_data.to_csv('data/processed/processed_HTN.csv', index=False)
    print("Data cleaned and saved to data/processed/processed_HTN.csv")
