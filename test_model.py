from PIL import Image
from vision.predict import (
    load_model,
    predict_image,
    suggest_category
)

print("Loading EcoSort Edge trained model...")

model, preprocess, categories = load_model()

print("Model loaded successfully!")
print("Available classes:", categories)

image_path = input("\nEnter image path: ")

image = Image.open(image_path).convert("RGB")

predictions, response_time = predict_image(
    image,
    model,
    preprocess,
    categories
)

print("\nPREDICTION RESULTS")

for item in predictions:
    print(
        item["label"],
        f'{item["confidence"] * 100:.2f}%'
    )

print(
    "\nSuggested category:",
    suggest_category(predictions[0]["label"])
)

print(f"Processing time: {response_time:.2f} ms")