from urllib.parse import urlparse

from transmission_rpc import client, torrent

from .schemas import Ctx, Torrent, TorrentFileData


def _make_client(ctx: Ctx) -> client.Client:
    settings = ctx.config.torrent.connection_settings
    parsed = urlparse(settings.url)
    return client.Client(
        protocol=parsed.scheme,
        host=parsed.hostname,
        port=parsed.port,
        username=settings.username,
        password=settings.password,
    )


def add_torrent(ctx: Ctx, tfd: TorrentFileData) -> Torrent:
    c = _make_client(ctx)
    file_uri = f"file://{tfd.path}"
    torrent_id = c.add_torrent(file_uri)
    torrent = c.get_torrent(torrent_id.id)
    return Torrent(
        data=tfd,
        ratio=torrent.ratio if torrent.ratio >= 0 else 0,
        progress=torrent.progress,
        done=torrent.status == 'seeding',
    )
