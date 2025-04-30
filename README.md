# model-registry
Library to interact with S3 bucket as a Model Registry.


# How to use this Repo

## Warning
- Never commit your AWS Account ID to git. Save it in an `.env` file and ensure `.env` is added to your `.gitiginore`


## Setup, Deploy, and Install

### Setup
Add an `.env` file containing your AWS account ID and region. Example file:
```
AWS_ACCOUNT_ID=1234567890
AWS_DEFAULT_REGION=ap-southeast-1
AWS_ACCESS_KEY_ID=accesskeyvalue
AWS_SECRET_ACCESS_KEY=secretkeyvalue
REGISTRY_NAME=my-model-registry
```

Optionally, you can set your terraform state to be saved in an S3 bucket by adding the following block to the top of the `main.tf` file
```
terraform {
  backend "s3" {
    bucket = "bucketname"
    key    = "mypath/terraform.tfstate"
    region = "ap-southeast-1"
  }
}
```

### Terraform Init 
Run the following command to initialize terraform
```
make tf-init
```

### Deploy
Deploy the registry to S3 using the following command
```
make deploy-registry
```

Export the bucket name to your envrionment.
At the end of the above command, Terraform will print your `bucket_name`. Export that using the following command:
```
export REGISTRY_BUCKET=<bucket_name_from_terraform_output>
```

### Install 
Install the Python library

```
make install
```


## Usage 

#### Create model
    Using PyTorch as an example:
    ```
    from registry.torch import TorchModel
    from registry.registry import ModelRegistry
    model = TorchModel(obj=NeuralNetwork(), name="my_torch_model")
    ```

#### Upload to registry
    ```
    registry = ModelRegistry()
    registry.upload_model(model)
    ```

#### Load model from registry
    ```
    registry = ModelRegistry()
    loaded_model = registry.load_model(model_id)
    ```

#### list model_ids
    ```
    registry = ModelRegistry()
    model_ids = registry.list_models()
    print(model_ids)
    ```

#### Delete model
    ```
    registry.delete_model(model_id)
    ```