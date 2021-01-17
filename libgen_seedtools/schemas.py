import json
import os
from typing import Any, Dict, List, Literal, Union

from pydantic import BaseModel


class TorrentFileData(BaseModel):
    name: str
    link: str
    infohash: str
    created_unix: int
    scraped_date: int
    dht_scraped: int
    dht_peers: int
    seeders: int
    leechers: int
    size_bytes: int
    type: str
    ipfs_cid: Union[str, None]
    path: Union[str, None]


class Torrent(BaseModel):
    data: TorrentFileData
    ratio: float
    progress: float
    done: bool


class TorrentConnectionSettings(BaseModel):
    url: str = "http://localhost:9091"
    username: str = "username"
    password: str = "password"


class TorrentConfigSchema(BaseModel):
    provider = "transmission"
    enabled = True
    connection_settings = TorrentConnectionSettings()


class IpfsConfigSchema(BaseModel):
    enabled: bool = False
    connection_settings: Dict[str, Any] = {"addr": "/dns/localhost/tcp/5001/http"}


class SettingsSchema(BaseModel):
    torrent_files_dir: str = "./libgen-seedtools-data/torrentfiles"
    assets_dir: str = "./libgen-seedtools-data/data"
    torrent_data_url: str = "https://phillm.net/libgen-stats-formatted.php"
    max_disk_usage: str = "2TB"
    default_source: str = "torrent"
    include_types: List[
        Union[Literal["fiction"], Literal["books"], Literal["scimag"]]
    ] = ["fiction", "books", "scimag"]
    torrent_seeders_range: List[int] = [1, 3]
    ipfs_seeders_range: List[int] = [1, 3]
    ipfs_default_hash_algo: str = "blake2b-256"


class ConfigSchema(BaseModel):
    version: float = 1.0
    torrent: TorrentConfigSchema = TorrentConfigSchema()
    ipfs: IpfsConfigSchema = IpfsConfigSchema()
    settings: SettingsSchema = SettingsSchema()


class Ctx(BaseModel):
    config: ConfigSchema
    configPath: str

    class Config:
        arbitrary_types_allowed = True


def getctx(ctx: Dict[str, Any]) -> Ctx:
    return Ctx(**ctx)


def save(ctx: Ctx):
    with open(ctx.configPath, "w") as out:
        out.write(json.dumps(ctx.config.dict(), indent=2, sort_keys=True))


def load_config(path: str) -> ConfigSchema:
    if os.path.exists(path):
        try:
            with open(path) as config_file:
                return ConfigSchema(**json.loads(config_file.read()))
        except:
            return ConfigSchema()
    return ConfigSchema()
