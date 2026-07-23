import numpy as np


def create_features(df):
    """
    Create all project-specific metrics.
    """

    # ----------------------------------
    # Total System Load
    # ----------------------------------

    df["Total_System_Load"] = (
        df["CBP_Custody"]
        +
        df["HHS_Care"]
    )

    # ----------------------------------
    # Net Daily Intake
    # ----------------------------------

    df["Net_Daily_Intake"] = (
        df["Transferred_Out_CBP"]
        -
        df["HHS_Discharged"]
    )

    # ----------------------------------
    # Growth Rate
    # ----------------------------------

    df["Care_Load_Growth_Rate"] = (
        df["Total_System_Load"]
        .pct_change()
        * 100
    )

    # ----------------------------------
    # Backlog Indicator
    # ----------------------------------

    df["Backlog_Indicator"] = (
        df["Net_Daily_Intake"]
        .fillna(0)
        .cumsum()
    )

    # ----------------------------------
    # Discharge Offset Ratio
    # ----------------------------------

    df["Discharge_Offset_Ratio"] = np.where(
        df["Transferred_Out_CBP"] > 0,
        df["HHS_Discharged"]
        /
        df["Transferred_Out_CBP"],
        np.nan
    )

    # ----------------------------------
    # Rolling Load Metrics
    # ----------------------------------

    df["Load_7D"] = (
        df["Total_System_Load"]
        .rolling(window=7)
        .mean()
    )

    df["Load_14D"] = (
        df["Total_System_Load"]
        .rolling(window=14)
        .mean()
    )

    # ----------------------------------
    # Volatility Index
    # ----------------------------------

    df["Volatility_Index"] = (
        df["Total_System_Load"]
        .rolling(window=7)
        .std()
    )

    return df


def calculate_kpis(df):
    """
    Calculate dashboard KPI values.
    """

    latest = df.iloc[-1]

    total_under_care = latest["Total_System_Load"]

    avg_net_intake = (
        df["Net_Daily_Intake"]
        .mean()
    )

    volatility_series = (
        df["Volatility_Index"]
        .dropna()
    )

    volatility = (
        volatility_series.iloc[-1]
        if len(volatility_series) > 0
        else 0
    )

    backlog_rate = (
        df["Backlog_Indicator"]
        .iloc[-1]
    )

    discharge_offset_ratio = (
        df["HHS_Discharged"].sum()
        /
        df["Transferred_Out_CBP"].sum()
    )

    return {
        "Total_Under_Care":
            total_under_care,

        "Net_Intake_Pressure":
            avg_net_intake,

        "Volatility_Index":
            volatility,

        "Backlog_Accumulation":
            backlog_rate,

        "Discharge_Offset_Ratio":
            discharge_offset_ratio
    }