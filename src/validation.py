import pandas as pd


def validate_business_rules(df):
    """
    Validate logical constraints.
    """

    df["Transfer_Anomaly"] = (
        df["Transferred_Out_CBP"] >
        df["CBP_Custody"]
    )

    df["Discharge_Anomaly"] = (
        df["HHS_Discharged"] >
        df["HHS_Care"]
    )

    return df


def get_validation_summary(df):
    """
    Generate validation statistics.
    """

    summary = {
        "Transfer Anomalies":
            int(df["Transfer_Anomaly"].sum()),

        "Discharge Anomalies":
            int(df["Discharge_Anomaly"].sum()),

        "Total Records":
            len(df)
    }

    return summary


def get_anomaly_records(df):
    """
    Return all anomaly rows.
    """

    anomalies = df[
        (df["Transfer_Anomaly"] == True)
        |
        (df["Discharge_Anomaly"] == True)
    ]

    return anomalies