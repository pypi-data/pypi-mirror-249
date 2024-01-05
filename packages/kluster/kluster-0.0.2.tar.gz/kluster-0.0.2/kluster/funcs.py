""" This module provides helpers for the mikro rath api
they are wrapped functions for the turms generated api"""
from .rath import KlusterRath, current_kluster_rath
from koil.helpers import unkoil, unkoil_gen
from typing import Optional, Protocol, Type, Dict, Any, TypeVar, Iterator, AsyncIterator
from pydantic import BaseModel


class MetaProtocol(Protocol):
    document: str


class Operation(Protocol):
    Meta: MetaProtocol
    Arguments: Type[BaseModel]


T = TypeVar("T")


async def aexecute(
    operation: Type[T],
    variables: Dict[str, Any],
    rath: Optional[KlusterRath] = None,
) -> T:
    rath = rath or current_kluster_rath.get()

    x = await rath.aquery(
        operation.Meta.document,  # type: ignore
        operation.Arguments(**variables).dict(by_alias=True),  # type: ignore
    ) # type: ignore
    return operation(**x.data)


def execute(
    operation: Type[T],
    variables: Dict[str, Any],
    rath: Optional[KlusterRath] = None,
) -> T:
    return unkoil(aexecute, operation, variables, rath=rath)


def subscribe(
    operation: Type[T],
    variables: Dict[str, Any],
    rath: Optional[KlusterRath] = None,
) -> Iterator[T]:
    return unkoil_gen(asubscribe, operation, variables, rath=rath)


async def asubscribe(
    operation: Type[T],
    variables: Dict[str, Any],
    rath: Optional[KlusterRath] = None,
) -> AsyncIterator[T]:
    rath = rath or current_kluster_rath.get()
    async for event in rath.asubscribe(
        operation.Meta.document, operation.Arguments(**variables).dict(by_alias=True), # type: ignore
    ):
        yield operation(**event.data)
