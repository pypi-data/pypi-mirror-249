# pylint: disable=too-many-locals, too-many-branches

"""CLI 'publish' command"""

from pathlib import Path

import click

from matatika.channel import Channel
from matatika.cli.display import Column, Table
from matatika.cli.parse_service import SUPPORTED_FILETYPES, parse_resources
from matatika.cli.utility import Resolver
from matatika.dataset import Dataset
from matatika.types import Resource

from .root import matatika


@matatika.command("publish", short_help="Publish one or more files(s)")
@click.pass_context
@click.argument("user-file", type=click.Path(exists=True, path_type=Path))
@click.option("--workspace-id", "-w", type=click.UUID, help="Workspace ID")
@click.option("--dataset-alias", "-alias", type=click.STRING, help="Dataset Alias")
def publish(ctx, user_file: Path, workspace_id, dataset_alias):
    """Publish one or more dataset(s) or channel(s) from files into a workspace"""

    ctx.obj["workspace_id"] = workspace_id
    client = Resolver(ctx).client()

    if user_file.is_file() and user_file.suffix not in SUPPORTED_FILETYPES:
        click.secho(f"File type '{user_file.suffix}' not supported", fg="red")
        return

    resources = parse_resources(user_file)
    datasets = [r for r in resources if isinstance(r, Dataset)]
    channels = [r for r in resources if isinstance(r, Channel)]

    if dataset_alias:
        if len(datasets) > 1:
            click.secho(
                "Cannot specify alias option with more than one dataset",
                fg="red",
            )

            return

        datasets[0].alias = dataset_alias

    if datasets:
        published_files = client.publish(Resource.DATASET, datasets)

        click.secho(
            f"Successfully published {len(published_files)} dataset(s)\n",
            fg="green",
        )

        ids = Column("DATASET ID")
        aliases = Column("ALIAS")
        titles = Column("TITLE")
        statuses = Column("STATUS")

        for dataset, status_code in published_files:
            if status_code == 201:
                status = click.style("NEW", fg="magenta")
            else:
                status = click.style("UPDATED", fg="cyan")

            if not dataset.alias:
                dataset.alias = click.style(str(dataset.alias), fg="yellow")

            ids.add(dataset.dataset_id)
            aliases.add(dataset.alias)
            titles.add(dataset.title)
            statuses.add(status)

        table = Table(ids, aliases, titles, statuses)
        click.echo(table)

    if channels:
        published_files = client.publish(Resource.CHANNEL, channels)

        click.secho(
            f"Successfully published {len(published_files)} channels(s)\n",
            fg="green",
        )

        ids = Column("CHANNEL ID")
        name = Column("NAME")
        description = Column("DESCRIPTION")
        statuses = Column("STATUS")

        for channel, status_code in published_files:
            if status_code == 201:
                status = click.style("NEW", fg="magenta")
            else:
                status = click.style("UPDATED", fg="cyan")

            ids.add(channel.channel_id)
            name.add(channel.name)
            description.add(channel.description)
            statuses.add(status)

        table = Table(ids, name, description, statuses)
        click.echo(table)
