"""
Financial Analyzer Module
Contains functions for calculating financial KPIs and ratios.
"""

import pandas as pd
import numpy as np


def calculate_kpis(df: pd.DataFrame) -> dict:
    """
    Calculate key performance indicators from financial data.
    
    Args:
        df: DataFrame with financial data
        
    Returns:
        Dictionary with KPI values
    """
    latest = df.iloc[-1]
    
    # Get previous period for comparison
    if len(df) > 1:
        previous = df.iloc[-2]
        revenue_change = ((latest['revenue'] / previous['revenue']) - 1) * 100
        net_income_change = ((latest['net_income'] / previous['net_income']) - 1) * 100
    else:
        revenue_change = 0
        net_income_change = 0
    
    return {
        # Revenue metrics
        'total_revenue': latest['revenue'],
        'revenue_change': revenue_change,
        'gross_profit': latest['gross_profit'],
        'gross_margin': latest['gross_margin'],
        
        # Profitability
        'operating_income': latest['operating_income'],
        'operating_margin': latest['operating_margin'],
        'net_income': latest['net_income'],
        'net_income_change': net_income_change,
        'net_margin': latest['net_margin'],
        'ebitda': latest['ebitda'],
        'ebitda_margin': latest['ebitda_margin'],
        
        # Balance sheet
        'total_assets': latest['total_assets'],
        'total_liabilities': latest['total_liabilities'],
        'total_equity': latest['total_equity'],
        'cash': latest['cash'],
    }


def calculate_liquidity_ratios(df: pd.DataFrame) -> dict:
    """
    Calculate liquidity ratios.
    
    Args:
        df: DataFrame with financial data
        
    Returns:
        Dictionary with liquidity ratios
    """
    latest = df.iloc[-1]
    
    current_ratio = latest['current_assets'] / latest['current_liabilities']
    
    # Quick ratio = (Current Assets - Inventory) / Current Liabilities
    quick_ratio = (latest['current_assets'] - latest['inventory']) / latest['current_liabilities']
    
    # Cash ratio = Cash / Current Liabilities
    cash_ratio = latest['cash'] / latest['current_liabilities']
    
    return {
        'current_ratio': round(current_ratio, 2),
        'quick_ratio': round(quick_ratio, 2),
        'cash_ratio': round(cash_ratio, 2)
    }


def calculate_efficiency_ratios(df: pd.DataFrame) -> dict:
    """
    Calculate efficiency/activity ratios.
    
    Args:
        df: DataFrame with financial data
        
    Returns:
        Dictionary with efficiency ratios
    """
    latest = df.iloc[-1]
    
    # Asset Turnover = Revenue / Total Assets (annualized)
    asset_turnover = (latest['revenue'] * 12) / latest['total_assets']
    
    # Inventory Turnover = COGS / Inventory (annualized)
    inventory_turnover = (latest['cogs'] * 12) / latest['inventory']
    
    # Receivables Turnover = Revenue / Accounts Receivable (annualized)
    receivables_turnover = (latest['revenue'] * 12) / latest['accounts_receivable']
    
    # Days Sales Outstanding = 365 / Receivables Turnover
    dso = 365 / receivables_turnover
    
    # Days Inventory Outstanding = 365 / Inventory Turnover
    dio = 365 / inventory_turnover
    
    # Days Payable Outstanding
    payables_turnover = (latest['cogs'] * 12) / latest['accounts_payable']
    dpo = 365 / payables_turnover
    
    # Cash Conversion Cycle = DSO + DIO - DPO
    ccc = dso + dio - dpo
    
    return {
        'asset_turnover': round(asset_turnover, 2),
        'inventory_turnover': round(inventory_turnover, 2),
        'receivables_turnover': round(receivables_turnover, 2),
        'dso': round(dso, 1),
        'dio': round(dio, 1),
        'dpo': round(dpo, 1),
        'cash_conversion_cycle': round(ccc, 1)
    }


