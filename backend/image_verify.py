from transformers import CLIPProcessor, CLIPModel
from PIL import Image
import torch
import numpy as np
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32").to(DEVICE)
processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")
def verify_image_with_clip(image_path, text):
    try:
        image = Image.open(image_path).convert("RGB")
        short_text = text[:120] if text else "news image"
        prompts = [
            short_text,
            "a real news photograph",
            "a fake or edited image",
            "an AI generated image",
            "a manipulated news image"
        ]
        inputs = processor(
            text=prompts,
            images=image,
            return_tensors="pt",
            padding=True
        ).to(DEVICE)
        with torch.no_grad():
            outputs = model(**inputs)
        probs = outputs.logits_per_image.softmax(dim=1).cpu().numpy()[0]
        text_match = float(probs[0])
        real_score = float(probs[1])
        fake_score = float(probs[2] + probs[3] + probs[4])
        if text_match < 0.35:
            verdict = "Mismatch (Possible Fake Context)"
        elif fake_score > real_score:
            verdict = "Possibly Fake / Manipulated"
        else:
            verdict = "Likely Real"
        return {
            "scores": {
                "text_match": round(text_match, 3),
                "real": round(real_score, 3),
                "fake_combined": round(fake_score, 3)
            },
            "verdict": verdict,
            "confidence": round(max(real_score, fake_score), 3)
        }
    except Exception as e:
        return {"error": str(e)}