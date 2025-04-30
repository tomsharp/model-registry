include .env 

.EXPORT_ALL_VARIABLES:
TF_VAR_region=${AWS_DEFAULT_REGION}
TF_VAR_registry_name=${REGISTRY_NAME}

tf-init:
	cd infra && terraform init

deploy-registry: 
	cd infra && terraform init && terraform apply -auto-approve

destroy-registry: 
	cd infra && terraform init && terraform destroy -auto-approve

install:
	pdm install

run-examples:
	pdm run examples/pytorch.py
