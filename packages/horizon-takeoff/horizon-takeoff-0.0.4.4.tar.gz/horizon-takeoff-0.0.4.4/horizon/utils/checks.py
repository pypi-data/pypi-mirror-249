import subprocess
import json
from typing import Optional


class EnvChecker:
    @staticmethod
    def check_aws_cli_installed() -> Optional[str]:
        """
        Check if the AWS CLI is installed and return its version.

        Returns:
            str or None: The AWS CLI version if installed, or None if not installed.
        """
        try:
            aws_cli_version = subprocess.check_output(
                ["aws", "--version"], stderr=subprocess.STDOUT, text=True
            )
            return aws_cli_version.strip()
        except subprocess.CalledProcessError:
            return None

    @staticmethod
    def check_docker_installed() -> Optional[str]:
        """
        Check if Docker is installed and return its version.

        Returns:
            str or None: The Docker version if installed, or None if not installed.
        """
        try:
            docker_version = subprocess.check_output(
                ["docker", "--version"], stderr=subprocess.STDOUT, text=True
            )
            return docker_version.strip()
        except subprocess.CalledProcessError:
            return None

    @staticmethod
    def check_aws_account_id() -> Optional[str]:
        """
        Check if AWS CLI is configured and return the AWS account ID.

        Returns:
            str or None: The AWS account ID if AWS CLI is configured, or None if not configured.
        """
        result = subprocess.run(
            ["aws", "sts", "get-caller-identity"], capture_output=True, text=True
        )

        if result.returncode == 0:
            # Parse the JSON output to extract the account ID
            caller_identity = json.loads(result.stdout)
            account_id = caller_identity.get("Account", "Unknown")
            return account_id
        else:
            print(f"Error: {result.stderr}")
            return None
