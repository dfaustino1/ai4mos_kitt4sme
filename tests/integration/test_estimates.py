from roughnator.ngsy import MachineEntity, RoughnessEstimateEntity
from roughnator.util.ngsi.entity import FloatAttr
from roughnator.util.ngsi.orion import OrionClient
from tests.integration.conftest import ROUGHNATOR_HOST, wait_for


SUB = {
    "description": "Notify Roughnator of changes to any entity.",
    "subject": {
        "entities": [
            {
                "idPattern": ".*"
            }
        ]
    },
    "notification": {
        "http": {
            "url": f"http://{ROUGHNATOR_HOST}:8000/updates"
        }
    }
}


def create_roughnator_sub(orion: OrionClient):
    orion.subscribe(SUB)


def machine_entity(nid: int) -> MachineEntity:
    m = MachineEntity(id='', AcelR=FloatAttr.new(1.0335),
                      fz=FloatAttr.new(0.98201), Diam=FloatAttr.new(0.98201),
                      ae=FloatAttr.new(1.0335), HB=FloatAttr.new(145),
                      geom=FloatAttr.new(-0.021), Ra=FloatAttr.new(0.1))
    m.set_id_with_type_prefix(f"{nid}")
    return m


def upload_machine_entities(orion: OrionClient) -> [MachineEntity]:
    machine1 = machine_entity(1)
    machine1.AcelR = FloatAttr.new(1.0)
    orion.upsert_entity(machine1)

    machine2 = machine_entity(2)
    machine2.AcelR = FloatAttr.new(2.0)
    orion.upsert_entity(machine2)

    machine2.AcelR = FloatAttr.new(3.0)
    orion.upsert_entity(machine2)

    return [machine1, machine2]


def list_estimate_entities(orion: OrionClient) -> [RoughnessEstimateEntity]:
    like = RoughnessEstimateEntity(id='',
                                   acceleration=FloatAttr.new(1),
                                   roughness=FloatAttr.new(1))
    es = orion.list_entities_of_type(like)
    assert len(es) > 0

    sorted_estimates = sorted(es, key=lambda e: e.id)
    return sorted_estimates


def test_estimates(orion: OrionClient):
    create_roughnator_sub(orion)
    sorted_machines = upload_machine_entities(orion)

    wait_for(lambda: list_estimate_entities(orion))
    sorted_estimates = list_estimate_entities(orion)

    assert len(sorted_machines) == len(sorted_estimates)
    for i in range(len(sorted_machines)):
        assert sorted_machines[i].id == sorted_estimates[i].id
