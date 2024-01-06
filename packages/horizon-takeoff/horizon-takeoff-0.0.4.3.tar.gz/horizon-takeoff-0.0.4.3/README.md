<h1 align="center">
Horizon Takeoff
</h1>

<div align="center">
    <img width="400" height="350" src="/img/rocket.png">
</div>

**Horizon Takeoff** is a Python library for simplifying the cloud deployment of LLMs with TitanML's [Takeoff Server](https://github.com/titanml/takeoff-community) on AWS, with a specific focus on EC2 and SageMaker. The deployment process is facilitated through an interactive Terminal User Interface (TUI) for streamlining the configuration of your cloud environment. To gain a deeper understanding of the features offered by the Takeoff Server, refer to TitanML's [documentation](https://docs.titanml.co/docs/intro).

With Horizon-Takeoff, you have the flexibility to choose between two distinct workflows:

**1. Terminal User Interface (TUI):** This approach guides you through a step-by-step process within the terminal. This procedure automatically saves your cloud environment settings in a YAML file and handles cloud orchestration tasks such as handling of the Takeoff Server image to AWS's Elastic Container Registry (ECR), initiating the instance launch and Takeoff Server configuration for LLM inference.

**2. Python API:** Alternatively, you can can manually create the YAML config file according to your specific requirements and execute the orchestration and instance launch in Python. Further details found in the `YAML Configuration` section.

## Requirements

**1.** AWS CLI installed and configured on local machine.  
**2.** Docker installed.  
**3.** Own an AWS account with the following configurations:

* Have an instance profile role with access to `AmazonEC2ContainerRegistryReadOnly`. This will allow access to Docker pulls from ECR within an instance.

* Own a security group allowing inbound traffic to `port: 8000` (required for Takeoff Server community edition) and `port: 3000` (required for Takeoff Server pro edition). This will expose the appropriate Docker endpoints for API calling depending on your server edition of choice.

> Currently, only EC2 instance deployment on the Community edition server is stable, Sagemaker and/or Takeoff Server Pro edition is under development.

# Install <img align="center" width="30" height="29" src="https://media.giphy.com/media/sULKEgDMX8LcI/giphy.gif">
<br>

```
pip install horizon-takeoff
```

# TUI Launch <img align="center" width="30" height="29" src="https://media.giphy.com/media/QLcCBdBemDIqpbK6jA/giphy.gif">
<br>

Launch the TUI for configuring an EC2 instance with the community version of the Takeoff Server:


```bash
horizon-takeoff ec2 community
```

<div style="display: flex; justify-content: center;">
  <video muted controls src="https://private-user-images.githubusercontent.com/79061523/293062674-cd626c61-4397-4498-91d3-f11e2e4ea540.mp4" class="d-block rounded-bottom-2 border-top width-fit" style="max-height:640px; min-height: 200px"></video>
</div>

# Staging <img align="center" width="30" height="29" src="https://media.giphy.com/media/SmaYvew52UlC9MmB6l/giphy.gif">
<br>

After you've finished the TUI workflow, a YAML configuration file will be automatically stored in your working directory. This file will trigger the staging process of your deployment and you will receive a notification in terminal of your instance launch. 

Wait a few minutes as the instance downloads the LLM model and initiates the Docker container containing the Takeoff Server. To keep track of the progress and access your instance's initialization logs, you can SSH into your instance:

```bash
ssh -i ~/<pem.key> <user>@<public-ipv4-dns>  # e.g. ssh -i ~/aws.pem ubuntu@ec2-44-205-255-59.compute-1.amazonaws.com
```

In your instance's terminal, run the following command to view your logs to confirm when your container is up and running:

```bash
cat /var/log/cloud-init-output.log
```

If you observe the Uvicorn URL endpoint being displayed, it signifies that your Docker container is operational and you are now ready to invoke API calls to the inference endpoint.

# Calling the Endpoint <img align="center" width="30" height="29" src="https://media.giphy.com/media/l41YvpiA9uMWw5AMU/giphy.gif">
<br>

Once you've initialized the EC2Endpoint class, you can effortlessly invoke your LLM in the cloud with just a single line of code.

```py
from horizon import EC2Endpoint

endpoint = EC2Endpoint()
generation = endpoint('List 3 things to do in London.')
print(generation)
```

# Deleting Instance <img align="center" width="30" height="29" src="https://media.giphy.com/media/HhTXt43pk1I1W/giphy.gif">
<br>

To delete your working instance via the terminal, run:

```bash
horizon-del
```

# YAML Configuration <img align="center" width="30" height="29" src="https://media.giphy.com/media/mrYOnKZ7MJFCM/giphy.gif">
<br>

If you prefer to bypass the TUI, you can enter your YAML configuration manually. Make sure to add the following EC2-related variables and save them in a `ec2_config.yaml` file:

```yaml
EC2:
  ami_id: ami-0c7217cdde317cfec             # Set the ID of the Amazon Machine Image (AMI) to use for EC2 instances.
  ecr_repo_name: takeoff                    # Set the name of the ECR repository. If it doesn't exist it will be created.
  hardware: cpu                             # Set the hardware type: 'cpu' or 'gpu'
  hf_model_name: tiiuae/falcon-7b-instruct  # Set the name of the Hugging Face model to use.
  instance_role_arn: arn:aws:iam::^^^:path  # Set the ARN of the IAM instance profile role.
  instance_type: c5.2xlarge                 # Set the EC2 instance type.
  key_name: aws                             # Set the name of the AWS key pair.
  region_name: us-east-1                    # Set the AWS region name.
  security_group_ids:                       # Set the security group ID(s).
    - sg-0fefe7b366b0c0843
  server_edition: community                 # defaults to "community" ("pro" not available yet)                
```

# Launch in Python <img align="center" width="30" height="29" src="https://media.giphy.com/media/PeaNPlyOVPNMHjqTm7/giphy.gif">
<br>

Upon configuring the YAML file, instantiate the `DockerHandler` and `TitanEC2` classes to handle Docker image flows and instance launch.

### Docker 

Load the YAML file into the `DockerHandler`. These commands will pull the Takeoff Docker image, tag it, and push it to ECR:

```py
from horizon import DockerHandler, TitanEC2

docker = DockerHandler("ec2_config.yaml")

docker.pull_takeoff_image()
docker.push_takeoff_image()
```

### Create Instance

Launch the EC2 instance:

```py
titan = TitanEC2("ec2_config.yaml")
instance_id, meta_data = titan.create_instance()
print(meta_data)
```
When you instance is created, you will get a JSON output of the instance's meta data.

Revisit the `Staging` and `Calling the Inference Endpoint` section for API handling.

### Delete Instance

Pass your `Instance Id` to the `delete_instance` method:

```py
titan.delete_instance(instance_id)
```
