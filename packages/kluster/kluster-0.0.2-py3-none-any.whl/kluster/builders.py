from arkitekt.healthz import FaktsHealthz
from rath.contrib.fakts.links.aiohttp import FaktsAIOHttpLink
from rath.links.split import SplitLink
from rath.contrib.fakts.links.graphql_ws import FaktsGraphQLWSLink
from rath.contrib.herre.links.auth import HerreAuthLink
from kluster.rath import KlusterRathLinkComposition, KlusterRath
from kluster.kluster import Kluster
from graphql import OperationType
from herre import Herre
from fakts import Fakts
from kluster.contrib.arkitekt_repository import ArkitektRepository


class ArkitektKluster(Kluster):
    rath: KlusterRath
    repo: ArkitektRepository
    healthz: FaktsHealthz


def build_arkitekt_kluster(
    fakts: Fakts, herre: Herre, fakts_group: str = "kluster"
) -> KlusterRath:
    repo = ArkitektRepository(
        fakts=fakts,
        herre=herre,
        fakts_key="kluster.gateway_url",
    )

    rath = KlusterRath(
        link=KlusterRathLinkComposition(
            auth=HerreAuthLink(herre=herre),
            split=SplitLink(
                left=FaktsAIOHttpLink(fakts_group=fakts_group, fakts=fakts),
                right=FaktsGraphQLWSLink(fakts_group=fakts_group, fakts=fakts),
                split=lambda o: o.node.operation != OperationType.SUBSCRIPTION,
            ),
        )
    )

    return ArkitektKluster(
        rath=rath,
        repo=repo,
        healthz=FaktsHealthz(fakts_group=fakts_group, fakts=fakts),
    )
