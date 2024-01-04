from rath.scalars import ID
from omero_ark.funcs import execute, aexecute
from typing_extensions import Literal
from typing import Optional, List, Tuple
from enum import Enum
from datetime import datetime
from pydantic import BaseModel, Field
from omero_ark.rath import OmeroArkRath


class ProjectFilter(BaseModel):
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


class DatasetFilter(BaseModel):
    ids: Optional[Tuple[ID, ...]]
    search: Optional[str]

    class Config:
        frozen = True
        extra = "forbid"
        use_enum_values = True


class ImageFilter(BaseModel):
    ids: Optional[Tuple[ID, ...]]
    search: Optional[str]

    class Config:
        frozen = True
        extra = "forbid"
        use_enum_values = True


class OmerUserInput(BaseModel):
    username: str
    password: str

    class Config:
        frozen = True
        extra = "forbid"
        use_enum_values = True


class ProjectFragmentDatasets(BaseModel):
    typename: Optional[Literal["Dataset"]] = Field(alias="__typename", exclude=True)
    id: str
    name: str
    description: str

    class Config:
        frozen = True


class ProjectFragment(BaseModel):
    typename: Optional[Literal["Project"]] = Field(alias="__typename", exclude=True)
    id: str
    name: str
    description: str
    datasets: Tuple[ProjectFragmentDatasets, ...]

    class Config:
        frozen = True


class ImageFragment(BaseModel):
    typename: Optional[Literal["Image"]] = Field(alias="__typename", exclude=True)
    id: str
    name: str
    description: str

    class Config:
        frozen = True


class EnsureOmeroUserMutationEnsureomerouserUser(BaseModel):
    typename: Optional[Literal["User"]] = Field(alias="__typename", exclude=True)
    id: ID
    sub: str

    class Config:
        frozen = True


class EnsureOmeroUserMutationEnsureomerouser(BaseModel):
    typename: Optional[Literal["OmeroUser"]] = Field(alias="__typename", exclude=True)
    id: ID
    omero_username: str = Field(alias="omeroUsername")
    omero_password: str = Field(alias="omeroPassword")
    user: EnsureOmeroUserMutationEnsureomerouserUser

    class Config:
        frozen = True


class EnsureOmeroUserMutation(BaseModel):
    ensure_omero_user: EnsureOmeroUserMutationEnsureomerouser = Field(
        alias="ensureOmeroUser"
    )

    class Arguments(BaseModel):
        username: str
        password: str

    class Meta:
        document = "mutation EnsureOmeroUser($username: String!, $password: String!) {\n  ensureOmeroUser(input: {username: $username, password: $password}) {\n    id\n    omeroUsername\n    omeroPassword\n    user {\n      id\n      sub\n    }\n  }\n}"


class ListProjectsQueryProjectsDatasetsImages(BaseModel):
    typename: Optional[Literal["Image"]] = Field(alias="__typename", exclude=True)
    name: str
    acquisition_date: Optional[datetime] = Field(alias="acquisitionDate")

    class Config:
        frozen = True


class ListProjectsQueryProjectsDatasets(BaseModel):
    typename: Optional[Literal["Dataset"]] = Field(alias="__typename", exclude=True)
    name: str
    description: str
    images: Tuple[ListProjectsQueryProjectsDatasetsImages, ...]

    class Config:
        frozen = True


class ListProjectsQueryProjects(BaseModel):
    typename: Optional[Literal["Project"]] = Field(alias="__typename", exclude=True)
    name: str
    description: str
    datasets: Tuple[ListProjectsQueryProjectsDatasets, ...]

    class Config:
        frozen = True


class ListProjectsQuery(BaseModel):
    projects: Tuple[ListProjectsQueryProjects, ...]

    class Arguments(BaseModel):
        pass

    class Meta:
        document = "query ListProjects {\n  projects {\n    name\n    description\n    datasets {\n      name\n      description\n      images {\n        name\n        acquisitionDate\n      }\n    }\n  }\n}"


class GetProjectQuery(BaseModel):
    project: ProjectFragment

    class Arguments(BaseModel):
        id: ID

    class Meta:
        document = "fragment Project on Project {\n  id\n  name\n  description\n  datasets {\n    id\n    name\n    description\n  }\n}\n\nquery GetProject($id: ID!) {\n  project(id: $id) {\n    ...Project\n  }\n}"


