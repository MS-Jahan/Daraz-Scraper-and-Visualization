import pandas as pd
from config import get_db

def clean_data(df):
    """
    Performs data cleaning tasks on the DataFrame (if needed).
    """
    # Example: Remove rows with missing values in 'name' column
    df.dropna(subset=['name'], inplace=True)

    # Example: Convert 'current_price' and 'original_price' to numeric
    df['current_price'] = pd.to_numeric(df['current_price'])
    df['original_price'] = pd.to_numeric(df['original_price'])

    return df

def prepare_data(data_json):
    """
    Extracts, cleans, and prepares the data for analysis.
    """
    df = pd.DataFrame.from_records(data_json)
    df = clean_data(df)
    return df