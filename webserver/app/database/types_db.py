from dataclasses import dataclass
from typing import Tuple
import json

from datetime import datetime

@dataclass(frozen=True)
class ImgObject:
    user: str
    object_name: str
    p1: Tuple[float]
    p2: Tuple[float]
    img_url: str
    created_at: datetime

    def to_dict(self):
        return vars(self)
    
    # TODO remove?
    # def to_json(self):
    #     return json.dumps(
    #         self,
    #         default=lambda o: o.__dict__, 
    #         sort_keys=True,
    #         indent=4)


@dataclass(frozen=True)
class ImgObjectQuery:
    user: str
    object_name: str
    # TODO: can potentially filter using this 
    # created_at: datetime

    def to_dict(self):
        return vars(self)
    