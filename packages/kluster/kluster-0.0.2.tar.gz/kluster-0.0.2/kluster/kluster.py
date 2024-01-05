from koil.composition import Composition
from .rath import KlusterRath
from .repository import Repository


class Kluster(Composition):
    """The Mikro Composition

    This composition provides a datalayer and a omero_ark for interacting with the
    mikro api and beyond

    """

    rath: KlusterRath
    repo: Repository

    def _repr_html_inline_(self):
        return f"<table><td>rath</td><td>{self.rath._repr_html_inline_()}</td></tr></table>"
