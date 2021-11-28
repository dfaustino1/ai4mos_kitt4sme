import random
import time

from roughnator.ngsy import MachineEntity
from roughnator.util.ngsi.entity import FloatAttr
from roughnator.util.ngsi.orion import OrionClient
from tests.util.fiware import orion_client


class MachineSampler:

    def __init__(self, machines_n: int, orion: OrionClient = None):
        self._machines_n = machines_n
        self._orion = orion if orion else orion_client()

    def _ensure_nid_bounds(self, nid: int):
        assert 0 < nid <= self._machines_n

    def new_machine_entity(self, nid: int) -> MachineEntity:
        self._ensure_nid_bounds(nid)

        seed = random.uniform(0, 1)
        m = MachineEntity(id='',
                          AcelR=FloatAttr.new(1.0335 + seed),
                          fz=FloatAttr.new(0.98201 + seed),
                          Diam=FloatAttr.new(0.98201 + seed),
                          ae=FloatAttr.new(1.0335 + seed),
                          HB=FloatAttr.new(145 + seed),
                          geom=FloatAttr.new(-0.021 + seed),
                          Ra=FloatAttr.new(seed))
        m.set_id_with_type_prefix(f"{nid}")

        return m

    def entity_id(self, nid: int) -> str:
        return self.new_machine_entity(nid).id

    def send_machine_readings(self, nid: int) -> MachineEntity:
        machine = self.new_machine_entity(nid)
        self._orion.upsert_entity(machine)
        return machine

    def sample(self, samples_n: int, sampling_rate: float):
        for _ in range(samples_n):
            ms = [self.new_machine_entity(nid)
                  for nid in range(1, self._machines_n + 1)]
            self._orion.upsert_entities(ms)

            time.sleep(sampling_rate)
