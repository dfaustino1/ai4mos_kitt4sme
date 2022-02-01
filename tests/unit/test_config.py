import contextlib
import os

from roughnator.config import *


# ripped from: https://stackoverflow.com/questions/2059482
@contextlib.contextmanager
def env(**environ):
    old_environ = dict(os.environ)
    os.environ.update(environ)
    try:
        yield
    finally:
        os.environ.clear()
        os.environ.update(old_environ)


def test_no_orion_base_url():
    with env():
        assert URI() == orion_base_url()


def test_http_orion_base_url():
    url = 'http://orion:1026'
    want = URI(url)
    with env(**{ ORION_BASE_URL_VAR.name: url }):
        assert want == orion_base_url()
