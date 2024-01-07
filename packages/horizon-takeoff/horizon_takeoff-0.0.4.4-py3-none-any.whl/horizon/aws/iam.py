import boto3
import botocore.exceptions
from typing import List, Optional


class IAMHandler:
    """
    A class for managing AWS Identity and Access Management (IAM) operations.
    """

    def __init__(self):
        """
        Initialize IAMHandler and create an IAM client.
        """
        self.iam_client = boto3.client("iam")

    def get_aws_account_id(self) -> Optional[str]:
        """
        Get the AWS account ID associated with the IAM user.

        Returns:
            str or None: The AWS account ID or None if an error occurs.
        """
        try:
            response = self.iam_client.get_user()
            account_id = response["User"]["Arn"].split(":")[4]
            return account_id
        except botocore.exceptions.ClientError as e:
            print(f"Error retrieving AWS account ID: {e}")
            return None

    def attach_policy_to_role(self, role_name: str, policy_arn: str) -> None:
        """
        Attach a managed policy to an IAM role.

        Args:
            role_name (str): The name of the IAM role.
            policy_arn (str): The Amazon Resource Name (ARN) of the policy to attach.
        """
        try:
            self.iam_client.attach_role_policy(RoleName=role_name, PolicyArn=policy_arn)
            print(
                f"Policy '{policy_arn}' attached to IAM Role '{role_name}' successfully."
            )
        except botocore.exceptions.ClientError as e:
            print(
                f"Error attaching policy '{policy_arn}' to IAM role '{role_name}': {e}"
            )

    def create_instance_profile_and_associate_role(self, role_name: str) -> None:
        """
        Create an instance profile and associate it with an IAM role.

        Args:
            role_name (str): The name of the IAM role.
        """
        try:
            self.iam_client.create_instance_profile(InstanceProfileName=role_name)
            self.iam_client.add_role_to_instance_profile(
                InstanceProfileName=role_name, RoleName=role_name
            )
            print(
                f"Instance profile '{role_name}' created and associated with IAM role '{role_name}' successfully."
            )
        except botocore.exceptions.ClientError as e:
            print(
                f"Error creating instance profile and associating it with IAM role '{role_name}': {e}"
            )

    def list_roles(self, count: int) -> List[dict]:
        """
        List the specified number of roles for the account.

        Args:
            count (int): The number of roles to list.

        Returns:
            List[dict]: A list of role dictionaries.
        """
        try:
            roles = self.iam_client.list_roles(MaxItems=count)["Roles"]
            for role in roles:
                print("Role:", role["RoleName"])
            return roles
        except botocore.exceptions.ClientError as e:
            print("Couldn't list roles for the account:", e)

    def list_instance_profile_arns(self) -> List[str]:
        """
        List the Amazon Resource Names (ARNs) of instance profiles in the AWS account.

        Returns:
            List[str]: A list of instance profile ARNs.
        """
        try:
            response = self.iam_client.list_instance_profiles()

            print("\nList of instance profile ARNs:\n")
            for profile in response["InstanceProfiles"]:
                role_name = profile["Roles"][0]["RoleName"]
                arn = profile["Arn"]
                print(f"Role Name: {role_name}")
                print(f"Arn: {arn}")

            return response
        except Exception as e:
            # Handle exceptions or errors here
            print(f"An error occurred: {str(e)}")
            return []
