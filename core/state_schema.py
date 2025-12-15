
from typing import TypedDict, Dict, Any, List
import pandas as pd

class State(TypedDict):
    user_query: str
    metadata: Dict[str, Any]
    summary_mode: str
    final_metric: str
    intent: Dict[str, Any]
    validated: bool
    sql_query: str
    sql_result: pd.DataFrame
    retrieved_chunks: List[str]
    final_answer: str
