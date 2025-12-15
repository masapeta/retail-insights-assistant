from core.prompts import INSIGHT
from models.llm_factory import llm

def insight_generation_agent(state):
    df = state.get("sql_result")

    if df is not None and not df.empty:
        try:
            table = df.to_string(index=False)
        except:
            table = "Unable to render SQL table."
    else:
        table = "No SQL results available."

    context = "\n\n".join(state.get("retrieved_chunks", []))

    prompt = INSIGHT.format(
        user_query=state.get("user_query", ""),
        data_table=table,
        context=context,
        summary_mode=state.get("summary_mode", "narrative"),
        metric=state.get("final_metric") or "COUNT(*) fallback"
    )

    answer = llm(prompt)
    state["final_answer"] = answer
    return state
