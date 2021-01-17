import json
import os
from typing import Optional
from urllib.parse import urlparse

import click
import requests
import requests.auth
from click_aliases import ClickAliasedGroup
from requests.exceptions import RequestException

from .routines import fetchall
from .schemas import Ctx, load_config, save


@click.group(cls=ClickAliasedGroup)
@click.option(
    "--config",
    default="config.json",
    envvar="LIBGEN_SEEDTOOLS_CONFIG_PATH",
    type=click.Path(dir_okay=False, file_okay=True, writable=True, resolve_path=True),
)
@click.version_option()
@click.pass_context
def cli(ctx, config):
    conf = load_config(config)
    ctx.obj = Ctx(
        config=conf,
        configPath=config,
    )


@cli.command(name="generate-config")
@click.pass_obj
def generate_config(ctx):
    save(ctx)
    click.secho(f"generated {ctx.configPath}", fg="green")
    click.secho(f"Edit this file, then run the fetch command")


@cli.command(name="fetch")
@click.option("-ul", "--update-list", is_flag=True)
@click.option("-d", "--dry-run", is_flag=True)
@click.pass_obj
def fetch(ctx, update_list, dry_run):
    fetchall(ctx, update_list, dry_run)
