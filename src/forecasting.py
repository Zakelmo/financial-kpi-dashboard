"""
Forecasting Module
Contains functions for time series forecasting of financial metrics.
"""

import pandas as pd
import numpy as np
from statsmodels.tsa.holtwinters import ExponentialSmoothing
from statsmodels.tsa.seasonal import seasonal_decompose
import warnings
warnings.filterwarnings('ignore')


def forecast_revenue(df: pd.DataFrame, periods: int = 6) -> dict:
    """
    Forecast revenue using Holt-Winters Exponential Smoothing.
    
    Args:
        df: DataFrame with financial data
        periods: Number of periods to forecast
        
    Returns:
        Dictionary with forecast data and metrics
    """
    # Prepare data
    revenue_series = df.set_index('date')['revenue']
    
    try:
        # Fit Holt-Winters model with multiplicative seasonality
        model = ExponentialSmoothing(
            revenue_series,
            seasonal_periods=12,
            trend='add',
            seasonal='mul',
            damped_trend=True
        ).fit(optimized=True)
        
        # Generate forecast
        forecast = model.forecast(periods)
        
        # Calculate confidence intervals (approximate)
        residuals = model.resid
        std_error = residuals.std()
        
        forecast_dates = pd.date_range(
            start=df['date'].max() + pd.DateOffset(months=1),
            periods=periods,
            freq='MS'
        )
        
        forecast_df = pd.DataFrame({
            'date': forecast_dates,
            'forecast': forecast.values,
            'lower_bound': forecast.values - 1.96 * std_error,
            'upper_bound': forecast.values + 1.96 * std_error
        })
        
        # Calculate accuracy metrics on training data
        fitted_values = model.fittedvalues
        actual = revenue_series[fitted_values.index]
        
        mae = np.mean(np.abs(actual - fitted_values))
        mape = np.mean(np.abs((actual - fitted_values) / actual)) * 100
        rmse = np.sqrt(np.mean((actual - fitted_values) ** 2))
        
        return {
            'forecast_df': forecast_df,
            'historical': df[['date', 'revenue']],
            'mae': round(mae, 2),
            'mape': round(mape, 2),
            'rmse': round(rmse, 2),
            'model_params': {
                'alpha': round(model.params['smoothing_level'], 4),
                'beta': round(model.params['smoothing_trend'], 4),
                'gamma': round(model.params['smoothing_seasonal'], 4)
            }
        }
    except Exception as e:
        # Fallback to simple moving average forecast
        return simple_forecast(df, 'revenue', periods)


def forecast_metric(df: pd.DataFrame, metric: str, periods: int = 6) -> dict:
    """
    Forecast any metric using exponential smoothing.
    
    Args:
        df: DataFrame with financial data
        metric: Column name to forecast
        periods: Number of periods to forecast
        
    Returns:
        Dictionary with forecast data
    """
    series = df.set_index('date')[metric]
    
    try:
        model = ExponentialSmoothing(
            series,
            seasonal_periods=12,
            trend='add',
            seasonal='add',
            damped_trend=True
        ).fit(optimized=True)
        
        forecast = model.forecast(periods)
        
        forecast_dates = pd.date_range(
            start=df['date'].max() + pd.DateOffset(months=1),
            periods=periods,
            freq='MS'
        )
        
        forecast_df = pd.DataFrame({
            'date': forecast_dates,
            'forecast': forecast.values
        })
        
        return {
            'forecast_df': forecast_df,
            'historical': df[['date', metric]],
            'metric': metric
        }
    except Exception:
        return simple_forecast(df, metric, periods)


