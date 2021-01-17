import json
import os
import re
import statistics
from pathlib import Path, PurePath
from typing import List
from urllib.parse import urlparse
from urllib.request import urlretrieve

import click
import humanfriendly
import requests
import torrentool.api

from .schemas import Ctx, Torrent, TorrentFileData
from .transmission import add_torrent as transmission_add_torrent

jsonfilepath = "./torrent_data.json"


def fetch_torrent_file(ctx: Ctx, data: TorrentFileData, depth=0):
    filename = Path(data.link).name
    parent = Path(ctx.config.settings.torrent_files_dir)
    parent.mkdir(parents=True, exist_ok=True)
    expected_path = parent / filename
    data.path = os.path.abspath(expected_path)
    if not expected_path.exists():
        urlretrieve(data.link, expected_path)
    try:
        tf = torrentool.api.Torrent.from_file(str(expected_path))
        if tf.info_hash != data.infohash:
            raise ValueError(f"Info hash does not match for {filename}")
    except AttributeError as err:
        if depth == 0:
            os.remove(expected_path)
            return fetch_torrent_file(ctx, data, 1)
        else:
            raise err


def load_torrent_data(
    ctx: Ctx, jsonfilepath: str, force=False
) -> List[TorrentFileData]:
    data: List[TorrentFileData] = []
    if not os.path.exists(jsonfilepath) or force:
        with open(jsonfilepath, "w") as f:
            resp = requests.get(ctx.config.settings.torrent_data_url)
            json.dump(resp.json(), f)
    with open(jsonfilepath) as f:
        raw = json.load(f)
        for d in raw:
            data.append(TorrentFileData(**d))
    return data


def fetchall(ctx: Ctx, update_list=False, dry_run=False) -> None:
    settings = ctx.config.settings
    max_bytecount = humanfriendly.parse_size(settings.max_disk_usage)
    filtered_filedata = []

    bytecount = 0
    click.secho("Loading torrent data.", bold=True, fg="black")
    filedata = sorted(
        load_torrent_data(ctx, jsonfilepath, force=update_list),
        key=lambda x: int(re.search('\d+', x.name)[0]),
    )

    seeders_arr = [x.seeders for x in filedata]
    seeders_mean = statistics.mean(seeders_arr)
    seeders_median = statistics.median(seeders_arr)
    dht_peers_arr = [x.dht_peers for x in filedata]
    dht_peers_mean = statistics.mean(dht_peers_arr)
    dht_peers_median = statistics.median(dht_peers_arr)
    size_arr = [x.size_bytes for x in filedata]
    size_total = humanfriendly.format_size(sum(size_arr))
    size_mean = humanfriendly.format_size(statistics.mean(size_arr))
    size_median = humanfriendly.format_size(statistics.median(size_arr))

    click.secho(
        f"Found {len(filedata)} torrent files ({size_total}) needing seeders",
        bold=True,
    )
    click.secho(
        f"  Seeders   MEAN={seeders_mean} MEDIAN={seeders_median}",
        fg="yellow",
        reset=False,
    )
    click.secho(
        f"  DHT Peers MEAN={dht_peers_mean} MEDIAN={dht_peers_median}",
        reset=False,
    )
    click.secho(
        f"  Size      MEAN={size_mean} MEDIAN={size_median}",
    )
    click.secho(
        f"Searching for criteria:",
        bold=True,
    )
    click.secho(
        f"  max_disk_usage: {settings.max_disk_usage}",
        fg="yellow",
        reset=False,
    )
    click.secho(
        f"  min_seeders:    {settings.torrent_seeders_range[0]}",
        reset=False,
    )
    click.secho(
        f"  max_seeders:    {settings.torrent_seeders_range[1]}",
        reset=False,
    )
    click.secho(
        f"  types:          {str(settings.include_types)}",
    )

    for row in filedata:
        if (
            row.type in settings.include_types
            and row.seeders >= settings.torrent_seeders_range[0]
            and row.seeders <= settings.torrent_seeders_range[1]
        ):
            if (bytecount + row.size_bytes) < max_bytecount:
                filtered_filedata.append(row)
                bytecount += row.size_bytes

    click.secho(
        f"Found {len(filtered_filedata)} matches totaling {humanfriendly.format_size(bytecount)}",
        fg="green",
        bold=True,
    )
    bytecount = 0
    torrents: List[Torrent] = []

    itemshowfunc = (
        lambda x: f"{humanfriendly.format_size(bytecount)} {x.type}:{x.name}"
        if x
        else ""
    )
    with click.progressbar(
        filtered_filedata,
        label="Fetching torrent files...",
        item_show_func=itemshowfunc,
    ) as bar:
        for row in bar:
            if dry_run:
                click.secho(f"dry run: adding {row.name}: {row.type}: {row.infohash}")
            else:
                fetch_torrent_file(ctx, row)
                if ctx.config.torrent.enabled:
                    torrents.append(transmission_add_torrent(ctx, row))
                bytecount += row.size_bytes

    if ctx.config.torrent.enabled and len(torrents) > 0:
        click.secho("Torrent progress stats", bold=True)
        ratio_arr = [x.ratio for x in torrents]
        ratio_mean = statistics.mean(ratio_arr)
        click.secho(f"  Ratio    MEAN={ratio_mean}", fg="yellow")

        progress_arr = [x.progress for x in torrents]
        progress_mean = statistics.mean(progress_arr)
        click.secho(f"  Progress MEAN={progress_mean}", fg="yellow")

    click.secho("Done", fg="green", bold=True)
