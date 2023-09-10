import torch.nn.functional as F
import io
from PIL import Image
from transformers import ViTForImageClassification, ViTFeatureExtractor

device = "cpu"  # "cuda" if torch.cuda.is_available() else "cpu"
model = ViTForImageClassification.from_pretrained("imjeffhi/pokemon_classifier").to(device)
feature_extractor = ViTFeatureExtractor.from_pretrained('imjeffhi/pokemon_classifier')

def recognize_pokemon(data: bytes) -> str:
    img = Image.open(io.BytesIO(data))
    extracted = feature_extractor(images=img, return_tensors='pt').to(device)
    outputs = model(**extracted)
    logits = outputs.logits
    predicted_id = logits.argmax(-1).item()
    predicted_pokemon = model.config.id2label[predicted_id]
    confidence_scores = F.softmax(logits, dim=1).squeeze().tolist()
    confidence_score = confidence_scores[predicted_id]
    if confidence_score > 0.7:
        return predicted_pokemon
    return None

if __name__ == "__main__":
    with open("eve.png", "rb") as f:
        print(f"POKEMON FOUND: {recognize_pokemon(f.read())}")