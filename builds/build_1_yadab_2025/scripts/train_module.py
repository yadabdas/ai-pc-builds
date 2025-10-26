import torch
import torch.nn as nn
import pandas as pd
import numpy as np
import random
from sklearn.model_selection import train_test_split

# -----------------------
# Reproducibility
# -----------------------
SEED = 42
torch.manual_seed(SEED)
np.random.seed(SEED)
random.seed(SEED)
torch.cuda.manual_seed_all(SEED)

# -----------------------
# Synthetic dataset generation
# This simulates a structured asset-valuation style regression problem.
# Each row is an "asset record" with numerical features and a target value.
# -----------------------
num_records = 100
data = {
    "asset_value": np.random.uniform(100_000, 1_000_000, num_records),         # target
    "coverage_ratio": np.random.uniform(10, 80, num_records),                  # %
    "frontage_meters": np.random.uniform(5, 50, num_records),                  # m
    "area_sqm": np.random.uniform(50, 500, num_records),                       # square meters
}

df = pd.DataFrame(data)
df.to_parquet("records.parquet")  # saved for downstream inference / profiling

# -----------------------
# Normalization
# -----------------------
feature_cols = ["coverage_ratio", "frontage_meters", "area_sqm"]
target_col = "asset_value"

features = df[feature_cols].values
targets = df[target_col].values

feature_mean = features.mean(axis=0)
feature_std = features.std(axis=0)
target_mean = targets.mean()
target_std = targets.std()

features_norm = (features - feature_mean) / feature_std
targets_norm = (targets - target_mean) / target_std

# Save normalization params so inference code can reverse-transform
np.savetxt("norm_feature_mean.txt", feature_mean)
np.savetxt("norm_feature_std.txt", feature_std)
np.savetxt("norm_target_mean.txt", [target_mean])
np.savetxt("norm_target_std.txt", [target_std])

# -----------------------
# Train / val split
# -----------------------
X_train, X_val, y_train, y_val = train_test_split(
    features_norm, targets_norm, test_size=0.2, random_state=SEED
)

# -----------------------
# Model definition
# -----------------------
class MLP(nn.Module):
    def __init__(self):
        super().__init__()
        self.layers = nn.Sequential(
            nn.Linear(3, 512),
            nn.ReLU(),
            nn.Linear(512, 256),
            nn.ReLU(),
            nn.Linear(256, 1),
        )

    def forward(self, x):
        return self.layers(x)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = MLP().to(device)

criterion = nn.MSELoss()
optimizer = torch.optim.Adam(model.parameters(), lr=1e-3)

X_train = torch.tensor(X_train, dtype=torch.float32, device=device)
y_train = torch.tensor(y_train, dtype=torch.float32, device=device)
X_val = torch.tensor(X_val, dtype=torch.float32, device=device)
y_val = torch.tensor(y_val, dtype=torch.float32, device=device)

# -----------------------
# Training loop
# -----------------------
for epoch in range(500):
    model.train()
    optimizer.zero_grad()
    outputs = model(X_train).squeeze()
    loss = criterion(outputs, y_train)
    loss.backward()
    optimizer.step()

    if epoch % 100 == 0 or epoch == 499:
        model.eval()
        with torch.no_grad():
            val_outputs = model(X_val).squeeze()
            val_loss = criterion(val_outputs, y_val)
        print(
            f"Epoch {epoch:03d} | "
            f"Train Loss: {loss.item():.4f} | "
            f"Val Loss: {val_loss.item():.4f}"
        )

final_loss = loss.item()

# -----------------------
# Export model to ONNX
# We allow a dynamic batch dimension ("batch_size") so the ONNX model can
# run on multiple rows at once in C++ inference.
# -----------------------
dummy_input = torch.randn(1, 3, device=device)

torch.onnx.export(
    model,
    dummy_input,
    "model.onnx",
    input_names=["input"],
    output_names=["output"],
    dynamic_axes={"input": {0: "batch_size"}, "output": {0: "batch_size"}},
    opset_version=17,
)

print(f"Training complete. Final train loss: {final_loss:.4f}")
print("Saved model.onnx and normalization files.")
