include .env 

.EXPORT_ALL_VARIABLES:
TF_VAR_region=${AWS_DEFAULT_REGION}
TF_VAR_app_name=${APP_NAME}

tf-init:
	cd infra && terraform init

deploy-registry: 
	cd infra && terraform init && terraform apply -target=resource.aws_s3_bucket.registry_bucket -auto-approve

destroy-registry: 
	cd infra && terraform init && terraform destroy -target=resource.aws_s3_bucket.registry_bucket -auto-approve

deploy-serving:
	cd infra && terraform init && terraform apply -target=module.serving -auto-approve

destroy-serving: 
	cd infra && terraform init && terraform destroy -target=module.serving -auto-approve

build-push-image-sklearn:
	bash serving/docker/build.sh ${TF_VAR_app_name} sklearn

build-push-image-pytorch:
	bash serving/docker/build.sh ${TF_VAR_app_name} pytorch

deploy: 
	cd infra && terraform init && terraform apply -auto-approve
	bash serving/docker/build.sh ${TF_VAR_app_name} pytorch

destroy:
	cd infra && terraform init && terraform destroy -auto-approve