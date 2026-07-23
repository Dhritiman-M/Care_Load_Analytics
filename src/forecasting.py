"""
Forecasting Module
Using Facebook Prophet
"""

import pandas as pd
from prophet import Prophet


def prepare_prophet_data(
    df,
    target_column
):
    """
    Prophet expects:

    ds = date
    y = target
    """

    prophet_df = pd.DataFrame({
        "ds": df["Date"],
        "y": df[target_column]
    })

    prophet_df = (
        prophet_df
        .dropna()
        .sort_values("ds")
    )

    return prophet_df


def train_prophet_model(
    prophet_df
):
    """
    Train Prophet model.
    """

    model = Prophet(

        yearly_seasonality=True,

        weekly_seasonality=True,

        daily_seasonality=False,

        seasonality_mode="additive"

    )

    model.fit(
        prophet_df
    )

    return model


def generate_forecast(
    model,
    forecast_days=30
):
    """
    Future prediction.
    """

    future = (
        model
        .make_future_dataframe(
            periods=forecast_days
        )
    )

    forecast = (
        model
        .predict(future)
    )

    return forecast


def forecast_metric(
    df,
    target_column,
    forecast_days=30
):
    """
    Complete forecasting pipeline.
    """

    prophet_df = (
        prepare_prophet_data(
            df,
            target_column
        )
    )

    model = (
        train_prophet_model(
            prophet_df
        )
    )

    forecast = (
        generate_forecast(
            model,
            forecast_days
        )
    )

    return model, forecast


def forecast_total_system_load(
    df,
    forecast_days=30
):
    """
    Forecast Total Load.
    """

    return forecast_metric(

        df,

        target_column=
        "Total_System_Load",

        forecast_days=
        forecast_days
    )


def forecast_hhs_load(
    df,
    forecast_days=30
):
    """
    Forecast HHS Load.
    """

    return forecast_metric(

        df,

        target_column=
        "HHS_Care",

        forecast_days=
        forecast_days
    )


def forecast_cbp_load(
    df,
    forecast_days=30
):
    """
    Forecast CBP Load.
    """

    return forecast_metric(

        df,

        target_column=
        "CBP_Custody",

        forecast_days=
        forecast_days
    )


def forecast_net_intake(
    df,
    forecast_days=30
):
    """
    Forecast Net Intake.
    """

    return forecast_metric(

        df,

        target_column=
        "Net_Daily_Intake",

        forecast_days=
        forecast_days
    )