def calculate_leverage_ratios(df: pd.DataFrame) -> dict:
    """
    Calculate leverage/solvency ratios.
    
    Args:
        df: DataFrame with financial data
        
    Returns:
        Dictionary with leverage ratios
    """
    latest = df.iloc[-1]
    
    # Debt to Equity = Total Liabilities / Total Equity
    debt_to_equity = latest['total_liabilities'] / latest['total_equity']
    
    # Debt Ratio = Total Liabilities / Total Assets
    debt_ratio = latest['total_liabilities'] / latest['total_assets']
    
    # Interest Coverage = Operating Income / Interest Expense
    interest_coverage = latest['operating_income'] / latest['interest_expense'] if latest['interest_expense'] > 0 else 0
    
    # Long-term Debt to Equity
    lt_debt_to_equity = latest['long_term_debt'] / latest['total_equity']
    
    return {
        'debt_to_equity': round(debt_to_equity, 2),
        'debt_ratio': round(debt_ratio, 2),
        'interest_coverage': round(interest_coverage, 2),
        'lt_debt_to_equity': round(lt_debt_to_equity, 2)
    }


def calculate_profitability_ratios(df: pd.DataFrame) -> dict:
    """
    Calculate profitability ratios.
    
    Args:
        df: DataFrame with financial data
        
    Returns:
        Dictionary with profitability ratios
    """
    latest = df.iloc[-1]
    
    # Return on Assets = Net Income / Total Assets (annualized)
    roa = (latest['net_income'] * 12) / latest['total_assets'] * 100
    
    # Return on Equity = Net Income / Total Equity (annualized)
    roe = (latest['net_income'] * 12) / latest['total_equity'] * 100
    
    # Return on Invested Capital
    invested_capital = latest['total_equity'] + latest['long_term_debt']
    roic = (latest['operating_income'] * 12) / invested_capital * 100
    
    return {
        'roa': round(roa, 2),
        'roe': round(roe, 2),
        'roic': round(roic, 2),
        'gross_margin': latest['gross_margin'],
        'operating_margin': latest['operating_margin'],
        'net_margin': latest['net_margin']
    }


