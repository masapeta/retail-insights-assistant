import json
from core.prompts import VALIDATION
from models.llm_factory import llm

def validation_agent(state):
    intent = state.get("intent", {})
    metadata = state.get("metadata", {})

    prompt = VALIDATION.format(
        intent_json=json.dumps(intent),
        numeric_cols=metadata.get("numeric_cols", []),
        categorical_cols=metadata.get("categorical_cols", []),
        date_cols=metadata.get("date_cols", [])
    )

    resp = llm(prompt)

    try:
        block = json.loads(resp)
    except Exception:
        state["validated"] = True
        return state

    cleaned = block.get("cleaned_intent", intent)

    numeric_cols = metadata.get("numeric_cols", [])
    filters = cleaned.get("filters", {})
    safe_filters = {}

    for col, val in filters.items():
        if col in numeric_cols or col in metadata.get("categorical_cols", []):
            safe_filters[col] = val

    cleaned["filters"] = safe_filters

    state["validated"] = block.get("validated", True)
    state["intent"] = cleaned

    return state
