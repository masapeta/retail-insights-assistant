from models.embedding_model import embedding_model
import numpy as np

def embed_text(text: str):
    vec = embedding_model.encode([text])[0]
    return np.array(vec, dtype="float32")


def embed_hybrid_chunks(hybrid_chunks):
    embedded = []

    for chunk in hybrid_chunks:
        text = chunk["content"]
        ctype = chunk["type"]

        vec = embed_text(text)

        embedded.append({
            "type": ctype,
            "content": text,
            "vector": vec
        })

    return embedded
