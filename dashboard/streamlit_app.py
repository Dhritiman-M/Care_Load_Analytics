# --------------------------------------------------
# IMPORT LIBRARIES
# --------------------------------------------------
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT_DIR))

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


from src.preprocessing import (
    load_and_clean_data,
    create_complete_daily_index
)

from src.validation import (
    validate_business_rules,
    get_validation_summary
)

from src.feature_engineering import (
    create_features,
    calculate_kpis
)

from src.trend_analysis import (
    aggregate_by_granularity,
    identify_stress_periods,
    identify_relief_periods,
    compare_early_vs_late_periods,
    longest_stress_period,
    get_monthly_summary,
    get_weekly_summary,
)

from src.forecasting import (
    forecast_total_system_load,
    forecast_hhs_load,
    forecast_cbp_load
)

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="UAC Care Load Analytics",
    # page_icon="📊",
    layout="wide"
)

# --------------------------------------------------
# HEADER
# --------------------------------------------------

st.title(
    "System Capacity & Care Load Analytics for Unaccompanied Children"
)

st.markdown(
"""
This dashboard provides operational visibility into:
- CBP Care Load             
- HHS Care Load
- Total System Load         
- Net Intake Pressure
- Backlog Accumulation
- Capacity Stress Monitoring
- Forecasted Care Demand
"""
)

# --------------------------------------------------
# DATA LOADING
# --------------------------------------------------

@st.cache_data
def load_dataset(uploaded_file):

    df = load_and_clean_data(uploaded_file)

    df = create_complete_daily_index(df)

    df = validate_business_rules(df)

    df = create_features(df)

    df = identify_stress_periods(df)

    df = identify_relief_periods(df)

    return df



data_file = ROOT_DIR / "data" / "HHS_Unaccompanied_Alien_Children_Program.csv"
df=load_dataset(data_file)


# --------------------------------------------------
# SIDEBAR FILTERS
# --------------------------------------------------
st.sidebar.header("Download Dataset")
st.sidebar.download_button(
    use_container_width=True,
    label="Download",
    data=df.to_csv(index=False).encode("utf-8"),
    file_name="HHS_Unaccompanied_Alien_Children_Program.csv",

)

st.sidebar.header("Filters")

start_date = st.sidebar.date_input(
    "Start Date",
    min_value=df["Date"].min(),
    max_value=df["Date"].max(),
    value=df["Date"].min()
)

end_date = st.sidebar.date_input(
    "End Date", 
    min_value=df["Date"].min(),
    max_value=df["Date"].max(),
    value=df["Date"].max()
)

granularity = st.sidebar.selectbox(
    "Time Granularity",
    [
        "Daily",
        "Weekly",
        "Monthly"
    ]
)

filtered_df = df[
    (
        df["Date"] >= pd.to_datetime(start_date)
    )
    &
    (
        df["Date"] <= pd.to_datetime(end_date)
    )
]

analysis_df = aggregate_by_granularity(
    filtered_df,
    granularity
)

# --------------------------------------------------
# KPI SECTION
# --------------------------------------------------

kpis = calculate_kpis(filtered_df)

st.subheader("Key Performance Indicators")

col1, col2, col3, col4, col5 = st.columns(5)

col1.metric(
    "Total Under Care",
    f"{kpis['Total_Under_Care']:,.0f}"
)

col2.metric(
    "Net Intake Pressure",
    f"{kpis['Net_Intake_Pressure']:,.2f}"
)

col3.metric(
    "Volatility Index",
    f"{kpis['Volatility_Index']:,.2f}"
)

col4.metric(
    "Backlog Accumulation",
    f"{kpis['Backlog_Accumulation']:,.0f}"
)

col5.metric(
    "Discharge Offset Ratio",
    f"{kpis['Discharge_Offset_Ratio']:.2f}"
)

# --------------------------------------------------
# TABS
# --------------------------------------------------

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "Overview",
    "CBP vs HHS",
    "Net Intake & Backlog",
    "Stress Monitoring",
    "Temporal Analysis",
    "Forecasting"
])

