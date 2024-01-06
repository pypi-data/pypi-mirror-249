import os
from subprocess import Popen
from loguru import logger


import requests
import click
from ellipsis import ellipsis_api_client

from ellipsis.ellipsis_api_client import EllipsisApiClient
from ellipsis.src.models.workspaces.constants import HEALTH_CHECK_URL_ROUTE, LISTENER_PORT



def _expect_env_var_to_exist(env_var_name: str):
    env_var_value = os.environ.get(env_var_name, None)
    if env_var_value is None:
        raise ValueError(f"Environment variable {env_var_name} not set.")
    return env_var_value



def _create_EllipsisApiClient():
    override_api_url = os.environ.get('ELLIPSIS_API_URL', None)
    codespace_name = os.environ.get('CODESPACE_NAME', None)
    if override_api_url is not None:
        return EllipsisApiClient(override_api_url)
    elif codespace_name is not None and codespace_name.startswith('ellipsis-test'):
        return EllipsisApiClient('https://beta-api.ellipsis.dev')
    return EllipsisApiClient('https://api.ellipsis.dev')


def _register_as_codespace():
    codespace_name = _expect_env_var_to_exist('CODESPACE_NAME')
    github_token = _expect_env_var_to_exist('GITHUB_TOKEN')
    github_user = _expect_env_var_to_exist('GITHUB_USER')
    github_repository = _expect_env_var_to_exist('GITHUB_REPOSITORY')
    repo_name_split = github_repository.split('/')
    assert len(repo_name_split) == 2, f'Invalid repository name: {github_repository}'
    api_client = _create_EllipsisApiClient()
    api_client.register_codespace(
        codespace_name,
        repo_name_split[0],
        repo_name_split[1],
        github_token,
        github_user
    )
    logger.info(f"Registered workspace as CODESPACE {codespace_name} with Ellipsis API at {api_client.base_url}")


def _register_as_internal_ec2():
    workspace_id = _expect_env_var_to_exist('ELLIPSIS_WORKSPACE_ID')
    workflow_id = _expect_env_var_to_exist('ELLIPSIS_WORKFLOW_ID')
    host_name = _expect_env_var_to_exist('HOSTNAME') # Added by AWS when launching EC2 instance
    api_client = _create_EllipsisApiClient()
    api_client.register_internal_ec2_workspace(
        workspace_id,
        host_name,
        workflow_id
    )
    logger.info(f"Registered workspace as INTERNAL_EC2 {workspace_id} with Ellipsis API at {api_client.base_url}")


CLI_VERSION = '0.2.7'


@click.group()
def cli():
    pass

@cli.command()
def version():
    click.echo(f"Version {CLI_VERSION}")

@cli.command()
def ping():
    api_client = _create_EllipsisApiClient()
    click.echo(f'Pinging {api_client.base_url}...')
    click.echo("Success!")

@click.group()
def listener():
    pass

@listener.command()
@click.argument('repo_dir')
def start(repo_dir: str):
    # Get all the required env vars
    codespaces = os.environ.get('CODESPACES', None)
    if codespaces is 'true':
        _register_as_codespace()
    else:
        _register_as_internal_ec2()

    try:
        response = requests.get(f"http://localhost:{LISTENER_PORT}{HEALTH_CHECK_URL_ROUTE}")
        if response.status_code == 200:
            logger.info(f"Listener already listening on port {LISTENER_PORT} with PID {response.json()['pid']}.")
            click.echo("Listener already running.")
            return
    except requests.exceptions.ConnectionError:
        # Listener not running, so we can start it
        logger.info(f"Listener not running, starting...")
        pass
    module_path = os.path.dirname(__file__)
    listener_file_path = os.path.join(module_path, '_listener.py')
    background_process = Popen(['python3', listener_file_path, repo_dir])
    logger.info(f"Starting listener in background process with PID {background_process.pid}...")


@listener.command()
def stop():
    raise NotImplementedError(f'Not implemented for some archietctures.')
    # try:
    #     response = requests.get(f"http://localhost:{LISTENER_PORT}{HEALTH_CHECK_URL_ROUTE}")
    #     click.echo(response.json())
    #     if response.status_code != 200:
    #         click.echo("Listener not running, nothing to stop.")
    #         return
    # except requests.exceptions.ConnectionError:
    #     click.echo("Listener not running, nothing to stop.")
    #     return
    # response_json = response.json()
    # pid = response_json['pid']
    # Popen(['kill', str(pid)])
    # click.echo(f"Killed listener with PID {pid}.")

cli.add_command(ping)
cli.add_command(version)
cli.add_command(listener)


if __name__ == '__main__':
    cli()
