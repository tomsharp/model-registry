import os
from setuptools import setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name="model_registry",
    version="0.0.1",
    author="Tom Sharp",
    author_email="tom@tomsharp.io",
    packages=["model_registry"],
)