def calculate_annual_summary(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate annual summary statistics.
    
    Args:
        df: DataFrame with financial data
        
    Returns:
        DataFrame with annual summaries
    """
    annual = df.groupby('year').agg({
        'revenue': 'sum',
        'gross_profit': 'sum',
        'operating_income': 'sum',
        'net_income': 'sum',
        'ebitda': 'sum',
        'total_assets': 'last',
        'total_equity': 'last',
        'cash': 'last'
    }).reset_index()
    
    # Calculate margins
    annual['gross_margin'] = (annual['gross_profit'] / annual['revenue'] * 100).round(2)
    annual['operating_margin'] = (annual['operating_income'] / annual['revenue'] * 100).round(2)
    annual['net_margin'] = (annual['net_income'] / annual['revenue'] * 100).round(2)
    
    # Calculate YoY growth
    annual['revenue_growth'] = annual['revenue'].pct_change() * 100
    annual['net_income_growth'] = annual['net_income'].pct_change() * 100
    
    return annual


def calculate_quarterly_summary(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate quarterly summary statistics.
    
    Args:
        df: DataFrame with financial data
        
    Returns:
        DataFrame with quarterly summaries
    """
    quarterly = df.groupby(['year', 'quarter']).agg({
        'revenue': 'sum',
        'gross_profit': 'sum',
        'operating_income': 'sum',
        'net_income': 'sum',
        'ebitda': 'sum'
    }).reset_index()
    
    quarterly['period'] = quarterly['year'].astype(str) + ' Q' + quarterly['quarter'].astype(str)
    
    # Calculate margins
    quarterly['gross_margin'] = (quarterly['gross_profit'] / quarterly['revenue'] * 100).round(2)
    quarterly['net_margin'] = (quarterly['net_income'] / quarterly['revenue'] * 100).round(2)
    
    return quarterly


def calculate_revenue_breakdown(df: pd.DataFrame) -> dict:
    """
    Calculate revenue breakdown by segment.
    
    Args:
        df: DataFrame with financial data
        
    Returns:
        Dictionary with revenue breakdowns
    """
    latest = df.iloc[-1]
    total_revenue = latest['revenue']
    
    # Product breakdown
    product_breakdown = {
        'Software': {'value': latest['product_software'], 'pct': latest['product_software'] / total_revenue * 100},
        'Services': {'value': latest['product_services'], 'pct': latest['product_services'] / total_revenue * 100},
        'Hardware': {'value': latest['product_hardware'], 'pct': latest['product_hardware'] / total_revenue * 100}
    }
    
    # Region breakdown
    region_breakdown = {
        'North America': {'value': latest['region_north_america'], 'pct': latest['region_north_america'] / total_revenue * 100},
        'Europe': {'value': latest['region_europe'], 'pct': latest['region_europe'] / total_revenue * 100},
        'Asia': {'value': latest['region_asia'], 'pct': latest['region_asia'] / total_revenue * 100},
        'Other': {'value': latest['region_other'], 'pct': latest['region_other'] / total_revenue * 100}
    }
    
    # Customer segment breakdown
    customer_breakdown = {
        'Enterprise': {'value': latest['customers_enterprise'], 'pct': latest['customers_enterprise'] / total_revenue * 100},
        'SMB': {'value': latest['customers_smb'], 'pct': latest['customers_smb'] / total_revenue * 100},
        'Consumer': {'value': latest['customers_consumer'], 'pct': latest['customers_consumer'] / total_revenue * 100}
    }
    
    return {
        'by_product': product_breakdown,
        'by_region': region_breakdown,
        'by_customer': customer_breakdown
    }


def get_health_indicators(df: pd.DataFrame) -> list:
    """
    Generate financial health indicators.
    
    Args:
        df: DataFrame with financial data
        
    Returns:
        List of health indicator dictionaries
    """
    liquidity = calculate_liquidity_ratios(df)
    leverage = calculate_leverage_ratios(df)
    profitability = calculate_profitability_ratios(df)
    
    indicators = []
    
    # Current Ratio
    cr = liquidity['current_ratio']
    indicators.append({
        'metric': 'Current Ratio',
        'value': cr,
        'status': 'Good' if cr >= 1.5 else ('Warning' if cr >= 1.0 else 'Critical'),
        'benchmark': '≥ 1.5',
        'description': 'Ability to pay short-term obligations'
    })
    
    # Quick Ratio
    qr = liquidity['quick_ratio']
    indicators.append({
        'metric': 'Quick Ratio',
        'value': qr,
        'status': 'Good' if qr >= 1.0 else ('Warning' if qr >= 0.7 else 'Critical'),
        'benchmark': '≥ 1.0',
        'description': 'Liquid assets coverage of current liabilities'
    })
    
    # Debt to Equity
    de = leverage['debt_to_equity']
    indicators.append({
        'metric': 'Debt to Equity',
        'value': de,
        'status': 'Good' if de <= 1.0 else ('Warning' if de <= 2.0 else 'Critical'),
        'benchmark': '≤ 1.0',
        'description': 'Financial leverage level'
    })
    
    # Interest Coverage
    ic = leverage['interest_coverage']
    indicators.append({
        'metric': 'Interest Coverage',
        'value': ic,
        'status': 'Good' if ic >= 3.0 else ('Warning' if ic >= 1.5 else 'Critical'),
        'benchmark': '≥ 3.0',
        'description': 'Ability to service debt'
    })
    
    # Return on Equity
    roe = profitability['roe']
    indicators.append({
        'metric': 'Return on Equity',
        'value': f"{roe}%",
        'status': 'Good' if roe >= 15 else ('Warning' if roe >= 10 else 'Critical'),
        'benchmark': '≥ 15%',
        'description': 'Shareholder return efficiency'
    })
    
    # Net Margin
    nm = profitability['net_margin']
    indicators.append({
        'metric': 'Net Profit Margin',
        'value': f"{nm}%",
        'status': 'Good' if nm >= 15 else ('Warning' if nm >= 10 else 'Critical'),
        'benchmark': '≥ 15%',
        'description': 'Bottom line profitability'
    })
    
    return indicators
