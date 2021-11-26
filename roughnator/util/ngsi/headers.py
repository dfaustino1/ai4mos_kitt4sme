from typing import Optional

from roughnator.util.http.header import HttpHeader


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
