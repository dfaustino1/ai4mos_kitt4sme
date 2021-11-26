"""
Estimates likely roughness and acceleration.
"""

from roughnator.ngsy import FloatAttr, MachineEntity, RoughnessEstimateEntity
import joblib


ROUGHNESS_MODEL_PATH_FROM_ROOT = 'data/roughness.model.pkl'


def estimate(machine: MachineEntity) -> RoughnessEstimateEntity:
    a = estimate_acceleration(machine)
    r = estimate_roughness(machine)

    return RoughnessEstimateEntity(id=machine.id,
                                   acceleration=FloatAttr.from_value(a),
                                   roughness=FloatAttr.from_value(r))
    # TODO what should the ID be? ideally there should be a bijection b/w
    # machine IDs and estimate IDs...


def estimate_roughness(machine: MachineEntity) -> float:
    xin = [machine.AcelR.value, machine.fz.value, machine.Diam.value,
           machine.ae.value, machine.HB.value, machine.geom.value]
    model = joblib.load(ROUGHNESS_MODEL_PATH_FROM_ROOT)
    return model.predict([xin])


def estimate_acceleration(machine: MachineEntity) -> float:
    return machine.AcelR.value
