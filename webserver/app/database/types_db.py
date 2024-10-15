from dataclasses import dataclass
from typing import Tuple
import json

@dataclass(frozen=True)
class ImgObject:
    user: str
    object_name: str
    p1: Tuple[float]
    p2: Tuple[float]
    img_url: str

    def to_dict(self):
        return vars(self)
    
    # TODO remove?
    # def to_json(self):
    #     return json.dumps(
    #         self,
    #         default=lambda o: o.__dict__, 
    #         sort_keys=True,
    #         indent=4)