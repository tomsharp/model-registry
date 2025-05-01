from typing import Optional
from pathlib import Path 
import shutil

import docker

from mlops.registry import ModelRegistry
from mlops.registry.base import ModelType

def build_docker_image(client, path, tag):
    # Build the Docker image
    for image, logs in client.images.build(path=path, tag=tag, nocache=True, rm=True):
        # Yield the image and logs as they are being built
        yield image, logs

class Deployer:
    def __init__(self, registry: ModelRegistry) -> None:
        self.registry = registry

    def pull_image(self):
        pass


    def serve(self):
        pass