# ==================================================
# TAB 1
# ==================================================

with tab1:

    st.subheader(
        "System Load Overview"
    )

    fig = px.line(
        analysis_df,
        x="Date",
        y="Total_System_Load",
        title="Total System Load Over Time"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# ==================================================
# TAB 2
# ==================================================

with tab2:

    st.subheader(
        "CBP vs HHS Care Load"
    )

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=analysis_df["Date"],
            y=analysis_df["CBP_Custody"],
            name="CBP Custody"
        )
    )

    fig.add_trace(
        go.Scatter(
            x=analysis_df["Date"],
            y=analysis_df["HHS_Care"],
            name="HHS Care"
        )
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# ==================================================
# TAB 3
# ==================================================

with tab3:

    st.subheader(
        "Net Intake & Backlog Trends"
    )

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=filtered_df["Date"],
            y=filtered_df["Net_Daily_Intake"],
            name="Net Daily Intake"
        )
    )

    fig.add_trace(
        go.Scatter(
            x=filtered_df["Date"],
            y=filtered_df["Backlog_Indicator"],
            name="Backlog Indicator"
        )
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# ==================================================
# TAB 4
# ==================================================

with tab4:

    st.subheader(
        "Capacity Stress Monitoring"
    )

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=filtered_df["Date"],
            y=filtered_df["Load_7D"],
            name="7 Day Average"
        )
    )

    fig.add_trace(
        go.Scatter(
            x=filtered_df["Date"],
            y=filtered_df["Load_14D"],
            name="14 Day Average"
        )
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    stress_days = int(
        filtered_df["Stress_Flag"].sum()
    )

    relief_days = int(
        filtered_df["Relief_Flag"].sum()
    )

    longest_window = longest_stress_period(
        filtered_df
    )

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "Stress Days",
        stress_days
    )

    c2.metric(
        "Relief Days",
        relief_days
    )

    c3.metric(
        "Longest Stress Window",
        longest_window
    )

# ==================================================
# TAB 5
# ==================================================

with tab5:

    st.subheader(
        "Trend & Temporal Analysis"
    )

    comparison = compare_early_vs_late_periods(
        filtered_df
    )

    st.write(
        "Early vs Late Timeline Comparison"
    )

    st.dataframe(
        comparison,
        use_container_width=True
    )
    weekly = get_weekly_summary(
        filtered_df
    )

    monthly = get_monthly_summary(
        filtered_df
    )

    fig = px.line(
        monthly,
        x="Date",
        y="Total_System_Load",
        title="Monthly Average System Load"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# ==================================================
# TAB 6
# ==================================================

with tab6:

    st.subheader(
        "30-Day Forecast"
    )

    forecast_option = st.selectbox(
        "Forecast Metric",
        [
            "Total System Load",
            "HHS Care",
            "CBP Custody"
        ]
    )

    if forecast_option == "Total System Load":

        model, forecast = (
            forecast_total_system_load(
                filtered_df
            )
        )
        forecast_df = filtered_df.dropna(
        subset=["Total_System_Load"]
        )

        if len(forecast_df) < 30:

            st.warning(
                "Not enough data available for forecasting."
            )

            st.stop()

    elif forecast_option == "HHS Care":

        model, forecast = (
            forecast_hhs_load(
                filtered_df
            )
        )

    else:

        model, forecast = (
            forecast_cbp_load(
                filtered_df
            )
        )

    forecast_plot = px.line(
        forecast,
        x="ds",
        y=[
            "yhat",
            "yhat_upper",
            "yhat_lower"
        ],
        title="Forecast with Confidence Interval"
    )

    st.plotly_chart(
        forecast_plot,
        use_container_width=True
    )

    st.dataframe(
        forecast[
            [
                "ds",
                "yhat",
                "yhat_lower",
                "yhat_upper"
            ]
        ].tail(30),
        use_container_width=True
    )

# --------------------------------------------------
# DATA QUALITY
# --------------------------------------------------

st.subheader("Data Quality Summary")

validation_summary = (
    get_validation_summary(filtered_df)
)

st.dataframe(validation_summary,width="stretch")