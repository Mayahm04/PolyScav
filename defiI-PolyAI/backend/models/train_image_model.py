import torch
import torch.nn as nn
from torch.utils.data import DataLoader
from torchvision import datasets, transforms, models
import joblib

# ----------- CONFIG -----------
DATA_DIR = "../dataset"
MODEL_PATH = "models/image_model.pth"
LABEL_MAP_PATH = "models/label_map.pkl"

BATCH_SIZE = 16
EPOCHS = 5
LR = 1e-4

# ----------- PREPROCESS -----------
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize([0.5, 0.5, 0.5],
                         [0.5, 0.5, 0.5])
])


dataset = datasets.ImageFolder(DATA_DIR, transform=transform)
train_loader = DataLoader(dataset, batch_size=BATCH_SIZE, shuffle=True)

# mapping dataset → tri écologique
label_map = {
    "cardboard": "papier",
    "paper": "papier",
    "plastic": "plastique",
    "glass": "verre",
    "metal": "métal",
    "trash": "autre"
}

inv_map = {v: k for k, v in label_map.items()}

joblib.dump(label_map, LABEL_MAP_PATH)
print("Label map saved!")

# ----------- MODEL -----------
model = models.efficientnet_b0(weights="DEFAULT")
model.classifier[1] = nn.Linear(model.classifier[1].in_features, 6)

device = "cuda" if torch.cuda.is_available() else "cpu"
model = model.to(device)

criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=LR)

# ----------- TRAIN LOOP -----------
for epoch in range(EPOCHS):
    model.train()
    total_loss = 0

    for imgs, labels in train_loader:
        imgs, labels = imgs.to(device), labels.to(device)

        optimizer.zero_grad()
        outputs = model(imgs)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()

        total_loss += loss.item()

    print(f"Epoch {epoch+1}/{EPOCHS} | Loss = {total_loss:.4f}")

torch.save(model.state_dict(), MODEL_PATH)
print("Model saved to", MODEL_PATH)
