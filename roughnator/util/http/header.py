from typing import Optional

from roughnator.util.dict import KeyValue, add_to_dict
from roughnator.util.identity import Named


class HttpHeader(KeyValue[str, str], Named):
    """
    Represent an HTTP header.
    """
    def __init__(self, value: Optional[str] = None):
        super().__init__(self.canonical_name(), value)
# NOTES.
# 1. Case-insensitive lookup. For now we assume the dictionary passed to
# ``KeyValue.read`` supports key case-insensitive lookup---this is the
# case when using the requests lib.
# 2. Case-insensitive name. We could override ``Name.is_named_as`` to
# do a case-insensitive comparison, but it's probably best to actually
# have ``Name`` implement that by default. So we're leaving this out
# for now.


def pack(*args: HttpHeader) -> dict:
    """
    Pack the given headers into a key-value dictionary.

    :param args: the headers to put into the dictionary.
    :return: the dictionary with the headers.
    """
    return add_to_dict(*args)


class ContentTypeHeader(HttpHeader):

    def __init__(self, value: Optional[str] = None):
        super().__init__(value)

    def canonical_name(self) -> str:
        return 'Content-Type'


class AppJsonContentTypeHeader(ContentTypeHeader):

    def __init__(self):
        super().__init__('application/json')


class AuthorizationHeader(HttpHeader):

    def __init__(self, value: Optional[str] = None):
        super().__init__(value)

    def canonical_name(self) -> str:
        return 'Authorization'

    def with_bearer(self, token: str) -> 'AuthorizationHeader':
        self._value = f"Bearer {token}"
        return self


class FiwareServiceHeader(HttpHeader):

    def __init__(self, value: Optional[str] = None):
        super().__init__(value)

    def canonical_name(self) -> str:
        return 'fiware-service'


class FiwareServicePathHeader(HttpHeader):

    def __init__(self, value: Optional[str] = None):
        super().__init__(value)

    def canonical_name(self) -> str:
        return 'fiware-servicepath'


class FiwareCorrelatorHeader(HttpHeader):

    def __init__(self, value: Optional[str] = None):
        super().__init__(value)

    def canonical_name(self) -> str:
        return 'fiware-correlator'
