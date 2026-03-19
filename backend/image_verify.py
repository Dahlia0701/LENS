from transformers import CLIPProcessor, CLIPModel
from PIL import Image
import torch
model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")
def verify_image_with_clip(image_path, text):
    try:
        image = Image.open(image_path)
        short_text = text[:100]
        prompts = [
            short_text,
            "real news image",
            "fake news image",
            "manipulated image"
        ]
        inputs = processor(
            text=prompts,
            images=image,
            return_tensors="pt",
            padding=True
        )
        outputs = model(**inputs)
        probs = outputs.logits_per_image.softmax(dim=1).detach().numpy()[0]
        return {
            "scores": {
                "text_match": float(probs[0]),
                "real": float(probs[1]),
                "fake": float(probs[2]),
                "manipulated": float(probs[3])
            },
            "image_match": probs[0] > 0.5
        }
    except Exception as e:
        return {"error": str(e)}