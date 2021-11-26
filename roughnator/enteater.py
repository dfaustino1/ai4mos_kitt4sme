"""
Eats NGSI entities for breakfast.

Endpoint to process machine entity updates from Orion.

"""

from roughnator.ai import estimate
from roughnator.ngsy import MachineEntity, RoughnessEstimateEntity


def process_update(ms: [MachineEntity]):
    for m in ms:
        print(m)

    estimates = [estimate(m) for m in ms]
    update_context(estimates)


def update_context(estimates: [RoughnessEstimateEntity]):
    pass
    # TODO write back to Orion
