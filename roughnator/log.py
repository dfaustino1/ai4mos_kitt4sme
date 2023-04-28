from fipy.ngsi.entity import EntityUpdateNotification
from fipy.ngsi.headers import FiwareContext
import logging
from typing import Any, List
from roughnator.ngsy import Productions, Schedule


def _logger() -> logging.Logger:
    return logging.getLogger(__name__)


def _format_mgs(lines: List[Any]) -> str:
    ls = [f"{line}\n" for line in lines]
    return ''.join(ls)


def info(msg: str):
    # _logger().info(msg)
    # TODO. ^ not printing anything to stdout. Figure out why.
    # Have a look at:
    # - uvicorn.main, uvicorn.config.LOGGING_CONFIG
    # - https://github.com/tiangolo/uvicorn-gunicorn-fastapi-docker/issues/19
    # - https://nuculabs.dev/2021/05/18/fastapi-uvicorn-logging-in-production/
    # - https://stackoverflow.com/questions/66602480

    print(msg)


def received_ngsi_entity_update(ctx: FiwareContext,
                                notification: EntityUpdateNotification):
    header = f"got entity updates for {ctx}:"
    msg = _format_mgs([header] + notification.data)
    info(msg)
    

def going_to_process_updates(ctx: FiwareContext, ms: List[Productions]):
    header = f"going to process updates for {ctx}:"
    msg = _format_mgs([header] + ms)
    info(msg)


def going_to_update_context_with_estimates(ctx: FiwareContext,
                                           rs: List[Schedule]):
    header = f"going to update context ({ctx}) with estimates:"
    msg = _format_mgs([header] + rs)
    info(msg)
