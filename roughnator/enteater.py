"""
Eats NGSI entities for breakfast.

Endpoint to process machine entity updates from Orion.

"""

from roughnator.ai import estimate
from roughnator.ngsy import MachineEntity, RoughnessEstimateEntity
from roughnator.util.ngsi.headers import FiwareContext


def process_update(ctx: FiwareContext, ms: [MachineEntity]):
    for m in ms:  # TODO zap
        print(m)

    estimates = [estimate(m) for m in ms]
    update_context(ctx, estimates)


def update_context(ctx: FiwareContext, estimates: [RoughnessEstimateEntity]):
    print(ctx)  # TODO zap
    for e in estimates:  # TODO zap
        print(e)
    # TODO write back to Orion
