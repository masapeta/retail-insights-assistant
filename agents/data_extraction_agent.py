from core.query_builder import build_sql
from storage.duckdb_engine import execute_duckdb_query

def data_extraction_agent(state):
    intent = state.get("intent", {})
    metric = state.get("final_metric")

    sql = build_sql(intent, metric)
    state["sql_query"] = sql

    try:
        df = execute_duckdb_query(sql)
        state["sql_result"] = df
    except Exception as e:
        state["sql_error"] = str(e)
        state["sql_result"] = None

    return state
