from fipy.ngsi.orion import OrionClient
from fipy.ngsi.quantumleap import QuantumLeapClient
from fipy.wait import wait_until

from tests.util.fiware import SubMan
from tests.util.sampler import MachineSampler


MACHINE_N = 2
SAMPLES_PER_MACHINE = 3
ESTIMATE_ENTITY_TYPE = 'RoughnessEstimate'
ROUGHNESS_ATTR_NAME = 'roughness'


def upload_machine_entities(orion: OrionClient):
    sampler = MachineSampler(pool_size=MACHINE_N, orion=orion)
    sampler.sample(samples_n=SAMPLES_PER_MACHINE, sampling_rate=1.5)


def has_time_series(quantumleap: QuantumLeapClient) -> bool:
    size = quantumleap.count_data_points(ESTIMATE_ENTITY_TYPE,
                                         ROUGHNESS_ATTR_NAME)
    return size > (SAMPLES_PER_MACHINE * MACHINE_N) / 2  # (*)
# NOTE. Orion missed notifications. If things happen too fast, Orion might
# not notify QL of all RoughnessEstimate entities it got from Roughnator.
# If memory serves, by default, if Orion gets multiple updates for the
# same entity within one second, it'll only notify subscribers of the
# latest update.


def test_roughness_series(orion: OrionClient, quantumleap: QuantumLeapClient):
    SubMan().create_subscriptions()
    upload_machine_entities(orion)
    wait_until(lambda: has_time_series(quantumleap))
