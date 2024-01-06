import boto3
import requests
from typing import Any, Dict

from .utils.yaml_utils import YamlFileManager
from .utils.ec2_utils import EC2ConfigHandler


class EC2Endpoint:
    """A class for invoking a API endpoint on EC2Instance."""

    BASE_URLS = {
        (False, False): "8000/generate",
        (False, True): "8000/generate_stream",
        (True, False): "3000/generate",
        (True, True): "3000/generate_stream",
    }

    config_file = EC2ConfigHandler.config_file

    def __init__(self, pro: bool = False, stream: bool = False):
        """
        Initialize an Endpoint instance.

        Args:
            stream (bool): Whether to use a streaming endpoint. Defaults to False.
            pro (bool): Whether to use a pro or community endpoint. Defaults to False.
        """
        address = self.get_ip_address()
        base_url = "http://" + address + ":"
        self.url = base_url + self.BASE_URLS[(pro, stream)]

    def __call__(self, input_text: str) -> Dict[str, Any]:
        """
        Invoke the URL with JSON data.

        Args:
            input_text (str): The input text to include in the JSON data.

        Returns:
            Dict[str, Any]: The JSON response from the URL.
        """
        json_data = {"text": input_text}
        response = requests.post(self.url, json=json_data)
        return response.json()

    def get_ip_address(self) -> str:
        """Get the IPv4 address of a running EC2 instance.

        Returns:
            str: The IPv4 address of the instance.
        """

        ec2_config = YamlFileManager.parse_yaml_file(self.config_file)
        self.ec2_client = boto3.client("ec2", region_name=ec2_config.region_name)
        response = self.ec2_client.describe_instances(
            InstanceIds=ec2_config.instance_ids
        )

        if "Reservations" in response and len(response["Reservations"]) > 0:
            instances = response["Reservations"][0]["Instances"]
            if len(instances) > 0 and "PublicIpAddress" in instances[0]:
                public_ip = instances[0]["PublicIpAddress"]
                return public_ip
            else:
                return f"No public IPv4 address found for instance {ec2_config.instance_ids}"
        else:
            return f"No information found for instance {ec2_config.instance_ids}"
