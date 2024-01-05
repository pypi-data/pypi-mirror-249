from kluster.api.schema import DaskClusterFragment, DaskClusterState
from dask.distributed import Client, Security
from dask_gateway import Gateway, BasicAuth
from dask_gateway.auth import GatewayAuth
from herre.herre import get_current_herre


class JWTAuth(GatewayAuth):
    """Attaches HTTP Basic Authentication to the given Request object."""

    def __init__(self, token):
        self.token = token

        print(self.token)

    def pre_request(self, resp):
        headers = {"Authorization": "Bearer " + self.token}
        return headers, None


from herre import Herre


def get_client_for_cluster(cluster: DaskClusterFragment, herre: Herre = None) -> Client:
    """Get Client for Cluster

    Parameters
    ----------
    cluster : DaskClusterFragment
        The cluster

    Returns
    -------
    Client
        The client
    """
    from kluster.api.schema import DaskClusterState

    address = cluster.scheduler_address.replace(
        "gateway://dask_gateway", "tcp://localhost"
    )
    herre = herre or get_current_herre()

    token = herre.get_token()

    gateway = Gateway(
        address="http://localhost:9020",
        auth=JWTAuth(token),
    )

    x = gateway.connect(cluster.id)
    return x.get_client()
