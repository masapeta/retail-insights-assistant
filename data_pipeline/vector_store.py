import faiss
import numpy as np
from storage.config import VECTOR_DIM

class HybridVectorStore:

    def __init__(self):
        self.index = faiss.IndexFlatL2(VECTOR_DIM)

        self.chunks = []
        
        self.type_weights = {
            "row": 1.0,
            "column_schema": 1.5,
            "stat_summary": 2.0,
            "metric_global": 2.5,
            "date_monthly": 2.2,
            "date_quarterly": 2.2,
            "date_yearly": 2.0,
        }

    def normalize(self, vec):
        norm = np.linalg.norm(vec)
        if norm == 0:
            return vec
        return vec / norm

    def add_chunks(self, embedded_chunks):
        vectors = []
        for chunk in embedded_chunks:
            norm_vec = self.normalize(chunk["vector"])
            vectors.append(norm_vec.astype("float32"))
            self.chunks.append(chunk)
        vectors = np.array(vectors).astype("float32")
        self.index.add(vectors)

    def search(self, query_vec, k=5):
        query_vec = self.normalize(query_vec).astype("float32")
        distances, indices = self.index.search(np.array([query_vec]), k*3)
        indices = indices[0]
        distances = distances[0]
        weighted_results = []
        for idx, dist in zip(indices, distances):
            if idx >= len(self.chunks):
                continue
            chunk = self.chunks[idx]
            ctype = chunk["type"]
            weight = self.type_weights.get(ctype, 1.0)
            weighted_score = dist / weight
            weighted_results.append((weighted_score, chunk))
        weighted_results.sort(key=lambda x: x[0])
        top_chunks = [chunk for (_, chunk) in weighted_results[:k]]

        return top_chunks

vector_store = HybridVectorStore()
