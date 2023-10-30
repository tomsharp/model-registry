aws codeartifact login --tool twine --domain mlops --domain-owner $AWS_ACCOUNT_ID --repository model-registry
export TWINE_USERNAME=aws
export TWINE_PASSWORD=`aws codeartifact get-authorization-token --domain mlops --domain-owner $AWS_ACCOUNT_ID --query authorizationToken --output text`
export TWINE_REPOSITORY_URL=`aws codeartifact get-repository-endpoint --domain mlops --domain-owner $AWS_ACCOUNT_ID --repository model-registry --format pypi --query repositoryEndpoint --output text`
twine upload --repository codeartifact dist/*
