"""
Visualizations Module
Contains functions for creating interactive financial charts and graphs.
"""

import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np


# Color scheme
COLORS = {
    'primary': '#1565C0',
    'secondary': '#4CAF50',
    'accent': '#FF9800',
    'danger': '#F44336',
    'success': '#2E7D32',
    'warning': '#FFC107',
    'info': '#00BCD4',
    'dark': '#424242',
    'light': '#F5F5F5'
}

CHART_COLORS = ['#1565C0', '#4CAF50', '#FF9800', '#9C27B0', '#00BCD4', '#F44336']


def create_kpi_card(value: float, title: str, delta: float = None, prefix: str = "$", suffix: str = "") -> go.Figure:
    """Create a KPI indicator card."""
    fig = go.Figure()
    
    fig.add_trace(go.Indicator(
        mode="number+delta" if delta else "number",
        value=value,
        title={"text": title, "font": {"size": 14}},
        number={"prefix": prefix, "suffix": suffix, "font": {"size": 28}},
        delta={"reference": value - delta, "relative": True, "valueformat": ".1%"} if delta else None,
        domain={'x': [0, 1], 'y': [0, 1]}
    ))
    
    fig.update_layout(
        height=120,
        margin=dict(l=10, r=10, t=40, b=10)
    )
    
    return fig


def create_revenue_trend_chart(df: pd.DataFrame) -> go.Figure:
    """Create revenue trend line chart with area fill."""
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=df['date'],
        y=df['revenue'],
        mode='lines',
        name='Revenue',
        line=dict(color=COLORS['primary'], width=3),
        fill='tozeroy',
        fillcolor='rgba(21, 101, 192, 0.1)'
    ))
    
    # Add moving average
    if 'revenue_ma' in df.columns:
        fig.add_trace(go.Scatter(
            x=df['date'],
            y=df['revenue_ma'],
            mode='lines',
            name='3-Month MA',
            line=dict(color=COLORS['accent'], width=2, dash='dash')
        ))
    
    fig.update_layout(
        title='Revenue Trend',
        xaxis_title='Date',
        yaxis_title='Revenue ($)',
        height=350,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        hovermode='x unified'
    )

    fig.update_yaxes(tickformat='$,.0f')
    
    return fig


def create_profitability_chart(df: pd.DataFrame) -> go.Figure:
    """Create profitability margins chart."""
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=df['date'],
        y=df['gross_margin'],
        mode='lines+markers',
        name='Gross Margin',
        line=dict(color=COLORS['primary'], width=2)
    ))
    
    fig.add_trace(go.Scatter(
        x=df['date'],
        y=df['operating_margin'],
        mode='lines+markers',
        name='Operating Margin',
        line=dict(color=COLORS['secondary'], width=2)
    ))
    
    fig.add_trace(go.Scatter(
        x=df['date'],
        y=df['net_margin'],
        mode='lines+markers',
        name='Net Margin',
        line=dict(color=COLORS['accent'], width=2)
    ))
    
    fig.update_layout(
        title='Profitability Margins Trend',
        xaxis_title='Date',
        yaxis_title='Margin (%)',
        height=350,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        hovermode='x unified'
    )

    fig.update_yaxes(ticksuffix='%')
    
    return fig


def create_income_statement_waterfall(row: pd.Series) -> go.Figure:
    """Create income statement waterfall chart."""
    fig = go.Figure(go.Waterfall(
        name="Income Statement",
        orientation="v",
        measure=["absolute", "relative", "relative", "relative", "relative", "total"],
        x=["Revenue", "COGS", "Operating Exp", "Interest", "Taxes", "Net Income"],
        y=[
            row['revenue'],
            -row['cogs'],
            -row['operating_expenses'],
            -row['interest_expense'],
            -row['tax_expense'],
            row['net_income']
        ],
        textposition="outside",
        text=[
            f"${row['revenue']:,.0f}",
            f"-${row['cogs']:,.0f}",
            f"-${row['operating_expenses']:,.0f}",
            f"-${row['interest_expense']:,.0f}",
            f"-${row['tax_expense']:,.0f}",
            f"${row['net_income']:,.0f}"
        ],
        connector={"line": {"color": "rgb(63, 63, 63)"}},
        increasing={"marker": {"color": COLORS['success']}},
        decreasing={"marker": {"color": COLORS['danger']}},
        totals={"marker": {"color": COLORS['primary']}}
    ))
    
    fig.update_layout(
        title="Income Statement Breakdown",
        showlegend=False,
        height=400
    )
    
    return fig


def create_revenue_breakdown_pie(breakdown: dict, breakdown_type: str = 'by_product') -> go.Figure:
    """Create revenue breakdown pie chart."""
    data = breakdown[breakdown_type]
    
    labels = list(data.keys())
    values = [data[k]['value'] for k in labels]
    
    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        hole=0.4,
        marker_colors=CHART_COLORS[:len(labels)],
        textinfo='label+percent',
        textposition='outside'
    )])
    
    title_map = {
        'by_product': 'Revenue by Product',
        'by_region': 'Revenue by Region',
        'by_customer': 'Revenue by Customer Segment'
    }
    
    fig.update_layout(
        title=title_map.get(breakdown_type, 'Revenue Breakdown'),
        height=350,
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5)
    )
    
    return fig


