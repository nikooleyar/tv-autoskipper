"""Pairing with the TV and keeping a connection to it open."""

import asyncio
import json
import logging
from pathlib import Path

from pyytlounge import YtLoungeApi

from .skipper import AdSkipper

log = logging.getLogger(__name__)

DEVICE_NAME = "tv-autoskipper"  # shown on the TV when we connect
RETRY_SECONDS = 10
# Outside the repo, so the saved login can never be committed.
DEFAULT_AUTH_FILE = Path.home() / ".config" / "tv-autoskipper" / "auth.json"


def _api() -> YtLoungeApi:
    return YtLoungeApi(DEVICE_NAME, logger=logging.getLogger("pyytlounge"))


async def pair(code: str, auth_file: Path) -> None:
    """Link to the TV with the code from YouTube > Settings > Link with TV code."""
    async with _api() as api:
        if not await api.pair(code.replace(" ", "").replace("-", "")):
            raise SystemExit("Pairing failed: check the code and try again.")
        auth_file.parent.mkdir(parents=True, exist_ok=True)
        auth_file.write_text(json.dumps(api.store_auth_state()))
        print(f"Paired with {api.screen_name}")


async def run(auth_file: Path) -> None:
    """Stay connected to the TV and skip ads until stopped."""
    if not auth_file.exists():
        raise SystemExit("Not paired yet. Run: tv-autoskipper pair <code>")
    async with _api() as api:
        api.load_auth_state(json.loads(auth_file.read_text()))
        api.event_listener = AdSkipper(api)
        while True:
            try:
                if not api.linked():
                    await api.refresh_auth()
                if await api.connect():
                    log.info("Connected to %s", api.screen_name)
                    await api.subscribe()  # returns when the connection drops
            except Exception:
                # Long-running service: log and retry instead of dying when
                # the TV is off or the network blips.
                log.exception("Connection problem, retrying")
            await asyncio.sleep(RETRY_SECONDS)
