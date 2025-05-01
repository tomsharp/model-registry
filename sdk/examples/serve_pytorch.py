from mlops.registry.torch import TorchModel
from mlops.registry import ModelRegistry
from mlops.serving.serve import Serving


registry = ModelRegistry()
serving = Serving(registry)

model_id = "defe0b5d4984494d9fdabaa2e3e9ddb1"
serving._create_image(model_id)