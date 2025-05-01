from typing import Optional
from pathlib import Path 
import shutil

import docker

from mlops.registry.base import ModelType
from mlops.registry._registry import ModelRegistry

def build_docker_image(client, path, tag):
    # Build the Docker image
    for image, logs in client.images.build(path=path, tag=tag, nocache=True, rm=True):
        # Yield the image and logs as they are being built
        yield image, logs


class Serving:
    def __init__(self, registry: ModelRegistry) -> None:
        self.registry = registry

    def _create_image(self, model_id: int, model_version: Optional[int] = None) -> str:
        try:
            model = self.registry.load_model(model_id, model_version)
            
            if model.type == ModelType.PT: 
                directory = "pytorch"
                tmp_path = Path(f"docker/{directory}/tmp")
                tmp_path.mkdir(parents=True)
                model_path = f"{tmp_path}/model.pt"

                
            model.save_artifact(model_path)

            client = docker.from_env()
            image, logs = client.images.build(path="docker/pytorch", tag="my-python-app", nocache=True)
            for log in logs:
                print(log.get("stream", ""))

            # clean up tmp 
            shutil.rmtree(tmp_path)

        except Exception as e:
            shutil.rmtree(tmp_path)
            raise e

    def serve(self):
        pass