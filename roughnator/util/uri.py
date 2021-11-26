"""
Helper functions to build and parse URIs.

TODO: rather use a full-fledged lib like: https://github.com/marrow/uri
"""

import re
from urllib.parse import urlencode, urlparse, parse_qs, urlunparse, \
    ParseResult, quote
from typing import Optional


def _prune_query_params(qs: dict) -> dict:
    pruned = {}
    if qs:
        for k in qs.keys():
            v = qs.get(k)
            if v:
                pruned[k] = v
    return pruned


def _stringify_query_params(qs: dict) -> dict:
    xs = {}
    if qs:
        for k in qs.keys():
            v = qs.get(k)
            if v:
                if isinstance(v, tuple) or isinstance(v, list):
                    xs[k] = ' '.join([str(h) for h in v])
                else:
                    xs[k] = str(v)
    return xs


def parse_url(url: str, scheme: str = '', allow_fragments: bool = True) \
        -> ParseResult:
    """
    Alias for ``urllib.parse.urlparse``.
    """
    return urlparse(url, scheme, allow_fragments)


def url_str(scheme: str, netloc: str, path: str,
            params: str = None, query: dict = None, fragment: str = None) \
        -> str:
    """
    Build a URL string from the input params.
    Pass query parameters, if any, in the query dictionary. We'll handle them
    like this:

        * Remove keys with no corresponding value from the resulting URL.
        * If a key ``k`` has a string value ``v``, add ``ek=ev`` to the
          the query fragment of the URL, where ``ek`` and ``ev`` are the
          URL-encoded key and value, respectively.
        * If a key ``k`` has a tuple or list value ``[v1, v2, ...]``, add
          ``ek=esv1+esv2+...`` to the URL where ``esv[k]`` is the sequence
          element ``v[k]`` converted to string and then URL-encoded.
        * If a key ``k`` has a value ``v`` of any other type, add `ek=esv``
          to the the query fragment of the URL, where ``esv`` is ``v``
          converted to string and then URL-encoded.

    :param scheme: as in ``urllib.parse.ParseResult``.
    :param netloc: as in ``urllib.parse.ParseResult``.
    :param path: as in ``urllib.parse.ParseResult``.
    :param params: as in ``urllib.parse.ParseResult``.
    :param query: dictionary representation of query string.
    :param fragment: as in ``urllib.parse.ParseResult``.
    :return: the URL string.
    """
    query_str = ''
    if query:
        pruned_query_params = _prune_query_params(query)
        stringified_query_params = _stringify_query_params(pruned_query_params)
        query_str = urlencode(stringified_query_params)
    components = (scheme, netloc, path, params, query_str, fragment)
    return urlunparse(components)


def query_from_url(url: str) -> dict:
    """
    Extract the query part, if any, from the given URL string.

    :param url: the URL.
    :return: the query string as a dictionary. The dictionary will be empty
        if the URL has no query component or all query params have no value.
    """
    parsed = urlparse(url)
    qs = parse_qs(parsed.query)
    return _prune_query_params(qs)


def query_param(url: str, name: str, separator: str = '') -> Optional[str]:
    """
    Extract the named query parameter's value if present in the given URL.
    If more than one instance of the named parameter is in the URL, their
    values get joined using ``separator``.

    :param url: the URL.
    :param name: the parameter name.
    :param separator: used to join values if there's more than one; defaults
        to the empty string.
    :return: the parameter value if present or ``None`` otherwise.
    """
    ps = query_from_url(url).get(name)  # each parsed query param is an array
    return separator.join(ps) if ps else None


def abspath(*components):
    """
    Joins the given components to form an absolute path.
    Each component gets converted to a string and escaped as needed.

    :param components: the path components in the order in which to join them.
    :return: the joined path.
    """
    cs = [quote(str(c)) for c in components]
    p = '/' + '/'.join(cs)
    return re.sub(r'[/]+', '/', p)
