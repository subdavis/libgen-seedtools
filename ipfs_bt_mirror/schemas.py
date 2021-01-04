from typing import Dict, Any

from pydantic import BaseModel
from requests_toolbelt.sessions import BaseUrlSession


class TorrentConfigSchema(BaseModel):
    provider: str = "qbittorrent"
    enabled: bool = True
    connection_settings: Dict[str, Any] = {
        "host": "http://localhost:8080"
    }


class IpfsConfigSchema(BaseModel):
    enabled: bool = True
    connection_settings: Dict[str, Any] = {
        "addr": "/dns/localhost/tcp/5001/http"
    }


class SettingsSchema(BaseModel):
    manifest_dir: str = "./pmir/manifests"
    torrent_files_dir: str = "./pmir/torrentfiles"
    assets_dir: str = "./pmir/data"
    max_disk_usage: str = "10GB"
    default_source: str = "torrent"
    torrent_seeders_range: [int, int] = [0, 4]
    ipfs_seeders_range: [int, int] = [0, 4]
    ipfs_default_hash_algo: str = "blake2b-256"


class Config(BaseModel):
    version: float = 1.0
    torrent: TorrentConfigSchema
    ipfs: IpfsConfigSchema
    settings: SettingsSchema


class Ctx(BaseModel):
    config: Config
    configPath: str
    session: BaseUrlSession

    class Config:
        arbitrary_types_allowed = True


def getctx(ctx: Dict[str, Any]) -> Ctx:
    return Ctx(**ctx)


def save(ctx: Ctx):
    with open(ctx.configPath, "w") as out:
        out.write(ctx.config.json())


def load_config(path: str) -> Config:
    if os.path.exists(path):
        try:
            with open(path) as config_file:
                return Config(**json.loads(config_file.read()))
        except:
            return Config()
    return Config()
