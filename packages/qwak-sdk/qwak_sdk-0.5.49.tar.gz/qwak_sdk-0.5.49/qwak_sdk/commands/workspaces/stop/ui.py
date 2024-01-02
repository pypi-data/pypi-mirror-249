from typing import Optional

import click

from qwak_sdk.commands.workspaces.stop._logic import _stop_workspace
from qwak_sdk.inner.tools.cli_tools import QwakCommand


@click.command("stop", cls=QwakCommand)
@click.option(
    "--workspace-id",
    required=False,
    metavar="WORKSPACE-ID",
    help="The id of the workspace",
)
@click.option(
    "--name",
    required=False,
    metavar="WORKSPACE-NAME",
    help="The name of the workspace",
)
def stop_workspace(workspace_id: Optional[str], name: Optional[str], **kwargs):
    _stop_workspace(workspace_id=workspace_id, workspace_name=name)
