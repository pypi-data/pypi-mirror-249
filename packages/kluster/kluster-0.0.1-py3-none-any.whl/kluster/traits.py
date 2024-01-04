"""
Traits for omero_ark


Traits are mixins that are added to every graphql type that exists on the mikro schema.
We use them to add functionality to the graphql types that extend from the base type.

Every GraphQL Model on Mikro gets a identifier and shrinking methods to ensure the compatibliity
with arkitekt. This is done by adding the identifier and the shrinking methods to the graphql type.
If you want to add your own traits to the graphql type, you can do so by adding them in the graphql
.config.yaml file.

"""

from typing import Awaitable, List, TypeVar, Tuple, Protocol, Optional
import numpy as np
from pydantic import BaseModel
import xarray as xr
import pandas as pd
from rath.links.shrink import ShrinkByID
from typing import TYPE_CHECKING
from rath.scalars import ID
from typing import Any
import pyarrow.parquet as pq

if TYPE_CHECKING:
    pass


class Image(BaseModel):
    """Representation Trait

    Implements both identifier and shrinking methods.
    Also Implements the data attribute

    Attributes:
        data (xarray.Dataset): The data of the representation.

    """

    @property
    def data(self) -> xr.DataArray:
        store = get_attributes_or_error(self, "store")
        return xr.open_zarr(store=store.zarr_store, consolidated=True)["data"]

    async def adata(self) -> Awaitable[xr.DataArray]:
        """The Data of the Representation as an xr.DataArray. Accessible from asyncio.

        Returns:
            xr.DataArray: The associated object.

        Raises:
            AssertionError: If the representation has no store attribute quries
        """
        pstore = get_attributes_or_error(self, "store")
        return await pstore.aopen()

    def get_pixel_size(self, stage: ID = None) -> Tuple[float, float, float]:
        """The pixel size of the representation

        Returns:
            Tuple[float, float, float]: The pixel size
        """
        views = get_attributes_or_error(self, "views")

        for view in views:
            if isinstance(view, PixelTranslatable):
                if stage is None:
                    return view.pixel_size
                else:
                    if get_attributes_or_error(view, "stage.id") == stage:
                        return view.pixel_size

        raise NotImplementedError(
            f"No pixel size found for this representation {self}. Have you attached any views?"
        )
