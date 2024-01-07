import os
import yaml
from typing import Dict, Optional
from io import TextIOWrapper
from ..aws.models import EC2Config


class YamlFileManager:
    @staticmethod
    def parse_yaml_file(yaml_file_path: str) -> Optional[EC2Config]:
        """Parse a YAML file and return an EC2Config object.

        Args:
            yaml_file_path (str): The path to the YAML file, or just the filename.

        Returns:
            Optional[EC2Config]: An EC2Config object representing the parsed YAML data, or None on error.
        """
        try:
            with open(yaml_file_path, "r") as yaml_file:
                yaml_content = yaml.safe_load(yaml_file)
            return EC2Config(**yaml_content["EC2"])
        except (FileNotFoundError, yaml.YAMLError) as e:
            print(f"Error parsing YAML file: {e}")
            return None

    @staticmethod
    def update_yaml_config(
        yaml_file_path: str, field_name: str, value_to_add: str
    ) -> None:
        """Update a field in a YAML configuration file.

        Args:
            yaml_file_path (str): The path to the YAML file.
            field_name (str): The name of the field to update.
            value_to_add (str): The value to add to the field.

        Returns:
            None
        """
        ec2_config = YamlFileManager.parse_yaml_file(yaml_file_path)

        try:
            if ec2_config is not None:
                if field_name == "instance_ids":
                    if ec2_config.instance_ids is None:
                        ec2_config.instance_ids = []
                    ec2_config.instance_ids.append(value_to_add)
                elif field_name == "ecr_repo_name":
                    ec2_config.ecr_repo_name = value_to_add
                elif field_name == "server_edition":
                    ec2_config.server_edition = value_to_add
                elif field_name == "hf_model_name":
                    ec2_config.hf_model_name = value_to_add
                elif field_name == "hardware":
                    ec2_config.hardware = value_to_add

                updated_data = {"EC2": ec2_config.model_dump()}
                YamlFileManager.write_yaml_to_file(yaml_file_path, updated_data)

        except (FileNotFoundError, yaml.YAMLError) as e:
            print(f"Error updating YAML file: {e}")

    @staticmethod
    def yaml_config_exists(name: str) -> bool:
        """Check if a YAML configuration file exists.

        Args:
            name (str): Name of the configuration.

        Returns:
            bool: True if the configuration file exists, False otherwise.
        """
        return os.path.exists(f"{name}_config.yaml")

    @staticmethod
    def write_yaml_to_file(filename: str, data: Dict) -> TextIOWrapper:
        """Write YAML data to a file.

        Args:
            filename (str): The name of the file to write to.
            data (dict): The YAML data to write.

        Returns:
            None
        """
        with open(filename, "w") as config_file:
            yaml.dump(data, config_file, default_flow_style=False)

        return config_file

    @staticmethod
    def read_yaml_file(yaml_file_path: str) -> None:
        """Print the entire content of a YAML file.

        Args:
            yaml_file_path (str): The path to the YAML file, or just the filename.

        Returns:
            None
        """
        try:
            with open(yaml_file_path, "r") as config_file:
                yaml_content = config_file.read()
                return yaml_content
        except FileNotFoundError as e:
            print(f"Error reading YAML file: {e}")
