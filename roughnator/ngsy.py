from fipy.ngsi.entity import BaseEntity, StructuredValueAttr
from pydantic import BaseModel
from typing import Optional


class Productions(BaseEntity):
    type = 'Productions'
    productions: Optional[StructuredValueAttr]
    

class Schedule(BaseEntity):
    type = 'Schedule'
    schedule: StructuredValueAttr
    