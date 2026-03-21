from transformers import CLIPProcessor, CLIPModel
from PIL import Image
import torch
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
model = CLIPModel.from_pretrained(
    "openai/clip-vit-base-patch32"
).to(DEVICE)
processor = CLIPProcessor.from_pretrained(
    "openai/clip-vit-base-patch32"
)
def verify_image_with_clip(image_path, text):
    try:
        image = Image.open(image_path).convert("RGB")
        short_text = text[:100] if text else "news image"
        prompts = [
            short_text,
            "real news image",
            "fake news image",
            "manipulated or edited image"
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
        result = {
            "scores": {
                "text_match": float(probs[0]),
                "real": float(probs[1]),
                "fake": float(probs[2]),
                "manipulated": float(probs[3])
            },
            "image_match": bool(probs[0] > 0.5),
            "verdict": get_verdict(probs)
        }
        return result
    except Exception as e:
        return {"error": str(e)}
def get_verdict(probs):
    labels = ["text_match", "real", "fake", "manipulated"]
    max_index = probs.argmax()
    return {
        "label": labels[max_index],
        "confidence": float(probs[max_index])
    }