import boto3
import pickle
import os
from fastapi import FastAPI

app = FastAPI()

s3_client = boto3.client('s3')
model = None

def fetch_model_from_s3(model_id: str, version: int, framework: str):
    bucket_name = "your-model-registry-bucket"
    model_key = f"{model_id}/v{version}/model.{framework}"  # Model path in registry
    model_data = s3_client.get_object(Bucket=bucket_name, Key=model_key)
    
    if framework == "pytorch":
        import torch
        return torch.load(model_data['Body'])  # Or use appropriate method for loading the model
    elif framework == "tensorflow":
        import tensorflow
        return tensorflow.keras.models.load_model(model_data['Body'])
    else:
        raise ValueError("Unsupported framework")

@app.on_event("startup")
async def startup():
    model_id = os.getenv("MODEL_ID", "default_model_id")
    model_version = int(os.getenv("MODEL_VERSION", 1))
    model_framework = os.getenv("MODEL_FRAMEWORK", "pytorch")
    
    global model
    model = fetch_model_from_s3(model_id, model_version, model_framework)

@app.post("/predict")
async def predict(data: list):
    if model:
        prediction = model.predict(data)  # Adjust according to your framework (e.g., model.forward() for PyTorch)
        return {"prediction": prediction.tolist()}
    else:
        return {"error": "Model not loaded."}