class SearchProjectsQueryOptions(BaseModel):
    typename: Optional[Literal["Project"]] = Field(alias="__typename", exclude=True)
    value: str
    label: str

    class Config:
        frozen = True


class SearchProjectsQuery(BaseModel):
    options: Tuple[SearchProjectsQueryOptions, ...]

    class Arguments(BaseModel):
        search: Optional[str] = Field(default=None)
        values: Optional[List[ID]] = Field(default=None)

    class Meta:
        document = "query SearchProjects($search: String, $values: [ID!]) {\n  options: projects(\n    filters: {search: $search, ids: $values}\n    pagination: {limit: 10}\n  ) {\n    value: id\n    label: name\n  }\n}"


class ListImagesQueryImages(BaseModel):
    typename: Optional[Literal["Image"]] = Field(alias="__typename", exclude=True)
    name: str
    description: str

    class Config:
        frozen = True


class ListImagesQuery(BaseModel):
    images: ListImagesQueryImages

    class Arguments(BaseModel):
        pass

    class Meta:
        document = "query ListImages {\n  images {\n    name\n    description\n  }\n}"


class GetImageQuery(BaseModel):
    image: ImageFragment

    class Arguments(BaseModel):
        id: ID

    class Meta:
        document = "fragment Image on Image {\n  id\n  name\n  description\n}\n\nquery GetImage($id: ID!) {\n  image(id: $id) {\n    ...Image\n  }\n}"


class SearchImagesQueryOptions(BaseModel):
    typename: Optional[Literal["Image"]] = Field(alias="__typename", exclude=True)
    value: str
    label: str

    class Config:
        frozen = True


class SearchImagesQuery(BaseModel):
    options: SearchImagesQueryOptions

    class Arguments(BaseModel):
        search: Optional[str] = Field(default=None)
        values: Optional[List[ID]] = Field(default=None)

    class Meta:
        document = "query SearchImages($search: String, $values: [ID!]) {\n  options: images(\n    filters: {search: $search, ids: $values}\n    pagination: {limit: 10}\n  ) {\n    value: id\n    label: name\n  }\n}"


async def aensure_omero_user(
    username: str, password: str, rath: OmeroArkRath = None
) -> EnsureOmeroUserMutationEnsureomerouser:
    """EnsureOmeroUser



    Arguments:
        username (str): username
        password (str): password
        rath (omero_ark.rath.OmeroArkRath, optional): The omero_ark rath client

    Returns:
        EnsureOmeroUserMutationEnsureomerouser"""
    return (
        await aexecute(
            EnsureOmeroUserMutation,
            {"username": username, "password": password},
            rath=rath,
        )
    ).ensure_omero_user


def ensure_omero_user(
    username: str, password: str, rath: OmeroArkRath = None
) -> EnsureOmeroUserMutationEnsureomerouser:
    """EnsureOmeroUser



    Arguments:
        username (str): username
        password (str): password
        rath (omero_ark.rath.OmeroArkRath, optional): The omero_ark rath client

    Returns:
        EnsureOmeroUserMutationEnsureomerouser"""
    return execute(
        EnsureOmeroUserMutation, {"username": username, "password": password}, rath=rath
    ).ensure_omero_user


async def alist_projects(rath: OmeroArkRath = None) -> List[ListProjectsQueryProjects]:
    """ListProjects



    Arguments:
        rath (omero_ark.rath.OmeroArkRath, optional): The omero_ark rath client

    Returns:
        List[ListProjectsQueryProjects]"""
    return (await aexecute(ListProjectsQuery, {}, rath=rath)).projects


def list_projects(rath: OmeroArkRath = None) -> List[ListProjectsQueryProjects]:
    """ListProjects



    Arguments:
        rath (omero_ark.rath.OmeroArkRath, optional): The omero_ark rath client

    Returns:
        List[ListProjectsQueryProjects]"""
    return execute(ListProjectsQuery, {}, rath=rath).projects


