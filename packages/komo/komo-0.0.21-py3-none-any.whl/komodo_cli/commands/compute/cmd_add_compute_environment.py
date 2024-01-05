import os
import sys

import click
from loguru import logger

import komodo_cli.printing as printing
from komodo_cli.commands.compute.utils import (
    get_compute_dir,
    get_vars,
    get_vars_filepath,
    run_cmd,
    update_vars,
)
from komodo_cli.utils import handle_errors


@click.command("add-compute-environment")
@click.option(
    "--compute-environment-name",
    "-n",
    type=str,
    required=True,
    default=None,
    help="Name of the compute environment to add.",
)
@click.option(
    "--instance-type",
    "-t",
    type=str,
    required=True,
    default=None,
    help="Instance type to add.",
)
@click.option(
    "--desired-vcpus",
    "-d",
    type=int,
    required=True,
    default=0,
    help="Desired number of vcpus for this compute environment.",
)
@click.option(
    "--min-vcpus",
    "-l",
    type=int,
    required=True,
    default=0,
    help="Mininum number of vcpus for this compute environment.",
)
@click.option(
    "--max-vcpus",
    "-h",
    type=int,
    required=True,
    default=8,
    help="Maximum number of vcpus for this compute environment.",
)
@click.option(
    "--volume-size",
    "-v",
    type=int,
    required=True,
    default=100,
    help="Size of the volume in GB.",
)
@click.option(
    "--manual_confirm",
    "-m",
    type=bool,
    is_flag=True,
    default=False,
    required=False,
    help="Manually confirm terraform plan.",
)
@click.pass_context
@handle_errors
def cmd_add_compute_environment(
    ctx: click.Context,
    compute_environment_name: str,
    instance_type: str,
    desired_vcpus: int,
    min_vcpus: int,
    max_vcpus: int,
    volume_size: int,
    manual_confirm: bool,
):
    """
    Add a compute environment to AWS Batch.
    """
    compute_dir = get_compute_dir()
    if not os.path.exists(compute_dir):
        printing.error(f"No compute configuration found.", bold=True)
        sys.exit(1)

    try:
        tf_vars = get_vars()
    except Exception as e:
        logger.error(e)
        printing.error(f"Error loading tf vars", bold=True)
        sys.exit(1)

    if "aws_batch_compute_environments" not in tf_vars:
        tf_vars["aws_batch_compute_environments"] = {}

    tf_vars["aws_batch_compute_environments"][compute_environment_name] = {
        "instance_type": instance_type,
        "desired_vcpus": desired_vcpus,
        "min_vcpus": min_vcpus,
        "max_vcpus": max_vcpus,
        "volume_size": volume_size,
    }

    update_vars(tf_vars)

    cmd = [
        "terraform",
        f"-chdir={compute_dir}",
        "apply",
        f"-var-file={get_vars_filepath()}",
    ]

    if not manual_confirm:
        cmd.append("-auto-approve")

    exit_code, _, stderr = run_cmd(" ".join(cmd))
    if exit_code != 0:
        logger.error(stderr)
        printing.error(
            f"Error adding compute environment {compute_environment_name}",
            bold=True,
        )
        sys.exit(1)

    printing.success(
        f"Successfully added compute environment {compute_environment_name}",
        bold=True,
    )
