"""
Estimates likely roughness and acceleration.
"""

from fipy.ngsi.entity import FloatAttr
import joblib

from roughnator.ngsy import MachineEntity, RoughnessEstimateEntity


ROUGHNESS_MODEL_PATH_FROM_ROOT = 'data/roughness.model.pkl'


def estimate(machine: MachineEntity) -> RoughnessEstimateEntity:
    a = estimate_acceleration(machine)
    r = estimate_roughness(machine)

    return RoughnessEstimateEntity(id=machine.id,
                                   acceleration=FloatAttr.new(a),
                                   roughness=FloatAttr.new(r))
    # TODO what should the ID be? ideally there should be a bijection b/w
    # machine IDs and estimate IDs...


def estimate_roughness(machine: MachineEntity) -> float:
    xin = [machine.AcelR.value, machine.fz.value, machine.Diam.value,
           machine.ae.value, machine.HB.value, machine.geom.value]
    model = joblib.load(ROUGHNESS_MODEL_PATH_FROM_ROOT)
    return model.predict([xin])


def estimate_acceleration(machine: MachineEntity) -> float:
    return machine.AcelR.value
