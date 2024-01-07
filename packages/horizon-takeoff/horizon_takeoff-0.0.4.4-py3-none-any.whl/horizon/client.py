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

    def __init__(
        self,
        pro: bool = False,
        stream: bool = False,
        sampling_topk: int = 1,
        sampling_topp: float = 1.0,
        sampling_temperature: float = 1.0,
        repetition_penalty: int = 1,
        no_repeat_ngram_size: int = 0,
    ):
        """
        Initialize an Endpoint instance.

        Args:
            pro (bool): Whether to use a pro or community endpoint. Defaults to False.
            stream (bool): Whether to use a streaming endpoint. Defaults to False.
            sampling_topk (int): Sampling parameter for top-k candidates. Defaults to 1.
            sampling_topp (float): Sampling parameter for top-p candidates. Defaults to 1.0.
            sampling_temperature (float): The sampling temperature. Defaults to 1.0.
            repetition_penalty (int): Penalty for generating repeated tokens. Defaults to 1.
            no_repeat_ngram_size (int): The no_repeat_ngram_size. Defaults to 0.
        """
        address = self.get_ip_address()
        base_url = "http://" + address + ":"
        self.url = base_url + self.BASE_URLS[(pro, stream)]
        self.sampling_topk = sampling_topk
        self.sampling_topp = sampling_topp
        self.sampling_temperature = sampling_temperature
        self.repetition_penalty = repetition_penalty
        self.no_repeat_ngram_size = no_repeat_ngram_size

    def __call__(self, input_text: str) -> Dict[str, Any]:
        """
        Invoke the URL with JSON data.

        Args:
            input_text (str): The input text to include in the JSON data.

        Returns:
            Dict[str, Any]: The JSON response from the URL.
        """
        json_data = {
            "text": input_text,
            "sampling_topk": self.sampling_topk,
            "sampling_topp": self.sampling_topp,
            "sampling_temperature": self.sampling_temperature,
            "repetition_penalty": self.repetition_penalty,
            "no_repeat_ngram_size": self.no_repeat_ngram_size,
        }
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
