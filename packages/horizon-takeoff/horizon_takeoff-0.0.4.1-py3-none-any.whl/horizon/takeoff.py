import sys
import yaml
import argparse
from typing import Dict, Any

from rich import print
from rich.pretty import pprint
from rich.panel import Panel
from rich.prompt import Prompt
from rich.console import Console
from rich.markup import escape

from .aws.titan_ec2 import TitanEC2
from .utils.ec2_utils import EC2ConfigHandler
from .utils.docker_utils import DockerHandler
from .utils.checks import EnvChecker as env
from .utils.style import PromptHandler as prompt, banner
from .utils.yaml_utils import YamlFileManager as manager

shell = Console()
ec2 = EC2ConfigHandler()


requirements = [
    (env.check_aws_account_id, prompt.aws_id_exists),
    (env.check_aws_cli_installed, prompt.aws_cli_exists),
    (env.check_docker_installed, prompt.docker_exists),
]


def check_reqs():
    for condition, message in requirements:
        if condition is None:
            error_message = prompt.dependency_not_exists(
                escape(prompt.emoji_cross), message
            )
            shell.print(error_message)
            return  # Stop execution if any condition is None
        if condition:
            formatted_message = prompt.dependency_exists(
                escape(prompt.emoji_checkmark), message
            )
            shell.print(formatted_message)


def intro() -> None:
    shell.print(prompt.intro)


def create_ec2_config_file() -> None:
    ec2_config = ec2.create_ec2_config_dict()

    ec2_config["EC2"]["hf_model_name"] = Prompt.ask(prompt.enter_model)

    ec2_config["EC2"]["region_name"] = Prompt.ask(
        prompt.enter_region(ec2.get_aws_region())
    )

    ec2_config["EC2"]["ami_id"] = Prompt.ask(prompt.enter_ami)

    ec2_config["EC2"]["instance_type"] = Prompt.ask(prompt.enter_instance_type)

    ec2.list_key_pairs()
    ec2_config["EC2"]["key_name"] = Prompt.ask(prompt.enter_key_name)

    ec2.list_security_groups()
    security_group_ids: str = Prompt.ask(prompt.enter_security_group)
    ec2_config["EC2"]["security_group_ids"] = [
        sg.strip() for sg in security_group_ids.split(",")
    ]

    ec2.list_instance_profile_arns()
    ec2_config["EC2"]["instance_role_arn"]: str = Prompt.ask(
        prompt.enter_instance_profile_arn
    )

    config_file = manager.write_yaml_to_file(ec2.config_file, ec2_config)

    shell.print(prompt.config_created(config_file.name))

    return config_file


def deploy_docker(config_file):
    deploy = Prompt.ask(
        prompt.docker_flow,
        choices=prompt.boolean_choices,
        show_choices=False,
    )

    if deploy.lower() == "yes":
        ecr_repo_name = Prompt.ask(prompt.enter_ecr_name)
        hardware = Prompt.ask(
            prompt.enter_hardware, choices=prompt.hardware_choices, show_choices=False
        )
        manager.update_yaml_config(config_file.name, "ecr_repo_name", ecr_repo_name)
        manager.update_yaml_config(config_file.name, "hardware", hardware)

        handler = DockerHandler(config_file.name)
        handler.check_or_create_repository()
        handler.pull_takeoff_image()
        handler.push_takeoff_image()

    else:
        print(
            "Your configuration is almost complete. To launch your EC2 instance manually etc etc."
        )  # TODO write out manual flow using DockerHandler Class and TitanEC2/TitanSagemaker class


def create_ec2_instance(config_file):
    ec2 = TitanEC2(config_file.name)
    instance_id, instance_meta_data = ec2.create_instance()
    pprint(instance_meta_data, expand_all=True)
    return instance_id


def provision_ec2(choice):
    if manager.yaml_config_exists(choice):
        override_choice = Prompt.ask(
            prompt.ec2_warning_msg, choices=prompt.boolean_choices, show_choices=False
        )
        if override_choice == "yes":
            config_file = create_ec2_config_file()
            deploy_docker(config_file)
            instance_id = create_ec2_instance(config_file)
            return instance_id, config_file
        else:
            print(prompt.abort_config)
    else:
        config_file = create_ec2_config_file()
        deploy_docker(config_file)
        instance_id = create_ec2_instance(config_file)
        return instance_id, config_file


def create_sagemaker_config_file() -> None:
    sagemaker_config: Dict[str, Any] = {}
    sagemaker_config["account_id"] = Prompt.ask(
        "[magenta]Enter Sagemaker Account ID[/magenta]: "
    )
    sagemaker_config["model_name"] = Prompt.ask(
        "[magenta]Enter Sagemaker Model Name[/magenta]: "
    )
    sagemaker_config["instance_type"] = Prompt.ask(
        "[magenta]Enter Sagemaker Instance Type[/magenta]: "
    )
    sagemaker_config["endpoint_name"] = Prompt.ask(
        "[magenta]Enter Sagemaker Endpoint Name[/magenta]: "
    )

    with open("sagemaker_config.yaml", "w") as config_file:
        yaml.dump(sagemaker_config, config_file, default_flow_style=False)

    shell.print(prompt.config_created(config_file))


def provision_sagemaker(choice):
    if manager.yaml_config_exists(choice):
        override_choice = Prompt.ask(
            prompt.sagemaker_warning_msg,
            choices=prompt.boolean_choices,
            show_choices=False,
        )
        if override_choice == "yes":
            create_sagemaker_config_file()
        else:
            print(prompt.abort_config)
    else:
        create_sagemaker_config_file()


def deploy_cloud_service(service, server_edition):
    if service == "ec2":
        instance_id, config_file = provision_ec2(service)
        manager.update_yaml_config(config_file.name, "instance_ids", instance_id)
        manager.update_yaml_config(config_file.name, "server_edition", server_edition)
        shell.print(prompt.instance_id_added(instance_id))
    else:
        provision_sagemaker()
        # TODO add sagemaker support


def main():
    parser = argparse.ArgumentParser(
        description="Horizon CLI - Manage AWS EC2 and SageMaker"
    )
    parser.add_argument(
        "service",
        choices=["ec2", "sagemaker"],
        help="Select the cloud service to deploy.",
    )
    parser.add_argument(
        "server",
        choices=["community", "pro"],
        help="Select the server edition to deploy.",
    )

    args = parser.parse_args()

    print(Panel.fit(banner(), subtitle=prompt.subtitle, style="yellow"))
    print()
    check_reqs()
    intro()
    deploy_cloud_service(args.service, args.server)


if __name__ == "__main__":
    main(sys.argv[1:])