def create_budget_variance_chart(merged_df: pd.DataFrame) -> go.Figure:
    """Create budget vs actual variance chart."""
    fig = make_subplots(
        rows=1, cols=2,
        subplot_titles=('Revenue: Actual vs Budget', 'Variance %'),
        specs=[[{"type": "bar"}, {"type": "bar"}]]
    )
    
    # Actual vs Budget bars
    fig.add_trace(
        go.Bar(name='Actual', x=merged_df['date'], y=merged_df['revenue'],
               marker_color=COLORS['primary']),
        row=1, col=1
    )
    fig.add_trace(
        go.Bar(name='Budget', x=merged_df['date'], y=merged_df['budget_revenue'],
               marker_color=COLORS['light'], opacity=0.7),
        row=1, col=1
    )
    
    # Variance bars
    colors = [COLORS['success'] if v >= 0 else COLORS['danger'] for v in merged_df['revenue_variance_pct']]
    fig.add_trace(
        go.Bar(name='Variance %', x=merged_df['date'], y=merged_df['revenue_variance_pct'],
               marker_color=colors, showlegend=False),
        row=1, col=2
    )
    
    fig.update_layout(
        height=350,
        barmode='group',
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    
    fig.update_yaxes(tickformat='$,.0f', row=1, col=1)
    fig.update_yaxes(ticksuffix='%', row=1, col=2)
    
    return fig


def create_cash_flow_chart(cash_flow_df: pd.DataFrame) -> go.Figure:
    """Create cash flow stacked bar chart."""
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        name='Operating',
        x=cash_flow_df['date'],
        y=cash_flow_df['operating_cash_flow'],
        marker_color=COLORS['success']
    ))
    
    fig.add_trace(go.Bar(
        name='Investing',
        x=cash_flow_df['date'],
        y=cash_flow_df['investing_cash_flow'],
        marker_color=COLORS['danger']
    ))
    
    fig.add_trace(go.Bar(
        name='Financing',
        x=cash_flow_df['date'],
        y=cash_flow_df['financing_cash_flow'],
        marker_color=COLORS['warning']
    ))
    
    # Add net cash flow line
    fig.add_trace(go.Scatter(
        name='Net Cash Flow',
        x=cash_flow_df['date'],
        y=cash_flow_df['net_cash_flow'],
        mode='lines+markers',
        line=dict(color=COLORS['primary'], width=3)
    ))
    
    fig.update_layout(
        title='Cash Flow Analysis',
        xaxis_title='Date',
        yaxis_title='Cash Flow ($)',
        height=400,
        barmode='relative',
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        hovermode='x unified'
    )

    fig.update_yaxes(tickformat='$,.0f')
    
    return fig


def create_forecast_chart(forecast_result: dict) -> go.Figure:
    """Create forecast chart with confidence intervals."""
    historical = forecast_result['historical']
    forecast_df = forecast_result['forecast_df']
    
    fig = go.Figure()
    
    # Historical data
    metric_col = historical.columns[1]  # Second column is the metric
    fig.add_trace(go.Scatter(
        x=historical['date'],
        y=historical[metric_col],
        mode='lines',
        name='Historical',
        line=dict(color=COLORS['primary'], width=2)
    ))
    
    # Forecast
    fig.add_trace(go.Scatter(
        x=forecast_df['date'],
        y=forecast_df['forecast'],
        mode='lines+markers',
        name='Forecast',
        line=dict(color=COLORS['accent'], width=2, dash='dash')
    ))
    
    # Confidence interval
    if 'lower_bound' in forecast_df.columns:
        fig.add_trace(go.Scatter(
            x=pd.concat([forecast_df['date'], forecast_df['date'][::-1]]),
            y=pd.concat([forecast_df['upper_bound'], forecast_df['lower_bound'][::-1]]),
            fill='toself',
            fillcolor='rgba(255, 152, 0, 0.2)',
            line=dict(color='rgba(255,255,255,0)'),
            name='95% Confidence',
            showlegend=True
        ))
    
    fig.update_layout(
        title=f'{metric_col.replace("_", " ").title()} Forecast',
        xaxis_title='Date',
        yaxis_title='Value ($)',
        height=400,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        hovermode='x unified'
    )

    fig.update_yaxes(tickformat='$,.0f')
    
    return fig


