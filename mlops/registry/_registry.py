import os 
import io
import json 
from typing import Optional

import boto3 
import torch

from mlops.registry.base import Model, ModelType, Metadata
from mlops.registry.torch import TorchModel

class ModelRegistry:
    def __init__(self, bucket: Optional[str] = None) -> None:
        if not bucket:
            bucket = os.environ.get("REGISTRY_BUCKET")
            self._bucket = bucket
        if not self._bucket:
            raise ValueError("Registry bucket name must be passed or in environment.")

        self._s3_client = boto3.client("s3")

    def _get_artifact_key(self, model_id: str, model_version: int) -> str:
        return f"artifacts/{model_id}/{model_version}"

    def _get_metadata_key(self, model_id: str, model_version: int) -> str:
        return f"metadata/{model_id}/{model_version}"

    def upload_model(self, model: Model):
        try:
            model.version += 1
            self._s3_client.put_object(
                Body=model.obj_buffer(),
                Bucket=self._bucket,
                Key=self._get_artifact_key(model.id, model.version),
            )
            self._s3_client.put_object(
                Body=model.to_metadata(),
                Bucket=self._bucket,
                Key=self._get_metadata_key(model.id, model.version),
            )
        except Exception as e:
            # rollback model version if upload fails
            model.version + -1
            raise e

    def list_model_versions(self, model_id: str) -> int:
        response = self._s3_client.list_objects_v2(
            Bucket=self._bucket, Prefix=f"metadata/{model_id}"
        )
        versions = [int(c["Key"].split("/")[-1]) for c in response["Contents"]]
        return sorted(versions)

    def list_models(self) -> list[Metadata]:
        response = self._s3_client.list_objects_v2(
            Bucket=self._bucket, Prefix=f"metadata"
        )
        model_ids = [c["Key"].split("/")[1] for c in response["Contents"]]
        return list(set(model_ids))

    def load_model(
        self, model_id: str, model_version: Optional[int] = None
    ) -> Model:

        if not model_version:
            model_version = self.list_model_versions(model_id)[-1]

        # get metadata first
        metadata_response = self._s3_client.get_object(
            Bucket=self._bucket, Key=self._get_metadata_key(model_id, model_version)
        )
        metadata = Metadata(**json.loads(metadata_response["Body"].read()))

        # load model based on type
        if metadata.type == ModelType.PT:
            artifact_response = self._s3_client.get_object(
                Bucket=self._bucket, Key=self._get_artifact_key(model_id, model_version)
            )
            bytes = artifact_response["Body"].read()

            return TorchModel(
                obj=torch.load(io.BytesIO(bytes)), name=metadata.name, id=metadata.id, version=metadata.version
            )

        raise ValueError(f"Unrecognized model type: {metadata.type}")

    def _delete_model(self, model_id: str, model_version: int):
        self._s3_client.delete_object(
            Bucket=self._bucket, Key=self._get_artifact_key(model_id, model_version)
        )
        self._s3_client.delete_object(
            Bucket=self._bucket, Key=self._get_metadata_key(model_id, model_version)
        )

    def delete_model(self, model_id: str, model_version: Optional[int] = None):
        if not model_version:
            versions = self.list_model_versions(model_id)
            for version in versions:
                self._delete_model(model_id, version)
        else:
            self._delete_model(model_id, model_version)