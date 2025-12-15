from data_pipeline.vector_store import vector_store
from models.embedding_model import embed_texts

def rag_retrieval_agent(state):
    query = state.get("user_query", "")

    try:
        vec = embed_texts([query])[0]
    except:
        state["retrieved_chunks"] = []
        return state

    chunks = vector_store.search(vec, k=5)

    formatted = []
    for c in chunks:
        formatted.append(f"[TYPE={c['type']}]\n{c['content']}")

    state["retrieved_chunks"] = formatted
    return state
