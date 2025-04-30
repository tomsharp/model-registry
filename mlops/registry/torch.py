import io 

from pydantic import Field
import torch 

from mlops.registry.base import Model, ModelType


class TorchModel(Model):
    type: ModelType = Field(ModelType.PT, allow_mutation=False)

    def obj_buffer(self):
        buffer = io.BytesIO()
        torch.save(self.obj, buffer)
        return buffer.getvalue()