from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from deployment_api.services.deployer import deploy_model, undeploy_model, get_deployment_status

router = APIRouter()

# Pydantic models for validation
class DeployRequest(BaseModel):
    model_id: str
    version: int

class DeploymentStatusResponse(BaseModel):
    model_id: str
    version: int
    status: str

@router.post("/deploy")
async def deploy(request: DeployRequest):
    """
    Deploys a model to the serving environment.
    """
    try:
        url = await deploy_model(request.model_id, request.version)
        return {"url": url}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/undeploy/{model_id}")
async def undeploy(model_id: str):
    """
    Undeploys a model and stops serving it.
    """
    try:
        success = await undeploy_model(model_id)
        if success:
            return {"message": f"Model {model_id} undeployed successfully."}
        else:
            raise HTTPException(status_code=404, detail="Model not found or already stopped.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/deployments/{model_id}", response_model=DeploymentStatusResponse)
async def get_status(model_id: str):
    """
    Gets the status of a deployed model.
    """
    try:
        status = await get_deployment_status(model_id)
        return status
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
