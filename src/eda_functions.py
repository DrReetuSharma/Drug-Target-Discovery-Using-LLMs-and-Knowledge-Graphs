# scripts/eda.py
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def load_data(file_path):
    """Load dataset from a CSV file."""
    print(f"Loading data from {file_path}")
    return pd.read_csv(file_path)

def describe_data(df):
    """Print and save descriptive statistics of the dataset."""
    description = df.describe()
    print(description)
    description.to_csv('plots/descriptive_statistics.csv')
    print("Descriptive statistics saved to plots/descriptive_statistics.csv")

def plot_distributions(df):
    """Plot and save distributions of numerical features."""
    print("Plotting distributions")
    numerical_features = df.select_dtypes(include=['float64', 'int64']).columns
    for feature in numerical_features:
        plt.figure(figsize=(10, 6))
        sns.histplot(df[feature], kde=True)
        plt.title(f'Distribution of {feature}')
        plt.savefig(f'plots/{feature}_distribution.png')
        plt.close()
    print("Distributions saved to plots/")

def plot_correlations(df):
    """Plot and save correlation heatmap."""
    print("Plotting correlations")
    correlation_matrix = df.corr()
    plt.figure(figsize=(12, 8))
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt='.2f')
    plt.title('Correlation Heatmap')
    plt.savefig('plots/correlation_heatmap.png')
    plt.close()
    print("Correlation heatmap saved to plots/correlation_heatmap.png")

def plot_pairwise_relationships(df):
    """Plot and save pairwise relationships in the dataset."""
    print("Plotting pairwise relationships")
    sns.pairplot(df)
    plt.savefig('plots/pairplot.png')
    plt.close()
    print("Pairwise relationships saved to plots/pairplot.png")

if __name__ == "__main__":
    # Load the preprocessed dataset
    data = load_data('data/processed/preprocessed_HTN.csv')
    
    # Generate descriptive statistics
    describe_data(data)
    
    # Plot distributions of numerical features
    plot_distributions(data)
    
    # Plot correlation heatmap
    plot_correlations(data)
    
    # Plot pairwise relationships
    plot_pairwise_relationships(data)

