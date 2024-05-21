import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
import spacy
from tqdm import tqdm

# Load the spaCy model
nlp = spacy.load('en_core_web_sm')

def clean_text(text):
    """
    Clean and preprocess text data.
    """
    doc = nlp(text)
    tokens = [token.lemma_ for token in doc if not token.is_stop and not token.is_punct]
    return ' '.join(tokens)

def preprocess_data(input_file, output_file):
    """
    Preprocess the input data and save to output file.
    """
    # Load the dataset
    df = pd.read_csv(input_file)

    # Clean the text data
    tqdm.pandas(desc="Cleaning text")
    df['cleaned_text'] = df['text'].progress_apply(clean_text)

    # Save the preprocessed data
    df.to_csv(output_file, index=False)

if __name__ == "__main__":
    input_file = 'data/raw_data.csv'
    output_file = 'data/cleaned_data.csv'
    preprocess_data(input_file, output_file)
