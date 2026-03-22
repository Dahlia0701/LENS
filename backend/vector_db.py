import faiss
import numpy as np
import pandas as pd
from sentence_transformers import SentenceTransformer
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent
facts = pd.read_csv(BASE_DIR.parent / "fact.csv")
model = SentenceTransformer("all-MiniLM-L6-v2")
embeddings = model.encode(facts["claim"].tolist())
embeddings = np.array(embeddings).astype("float32")
index = faiss.IndexFlatL2(embeddings.shape[1])
index.add(embeddings)
def search(query, k=1):
    q_embed = model.encode([query]).astype("float32")
    distances, indices = index.search(q_embed, k)
    idx = indices[0][0]
    return facts.iloc[idx], float(distances[0][0])