import pandas as pd
import re
from pathlib import Path
from sentence_transformers import SentenceTransformer, util
from urllib.parse import urlparse
import torch
BASE_DIR = Path(__file__).resolve().parent
facts = pd.read_csv(BASE_DIR / "fact_db.csv")
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
model = SentenceTransformer("all-MiniLM-L6-v2", device=DEVICE)
fact_embeddings = model.encode(
    facts["claim"].tolist(),
    convert_to_tensor=True,
    device=DEVICE
)
def extract_claims(text):
    sentences = re.split(r"[.!?]", text)
    return [
        s.strip() for s in sentences
        if 8 < len(s.split()) < 40
    ]
def generate_reason(confidence):
    if confidence > 0.75:
        return "High semantic similarity with verified dataset."
    elif confidence > 0.5:
        return "Moderate similarity; partial match with known facts."
    else:
        return "Low similarity; claim may be misleading or unsupported."
def get_credibility_score(url):
    if not url:
        return None
    domain = urlparse(url).netloc
    if ".gov" in domain or ".edu" in domain:
        return 85
    elif "news" in domain:
        return 65
    elif "blog" in domain:
        return 50
    else:
        return 40
def verify_article(text, url=None):
    claims = extract_claims(text)
    if not claims:
        return {
            "claims": [],
            "truth_percentage": 0,
            "credibility_score": get_credibility_score(url),
            "confidence_graph": []
        }
    claim_embeddings = model.encode(
        claims,
        convert_to_tensor=True,
        device=DEVICE
    )
    scores = util.cos_sim(claim_embeddings, fact_embeddings)
    results = []
    confidence_data = []
    true_count = 0
    for i, claim in enumerate(claims):
        best_index = scores[i].argmax().item()
        fact = facts.iloc[best_index]
        confidence = float(scores[i][best_index])
        result = {
            "claim": claim,
            "status": "True" if fact["label"] == 1 else "False",
            "reason": generate_reason(confidence),
            "correct_fact": fact["correct_fact"],
            "source": fact["source"],
            "confidence": round(confidence, 4)
        }
        if result["status"] == "True":
            true_count += 1
        results.append(result)
        confidence_data.append({
            "claim": claim[:50],
            "confidence": round(confidence, 4)
        })
    truth_percentage = (true_count / len(results)) * 100
    return {
        "claims": results,
        "truth_percentage": round(truth_percentage, 2),
        "credibility_score": get_credibility_score(url),
        "confidence_graph": confidence_data
    }