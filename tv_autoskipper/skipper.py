"""The skipping rule: press skip as soon as the TV says it is allowed."""

import logging
from typing import Protocol

from pyytlounge import AdPlayingEvent, AdStateEvent, EventListener

log = logging.getLogger(__name__)


class Remote(Protocol):
    async def skip_ad(self) -> bool: ...


class AdSkipper(EventListener):
    def __init__(self, remote: Remote) -> None:
        super().__init__()
        self._remote = remote

    async def ad_playing_changed(self, event: AdPlayingEvent) -> None:
        log.info("Ad started: %s", event.ad_title)
        log.debug("ad_playing %s", vars(event))  # --verbose: everything the TV told us
        await self._skip_if_enabled(event.is_skip_enabled)

    async def ad_state_changed(self, event: AdStateEvent) -> None:
        log.debug("ad_state %s", vars(event))
        await self._skip_if_enabled(event.is_skip_enabled)

    async def _skip_if_enabled(self, skip_enabled: bool) -> None:
        if skip_enabled:
            log.info("Skip available, skipping ad")
            await self._remote.skip_ad()
