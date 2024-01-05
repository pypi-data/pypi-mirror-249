""" Strucutre Registration

This module is autoimported by arkitekt. It registers the default structure types with the arkitekt
structure-registry so that they can be used in the arkitekt app without having to import them.

You can of course overwrite this in your app if you need to expand to a more complex query.

"""
import logging

logger = logging.getLogger(__name__)


try:
    import rekuest
    from rekuest.structures.default import (
        get_default_structure_registry,
        Scope,
        id_shrink,
    )
    from rekuest.widgets import SearchWidget
    from kluster.api.schema import (
        DaskClusterFragment,
        aget_dask_cluster,
        SearchDaskClusterQuery,
    )

    structure_reg = get_default_structure_registry()
    structure_reg.register_as_structure(
        DaskClusterFragment,
        identifier="@kluster/dask-cluster",
        aexpand=aget_dask_cluster,
        ashrink=id_shrink,
        scope=Scope.GLOBAL,
        default_widget=SearchWidget(
            query=SearchDaskClusterQuery.Meta.document, ward="kluster"
        ),
    )


except ImportError:
    pass
