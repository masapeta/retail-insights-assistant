import sys
import os
import streamlit as st
import pandas as pd

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from data_pipeline.ingestion import load_data
from data_pipeline.cleaning import clean
from data_pipeline.preprocessing import detect_schema, enrich
from data_pipeline.chunking import hybrid_chunk_dataframe
from data_pipeline.embeddings import embed_hybrid_chunks
from data_pipeline.vector_store import vector_store

from storage.duckdb_engine import register_dataframe
from core.langgraph_workflow import run_assistant

st.set_page_config(page_title="Data Insights Assistant", layout="wide")
st.title("Data Insights Assistant (Hybrid RAG + Multi-Agent Analytics)")

@st.cache_resource(show_spinner=False)
def initialize_hybrid_rag(df, final_metric):
    vector_store.__init__()

    hybrid_chunks = hybrid_chunk_dataframe(
        df,
        metric=final_metric,
        top_n=5,
        chunk_size=200
    )

    embedded_chunks = embed_hybrid_chunks(hybrid_chunks)

    vector_store.add_chunks(embedded_chunks)

    return True

uploaded = st.file_uploader("Upload your CSV / Excel / JSON file", type=["csv", "xlsx", "json"])

df = None
metadata = None
final_metric = None
summary_mode = "narrative"
rag_ready = False

if uploaded:
    st.subheader("Data Preview")

    df = load_data(uploaded)
    df = clean(df)
    df = enrich(df)

    st.dataframe(df.head())

    metadata = detect_schema(df)

    register_dataframe(df)

    numeric_cols = metadata.get("numeric_cols", [])
    auto_metric = metadata.get("primary_metric")

    if numeric_cols:
        final_metric = st.selectbox(
            "Select numeric metric for analysis:",
            options=numeric_cols,
            index=numeric_cols.index(auto_metric) if auto_metric in numeric_cols else 0
        )
    else:
        st.info("No numeric columns found. COUNT-based insights will be used.")
        final_metric = None

    summary_mode = st.selectbox(
        "Choose summary mode:",
        ["narrative", "kpi"],
        index=0
    )

    st.subheader("Initializing Hybrid RAG Pipeline...")
    with st.spinner("Generating hybrid chunks, embeddings, and vector index…"):

        rag_ready = initialize_hybrid_rag(df, final_metric)

    if rag_ready:
        st.success("Hybrid RAG pipeline initialized successfully!")

query = st.text_input("Ask a question about your dataset:")

if st.button("Run Assistant"):
    if df is None:
        st.error("Please upload a dataset first.")
    else:
        state = {
            "user_query": query,
            "metadata": metadata,
            "summary_mode": summary_mode,
            "final_metric": final_metric,
            "intent": {},
            "validated": False,
            "sql_query": "",
            "sql_result": pd.DataFrame(),
            "retrieved_chunks": [],
            "final_answer": ""
        }

        with st.spinner("Analyzing your dataset..."):
            result = run_assistant(state)

        st.subheader("Final Answer")
        st.write(result.get("final_answer", "No answer returned."))
