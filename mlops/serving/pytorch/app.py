import torch
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()
model = torch.load("model.pt")
model.eval()

class PredictRequest(BaseModel):
    input: list

@app.post("/predict")
def predict(req: PredictRequest):
    try:
        input_tensor = torch.tensor(req.input)
        with torch.no_grad():
            output = model(input_tensor)
        return {"output": output.tolist()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
