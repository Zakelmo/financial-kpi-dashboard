"""
Financial KPI Dashboard
A comprehensive financial analytics dashboard built with Streamlit.

Author: Zakaria El Morabit
"""

import streamlit as st
import pandas as pd
from pathlib import Path

# Import custom modules
from src.data_loader import (
    load_financial_data, load_budget_data, load_cash_flow_data,
    merge_actual_budget, get_years, filter_by_period,
    get_period_comparison, calculate_rolling_averages
)
from src.financial_analyzer import (
    calculate_kpis, calculate_liquidity_ratios, calculate_efficiency_ratios,
    calculate_leverage_ratios, calculate_profitability_ratios,
    calculate_annual_summary, calculate_quarterly_summary,
    calculate_revenue_breakdown, get_health_indicators
)
from src.forecasting import (
    forecast_revenue, forecast_metric, calculate_growth_projections,
    scenario_analysis
)
from src.visualizations import (
    create_revenue_trend_chart, create_profitability_chart,
    create_income_statement_waterfall, create_revenue_breakdown_pie,
    create_budget_variance_chart, create_cash_flow_chart,
    create_forecast_chart, create_financial_ratios_gauge,
    create_quarterly_comparison_chart, create_health_indicator_table,
    create_scenario_chart
)


# Page configuration
st.set_page_config(
    page_title="Financial KPI Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load custom CSS
def load_css():
    css_file = Path("assets/style.css")
    if css_file.exists():
        with open(css_file) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()


# Cache data loading
@st.cache_data
def get_financial_data():
    return load_financial_data()

@st.cache_data
def get_budget_data():
    return load_budget_data()

@st.cache_data
def get_cash_flow():
    return load_cash_flow_data()


def format_currency(value: float, decimals: int = 0) -> str:
    """Format number as currency."""
    if abs(value) >= 1_000_000:
        return f"${value/1_000_000:.{decimals}f}M"
    elif abs(value) >= 1_000:
        return f"${value/1_000:.{decimals}f}K"
    return f"${value:,.{decimals}f}"


def format_percentage(value: float, decimals: int = 1) -> str:
    """Format number as percentage."""
    return f"{value:.{decimals}f}%"


# Main application
def main():
    # Load data
    df = get_financial_data()
    budget_df = get_budget_data()
    cash_flow_df = get_cash_flow()
    
    # Add rolling averages
    df = calculate_rolling_averages(df)
    
    # Header
    st.markdown("""
    <div style="background: linear-gradient(90deg, #0D47A1 0%, #1565C0 100%); 
                padding: 20px; border-radius: 10px; margin-bottom: 20px;">
        <h1 style="color: white; margin: 0;">📊 Financial KPI Dashboard</h1>
        <p style="color: #BBDEFB; margin: 5px 0 0 0;">
            Track revenue, profitability, cash flow, and key financial ratios
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar filters
    with st.sidebar:
        st.header("📅 Filters")
        
        years = get_years(df)
        selected_year = st.selectbox(
            "Select Year",
            options=years,
            index=len(years) - 1
        )
        
        quarters = [1, 2, 3, 4]
        selected_quarter = st.selectbox(
            "Select Quarter (optional)",
            options=[None] + quarters,
            format_func=lambda x: "All Quarters" if x is None else f"Q{x}"
        )
        
        st.divider()
        
        compare_year = st.selectbox(
            "Compare with Year",
            options=[None] + [y for y in years if y != selected_year],
            format_func=lambda x: "No comparison" if x is None else str(x)
        )
        
        st.divider()
        
        st.markdown("""
        ### About
        This dashboard provides comprehensive 
        financial analytics including:
        
        - Revenue & profitability trends
        - Cash flow analysis
        - Financial ratios
        - Budget variance
        - Forecasting
        
        ---
        **Built by:** Zakaria El Morabit  
        **Contact:** elmorabitzakaria@gmail.com
        """)
    
    # Filter data
    filtered_df = filter_by_period(df, year=selected_year, quarter=selected_quarter)
    
    # Main content tabs
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "📈 Executive Summary",
        "💰 Revenue Analysis", 
        "📊 Profitability",
        "💵 Cash Flow",
        "📉 Financial Ratios",
        "🔮 Forecasting"
    ])
    
    # Tab 1: Executive Summary
    with tab1:
        st.header("Executive Summary")
        
        kpis = calculate_kpis(filtered_df)
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                label="Total Revenue",
                value=format_currency(kpis['total_revenue']),
                delta=format_percentage(kpis['revenue_change'])
            )
        
        with col2:
            st.metric(
                label="Net Income",
                value=format_currency(kpis['net_income']),
                delta=format_percentage(kpis['net_income_change'])
            )
        
        with col3:
            st.metric(
                label="Gross Margin",
                value=format_percentage(kpis['gross_margin']),
                delta=None
            )
        
        with col4:
            st.metric(
                label="Net Margin",
                value=format_percentage(kpis['net_margin']),
                delta=None
            )
        
        st.divider()
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(label="EBITDA", value=format_currency(kpis['ebitda']))
        
        with col2:
            st.metric(label="Operating Income", value=format_currency(kpis['operating_income']))
        
        with col3:
            st.metric(label="Total Assets", value=format_currency(kpis['total_assets']))
        
        with col4:
            st.metric(label="Cash Position", value=format_currency(kpis['cash']))
        
        st.divider()
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Revenue Trend")
            revenue_chart = create_revenue_trend_chart(filtered_df)
            st.plotly_chart(revenue_chart, use_container_width=True)
        
        with col2:
            st.subheader("Profitability Margins")
            profit_chart = create_profitability_chart(filtered_df)
            st.plotly_chart(profit_chart, use_container_width=True)
        
        if compare_year:
            st.subheader(f"📊 Year-over-Year Comparison: {selected_year} vs {compare_year}")
            comparison = get_period_comparison(df, selected_year, compare_year)
            
            if comparison:
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric(
                        label=f"Revenue ({selected_year})",
                        value=format_currency(comparison['current_revenue']),
                        delta=format_percentage(comparison['revenue_growth']) + " YoY"
                    )
                
                with col2:
                    st.metric(
                        label=f"Net Income ({selected_year})",
                        value=format_currency(comparison['current_net_income']),
                        delta=format_percentage(comparison['net_income_growth']) + " YoY"
                    )
                
                with col3:
                    margin_change = comparison['current_gross_margin'] - comparison['previous_gross_margin']
                    st.metric(
                        label=f"Gross Margin ({selected_year})",
                        value=format_percentage(comparison['current_gross_margin']),
                        delta=format_percentage(margin_change) + " pts"
                    )
        
        st.subheader("📋 Financial Health Indicators")
        health_indicators = get_health_indicators(filtered_df)
        health_table = create_health_indicator_table(health_indicators)
        st.plotly_chart(health_table, use_container_width=True)
    
    # Tab 2: Revenue Analysis
    with tab2:
        st.header("Revenue Analysis")
        
        breakdown = calculate_revenue_breakdown(filtered_df)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.subheader("By Product")
            pie_product = create_revenue_breakdown_pie(breakdown, 'by_product')
            st.plotly_chart(pie_product, use_container_width=True)
        
        with col2:
            st.subheader("By Region")
            pie_region = create_revenue_breakdown_pie(breakdown, 'by_region')
            st.plotly_chart(pie_region, use_container_width=True)
        
        with col3:
            st.subheader("By Customer Segment")
            pie_customer = create_revenue_breakdown_pie(breakdown, 'by_customer')
            st.plotly_chart(pie_customer, use_container_width=True)
        
        st.divider()
        
        st.subheader("📊 Budget vs Actual Analysis")
        
        merged_df = merge_actual_budget(filtered_df, budget_df)
        variance_chart = create_budget_variance_chart(merged_df)
        st.plotly_chart(variance_chart, use_container_width=True)
        
        col1, col2, col3 = st.columns(3)
        
        total_actual = merged_df['revenue'].sum()
        total_budget = merged_df['budget_revenue'].sum()
        total_variance = total_actual - total_budget
        variance_pct = (total_variance / total_budget) * 100
        
        with col1:
            st.metric("Total Actual Revenue", format_currency(total_actual))
        with col2:
            st.metric("Total Budget", format_currency(total_budget))
        with col3:
            st.metric("Variance", format_currency(total_variance), delta=format_percentage(variance_pct))
        
        st.subheader("📈 Quarterly Performance")
        quarterly_df = calculate_quarterly_summary(df)
        quarterly_chart = create_quarterly_comparison_chart(quarterly_df)
        st.plotly_chart(quarterly_chart, use_container_width=True)
    
    # Tab 3: Profitability
    with tab3:
        st.header("Profitability Analysis")
        
        st.subheader("📊 Income Statement Breakdown")
        latest_row = filtered_df.iloc[-1]
        waterfall = create_income_statement_waterfall(latest_row)
        st.plotly_chart(waterfall, use_container_width=True)
        
        st.divider()
        
        st.subheader("📈 Profitability Ratios")
        
        prof_ratios = calculate_profitability_ratios(filtered_df)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Return on Assets (ROA)", format_percentage(prof_ratios['roa']))
        with col2:
            st.metric("Return on Equity (ROE)", format_percentage(prof_ratios['roe']))
        with col3:
            st.metric("Return on Invested Capital (ROIC)", format_percentage(prof_ratios['roic']))
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Gross Margin", format_percentage(prof_ratios['gross_margin']))
        with col2:
            st.metric("Operating Margin", format_percentage(prof_ratios['operating_margin']))
        with col3:
            st.metric("Net Margin", format_percentage(prof_ratios['net_margin']))
        
        st.divider()
        
        st.subheader("📉 Margin Trends")
        margin_chart = create_profitability_chart(df)
        st.plotly_chart(margin_chart, use_container_width=True)
        
        st.subheader("📋 Annual Summary")
        annual_df = calculate_annual_summary(df)
        
        display_cols = ['year', 'revenue', 'gross_profit', 'net_income', 
                       'gross_margin', 'net_margin', 'revenue_growth']
        annual_display = annual_df[display_cols].copy()
        annual_display.columns = ['Year', 'Revenue', 'Gross Profit', 'Net Income',
                                 'Gross Margin %', 'Net Margin %', 'Revenue Growth %']
        
        st.dataframe(
            annual_display.style.format({
                'Revenue': '${:,.0f}',
                'Gross Profit': '${:,.0f}',
                'Net Income': '${:,.0f}',
                'Gross Margin %': '{:.1f}%',
                'Net Margin %': '{:.1f}%',
                'Revenue Growth %': '{:+.1f}%'
            }),
            use_container_width=True,
            hide_index=True
        )
    
    # Tab 4: Cash Flow
    with tab4:
        st.header("Cash Flow Analysis")
        
        cf_filtered = cash_flow_df[cash_flow_df['date'].dt.year == selected_year]
        if selected_quarter:
            cf_filtered = cf_filtered[cf_filtered['date'].dt.quarter == selected_quarter]
        
        st.subheader("📊 Cash Flow Components")
        cf_chart = create_cash_flow_chart(cf_filtered)
        st.plotly_chart(cf_chart, use_container_width=True)
        
        st.divider()
        
        st.subheader("💵 Cash Flow Summary")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            operating_cf = cf_filtered['operating_cash_flow'].sum()
            st.metric("Operating Cash Flow", format_currency(operating_cf),
                     delta="Positive" if operating_cf > 0 else "Negative")
        
        with col2:
            investing_cf = cf_filtered['investing_cash_flow'].sum()
            st.metric("Investing Cash Flow", format_currency(investing_cf))
        
        with col3:
            financing_cf = cf_filtered['financing_cash_flow'].sum()
            st.metric("Financing Cash Flow", format_currency(financing_cf))
        
        with col4:
            net_cf = cf_filtered['net_cash_flow'].sum()
            st.metric("Net Cash Flow", format_currency(net_cf),
                     delta="Positive" if net_cf > 0 else "Negative")
        
        st.divider()
        
        st.subheader("📋 Monthly Cash Flow Details")
        
        cf_display = cf_filtered[['date', 'operating_cash_flow', 'investing_cash_flow', 
                                  'financing_cash_flow', 'net_cash_flow', 'ending_cash']].copy()
        cf_display['date'] = cf_display['date'].dt.strftime('%b %Y')
        cf_display.columns = ['Month', 'Operating', 'Investing', 'Financing', 'Net', 'Ending Cash']
        
        st.dataframe(
            cf_display.style.format({
                'Operating': '${:,.0f}',
                'Investing': '${:,.0f}',
                'Financing': '${:,.0f}',
                'Net': '${:,.0f}',
                'Ending Cash': '${:,.0f}'
            }),
            use_container_width=True,
            hide_index=True
        )
    
    # Tab 5: Financial Ratios
    with tab5:
        st.header("Financial Ratios")
        
        st.subheader("💧 Liquidity Ratios")
        liquidity = calculate_liquidity_ratios(filtered_df)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            value = liquidity['current_ratio']
            status = "✅ Good" if value >= 1.5 else ("⚠️ Warning" if value >= 1.0 else "❌ Critical")
            st.metric("Current Ratio", f"{value:.2f}", status)
            st.caption("Target: ≥ 1.5")
        
        with col2:
            value = liquidity['quick_ratio']
            status = "✅ Good" if value >= 1.0 else ("⚠️ Warning" if value >= 0.7 else "❌ Critical")
            st.metric("Quick Ratio", f"{value:.2f}", status)
            st.caption("Target: ≥ 1.0")
        
        with col3:
            value = liquidity['cash_ratio']
            status = "✅ Good" if value >= 0.5 else ("⚠️ Warning" if value >= 0.3 else "❌ Critical")
            st.metric("Cash Ratio", f"{value:.2f}", status)
            st.caption("Target: ≥ 0.5")
        
        liquidity_gauge = create_financial_ratios_gauge(liquidity, 'liquidity')
        st.plotly_chart(liquidity_gauge, use_container_width=True)
        
        st.divider()
        
        st.subheader("⚡ Efficiency Ratios")
        efficiency = calculate_efficiency_ratios(filtered_df)
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Asset Turnover", f"{efficiency['asset_turnover']:.2f}x")
        with col2:
            st.metric("Inventory Turnover", f"{efficiency['inventory_turnover']:.2f}x")
        with col3:
            st.metric("Receivables Turnover", f"{efficiency['receivables_turnover']:.2f}x")
        with col4:
            st.metric("Cash Conversion Cycle", f"{efficiency['cash_conversion_cycle']:.0f} days")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Days Sales Outstanding (DSO)", f"{efficiency['dso']:.0f} days")
        with col2:
            st.metric("Days Inventory Outstanding (DIO)", f"{efficiency['dio']:.0f} days")
        with col3:
            st.metric("Days Payable Outstanding (DPO)", f"{efficiency['dpo']:.0f} days")
        
        st.divider()
        
        st.subheader("📊 Leverage Ratios")
        leverage = calculate_leverage_ratios(filtered_df)
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            value = leverage['debt_to_equity']
            status = "✅ Good" if value <= 1.0 else ("⚠️ Warning" if value <= 2.0 else "❌ Critical")
            st.metric("Debt to Equity", f"{value:.2f}", status)
        
        with col2:
            st.metric("Debt Ratio", f"{leverage['debt_ratio']:.2f}")
        
        with col3:
            value = leverage['interest_coverage']
            status = "✅ Good" if value >= 3.0 else ("⚠️ Warning" if value >= 1.5 else "❌ Critical")
            st.metric("Interest Coverage", f"{value:.2f}x", status)
        
        with col4:
            st.metric("LT Debt to Equity", f"{leverage['lt_debt_to_equity']:.2f}")
        
        leverage_gauge = create_financial_ratios_gauge(leverage, 'leverage')
        st.plotly_chart(leverage_gauge, use_container_width=True)
    
    # Tab 6: Forecasting
    with tab6:
        st.header("Financial Forecasting")
        
        col1, col2 = st.columns([1, 3])
        
        with col1:
            forecast_periods = st.slider(
                "Forecast Periods (months)",
                min_value=3,
                max_value=12,
                value=6
            )
            
            metric_to_forecast = st.selectbox(
                "Metric to Forecast",
                options=['revenue', 'net_income', 'gross_profit'],
                format_func=lambda x: x.replace('_', ' ').title()
            )
        
        with col2:
            if metric_to_forecast == 'revenue':
                forecast_result = forecast_revenue(df, periods=forecast_periods)
            else:
                forecast_result = forecast_metric(df, metric_to_forecast, periods=forecast_periods)
            
            forecast_chart = create_forecast_chart(forecast_result)
            st.plotly_chart(forecast_chart, use_container_width=True)
        
        if 'mae' in forecast_result and forecast_result['mae'] > 0:
            st.subheader("📊 Forecast Accuracy Metrics")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Mean Absolute Error (MAE)", format_currency(forecast_result['mae']))
            with col2:
                mape = forecast_result['mape']
                status = "✅ Good" if mape < 10 else ("⚠️ Fair" if mape < 20 else "❌ Poor")
                st.metric("MAPE", format_percentage(mape), status)
            with col3:
                st.metric("RMSE", format_currency(forecast_result['rmse']))
        
        st.divider()
        
        st.subheader("📈 Growth Projections")
        
        growth = calculate_growth_projections(df)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Average Annual Growth", format_percentage(growth['avg_annual_growth']))
        with col2:
            st.metric("CAGR", format_percentage(growth['cagr']))
        with col3:
            st.metric("Avg Monthly Growth", format_percentage(growth['monthly_growth']))
        
        st.divider()
        
        st.subheader("🎯 Scenario Analysis")
        
        scenario_df = scenario_analysis(df)
        scenario_chart = create_scenario_chart(scenario_df)
        st.plotly_chart(scenario_chart, use_container_width=True)
        
        st.markdown("**Scenario Assumptions:**")
        scenario_details = scenario_df.copy()
        scenario_details['scenario'] = scenario_details['scenario'].str.title()
        scenario_details.columns = ['Scenario', 'Projected Revenue', 'Growth Rate %', 'Net Margin %', 'Projected Net Income']
        
        st.dataframe(
            scenario_details.style.format({
                'Projected Revenue': '${:,.0f}',
                'Growth Rate %': '{:+.1f}%',
                'Net Margin %': '{:.1f}%',
                'Projected Net Income': '${:,.0f}'
            }),
            use_container_width=True,
            hide_index=True
        )


if __name__ == "__main__":
    main()
