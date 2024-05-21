import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def load_data(file_path):
    """
    Load data from a CSV file.
    """
    return pd.read_csv(file_path)

def plot_distributions(df, column):
    """
    Plot distribution of a specified column.
    """
    plt.figure(figsize=(10, 6))
    sns.histplot(df[column], kde=True)
    plt.title(f'Distribution of {column}')
    plt.xlabel(column)
    plt.ylabel('Frequency')
    plt.show()

def plot_correlations(df):
    """
    Plot correlation matrix.
    """
    plt.figure(figsize=(12, 8))
    sns.heatmap(df.corr(), annot=True, cmap='coolwarm', fmt='.2f')
    plt.title('Correlation Matrix')
    plt.show()

def eda(file_path):
    """
    Perform exploratory data analysis.
    """
    df = load_data(file_path)
    
    # Plot distributions for numerical columns
    numerical_columns = df.select_dtypes(include=['int64', 'float64']).columns
    for column in numerical_columns:
        plot_distributions(df, column)
    
    # Plot correlation matrix
    plot_correlations(df)

if __name__ == "__main__":
    data_file = 'data/cleaned_data.csv'
    eda(data_file)
