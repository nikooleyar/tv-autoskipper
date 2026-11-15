import asyncio

from pyytlounge import AdStateEvent

from tv_autoskipper.skipper import AdSkipper


class FakeRemote:
    def __init__(self) -> None:
        self.skips = 0

    async def skip_ad(self) -> bool:
        self.skips += 1
        return True


def _ad_state(skip_enabled: bool) -> AdStateEvent:
    return AdStateEvent(
        {"adState": "1", "currentTime": "5", "isSkipEnabled": str(skip_enabled).lower()}
    )


def test_skips_once_skip_is_enabled():
    remote = FakeRemote()
    asyncio.run(AdSkipper(remote).ad_state_changed(_ad_state(True)))
    assert remote.skips == 1


def test_waits_while_skip_is_not_enabled():
    remote = FakeRemote()
    asyncio.run(AdSkipper(remote).ad_state_changed(_ad_state(False)))
    assert remote.skips == 0
