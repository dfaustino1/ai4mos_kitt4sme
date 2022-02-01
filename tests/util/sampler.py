from fipy.ngsi.entity import FloatAttr
from fipy.ngsi.orion import OrionClient
from fipy.sim.sampler import DevicePoolSampler
import random
from typing import Optional

from roughnator.ngsy import MachineEntity
from tests.util.fiware import orion_client


class MachineSampler(DevicePoolSampler):

    def __init__(self, pool_size: int, orion: Optional[OrionClient] = None):
        super().__init__(pool_size, orion if orion else orion_client())

    def new_device_entity(self) -> MachineEntity:
        seed = random.uniform(0, 1)
        return MachineEntity(
            id='',
            AcelR=FloatAttr.new(1.0335 + seed),
            fz=FloatAttr.new(0.98201 + seed),
            Diam=FloatAttr.new(0.98201 + seed),
            ae=FloatAttr.new(1.0335 + seed),
            HB=FloatAttr.new(145 + seed),
            geom=FloatAttr.new(-0.021 + seed),
            Ra=FloatAttr.new(seed)
        )
