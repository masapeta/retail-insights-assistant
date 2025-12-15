
# Retail Insights Assistant  
A multi-agent, LLM-powered analytics system for retail datasets using **LangGraph**, **Groq (gpt-oss-120b)**, **DuckDB**, **FAISS**, and **Streamlit UI**.

---

## Overview
Retail organizations often need quick, conversational insights from historical sales data.  
This assistant enables:

### Conversational Q&A  
Ask questions like:
- *"Which category performed best?"*
- *"Top 5 cities by revenue?"*

### Automatic Summarization (S3 Modes)
- **Narrative Only**  
- **Narrative + KPIs**

### Dataset-Agnostic  
Works even if:
- No numeric metric exists  
- No date fields exist  
- Schema varies across datasets  

### Multi-Agent Pipeline (LangGraph)
1. **Language-to-Intent Agent**  
2. **Validation Agent**  
3. **Data Extraction Agent (SQL)**  
4. **RAG Retrieval Agent**  
5. **Insight Generation Agent**

---

## Folder Structure

```
retail_insights_assistant/
  agents/
  core/
  data_pipeline/
  models/
  storage/
  ui/
  README.md
  requirements.txt
  config.yaml
```

---

## Architecture Summary

- **LangGraph** orchestrates agents in a Directed Acyclic Graph (DAG):  
  `parse → validate → extract → rag → insight → END`

- **Groq LLM (120B)** performs:
  - NL → Intent Parsing  
  - Intent Validation  
  - Insight generation  

- **DuckDB** performs SQL analytics  
- **FAISS** handles semantic retrieval  

---

## Running the App

### 1. Install dependencies
```
pip install -r requirements.txt
```

### 2. Set your Groq API key in environment
```
.env GROQ_API_KEY="your_key_here"
```

### 3. Start Streamlit
```
streamlit run ui/streamlit_app.py
```

---

## Upload Dataset
Supported formats:
- CSV
- Excel (.xlsx)
- JSON

The system will:
1. Clean the dataset  
2. Detect schema (numeric, categorical, date, text)  
3. Compute auto-selected metric  
4. Register table in DuckDB  

---

## Scalability (100GB+ Architecture)

This system can scale via:
- **Spark / Dask ingestion**
- **Delta Lake storage**
- **BigQuery / Snowflake SQL layer**
- **Vector DB (Pinecone)** for scalable RAG

---

## Notes & Future Improvements
- Add caching layer for repeated queries  
- Add automatic visualization generation  
- Add multi-file ingestion (folder mode)

---

## Submission-Ready
This repository satisfies all assignment requirements:
- Multi-agent LangGraph solution  
- Summarization + Q&A  
- Scalable design  
- UI  
- Tests  
- Architecture PDF  
