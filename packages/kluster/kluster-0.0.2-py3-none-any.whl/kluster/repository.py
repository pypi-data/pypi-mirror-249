from koil.composition import KoiledModel
from fakts import Fakts
from dask.distributed import Client, Security
from dask_gateway import Gateway, BasicAuth, GatewayCluster
from dask_gateway.auth import GatewayAuth
from herre.herre import get_current_herre
from typing import Callable, Awaitable, TypeVar
import contextvars

current_repository = contextvars.ContextVar("current_repository", default=None)


class JWTAuth(GatewayAuth):
    """Attaches HTTP Basic Authentication to the given Request object."""

    def __init__(self, token):
        self.token = token

        print(self.token)

    def pre_request(self, resp):
        headers = {"Authorization": "Bearer " + self.token}
        return headers, None


T = TypeVar("T", bound="Repository")


def get_current_repository() -> "Repository":
    """Get Current Repository

    Returns
    -------
    Repository
        The current repository
    """
    repo = current_repository.get()
    if repo is None:
        raise RuntimeError("No current repository")

    return repo


class Repository(KoiledModel):
    endpoint: str
    token_loader: Callable[[], Awaitable[str]]
    token_refresher: Callable[[], Awaitable[str]]

    async def aget_client_for_cluster(
        self, cluster_name: str, asynchronous: bool = False
    ) -> GatewayCluster:
        token = await self.token_loader()

        gateway = Gateway(
            address=self.endpoint,
            auth=JWTAuth(token),
            asynchronous=asynchronous,
        )

        return gateway.connect(cluster_name)

    async def aget_dashboard_url(self, dashboard_url: str) -> str:
        return self.endpoint + dashboard_url

    async def __aenter__(self: T) -> T:
        current_repository.set(self)
        return await super().__aenter__()

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        current_repository.set(None)
        return await super().__aexit__(exc_type, exc_val, exc_tb)

    class Config:
        underscore_attrs_are_private = True
        arbitrary_types_allowed = True
