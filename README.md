# Financial KPI Dashboard

A comprehensive financial analytics dashboard built with Python and Streamlit. Track revenue, expenses, profitability, cash flow, and key financial ratios with interactive visualizations and forecasting capabilities.

## Dashboard Preview
https://financial-kpi-dashboards.streamlit.app/


## 🎯 Features

- **Executive Summary**: High-level KPIs with trend indicators
- **Revenue Analytics**: Revenue breakdown by product, region, and customer segment
- **Profitability Analysis**: Gross margin, operating margin, net margin trends
- **Cash Flow Tracking**: Operating, investing, and financing cash flows
- **Financial Ratios**: Liquidity, efficiency, and leverage ratios
- **Budget vs Actual**: Variance analysis with drill-down capabilities
- **Forecasting**: Revenue and expense predictions using time series analysis
- **Export Reports**: Generate PDF reports for stakeholders

## 🛠️ Tech Stack

- **Python 3.9+**
- **Streamlit** - Web application framework
- **Pandas** - Data manipulation and analysis
- **Plotly** - Interactive visualizations
- **NumPy** - Numerical computing
- **Statsmodels** - Time series forecasting

## 📁 Project Structure

```
financial-kpi-dashboard/
├── README.md
├── requirements.txt
├── app.py                    # Main Streamlit application
├── src/
│   ├── __init__.py
│   ├── data_loader.py        # Data loading and processing
│   ├── financial_analyzer.py # Financial calculations and KPIs
│   ├── forecasting.py        # Time series forecasting
│   └── visualizations.py     # Chart and graph functions
├── data/
│   ├── financial_data.csv    # Monthly financial data
│   ├── budget_data.csv       # Budget figures
│   └── cash_flow_data.csv    # Cash flow statements
└── assets/
    └── style.css             # Custom styling
```

## 🚀 Quick Start

### 1. Clone the repository
```bash
git clone https://github.com/yourusername/financial-kpi-dashboard.git
cd financial-kpi-dashboard
```

### 2. Create a virtual environment (recommended)
```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the application
```bash
streamlit run app.py
```

The dashboard will open in your browser at `http://localhost:8501`

## 📊 Key Performance Indicators

### Revenue Metrics
- Total Revenue & YoY Growth
- Revenue by Product Line
- Revenue by Region
- Average Revenue Per Customer

### Profitability Metrics
- Gross Profit Margin
- Operating Profit Margin (EBIT)
- Net Profit Margin
- EBITDA

### Liquidity Ratios
- Current Ratio
- Quick Ratio
- Cash Ratio

### Efficiency Ratios
- Asset Turnover
- Inventory Turnover
- Receivables Turnover
- Days Sales Outstanding (DSO)

### Leverage Ratios
- Debt-to-Equity
- Interest Coverage Ratio

## 📈 Forecasting Methodology

The dashboard uses **Holt-Winters Exponential Smoothing** for time series forecasting, which captures:
- **Level**: Base value of the series
- **Trend**: Upward or downward movement
- **Seasonality**: Recurring patterns (monthly/quarterly)

Forecast accuracy is measured using:
- Mean Absolute Error (MAE)
- Mean Absolute Percentage Error (MAPE)
- Root Mean Square Error (RMSE)

## 🎨 Screenshots

### Executive Dashboard
View all critical KPIs at a glance with trend indicators.

### Revenue Analysis
Deep dive into revenue streams with interactive filters.

### Forecasting
Predict future performance with confidence intervals.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👤 Author

**Zakaria El Morabit**
- LinkedIn: [Your LinkedIn Profile]
- Email: elmorabitzakaria@gmail.com

---

*Built as a portfolio project demonstrating financial analytics and data visualization skills.*
