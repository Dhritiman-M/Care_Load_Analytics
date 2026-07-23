import pandas as pd


COLUMN_MAPPING = {
    "Children apprehended and placed in CBP custody*":
        "Children_Apprehended",

    "Children in CBP custody":
        "CBP_Custody",

    "Children transferred out of CBP custody":
        "Transferred_Out_CBP",

    "Children in HHS Care":
        "HHS_Care",

    "Children discharged from HHS Care":
        "HHS_Discharged"
}


def load_and_clean_data(file_path):
    """
    Load and clean raw dataset.
    """

    df = pd.read_csv(file_path)

    df = df.dropna(how="all")

    df = df.rename(columns=COLUMN_MAPPING)

    df["Date"] = pd.to_datetime(df["Date"])

    df["HHS_Care"] = (
        df["HHS_Care"]
        .astype(str)
        .str.replace(",", "", regex=False)
    )

    numeric_cols = [
        "Children_Apprehended",
        "CBP_Custody",
        "Transferred_Out_CBP",
        "HHS_Care",
        "HHS_Discharged"
    ]

    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    df = df.sort_values("Date")

    return df.reset_index(drop=True)


def create_complete_daily_index(df):
    """
    Creates complete daily timeline.
    """

    full_dates = pd.date_range(
        start=df["Date"].min(),
        end=df["Date"].max(),
        freq="D"
    )

    df = (
        df.set_index("Date")
        .reindex(full_dates)
        .rename_axis("Date")
        .reset_index()
    )

    numeric_cols = df.select_dtypes(
        include="number"
    ).columns

    df[numeric_cols] = (
        df[numeric_cols]
        .interpolate()
    )

    return df


def get_missing_dates(df):
    """
    Detect missing dates.
    """

    full_dates = pd.date_range(
        start=df["Date"].min(),
        end=df["Date"].max(),
        freq="D"
    )

    missing = full_dates.difference(df["Date"])

    return pd.DataFrame({"Missing_Date": missing})


def get_duplicate_dates(df):
    """
    Detect duplicate dates.
    """

    duplicates = df[df["Date"].duplicated()]

    return duplicates