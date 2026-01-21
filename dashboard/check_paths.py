from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
print(BASE_DIR / "data" / "models" / "lr_churn_model.pkl")
print((BASE_DIR / "data" / "models").exists())
