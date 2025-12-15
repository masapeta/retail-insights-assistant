import pandas as pd
import numpy as np

def generate_row_chunks(df: pd.DataFrame, chunk_size: int = 200):
    chunks = []
    for i in range(0, len(df), chunk_size):
        block = df.iloc[i:i+chunk_size]
        text = block.to_json()
        chunks.append({"type": "row", "content": text})
    return chunks


def generate_column_schema_chunks(df: pd.DataFrame):
    chunks = []

    for col in df.columns:
        series = df[col]
        dtype = str(series.dtype)

        unique_vals = series.dropna().unique()
        sample_vals = unique_vals[:5].tolist()

        chunk_text = (
            f"COLUMN SUMMARY:\n"
            f"Name: {col}\n"
            f"Type: {dtype}\n"
            f"Unique Values: {len(unique_vals)}\n"
            f"Sample Values: {sample_vals}\n"
            f"Missing Values: {series.isna().sum()}\n"
        )

        chunks.append({"type": "column_schema", "content": chunk_text})

    return chunks


def generate_statistical_chunks(df: pd.DataFrame, metric: str, top_n: int = 5):
    chunks = []

    if metric is None or metric not in df.columns:
        return chunks

    numeric_series = df[metric]
    numeric_summary = (
        f"GLOBAL METRIC SUMMARY:\n"
        f"Metric: {metric}\n"
        f"Total: {numeric_series.sum()}\n"
        f"Average: {numeric_series.mean()}\n"
        f"Std Dev: {numeric_series.std()}\n"
        f"Min: {numeric_series.min()}\n"
        f"Max: {numeric_series.max()}\n"
    )
    chunks.append({"type": "metric_global", "content": numeric_summary})

    categorical_cols = df.select_dtypes(include=['object']).columns.tolist()

    for col in categorical_cols:
        if col == metric:
            continue

        grouped = df.groupby(col)[metric].sum().sort_values(ascending=False)
        top_items = grouped.head(top_n)

        text = f"TOP {top_n} {col.upper()} BY {metric}:\n"
        for idx, value in top_items.items():
            text += f"{idx}: {value}\n"

        chunks.append({"type": "stat_summary", "content": text})

    return chunks


def generate_date_chunks(df: pd.DataFrame, metric: str, top_n: int = 5):

    chunks = []

    date_cols = [c for c in df.columns if pd.api.types.is_datetime64_any_dtype(df[c])]
    if not date_cols:
        return chunks

    date_col = date_cols[0]

    if metric not in df.columns:
        return chunks

    df['__month'] = df[date_col].dt.month
    monthly = df.groupby('__month')[metric].sum().sort_values(ascending=False)

    text = "MONTHLY SUMMARY (Top {}):\n".format(top_n)
    for month, value in monthly.head(top_n).items():
        text += f"Month {month}: {value}\n"
    chunks.append({"type": "date_monthly", "content": text})

    df['__quarter'] = df[date_col].dt.quarter
    quarterly = df.groupby('__quarter')[metric].sum().sort_values(ascending=False)

    text = "QUARTERLY SUMMARY (Top {}):\n".format(top_n)
    for q, value in quarterly.head(top_n).items():
        text += f"Q{q}: {value}\n"
    chunks.append({"type": "date_quarterly", "content": text})

    df['__year'] = df[date_col].dt.year
    yearly = df.groupby('__year')[metric].sum().sort_values(ascending=False)

    text = "YEARLY SUMMARY:\n"
    for year, value in yearly.items():
        text += f"{year}: {value}\n"
    chunks.append({"type": "date_yearly", "content": text})

    df.drop(columns=['__month', '__quarter', '__year'], inplace=True)

    return chunks


def hybrid_chunk_dataframe(df: pd.DataFrame, metric: str, top_n: int = 5, chunk_size: int = 200):

    chunks = []

    chunks.extend(generate_row_chunks(df, chunk_size))
    chunks.extend(generate_column_schema_chunks(df))
    chunks.extend(generate_statistical_chunks(df, metric, top_n))
    chunks.extend(generate_date_chunks(df, metric, top_n))

    return chunks
