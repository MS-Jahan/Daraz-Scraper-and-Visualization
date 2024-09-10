import pandas as pd

def descriptive_stats(df):
    """
    Calculates descriptive statistics for numerical columns.
    """
    numerical_cols = df.select_dtypes(include=['number']).columns
    return df[numerical_cols].describe()

def price_analysis(df):
    """
    Analyzes product prices.
    """
    price_stats = df['current_price'].describe()
    price_ranges = pd.cut(df['current_price'], bins=[0, 1000, 5000, 10000, float('inf')],
                         labels=['<1000', '1000-5000', '5000-10000', '>10000'])
    price_range_counts = price_ranges.value_counts()
    return price_stats, price_range_counts

def discount_analysis(df):
    """
    Analyzes product discounts.
    """
    avg_discount = df['discount_percentage'].mean()
    max_discount_products = df.loc[df['discount_percentage'] == df['discount_percentage'].max()]
    return avg_discount, max_discount_products

def rating_review_analysis(df):
    """
    Analyzes product ratings and reviews.
    """
    avg_rating = df['rating'].mean()
    rating_distribution = df['rating'].value_counts()
    return avg_rating, rating_distribution

def location_analysis(df):
    """
    Analyzes product locations.
    """
    location_counts = df['location'].value_counts()
    return location_counts

def correlation_analysis(df):
    """
    Analyzes correlations between numerical columns.
    """
    numerical_cols = df.select_dtypes(include=['number']).columns
    correlations = df[numerical_cols].corr()
    return correlations