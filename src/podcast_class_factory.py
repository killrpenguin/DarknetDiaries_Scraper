from __future__ import annotations
from requests import Session
from requests import Response
from requests.exceptions import RequestException


class BaseClass:
    """Base class for podcast episodes"""

    def __init__(self, classtype) -> None:
        self._type = classtype

    def dn_page(self) -> Response | None:
        """Method for requesting darknet diaries xml page."""
        try:
            with Session() as session:
                dn_request = session.get('https://podcast.darknetdiaries.com/',
                                         timeout=30)
        except RequestException:
            return None
        return dn_request


def episode_factory(name, arg_names, base_class=BaseClass):
    """ Factory funtion for producing podcast episode objects."""

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            if k not in arg_names:
                raise TypeError(
                    f'"Argument {k} not valid for {self.__class__.__name__}"')
            setattr(self, k, v)
        base_class.__init__(self, name[:-len("Class")])

    def __repr__(self) -> None:
        return f'{type(self).__name__}'

    return type(name, (base_class, ), {
        "__init__": __init__,
        "__repr__": __repr__,
    })
