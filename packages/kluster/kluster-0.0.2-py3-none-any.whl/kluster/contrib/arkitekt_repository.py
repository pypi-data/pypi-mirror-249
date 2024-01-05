from fakts import Fakts
from herre import Herre
from kluster.repository import Repository
from typing import Callable, Awaitable
from dask.distributed import Client


async def dummy_loader():
    return "dummy"


class ArkitektRepository(Repository):
    fakts: Fakts
    herre: Herre
    fakts_key: str
    endpoint: str = "dummy"
    token_loader: Callable[[], Awaitable[str]] = dummy_loader
    token_refresher: Callable[[], Awaitable[str]] = dummy_loader

    _configured = False

    async def aconfigure(self):
        self.endpoint = await self.fakts.aget(self.fakts_key)
        self.token_loader = self.herre.aget_token
        self.token_refresher = self.herre.arefresh_token
        self._configured = True

    async def aget_client_for_cluster(self, *args, **kwargs) -> Client:
        if not self._configured:
            await self.aconfigure()
        return await super().aget_client_for_cluster(*args, **kwargs)

    async def aget_dashboard_url(self, dashboard_url: str) -> str:
        if not self._configured:
            await self.aconfigure()
        return await super().aget_dashboard_url(dashboard_url)
