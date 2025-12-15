import pandas as pd

def maybe_convert_to_date(series: pd.Series):
    col = series.name.lower()
    date_keywords = ["date", "dt", "day", "time", "timestamp", "created", "updated"]

    if any(k in col for k in date_keywords):
        try:
            return pd.to_datetime(series, errors="coerce")
        except:
            return series

    return series


def clean(df):
    df.columns = df.columns.str.strip().str.replace(" ", "_").str.lower()

    for col in df.columns:
        if df[col].dtype == "object":
            df[col] = df[col].astype(str).str.strip()

    for col in df.columns:
        try:
            df[col] = pd.to_numeric(df[col])
        except:
            pass

    for col in df.columns:
        df[col] = maybe_convert_to_date(df[col])

    df = df.drop_duplicates()

    return df
