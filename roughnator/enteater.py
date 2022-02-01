"""
Eats NGSI entities for breakfast.

Endpoint to process machine entity updates from Orion.

"""

from fipy.ngsi.headers import FiwareContext
from fipy.ngsi.orion import OrionClient
from typing import List

from roughnator.ai import estimate
import roughnator.config as config
import roughnator.log as log
from roughnator.ngsy import MachineEntity, RoughnessEstimateEntity



def process_update(ctx: FiwareContext, ms: List[MachineEntity]):
    log.going_to_process_updates(ctx, ms)

    estimates = [estimate(m) for m in ms]
    update_context(ctx, estimates)


def update_context(ctx: FiwareContext,
                   estimates: List[RoughnessEstimateEntity]):
    log.going_to_update_context_with_estimates(ctx, estimates)

    orion = OrionClient(config.orion_base_url(), ctx)
    orion.upsert_entities(estimates)
