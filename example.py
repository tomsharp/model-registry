"""Example use of model registry."""
import json

from sklearn import datasets, svm

from model_registry.classes import ModelRegistry

# load config
with open("config.json", "rb") as fp:
    config = json.load(fp)
registry_name = config["registry_bucket_name"]

# train sklearn model
iris = datasets.load_iris()
digits = datasets.load_digits()
model = svm.SVC(gamma=0.001, C=100.0)
model.fit(digits.data[:-1], digits.target[:-1])

# register model
registry = ModelRegistry(registry_name)
model_id = registry.register_model(model)
print(model_id)

# get metadata
metadata = registry.get_metadata(model_id)
print(metadata)

# get model object
model_obj = registry.get_model(model_id)
print(model_obj)

# delete object
registry.delete_model(model_id)
