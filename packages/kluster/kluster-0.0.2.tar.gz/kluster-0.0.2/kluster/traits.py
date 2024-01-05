"""
Traits for omero_ark


Traits are mixins that are added to every graphql type that exists on the mikro schema.
We use them to add functionality to the graphql types that extend from the base type.

Every GraphQL Model on Mikro gets a identifier and shrinking methods to ensure the compatibliity
with arkitekt. This is done by adding the identifier and the shrinking methods to the graphql type.
If you want to add your own traits to the graphql type, you can do so by adding them in the graphql
.config.yaml file.

"""

from pydantic import BaseModel
from typing import TYPE_CHECKING
from rath.turms.utils import get_attributes_or_error
from dask.distributed import Client
from dask_gateway import Gateway, GatewayCluster
from .repository import get_current_repository
from koil import unkoil
import webbrowser

if TYPE_CHECKING:
    pass


class DaskClientBearer(BaseModel):
    """Representation Trait

    Implements both identifier and shrinking methods.
    Also Implements the data attribute

    Attributes:
        data (xarray.Dataset): The data of the representation.

    """

    async def aget_gateway(self, asynchronous: bool = False) -> GatewayCluster:
        """Get the dask client for the representation.

        Returns:
            Client: The dask client for the representation.
        """
        return await get_current_repository().aget_client_for_cluster(
            self.id, asynchronous=asynchronous
        )

    async def aget_dashboard_url(self) -> Client:
        """Get the dask client for the representation.

        Returns:
            Client: The dask client for the representation.
        """
        return await get_current_repository().aget_dashboard_url(self.dashboard_link)

    def get_gateway(self) -> GatewayCluster:
        return unkoil(self.aget_gateway)

    def open_dashboard(self) -> str:
        absolute_url = unkoil(self.aget_dashboard_url)
        webbrowser.open(absolute_url)
