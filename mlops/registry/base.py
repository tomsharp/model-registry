import uuid
from enum import Enum
from abc import abstractmethod

from pydantic import BaseModel, Field, ConfigDict, SkipValidation

def _new_id():
    id = uuid.uuid4()
    return id.hex

class ModelType(str, Enum):
    PT = "PyTorch"

class Metadata(BaseModel):
    id: str = Field(allow_mutation=False)
    name: str = Field(allow_mutation=False)
    version: int
    type: ModelType = Field(allow_mutation=False)


class Model(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    obj: SkipValidation[any]
    name: str

    id: str = Field(default_factory=_new_id, allow_mutation=False)
    version: int = 0
    type: ModelType

    def to_metadata(self) -> Metadata:
        return Metadata(
            id=self.id, name=self.name, version=self.version, type=self.type,
        ).model_dump_json()
    
    @abstractmethod
    def upload_artifact(self, s3_client, bucket, key):
        raise NotImplementedError

    @abstractmethod
    def save_artifact(self, s3_client, bucket, key):
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def load_model(self, s3_client, bucket, key) -> "Model":
        raise NotImplementedError