def simple_forecast(df: pd.DataFrame, metric: str, periods: int = 6) -> dict:
    """
    Simple moving average forecast as fallback.
    
    Args:
        df: DataFrame with financial data
        metric: Column name to forecast
        periods: Number of periods to forecast
        
    Returns:
        Dictionary with forecast data
    """
    series = df[metric]
    
    # Calculate growth rate
    growth_rate = series.pct_change().mean()
    last_value = series.iloc[-1]
    
    forecast_dates = pd.date_range(
        start=df['date'].max() + pd.DateOffset(months=1),
        periods=periods,
        freq='MS'
    )
    
    forecast_values = [last_value * (1 + growth_rate) ** (i + 1) for i in range(periods)]
    
    forecast_df = pd.DataFrame({
        'date': forecast_dates,
        'forecast': forecast_values,
        'lower_bound': [v * 0.9 for v in forecast_values],
        'upper_bound': [v * 1.1 for v in forecast_values]
    })
    
    return {
        'forecast_df': forecast_df,
        'historical': df[['date', metric]],
        'mae': 0,
        'mape': 0,
        'rmse': 0,
        'model_params': {'method': 'simple_growth'}
    }


def decompose_series(df: pd.DataFrame, metric: str = 'revenue') -> dict:
    """
    Decompose time series into trend, seasonal, and residual components.
    
    Args:
        df: DataFrame with financial data
        metric: Column name to decompose
        
    Returns:
        Dictionary with decomposition results
    """
    series = df.set_index('date')[metric]
    
    try:
        decomposition = seasonal_decompose(series, model='multiplicative', period=12)
        
        return {
            'trend': decomposition.trend,
            'seasonal': decomposition.seasonal,
            'residual': decomposition.resid,
            'original': series
        }
    except Exception:
        return {
            'trend': series,
            'seasonal': None,
            'residual': None,
            'original': series
        }


def calculate_growth_projections(df: pd.DataFrame) -> dict:
    """
    Calculate various growth projections.
    
    Args:
        df: DataFrame with financial data
        
    Returns:
        Dictionary with growth projections
    """
    # Historical growth rates
    df_annual = df.groupby('year')['revenue'].sum()
    
    if len(df_annual) >= 2:
        yoy_growth = df_annual.pct_change().dropna()
        avg_growth = yoy_growth.mean()
        cagr = ((df_annual.iloc[-1] / df_annual.iloc[0]) ** (1 / (len(df_annual) - 1))) - 1
    else:
        avg_growth = 0
        cagr = 0
    
    # Monthly growth
    monthly_growth = df['revenue'].pct_change().mean()
    
    # Project next year
    last_year_revenue = df[df['year'] == df['year'].max()]['revenue'].sum()
    
    projections = {
        'conservative': last_year_revenue * (1 + avg_growth * 0.5),
        'base': last_year_revenue * (1 + avg_growth),
        'optimistic': last_year_revenue * (1 + avg_growth * 1.5)
    }
    
    return {
        'avg_annual_growth': round(avg_growth * 100, 2),
        'cagr': round(cagr * 100, 2),
        'monthly_growth': round(monthly_growth * 100, 2),
        'projections': projections,
        'historical_annual': df_annual.to_dict()
    }


def scenario_analysis(df: pd.DataFrame, scenarios: dict = None) -> pd.DataFrame:
    """
    Perform scenario analysis on revenue projections.
    
    Args:
        df: DataFrame with financial data
        scenarios: Dictionary with scenario parameters
        
    Returns:
        DataFrame with scenario results
    """
    if scenarios is None:
        scenarios = {
            'pessimistic': {'growth': -0.05, 'margin_change': -0.02},
            'base': {'growth': 0.10, 'margin_change': 0},
            'optimistic': {'growth': 0.20, 'margin_change': 0.02}
        }
    
    base_revenue = df['revenue'].iloc[-1] * 12  # Annualized
    base_margin = df['net_margin'].iloc[-1] / 100
    
    results = []
    for scenario_name, params in scenarios.items():
        projected_revenue = base_revenue * (1 + params['growth'])
        projected_margin = base_margin + params['margin_change']
        projected_net_income = projected_revenue * projected_margin
        
        results.append({
            'scenario': scenario_name,
            'revenue': projected_revenue,
            'growth_rate': params['growth'] * 100,
            'net_margin': projected_margin * 100,
            'net_income': projected_net_income
        })
    
    return pd.DataFrame(results)