def create_financial_ratios_gauge(ratios: dict, ratio_type: str = 'liquidity') -> go.Figure:
    """Create gauge charts for financial ratios."""
    if ratio_type == 'liquidity':
        specs = [
            {'title': 'Current Ratio', 'value': ratios['current_ratio'], 'range': [0, 3], 'threshold': 1.5},
            {'title': 'Quick Ratio', 'value': ratios['quick_ratio'], 'range': [0, 2], 'threshold': 1.0},
            {'title': 'Cash Ratio', 'value': ratios['cash_ratio'], 'range': [0, 1.5], 'threshold': 0.5}
        ]
    elif ratio_type == 'leverage':
        specs = [
            {'title': 'Debt/Equity', 'value': ratios['debt_to_equity'], 'range': [0, 3], 'threshold': 1.0, 'reverse': True},
            {'title': 'Interest Coverage', 'value': ratios['interest_coverage'], 'range': [0, 30], 'threshold': 3.0}
        ]
    else:
        specs = []
    
    fig = make_subplots(
        rows=1, cols=len(specs),
        specs=[[{"type": "indicator"}] * len(specs)],
        subplot_titles=[s['title'] for s in specs]
    )
    
    for i, spec in enumerate(specs, 1):
        threshold = spec['threshold']
        value = spec['value']
        reverse = spec.get('reverse', False)
        
        if reverse:
            color = COLORS['success'] if value <= threshold else COLORS['danger']
        else:
            color = COLORS['success'] if value >= threshold else COLORS['danger']
        
        fig.add_trace(
            go.Indicator(
                mode="gauge+number",
                value=value,
                gauge={
                    'axis': {'range': spec['range']},
                    'bar': {'color': color},
                    'threshold': {
                        'line': {'color': COLORS['dark'], 'width': 4},
                        'thickness': 0.75,
                        'value': threshold
                    }
                }
            ),
            row=1, col=i
        )
    
    fig.update_layout(height=250, margin=dict(t=50, b=20))
    
    return fig


def create_quarterly_comparison_chart(quarterly_df: pd.DataFrame) -> go.Figure:
    """Create quarterly comparison bar chart."""
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        name='Revenue',
        x=quarterly_df['period'],
        y=quarterly_df['revenue'],
        marker_color=COLORS['primary'],
        yaxis='y'
    ))
    
    fig.add_trace(go.Scatter(
        name='Net Margin %',
        x=quarterly_df['period'],
        y=quarterly_df['net_margin'],
        mode='lines+markers',
        marker_color=COLORS['accent'],
        yaxis='y2'
    ))
    
    fig.update_layout(
        title='Quarterly Performance',
        xaxis_title='Quarter',
        yaxis=dict(title='Revenue ($)', tickformat='$,.0f'),
        yaxis2=dict(title='Net Margin (%)', overlaying='y', side='right', ticksuffix='%'),
        height=350,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        hovermode='x unified'
    )
    
    return fig


def create_health_indicator_table(indicators: list) -> go.Figure:
    """Create financial health indicator table."""
    colors = {
        'Good': '#C8E6C9',
        'Warning': '#FFF3E0',
        'Critical': '#FFEBEE'
    }
    
    cell_colors = [[colors.get(ind['status'], '#FFFFFF') for ind in indicators]]
    
    fig = go.Figure(data=[go.Table(
        header=dict(
            values=['Metric', 'Value', 'Status', 'Benchmark', 'Description'],
            fill_color=COLORS['primary'],
            font=dict(color='white', size=12),
            align='left'
        ),
        cells=dict(
            values=[
                [ind['metric'] for ind in indicators],
                [ind['value'] for ind in indicators],
                [ind['status'] for ind in indicators],
                [ind['benchmark'] for ind in indicators],
                [ind['description'] for ind in indicators]
            ],
            fill_color=[
                ['white'] * len(indicators),
                ['white'] * len(indicators),
                [colors.get(ind['status'], '#FFFFFF') for ind in indicators],
                ['white'] * len(indicators),
                ['white'] * len(indicators)
            ],
            align='left',
            font=dict(size=11)
        )
    )])
    
    fig.update_layout(height=300, margin=dict(l=20, r=20, t=20, b=20))
    
    return fig


def create_scenario_chart(scenario_df: pd.DataFrame) -> go.Figure:
    """Create scenario analysis chart."""
    colors = {
        'pessimistic': COLORS['danger'],
        'base': COLORS['primary'],
        'optimistic': COLORS['success']
    }
    
    fig = go.Figure()
    
    for _, row in scenario_df.iterrows():
        fig.add_trace(go.Bar(
            name=row['scenario'].title(),
            x=['Revenue', 'Net Income'],
            y=[row['revenue'], row['net_income']],
            marker_color=colors.get(row['scenario'], COLORS['primary']),
            text=[f"${row['revenue']:,.0f}", f"${row['net_income']:,.0f}"],
            textposition='outside'
        ))
    
    fig.update_layout(
        title='Scenario Analysis - Annual Projections',
        xaxis_title='Metric',
        yaxis_title='Amount ($)',
        height=400,
        barmode='group',
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )

    fig.update_yaxes(tickformat='$,.0f')
    
    return fig