async def aget_project(id: ID, rath: OmeroArkRath = None) -> ProjectFragment:
    """GetProject



    Arguments:
        id (ID): id
        rath (omero_ark.rath.OmeroArkRath, optional): The omero_ark rath client

    Returns:
        ProjectFragment"""
    return (await aexecute(GetProjectQuery, {"id": id}, rath=rath)).project


def get_project(id: ID, rath: OmeroArkRath = None) -> ProjectFragment:
    """GetProject



    Arguments:
        id (ID): id
        rath (omero_ark.rath.OmeroArkRath, optional): The omero_ark rath client

    Returns:
        ProjectFragment"""
    return execute(GetProjectQuery, {"id": id}, rath=rath).project


async def asearch_projects(
    search: Optional[str] = None,
    values: Optional[List[ID]] = None,
    rath: OmeroArkRath = None,
) -> List[SearchProjectsQueryOptions]:
    """SearchProjects



    Arguments:
        search (Optional[str], optional): search.
        values (Optional[List[ID]], optional): values.
        rath (omero_ark.rath.OmeroArkRath, optional): The omero_ark rath client

    Returns:
        List[SearchProjectsQueryProjects]"""
    return (
        await aexecute(
            SearchProjectsQuery, {"search": search, "values": values}, rath=rath
        )
    ).projects


def search_projects(
    search: Optional[str] = None,
    values: Optional[List[ID]] = None,
    rath: OmeroArkRath = None,
) -> List[SearchProjectsQueryOptions]:
    """SearchProjects



    Arguments:
        search (Optional[str], optional): search.
        values (Optional[List[ID]], optional): values.
        rath (omero_ark.rath.OmeroArkRath, optional): The omero_ark rath client

    Returns:
        List[SearchProjectsQueryProjects]"""
    return execute(
        SearchProjectsQuery, {"search": search, "values": values}, rath=rath
    ).projects


async def alist_images(rath: OmeroArkRath = None) -> ListImagesQueryImages:
    """ListImages



    Arguments:
        rath (omero_ark.rath.OmeroArkRath, optional): The omero_ark rath client

    Returns:
        ListImagesQueryImages"""
    return (await aexecute(ListImagesQuery, {}, rath=rath)).images


def list_images(rath: OmeroArkRath = None) -> ListImagesQueryImages:
    """ListImages



    Arguments:
        rath (omero_ark.rath.OmeroArkRath, optional): The omero_ark rath client

    Returns:
        ListImagesQueryImages"""
    return execute(ListImagesQuery, {}, rath=rath).images


async def aget_image(id: ID, rath: OmeroArkRath = None) -> ImageFragment:
    """GetImage



    Arguments:
        id (ID): id
        rath (omero_ark.rath.OmeroArkRath, optional): The omero_ark rath client

    Returns:
        ImageFragment"""
    return (await aexecute(GetImageQuery, {"id": id}, rath=rath)).image


def get_image(id: ID, rath: OmeroArkRath = None) -> ImageFragment:
    """GetImage



    Arguments:
        id (ID): id
        rath (omero_ark.rath.OmeroArkRath, optional): The omero_ark rath client

    Returns:
        ImageFragment"""
    return execute(GetImageQuery, {"id": id}, rath=rath).image


async def asearch_images(
    search: Optional[str] = None,
    values: Optional[List[ID]] = None,
    rath: OmeroArkRath = None,
) -> SearchImagesQueryOptions:
    """SearchImages



    Arguments:
        search (Optional[str], optional): search.
        values (Optional[List[ID]], optional): values.
        rath (omero_ark.rath.OmeroArkRath, optional): The omero_ark rath client

    Returns:
        SearchImagesQueryImages"""
    return (
        await aexecute(
            SearchImagesQuery, {"search": search, "values": values}, rath=rath
        )
    ).images


def search_images(
    search: Optional[str] = None,
    values: Optional[List[ID]] = None,
    rath: OmeroArkRath = None,
) -> SearchImagesQueryOptions:
    """SearchImages



    Arguments:
        search (Optional[str], optional): search.
        values (Optional[List[ID]], optional): values.
        rath (omero_ark.rath.OmeroArkRath, optional): The omero_ark rath client

    Returns:
        SearchImagesQueryImages"""
    return execute(
        SearchImagesQuery, {"search": search, "values": values}, rath=rath
    ).images
