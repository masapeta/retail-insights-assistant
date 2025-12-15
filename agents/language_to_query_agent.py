import json
from core.prompts import LANG_TO_QUERY
from models.llm_factory import llm

def language_to_query_agent(state):
    user_query = state.get("user_query", "")
    metadata = state.get("metadata", {})

    system_prompt = LANG_TO_QUERY.format(
        numeric_cols=metadata.get("numeric_cols", []),
        categorical_cols=metadata.get("categorical_cols", []),
        date_cols=metadata.get("date_cols", [])
    )

    resp = llm(prompt=user_query, system=system_prompt)

    try:
        intent = json.loads(resp)
    except:
        intent = {"intent": "unknown", "raw": resp}

    state["intent"] = intent
    return state
