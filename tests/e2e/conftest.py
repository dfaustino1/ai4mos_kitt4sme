from fipy.docker import DockerCompose
from fipy.ngsi.orion import OrionClient
from fipy.ngsi.quantumleap import QuantumLeapClient
import pytest

from tests.util.fiware import orion_client, quantumleap_client, \
    wait_on_orion, wait_on_quantumleap


docker = DockerCompose(__file__)


@pytest.fixture(scope='session', autouse=True)
def build_images():
    docker.build_images()


@pytest.fixture(scope='package', autouse=True)
def run_services():
    docker.start()
    wait_on_orion()
    wait_on_quantumleap()
    yield
    docker.stop()


@pytest.fixture(scope="module")
def orion() -> OrionClient:
    return orion_client()


@pytest.fixture(scope="module")
def quantumleap() -> QuantumLeapClient:
    return quantumleap_client()
