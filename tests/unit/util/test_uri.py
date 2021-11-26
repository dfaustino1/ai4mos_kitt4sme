import pytest

from roughnator.util.uri import *


@pytest.mark.parametrize('components, expected', [
    ({'scheme': 'http', 'netloc': 'h', 'path': '/'}, 'http://h/'),
    ({'scheme': 'http', 'netloc': 'h', 'path': '/',
      'query': {'p': 1, 'q': ''}}, 'http://h/?p=1'),
    ({'scheme': 'http', 'netloc': 'h', 'path': '/',
      'query': {'p': 1, 'q': 'x@y'}}, 'http://h/?p=1&q=x%40y'),
    ({'scheme': 'http', 'netloc': 'h', 'path': '/',
      'query': {'p': 1, 'q': []}}, 'http://h/?p=1'),
    ({'scheme': 'http', 'netloc': 'h', 'path': '/',
      'query': {'p': 1, 'q': [2]}}, 'http://h/?p=1&q=2'),
    ({'scheme': 'http', 'netloc': 'h', 'path': '/',
      'query': {'p': 1, 'q': [2, 'x@y']}}, 'http://h/?p=1&q=2+x%40y'),
    ({'scheme': 'http', 'netloc': 'h', 'path': '/',
      'query': {'p': 1, 'q': ()}}, 'http://h/?p=1'),
    ({'scheme': 'http', 'netloc': 'h', 'path': '/',
      'query': {'p': 1, 'q': (2,)}}, 'http://h/?p=1&q=2'),
    ({'scheme': 'http', 'netloc': 'h', 'path': '/',
      'query': {'p': 1, 'q': (2, 'x@y')}}, 'http://h/?p=1&q=2+x%40y'),
    ({'scheme': 'http', 'netloc': 'h:8080', 'path': '/', 'params': ''},
     'http://h:8080/'),
    ({'scheme': 'http', 'netloc': 'h:8080', 'path': '/', 'params': 'p'},
     'http://h:8080/;p'),
    ({'scheme': 'http', 'netloc': 'h:8080', 'path': '/', 'fragment': ''},
     'http://h:8080/'),
    ({'scheme': 'http', 'netloc': 'h:8080', 'path': '/', 'fragment': 'f'},
     'http://h:8080/#f')
])
def test_url_str(components, expected):
    assert url_str(**components) == expected


@pytest.mark.parametrize('url, expected', [
    ('http://h', {}), ('http://h/', {}), ('http://h?q', {}),
    ('http://h?q=', {}), ('http://h?q=&p', {}), ('http://h?q=&p=', {}),
    ('http://h?q=&p=1', {'p': ['1']}),
    ('http://h?q=&p=1&p', {'p': ['1']}),
    ('http://h?q=&p=1&p=', {'p': ['1']}),
    ('http://h?q=&p=1&p=2', {'p': ['1', '2']}),
    ('http://h?q=3&p=1&p=2', {'p': ['1', '2'], 'q': ['3']})
])
def test_query_from_url(url, expected):
    assert query_from_url(url) == expected


@pytest.mark.parametrize('url, separator, expected', [
    ('', '', None), ('', ',', None),
    ('http://a/', '', None), ('http://a/', ',', None),
    ('http://a/?q', '', None), ('http://a/?q=', '', None),
    ('http://a/?q', ',', None), ('http://a/?q=', ',', None),
    ('http://a/?p=1&q', '', None), ('http://a/?p=1&q=', '', None),
    ('http://a/?p=1&q', ',', None), ('http://a/?p=1&q=', ',', None),
    ('http://a/?p=1&q=+', '', ' '), ('http://a/?q=+', '', ' '),
    ('http://a/?p=1&q=+', ',', ' '), ('http://a/?q=+', ',', ' '),
    ('http://a/?p=1&q=+x', '', ' x'), ('http://a/?q=+x', '', ' x'),
    ('http://a/?p=1&q=+x', ',', ' x'), ('http://a/?q=+x', ',', ' x'),
    ('http://a/?p=1&q=+x', ',', ' x'), ('http://a/?q=x+y', ',', 'x y'),
    ('http://a/?q=y&p=1&q=x', '', 'yx'), ('http://a/?q=x&q=y', '', 'xy'),
    ('http://a/?q=y&p=1&q=x', ',', 'y,x'), ('http://a/?q=x&q=y', ',', 'x,y')
])
def test_query_param(url, separator, expected):
    assert query_param(url, 'q', separator) == expected


@pytest.mark.parametrize('components, expected', [
    ((), '/'),
    ((1,), '/1'), ((1, '/'), '/1/'),
    ((1, 2), '/1/2'), ((1, 2, '/'), '/1/2/'),
    (('/a/b@c/d', '/e'), '/a/b%40c/d/e'),
    (('/a/b@c/d', '/e/'), '/a/b%40c/d/e/'),
    (('a////b',), '/a/b'), (('a////b', 'c/', '/'), '/a/b/c/')
])
def test_abspath(components, expected):
    assert abspath(*components) == expected
