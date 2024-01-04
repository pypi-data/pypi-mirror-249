import os
import boto3
import subprocess
from .yaml_utils import YamlFileManager as manager

current_script_dir = os.path.dirname(os.path.abspath(__file__))

# Construct paths to the two Bash scripts in the parallel "scripts" directory
pull_path = os.path.join(current_script_dir, "..", "scripts", "pull_takeoff_image.sh")
push_path = os.path.join(current_script_dir, "..", "scripts", "push_takeoff_ecr.sh")


class DockerHandler:
    def __init__(self, config_path: str) -> None:
        """
        Initialize the Handler with the provided YAML config path.

        Args:
            config_path (str): Path to the YAML configuration file.
        """
        self.ec2_config = manager.parse_yaml_file(config_path)
        self.ecr_client = boto3.client("ecr", region_name=self.ec2_config.region_name)

    def check_or_create_repository(self) -> None:
        """
        Check if an ECR repository exists; create it if not.

        Args:
            repo_name (str): The name of the ECR repository to check or create.
        """
        try:
            response = self.ecr_client.describe_repositories(
                repositoryNames=[self.ec2_config.ecr_repo_name]
            )
            repository_exists = len(response["repositories"]) > 0
        except self.ecr_client.exceptions.RepositoryNotFoundException:
            repository_exists = False

        if not repository_exists:
            try:
                self.ecr_client.create_repository(
                    repositoryName=self.ec2_config.ecr_repo_name
                )
                print(
                    f"ECR repository '{self.ec2_config.ecr_repo_name}' created successfully."
                )
            except Exception as e:
                print(f"Error creating ECR repository: {e}")
        else:
            print(f"ECR repository '{self.ec2_config.ecr_repo_name}' already exists.")

    def pull_takeoff_image(self) -> None:
        """
        Pulls the Takeoff Server Docker image to local machine.

        Args:
            script_dir (str): The directory containing the script for pulling Takeoff server.
        """

        try:
            subprocess.run(["bash", pull_path])

        except Exception as e:
            print(f"Error during image pull: {e}")

    def push_takeoff_image(self) -> None:
        """
        Pushes the Takeoff Server Docker image to the ECR repository.

        Args:
            script_dir (str): The directory containing the Bash push script.
            repo_name (str): The name of the ECR repository.
        """

        try:
            subprocess.run(["bash", push_path, self.ec2_config.ecr_repo_name])

        except Exception as e:
            print(f"Error during image push: {e}")
