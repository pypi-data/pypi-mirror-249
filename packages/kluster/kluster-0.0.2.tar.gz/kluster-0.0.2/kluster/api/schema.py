from rath.scalars import ID
from typing_extensions import Literal
from typing import Optional, List, Tuple
from pydantic import BaseModel, Field
from kluster.funcs import aexecute, execute
from enum import Enum
from kluster.traits import DaskClientBearer
from kluster.rath import KlusterRath


class DaskClusterState(str, Enum):
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    STOPPING = "STOPPING"
    STOPPED = "STOPPED"
    FAILED = "FAILED"


class ClusterFilter(BaseModel):
    ids: Optional[Tuple[ID, ...]]
    search: Optional[str]

    class Config:
        frozen = True
        extra = "forbid"
        use_enum_values = True


class OffsetPaginationInput(BaseModel):
    offset: int
    limit: int

    class Config:
        frozen = True
        extra = "forbid"
        use_enum_values = True


class CreateClusterInput(BaseModel):
    name: str

    class Config:
        frozen = True
        extra = "forbid"
        use_enum_values = True


class DaskClusterFragmentSecurity(BaseModel):
    """A security object for a dask cluster"""

    typename: Optional[Literal["Security"]] = Field(alias="__typename", exclude=True)
    tls_cert: str = Field(alias="tlsCert")
    tls_key: str = Field(alias="tlsKey")

    class Config:
        frozen = True


class DaskClusterFragment(DaskClientBearer, BaseModel):
    typename: Optional[Literal["DaskCluster"]] = Field(alias="__typename", exclude=True)
    id: ID
    name: str
    dashboard_link: str = Field(alias="dashboardLink")
    status: DaskClusterState
    scheduler_address: str = Field(alias="schedulerAddress")
    security: Optional[DaskClusterFragmentSecurity]

    class Config:
        frozen = True


class CreateDaskClusterMutation(BaseModel):
    create_dask_cluster: DaskClusterFragment = Field(alias="createDaskCluster")

    class Arguments(BaseModel):
        name: str

    class Meta:
        document = "fragment DaskCluster on DaskCluster {\n  id\n  name\n  dashboardLink\n  status\n  schedulerAddress\n  security {\n    tlsCert\n    tlsKey\n  }\n}\n\nmutation CreateDaskCluster($name: String!) {\n  createDaskCluster(input: {name: $name}) {\n    ...DaskCluster\n  }\n}"


class ListDaskClustersQuery(BaseModel):
    dask_clusters: Tuple[DaskClusterFragment, ...] = Field(alias="daskClusters")

    class Arguments(BaseModel):
        pass

    class Meta:
        document = "fragment DaskCluster on DaskCluster {\n  id\n  name\n  dashboardLink\n  status\n  schedulerAddress\n  security {\n    tlsCert\n    tlsKey\n  }\n}\n\nquery ListDaskClusters {\n  daskClusters {\n    ...DaskCluster\n  }\n}"


class GetDaskClusterQuery(BaseModel):
    dask_cluster: DaskClusterFragment = Field(alias="daskCluster")

    class Arguments(BaseModel):
        id: ID

    class Meta:
        document = "fragment DaskCluster on DaskCluster {\n  id\n  name\n  dashboardLink\n  status\n  schedulerAddress\n  security {\n    tlsCert\n    tlsKey\n  }\n}\n\nquery GetDaskCluster($id: ID!) {\n  daskCluster(id: $id) {\n    ...DaskCluster\n  }\n}"


class SearchDaskClusterQueryOptions(DaskClientBearer, BaseModel):
    """A dask cluster"""

    typename: Optional[Literal["DaskCluster"]] = Field(alias="__typename", exclude=True)
    value: ID
    label: str

    class Config:
        frozen = True


class SearchDaskClusterQuery(BaseModel):
    options: Tuple[SearchDaskClusterQueryOptions, ...]

    class Arguments(BaseModel):
        search: Optional[str] = Field(default=None)
        values: Optional[List[ID]] = Field(default=None)

    class Meta:
        document = "query SearchDaskCluster($search: String, $values: [ID!]) {\n  options: daskClusters(\n    filters: {search: $search, ids: $values}\n    pagination: {limit: 10}\n  ) {\n    value: id\n    label: name\n  }\n}"


