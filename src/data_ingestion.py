import pandas as pd

def load_data(file_path):
    return pd.read_csv(file_path)

def clean_data(df):
    # Implement cleaning steps
    return df

if __name__ == "__main__":
    raw_data = load_data('data/raw/dataset_HTN.csv')
    cleaned_data = clean_data(raw_data)
    cleaned_data.to_csv('data/processed/processed_HTN.csv', index=False)
