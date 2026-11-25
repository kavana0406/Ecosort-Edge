from pathlib import Path
import time
import torch
import torch.nn as nn
from torchvision import models, transforms

BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_PATH = BASE_DIR / "models" / "ewaste_mobilenetv3.pth"

DEVICE = torch.device(
    "cuda" if torch.cuda.is_available() else "cpu"
)


def load_model():

    if not MODEL_PATH.exists():
        raise FileNotFoundError(
            "Trained model not found. Run train_model.py first."
        )

    checkpoint = torch.load(
        MODEL_PATH,
        map_location=DEVICE,
        weights_only=True
    )

    class_names = checkpoint["class_names"]

    model = models.mobilenet_v3_small(weights=None)

    input_features = model.classifier[3].in_features

    model.classifier[3] = nn.Linear(
        input_features,
        len(class_names)
    )

    model.load_state_dict(checkpoint["model_state_dict"])
    model.to(DEVICE)
    model.eval()

    preprocess = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(
            [0.485, 0.456, 0.406],
            [0.229, 0.224, 0.225]
        )
    ])

    return model, preprocess, class_names


def predict_image(image, model, preprocess, categories):

    start_time = time.perf_counter()

    image = image.convert("RGB")
    tensor = preprocess(image).unsqueeze(0).to(DEVICE)

    with torch.no_grad():
        output = model(tensor)
        probabilities = torch.softmax(output[0], dim=0)

    values, indices = torch.topk(
        probabilities,
        min(3, len(categories))
    )

    predictions = []

    for value, index in zip(values, indices):
        predictions.append({
            "label": categories[index.item()],
            "confidence": float(value.item())
        })

    response_time = (
        time.perf_counter() - start_time
    ) * 1000

    return predictions, response_time


def suggest_category(label):

    category_map = {
        "mobile_tablet": "Mobile / Tablet",
        "charger_adapter": "Charger / Adapter",
        "cable": "Cable",
        "circuit_board": "Circuit Board",
        "computer_accessory": "Computer Accessory",
        "other_ewaste": "Other E-waste",
        "non_ewaste": "Non-E-waste"
    }

    return category_map.get(label, "Uncertain")