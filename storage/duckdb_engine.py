
import duckdb
con = duckdb.connect("retail_insights.duckdb", read_only=False)

def register_dataframe(df, name="sales_data"):
    con.register(name, df)

def execute_duckdb_query(query: str):
    try:
        return con.execute(query).df()
    except Exception as e:
        raise RuntimeError(f"DuckDB query failed: {e}")
