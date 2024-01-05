from dask.distributed import Client
from fakts import Fakts
from herre import Herre
from kluster.repository import Repository
from typing import Callable, Awaitable


async def dummy_loader():
    return "dummy"


class ArkitektRepository(Repository):
    endpoint: str = "dummy"
    token_loader: Callable[[], Awaitable[str]] = dummy_loader
    token_refresher: Callable[[], Awaitable[str]] = dummy_loader
    fakts: Fakts
    herre: Herre
    fakts_key: str

    _configured = False

    async def aconfigure(self):
        self.endpoint = await self.fakts.aget(self.fakts_key)
        self.token_loader = self.herre.aget_token
        self.token_refresher = self.herre.arefresh_token
        self._configured

    async def aget_client_for_cluster(self, cluster_name: str) -> Client:
        if not self._configured:
            await self.aconfigure()
        return await super().aget_client_for_cluster(cluster_name)
