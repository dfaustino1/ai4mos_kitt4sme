"""
Eats NGSI entities for breakfast.

Endpoint to process machine entity updates from Orion.

"""

from roughnator.ai import estimate
import roughnator.log as log
from roughnator.ngsy import MachineEntity, RoughnessEstimateEntity
from roughnator.util.ngsi.headers import FiwareContext


def process_update(ctx: FiwareContext, ms: [MachineEntity]):
    log.going_to_process_updates(ctx, ms)

    estimates = [estimate(m) for m in ms]
    update_context(ctx, estimates)


def update_context(ctx: FiwareContext, estimates: [RoughnessEstimateEntity]):
    log.going_to_update_context_with_estimates(ctx, estimates)

    # TODO write back to Orion
