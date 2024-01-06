# ------ UNDER DEVELOPMENT

from sagemaker.model import Model
from sagemaker.predictor import Predictor
from typing import Optional


class TitanSageMaker:
    """
    A class for managing SageMaker setup and deployment.

    Args:
        account_id (str): Your AWS account ID.
        region (str): The AWS region where SageMaker will be used.
        role_name (str): The IAM role name used for SageMaker.
        instance_type (str): The SageMaker instance type.
        endpoint_name (str): The name for the SageMaker endpoint.

    Attributes:
        image_uri (str): The Docker image URI for the SageMaker model.
        role (str): The IAM role ARN for SageMaker.
        sagemaker_model (sagemaker.model.Model): The SageMaker model configuration.
    """

    def __init__(
        self,
        account_id: int,
        region: str,
        role_name: str,
        instance_type: str,
        instance_count: int,
        endpoint_name: str,
    ):
        self.account_id = account_id
        self.region = region
        self.role_name = role_name
        self.instance_type = instance_type
        self.instance_count = instance_count
        self.endpoint_name = endpoint_name

        self.image_uri = f"{account_id}.dkr.ecr.{region}.amazonaws.com/fabulinus:latest"
        self.role = f"arn:aws:iam::{account_id}:role/{role_name}"
        self.role = f"arn:aws:iam::{account_id}:role/service-role/{role_name}"

        self.sagemaker_model = Model(
            image_uri=self.image_uri,
            role=self.role,
            predictor_cls=Predictor,
            env={
                "TAKEOFF_MODEL_NAME": "facebook/opt-125m",
                "TAKEOFF_DEVICE": "cuda",
                "TAKEOFF_BACKEND": "fast",
                "TAKEOFF_LOG_LEVEL": "INFO",
            },
            image_config={"RepositoryAccessMode": "Platform"},
        )

    def deploy_endpoint(self) -> Optional[Predictor]:
        """
        Deploy a SageMaker endpoint with the specified configuration.

        Returns:
            sagemaker.predictor.Predictor or None: A SageMaker predictor if deployment is successful,
            or None if deployment fails.
        """
        try:
            # Deploy the SageMaker endpoint
            predictor = self.sagemaker_model.deploy(
                initial_instance_count=self.instance_count,
                instance_type=self.instance_type,
                endpoint_name=self.endpoint_name,
            )
            print(f"Deployed SageMaker endpoint: {self.endpoint_name}")
            return predictor
        except Exception as e:
            print(f"Failed to deploy SageMaker endpoint: {str(e)}")
            return None
