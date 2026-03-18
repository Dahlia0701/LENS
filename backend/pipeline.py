import pandas as pd
import re
from pathlib import Path
from sentence_transformers import SentenceTransformer, util
from urllib.parse import urlparse
BASE_DIR = Path(__file__).resolve().parent
facts = pd.read_csv(BASE_DIR / "fact_db.csv")
model = SentenceTransformer("all-MiniLM-L6-v2")
fact_embeddings = model.encode(
    facts["claim"].tolist(), convert_to_tensor=True
)
def extract_claims(text):
    sentences = re.split(r"[.!?]", text)
    return [s.strip() for s in sentences if len(s.strip()) > 25]
def verify_claim(claim):
    claim_embedding = model.encode(claim, convert_to_tensor=True)
    scores = util.cos_sim(claim_embedding, fact_embeddings)
    best_index = scores.argmax().item()
    fact = facts.iloc[best_index]
    confidence = float(scores[0][best_index])
    return {
        "claim": claim,
        "status": "True" if fact["label"] == 1 else "False",
        "reason": f"Matched with similar claim (confidence: {round(confidence,2)})",
        "correct_fact": fact["correct_fact"],
        "source": fact["source"],
        "confidence": confidence
    }
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
    results = []
    true_count = 0
    for claim in claims:
        result = verify_claim(claim)
        if result["status"] == "True":
            true_count += 1
        results.append(result)
    truth_percentage = (true_count / len(results)) * 100 if results else 0
    return {
        "claims": results,
        "truth_percentage": round(truth_percentage, 2),
        "credibility_score": get_credibility_score(url)
    }