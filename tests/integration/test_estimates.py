from roughnator.ngsy import MachineEntity, RoughnessEstimateEntity
from roughnator.util.ngsi.entity import FloatAttr
from roughnator.util.ngsi.orion import OrionClient
from tests.util.fiware import SubMan
from tests.util.sampler import MachineSampler
from tests.util.wait import wait_until


def upload_machine_entities(orion: OrionClient) -> [MachineEntity]:
    sampler = MachineSampler(machines_n=2, orion=orion)
    machine1 = sampler.send_machine_readings(1)
    machine2 = sampler.send_machine_readings(2)

    return [machine1, machine2]


def list_estimate_entities(orion: OrionClient) -> [RoughnessEstimateEntity]:
    like = RoughnessEstimateEntity(id='',
                                   acceleration=FloatAttr.new(1),
                                   roughness=FloatAttr.new(1))
    es = orion.list_entities_of_type(like)

    sorted_estimates = sorted(es, key=lambda e: e.id)
    return sorted_estimates


def has_estimate_entities(orion: OrionClient) -> bool:
    es = list_estimate_entities(orion)
    return len(es) > 0


def test_estimates(orion: OrionClient):
    SubMan().create_roughnator_sub()
    sorted_machines = upload_machine_entities(orion)

    wait_until(lambda: has_estimate_entities(orion))

    sorted_estimates = list_estimate_entities(orion)

    assert len(sorted_machines) == len(sorted_estimates)
    for i in range(len(sorted_machines)):
        assert sorted_machines[i].id == sorted_estimates[i].id
