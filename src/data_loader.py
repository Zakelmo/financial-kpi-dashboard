"""
Data Loader Module
Handles loading, cleaning, and preprocessing of financial data.
"""

import pandas as pd
import numpy as np
from pathlib import Path


def load_financial_data(file_path: str = "data/financial_data.csv") -> pd.DataFrame:
    """Load and preprocess financial data."""
    df = pd.read_csv(file_path)
    df['date'] = pd.to_datetime(df['date'])
    df = df.sort_values('date')
    
    # Add calculated columns
    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month
    df['quarter'] = df['date'].dt.quarter
    df['month_name'] = df['date'].dt.strftime('%b %Y')
    
    # Calculate margins
    df['gross_margin'] = (df['gross_profit'] / df['revenue'] * 100).round(2)
    df['operating_margin'] = (df['operating_income'] / df['revenue'] * 100).round(2)
    df['net_margin'] = (df['net_income'] / df['revenue'] * 100).round(2)
    
    # Calculate EBITDA
    df['ebitda'] = df['operating_income'] + df['depreciation']
    df['ebitda_margin'] = (df['ebitda'] / df['revenue'] * 100).round(2)
    
    return df


def load_budget_data(file_path: str = "data/budget_data.csv") -> pd.DataFrame:
    """Load budget data."""
    df = pd.read_csv(file_path)
    df['date'] = pd.to_datetime(df['date'])
    df = df.sort_values('date')
    return df


def load_cash_flow_data(file_path: str = "data/cash_flow_data.csv") -> pd.DataFrame:
    """Load cash flow data."""
    df = pd.read_csv(file_path)
    df['date'] = pd.to_datetime(df['date'])
    df = df.sort_values('date')
    return df


def merge_actual_budget(actual_df: pd.DataFrame, budget_df: pd.DataFrame) -> pd.DataFrame:
    """Merge actual and budget data for variance analysis."""
    merged = actual_df.merge(budget_df, on='date', suffixes=('_actual', '_budget'))
    
    # Calculate variances
    merged['revenue_variance'] = merged['revenue'] - merged['budget_revenue']
    merged['revenue_variance_pct'] = (merged['revenue_variance'] / merged['budget_revenue'] * 100).round(2)
    
    merged['net_income_variance'] = merged['net_income'] - merged['budget_net_income']
    merged['net_income_variance_pct'] = (merged['net_income_variance'] / merged['budget_net_income'] * 100).round(2)
    
    merged['opex_variance'] = merged['operating_expenses'] - merged['budget_operating_expenses']
    merged['opex_variance_pct'] = (merged['opex_variance'] / merged['budget_operating_expenses'] * 100).round(2)
    
    return merged


def get_years(df: pd.DataFrame) -> list:
    """Get unique years in the data."""
    return sorted(df['year'].unique().tolist())


def get_quarters(df: pd.DataFrame) -> list:
    """Get unique quarters."""
    return sorted(df['quarter'].unique().tolist())


def filter_by_period(df: pd.DataFrame, year: int = None, quarter: int = None) -> pd.DataFrame:
    """Filter data by year and/or quarter."""
    filtered = df.copy()
    if year:
        filtered = filtered[filtered['year'] == year]
    if quarter:
        filtered = filtered[filtered['quarter'] == quarter]
    return filtered


def get_ytd_data(df: pd.DataFrame, year: int) -> pd.DataFrame:
    """Get year-to-date data."""
    return df[df['year'] == year]


def get_period_comparison(df: pd.DataFrame, current_year: int, previous_year: int) -> dict:
    """Compare two periods (years)."""
    current = df[df['year'] == current_year]
    previous = df[df['year'] == previous_year]
    
    if current.empty or previous.empty:
        return {}
    
    return {
        'current_revenue': current['revenue'].sum(),
        'previous_revenue': previous['revenue'].sum(),
        'revenue_growth': ((current['revenue'].sum() / previous['revenue'].sum()) - 1) * 100,
        'current_net_income': current['net_income'].sum(),
        'previous_net_income': previous['net_income'].sum(),
        'net_income_growth': ((current['net_income'].sum() / previous['net_income'].sum()) - 1) * 100,
        'current_gross_margin': (current['gross_profit'].sum() / current['revenue'].sum()) * 100,
        'previous_gross_margin': (previous['gross_profit'].sum() / previous['revenue'].sum()) * 100,
    }


def calculate_rolling_averages(df: pd.DataFrame, window: int = 3) -> pd.DataFrame:
    """Calculate rolling averages for key metrics."""
    df = df.copy()
    df['revenue_ma'] = df['revenue'].rolling(window=window).mean()
    df['net_income_ma'] = df['net_income'].rolling(window=window).mean()
    df['gross_margin_ma'] = df['gross_margin'].rolling(window=window).mean()
    return df
