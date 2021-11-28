import pytest
from time import sleep
from uri import URI

from roughnator.util.ngsi.headers import FiwareContext
from roughnator.util.ngsi.orion import OrionClient
from tests.util.docker import DockerCompose


TENANT = 'csic'
ROUGHNATOR_HOST = 'roughnator'

docker = DockerCompose(__file__)


def orion_client() -> OrionClient:
    base_url = URI(f"http://localhost:1026")
    ctx = FiwareContext(service=TENANT)
    return OrionClient(base_url, ctx)


def wait_for(action, max_wait: float = 10.0, sleep_interval: float = 0.5):
    time_left_to_wait = max_wait
    while time_left_to_wait > 0:
        try:
            action()
            return
        except BaseException as e:
            print(e)
            time_left_to_wait -= sleep_interval
            sleep(sleep_interval)
    assert False, f"waited longer than {max_wait} secs for {action}!"


def wait_for_orion(max_wait: float = 10.0, sleep_interval: float = 0.5):
    client = orion_client()
    wait_for(lambda: client.list_entities(), max_wait, sleep_interval)


@pytest.fixture(scope='session', autouse=True)
def build_images():
    docker.build_images()


@pytest.fixture(scope='package', autouse=True)
def run_services():
    docker.start()
    wait_for_orion()
    yield
    docker.stop()


@pytest.fixture(scope="module")
def orion() -> OrionClient:
    return orion_client()
