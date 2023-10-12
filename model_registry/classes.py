"""Classes for model registry."""
from pydantic import BaseModel, Field
from uuid import uuid4
import boto3
import pickle
import json


def _uuid4_hex():
    return uuid4().hex


class ModelMetadata(BaseModel):
    id: str = Field(default_factory=_uuid4_hex)


class ModelRegistry:
    def __init__(self, registry_name: str):
        self._bucket_name = registry_name
        self._s3 = boto3.resource("s3")

    def _metadata_path(self, model_id: str) -> str:
        return f"{model_id}/metadata.json"

    def _model_obj_path(self, model_id: str) -> str:
        return f"{model_id}/model.pkl"

    def register_model(self, obj) -> str:
        model = ModelMetadata()

        # save metadata
        self._s3.Object(self._bucket_name, self._metadata_path(model.id)).put(
            Body=model.model_dump_json()
        )

        # save model
        self._s3.Object(self._bucket_name, self._model_obj_path(model.id)).put(
            Body=pickle.dumps(obj)
        )

        return model.id

    def get_metadata(self, model_id) -> ModelMetadata:
        # TODO - move to client for everything and delete s3 resource
        s3 = boto3.client("s3")
        response = s3.get_object(
            Bucket=self._bucket_name, Key=self._metadata_path(model_id)
        )
        metadata_json = json.loads(response["Body"].read().decode("utf-8"))
        return ModelMetadata(**metadata_json)

    def get_model(self, model_id):
        # TODO - add output type
        s3 = boto3.client("s3")
        response = s3.get_object(
            Bucket=self._bucket_name, Key=self._model_obj_path(model_id)
        )["Body"].read()
        return pickle.loads(response)

    def delete_model(self, model_id):
        s3 = boto3.client("s3")
        objects = s3.list_objects(Bucket=self._bucket_name, Prefix=model_id)
        for object in objects["Contents"]:
            s3.delete_object(Bucket=self._bucket_name, Key=object["Key"])
        s3.delete_object(Bucket=self._bucket_name, Key=model_id)
