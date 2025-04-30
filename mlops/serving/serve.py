from typing import Optional
from pathlib import Path 
import shutil

import docker

from mlops.registry.base import ModelType
from mlops.registry._registry import ModelRegistry


class Serving:
    def __init__(self, registry: ModelRegistry) -> None:
        self.registry = registry

    def _create_image(self, model_id: int, model_version: Optional[int] = None) -> str:
        try:
            tmp_path = (Path(".") / "tmp/serve")
            tmp_path.mkdir(parents=True)

            model = self.registry.load_model(model_id, model_version)
            file_path = f"{tmp_path}/downloaded.pt"
            model.save_artifact(file_path)

        except Exception as e:
            shutil.rmtree(tmp_path)
            raise e

    def serve(self):
        pass