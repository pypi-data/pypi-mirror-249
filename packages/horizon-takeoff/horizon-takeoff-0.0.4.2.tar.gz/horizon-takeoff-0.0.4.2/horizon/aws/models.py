from typing import List, Optional
from pydantic import BaseModel


class EC2Config(BaseModel):
    hf_model_name: str
    region_name: str
    ami_id: str
    instance_type: str
    key_name: str
    security_group_ids: List[str]
    instance_role_arn: str
    instance_ids: Optional[List[str]] = None
    ecr_repo_name: Optional[str] = None
    hardware: Optional[str] = None
    server_edition: Optional[str] = None
