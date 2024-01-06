from typing import List, Any
import boto3

from ..utils.yaml_utils import YamlFileManager as manager
from .models import EC2Config
from .iam import IAMHandler


def startup_script(account_id, region, repo, model_name, hardware, server_edition):
    port = 3000 if server_edition == "pro" else 8000
    hardware = "cuda" if hardware == "gpu" else "cpu"

    startup_script = f"""#!/bin/bash
    apt-get update
    apt install docker.io -y
    apt install awscli -y
    aws ecr get-login-password --region {region} |\
    docker login --username AWS --password-stdin\
    {account_id}.dkr.ecr.{region}.amazonaws.com/{repo}:latest
    docker pull {account_id}.dkr.ecr.{region}.amazonaws.com/{repo}:latest
    docker run -e TAKEOFF_MODEL_NAME={model_name} -e TAKEOFF_DEVICE={hardware} \
    -p {port}:80 {account_id}.dkr.ecr.{region}.amazonaws.com/{repo}:latest

    """
    return startup_script


class TitanEC2(IAMHandler):
    """Initialize a TitanEC2 instance.

    Args:
        ec2_config (EC2Config): A Pydantic model representing the EC2 configuration.
        min_count (int, optional): The minimum number of instances to create. Defaults to 1.
        max_count (int, optional): The maximum number of instances to create. Defaults to 1.
        volume_size (int, optional): Size of Storage disk on instance. Defaults to 20GB.
    """

    def __init__(
        self,
        ec2_config: EC2Config,
        min_count: int = 1,
        max_count: int = 1,
        volume_size: int = 20,
    ):
        super().__init__()

        self.min_count = min_count
        self.max_count = max_count
        self.volume_size = volume_size

        self.config = manager.parse_yaml_file(ec2_config)
        self.region = self.config.region_name
        self.ec2_client = boto3.client("ec2", region_name=self.region)
        self.ami_id = self.config.ami_id
        self.instance_type = self.config.instance_type
        self.key_name = self.config.key_name
        self.security_group_ids = self.config.security_group_ids
        self.instance_ids = self.config.instance_ids
        self.ecr_repo_name = self.config.ecr_repo_name
        self.instance_profile_arn = self.config.instance_role_arn
        self.model_name = self.config.hf_model_name
        self.hardware = self.config.hardware
        self.server_edition = self.config.server_edition
        self.account_id = self.get_aws_account_id()

    def create_instance(self) -> tuple[Any, Any]:
        """Create an EC2 instance based on the configured parameters.

        Returns:
            str: The ID of the created EC2 instance.
        """
        instance_params = {
            "ImageId": self.ami_id,
            "InstanceType": self.instance_type,
            "IamInstanceProfile": {"Arn": self.instance_profile_arn},
            "KeyName": self.key_name,
            "SecurityGroupIds": self.security_group_ids,
            "UserData": startup_script(
                self.account_id,
                self.region,
                self.ecr_repo_name,
                self.model_name,
                self.hardware,
                self.server_edition,
            ),
            "MinCount": self.min_count,
            "MaxCount": self.max_count,
            "BlockDeviceMappings": [
                {"DeviceName": "/dev/sda1", "Ebs": {"VolumeSize": self.volume_size}}
            ],
        }

        response = self.ec2_client.run_instances(**instance_params)
        return response["Instances"][0]["InstanceId"], response

    def delete_instance(self, instance_ids: List[str]) -> None:
        """Delete EC2 instances by providing a list of instance IDs.

        Args:
            instance_ids (List[str]): A list of EC2 instance IDs to delete.
        """
        if instance_ids:
            self.ec2_client.terminate_instances(InstanceIds=instance_ids)
            print(f"Instance {', '.join(instance_ids)} is being terminated.")
        else:
            print("No instance IDs provided. No instances will be terminated.")

    def get_instance_ipv4(self) -> str:
        """Get the IPv4 address of a running EC2 instance.

        Args:
            instance_id (str): The ID of the EC2 instance.

        Returns:
            str: The IPv4 address of the instance.
        """

        response = self.ec2_client.describe_instances(InstanceIds=self.instance_ids)

        if "Reservations" in response and len(response["Reservations"]) > 0:
            instances = response["Reservations"][0]["Instances"]
            if len(instances) > 0 and "PublicIpAddress" in instances[0]:
                public_ip = instances[0]["PublicIpAddress"]
                return public_ip
            else:
                return f"No public IPv4 address found for instance {self.instance_ids}"
        else:
            return f"No information found for instance {self.instance_ids}"
