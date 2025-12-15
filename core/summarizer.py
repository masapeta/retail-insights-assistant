
from models.llm_factory import llm
import pandas as pd

def summarize_dataframe(df: pd.DataFrame, mode: str = "narrative"):
    text = df.to_markdown(index=False)

    if mode == "narrative":
        prompt = f"Provide a narrative summary of this dataset:\n{text}"
    else:
        prompt = f"Provide key highlight KPIs and narrative for:\n{text}"

    return llm(prompt)
