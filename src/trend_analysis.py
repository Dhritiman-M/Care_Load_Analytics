"""
Trend & Temporal Analysis Module
"""

import pandas as pd
from src.config import (
    STRESS_PERCENTILE,
    RELIEF_PERCENTILE
)


def aggregate_by_granularity(
    df,
    granularity="Daily"
):
    """
    Aggregate data by
    Daily / Weekly / Monthly.
    """

    df = df.copy()
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

    if granularity == "Daily":
        return df

    if granularity == "Weekly":

        return (
            df
            .set_index("Date")
            .resample("W")
            .mean(numeric_only=True)
            .reset_index()
        )

    if granularity == "Monthly":

        return (
            df
            .set_index("Date")
            .resample("ME")
            .mean(numeric_only=True)
            .reset_index()
        )

    return df


def identify_stress_periods(df):
    """
    High-load periods.
    """

    threshold = (
        df["Total_System_Load"]
        .quantile(STRESS_PERCENTILE)
    )

    df["Stress_Flag"] = (
        df["Total_System_Load"]
        >= threshold
    )

    return df


def identify_relief_periods(df):
    """
    Low-load periods.
    """

    threshold = (
        df["Total_System_Load"]
        .quantile(RELIEF_PERCENTILE)
    )

    df["Relief_Flag"] = (
        df["Total_System_Load"]
        <= threshold
    )

    return df


def compare_early_vs_late_periods(df):
    """
    Compare first half
    vs second half.
    """

    midpoint = len(df) // 2

    early = df.iloc[:midpoint]
    late = df.iloc[midpoint:]

    comparison = pd.DataFrame({

        "Metric": [

            "Average Total Load",

            "Average Net Intake",

            "Average HHS Care",

            "Average CBP Custody"

        ],

        "Early Period": [

            early["Total_System_Load"].mean(),

            early["Net_Daily_Intake"].mean(),

            early["HHS_Care"].mean(),

            early["CBP_Custody"].mean()

        ],

        "Late Period": [

            late["Total_System_Load"].mean(),

            late["Net_Daily_Intake"].mean(),

            late["HHS_Care"].mean(),

            late["CBP_Custody"].mean()

        ]
    })

    return comparison


def get_monthly_summary(df):
    """
    Monthly KPI summary.
    """

    monthly = (
        df
        .set_index("Date")
        .resample("ME")
        .agg({
            "Total_System_Load": "mean",
            "Net_Daily_Intake": "mean",
            "HHS_Care": "mean",
            "CBP_Custody": "mean"
        })
        .reset_index()
    )

    return monthly


def get_weekly_summary(df):
    """
    Weekly KPI summary.
    """

    weekly = (
        df
        .set_index("Date")
        .resample("W")
        .agg({
            "Total_System_Load": "mean",
            "Net_Daily_Intake": "mean",
            "HHS_Care": "mean",
            "CBP_Custody": "mean"
        })
        .reset_index()
    )

    return weekly


def longest_stress_period(df):
    """
    Find longest continuous
    stress window.
    """

    stress_df = identify_stress_periods(
        df.copy()
    )

    max_length = 0
    current = 0

    for value in stress_df["Stress_Flag"]:

        if value:
            current += 1
            max_length = max(
                max_length,
                current
            )

        else:
            current = 0

    return max_length