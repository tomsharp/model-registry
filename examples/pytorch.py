import torch

from registry.base import Model
from registry.torch import TorchModel
from registry.registry import ModelRegistry

class NeuralNetwork(torch.nn.Module):
    def __init__(self):
        super().__init__()
        self.flatten = torch.nn.Flatten()
        self.linear_relu_stack = torch.nn.Sequential(
            torch.nn.Linear(28 * 28, 512),
            torch.nn.ReLU(),
            torch.nn.Linear(512, 512),
            torch.nn.ReLU(),
            torch.nn.Linear(512, 10),
        )

    def forward(self, x):
        x = self.flatten(x)
        logits = self.linear_relu_stack(x)
        return logits


if __name__ == "__main__":
    # create model
    model = TorchModel(obj=NeuralNetwork(), name="my_torch_model")

    # upload to registry
    registry = ModelRegistry()
    registry.upload_model(model)

    # load model from registry
    loaded_model = registry.load_model(model.id)
    print(loaded_model)

    # upload new model version
    print(loaded_model.version)
    registry.upload_model(loaded_model)

    # list model versions
    versions = registry.list_model_versions(model.id)
    print(versions)

    # # new model
    new_model = TorchModel(obj=NeuralNetwork(), name="new_model")
    print(new_model.id)
    registry.upload_model(new_model)

    # list models
    model_ids = registry.list_models()
    print(model_ids)

    # delete model
    registry.delete_model(model.id)
    registry.delete_model(new_model.id)