async def acreate_dask_cluster(
    name: str, rath: Optional[KlusterRath] = None
) -> DaskClusterFragment:
    """CreateDaskCluster


     createDaskCluster:  A dask cluster


    Arguments:
        name (str): name
        rath (kluster.rath.KlusterRath, optional): The omero_ark rath client

    Returns:
        DaskClusterFragment"""
    return (
        await aexecute(CreateDaskClusterMutation, {"name": name}, rath=rath)
    ).create_dask_cluster


def create_dask_cluster(
    name: str, rath: Optional[KlusterRath] = None
) -> DaskClusterFragment:
    """CreateDaskCluster


     createDaskCluster:  A dask cluster


    Arguments:
        name (str): name
        rath (kluster.rath.KlusterRath, optional): The omero_ark rath client

    Returns:
        DaskClusterFragment"""
    return execute(
        CreateDaskClusterMutation, {"name": name}, rath=rath
    ).create_dask_cluster


async def alist_dask_clusters(
    rath: Optional[KlusterRath] = None,
) -> List[DaskClusterFragment]:
    """ListDaskClusters


     daskClusters:  A dask cluster


    Arguments:
        rath (kluster.rath.KlusterRath, optional): The omero_ark rath client

    Returns:
        List[DaskClusterFragment]"""
    return (await aexecute(ListDaskClustersQuery, {}, rath=rath)).dask_clusters


def list_dask_clusters(rath: Optional[KlusterRath] = None) -> List[DaskClusterFragment]:
    """ListDaskClusters


     daskClusters:  A dask cluster


    Arguments:
        rath (kluster.rath.KlusterRath, optional): The omero_ark rath client

    Returns:
        List[DaskClusterFragment]"""
    return execute(ListDaskClustersQuery, {}, rath=rath).dask_clusters


async def aget_dask_cluster(
    id: ID, rath: Optional[KlusterRath] = None
) -> DaskClusterFragment:
    """GetDaskCluster


     daskCluster:  A dask cluster


    Arguments:
        id (ID): id
        rath (kluster.rath.KlusterRath, optional): The omero_ark rath client

    Returns:
        DaskClusterFragment"""
    return (await aexecute(GetDaskClusterQuery, {"id": id}, rath=rath)).dask_cluster


def get_dask_cluster(id: ID, rath: Optional[KlusterRath] = None) -> DaskClusterFragment:
    """GetDaskCluster


     daskCluster:  A dask cluster


    Arguments:
        id (ID): id
        rath (kluster.rath.KlusterRath, optional): The omero_ark rath client

    Returns:
        DaskClusterFragment"""
    return execute(GetDaskClusterQuery, {"id": id}, rath=rath).dask_cluster


async def asearch_dask_cluster(
    search: Optional[str] = None,
    values: Optional[List[ID]] = None,
    rath: Optional[KlusterRath] = None,
) -> List[SearchDaskClusterQueryOptions]:
    """SearchDaskCluster


     options:  A dask cluster


    Arguments:
        search (Optional[str], optional): search.
        values (Optional[List[ID]], optional): values.
        rath (kluster.rath.KlusterRath, optional): The omero_ark rath client

    Returns:
        List[SearchDaskClusterQueryDaskclusters]"""
    return (
        await aexecute(
            SearchDaskClusterQuery, {"search": search, "values": values}, rath=rath
        )
    ).dask_clusters


def search_dask_cluster(
    search: Optional[str] = None,
    values: Optional[List[ID]] = None,
    rath: Optional[KlusterRath] = None,
) -> List[SearchDaskClusterQueryOptions]:
    """SearchDaskCluster


     options:  A dask cluster


    Arguments:
        search (Optional[str], optional): search.
        values (Optional[List[ID]], optional): values.
        rath (kluster.rath.KlusterRath, optional): The omero_ark rath client

    Returns:
        List[SearchDaskClusterQueryDaskclusters]"""
    return execute(
        SearchDaskClusterQuery, {"search": search, "values": values}, rath=rath
    ).dask_clusters
