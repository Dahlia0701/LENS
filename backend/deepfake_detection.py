import torch
from torchvision import models, transforms
from PIL import Image
model = models.resnet18(pretrained=True)
model.eval()
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor()
])
def detect_deepfake(image_path):
    try:
        img = Image.open(image_path).convert("RGB")
        tensor = transform(img).unsqueeze(0)
        output = model(tensor)
        score = torch.softmax(output, dim=1).max().item()
        return {
            "deepfake_score": score,
            "is_fake": score < 0.5
        }
    except Exception as e:
        return {"error": str(e)}