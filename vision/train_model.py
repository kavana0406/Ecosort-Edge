from pathlib import Path
import json
import torch
import torch.nn as nn
from torch.utils.data import DataLoader
from torchvision import datasets, transforms, models

# Project paths
BASE_DIR = Path(__file__).resolve().parent.parent
TRAIN_DIR = BASE_DIR / "dataset" / "train"
VAL_DIR = BASE_DIR / "dataset" / "val"
MODEL_DIR = BASE_DIR / "models"

MODEL_DIR.mkdir(exist_ok=True)

# Device
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print("Training device:", device)

# Image transformations
train_transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.RandomHorizontalFlip(),
    transforms.RandomRotation(10),
    transforms.ToTensor(),
    transforms.Normalize(
        [0.485, 0.456, 0.406],
        [0.229, 0.224, 0.225]
    )
])

val_transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(
        [0.485, 0.456, 0.406],
        [0.229, 0.224, 0.225]
    )
])

# Load datasets
train_data = datasets.ImageFolder(
    TRAIN_DIR,
    transform=train_transform
)

val_data = datasets.ImageFolder(
    VAL_DIR,
    transform=val_transform
)

# Check class names
print("Classes:", train_data.classes)

if train_data.classes != val_data.classes:
    raise ValueError("Train and validation classes do not match.")

if len(train_data) == 0 or len(val_data) == 0:
    raise ValueError("Training or validation dataset is empty.")

# Data loaders
train_loader = DataLoader(
    train_data,
    batch_size=4,
    shuffle=True
)

val_loader = DataLoader(
    val_data,
    batch_size=4,
    shuffle=False
)

# Load pretrained MobileNetV3-Small
weights = models.MobileNet_V3_Small_Weights.DEFAULT
model = models.mobilenet_v3_small(weights=weights)

# Replace final classification layer
input_features = model.classifier[3].in_features
model.classifier[3] = nn.Linear(
    input_features,
    len(train_data.classes)
)

# Freeze feature extraction layers
for param in model.features.parameters():
    param.requires_grad = False

model = model.to(device)

# Loss and optimizer
criterion = nn.CrossEntropyLoss()

optimizer = torch.optim.Adam(
    model.classifier.parameters(),
    lr=0.001
)

# Training
epochs = 10

for epoch in range(epochs):

    model.train()
    running_loss = 0.0

    for images, labels in train_loader:
        images = images.to(device)
        labels = labels.to(device)

        optimizer.zero_grad()

        outputs = model(images)
        loss = criterion(outputs, labels)

        loss.backward()
        optimizer.step()

        running_loss += loss.item()

    # Validation
    model.eval()
    correct = 0
    total = 0

    with torch.no_grad():
        for images, labels in val_loader:
            images = images.to(device)
            labels = labels.to(device)

            outputs = model(images)
            predictions = outputs.argmax(dim=1)

            total += labels.size(0)
            correct += (predictions == labels).sum().item()

    accuracy = 100 * correct / total

    print(
        f"Epoch [{epoch + 1}/{epochs}] "
        f"Loss: {running_loss / len(train_loader):.4f} "
        f"Validation accuracy: {accuracy:.2f}%"
    )

# Save trained model
model_path = MODEL_DIR / "ewaste_mobilenetv3.pth"

torch.save({
    "model_state_dict": model.state_dict(),
    "class_names": train_data.classes
}, model_path)

# Save class names separately
with open(MODEL_DIR / "class_names.json", "w") as file:
    json.dump(train_data.classes, file, indent=4)

print("\nTraining completed.")
print("Model saved at:", model_path)