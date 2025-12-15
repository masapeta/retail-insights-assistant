import pandas as pd

def detect_schema(df: pd.DataFrame):

    numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns.tolist()

    for col in df.columns:
        if col not in numeric_cols:
            try:
                df[col].astype(float)
                numeric_cols.append(col)
            except:
                pass

    date_cols = df.select_dtypes(include=["datetime64[ns]"]).columns.tolist()

    categorical_cols = [
        col for col in df.columns
        if df[col].dtype == "object" and col not in date_cols
    ]

    text_cols = []
    for col in categorical_cols:
        if df[col].astype(str).str.len().mean() > 30:
            text_cols.append(col)

    primary_metric = None
    if numeric_cols:
        variances = {c: df[c].var() for c in numeric_cols if pd.api.types.is_numeric_dtype(df[c])}
        if variances:
            primary_metric = max(variances, key=variances.get)

    return {
        "numeric_cols": numeric_cols,
        "categorical_cols": categorical_cols,
        "text_cols": text_cols,
        "date_cols": date_cols,
        "primary_metric": primary_metric
    }


def enrich(df):
    date_cols = df.select_dtypes(include=["datetime64[ns]"]).columns.tolist()

    if date_cols:
        col = date_cols[0]
        df["year"] = df[col].dt.year
        df["month"] = df[col].dt.month
        df["quarter"] = df[col].dt.quarter

    return df
