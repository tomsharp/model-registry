include .env 

.EXPORT_ALL_VARIABLES:
TF_VAR_region=${AWS_REGION}
TF_VAR_registry_name=${REGISTRY_NAME}


deploy-registry: 
	cd infra && terraform init && terraform apply -auto-approve

destroy-registry: 
	cd infra && terraform init && terraform destroy -auto-approve

install:
	pdm install --no-self

run-examples:
	pdm run python -m examples.pytorch

build:
	pdm run python -m build