import io 
from pathlib import Path
import shutil

from pydantic import Field
import torch 
import boto3

from mlops.registry.base import Model, ModelType


class TorchModel(Model):
    type: ModelType = Field(ModelType.PT, allow_mutation=False)

    def upload_artifact(self, bucket: str, artifact_prefix: str):
        buffer = io.BytesIO()
        scripted_model = torch.jit.script(self.obj)
        torch.jit.save(scripted_model, buffer)
        buffer.seek(0)

        s3_client = boto3.client('s3')
        artifact_key = f"{artifact_prefix}/model.pt"
        s3_client.upload_fileobj(buffer, bucket, artifact_key)

    def save_artifact(self, save_path: str):
        torch.jit.save(self.obj, save_path)

    @classmethod
    def load_model(cls, metadata, bucket, artifact_prefix) -> "TorchModel":
        # Download from S3 to a buffer
        buffer = io.BytesIO()
        s3_client = boto3.client('s3')
        artifact_key = f"{artifact_prefix}/model.pt"
        s3_client.download_fileobj(bucket, artifact_key, buffer)
        buffer.seek(0)

        # Load TorchScript model
        loaded_model = torch.jit.load(buffer)
        loaded_model.eval()
        
        # Create a TorchModel instance with metadata
        return cls(
            id=metadata.id,
            name=metadata.name,
            version=metadata.version,
            type=ModelType.PT,
            obj=loaded_model
        )