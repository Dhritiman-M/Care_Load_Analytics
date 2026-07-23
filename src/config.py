"""
Configuration file for UAC Care Load Analytics Project
"""

# Forecast Settings
FORECAST_DAYS = 30

# Rolling Window Settings
WEEKLY_WINDOW = 7
BIWEEKLY_WINDOW = 14

# Stress & Relief Thresholds
STRESS_PERCENTILE = 0.90
RELIEF_PERCENTILE = 0.25

# KPI Names
KPI_NAMES = {
    "total_load": "Total Children Under Care",
    "net_intake": "Net Intake Pressure",
    "volatility": "Care Load Volatility Index",
    "backlog": "Backlog Accumulation Rate",
    "offset_ratio": "Discharge Offset Ratio"
}