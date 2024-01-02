import typing as t
from meili_sdk.models.base import BaseModel

__all__ = ("UpdateMapMessage","YamlFile")

class YamlFile(BaseModel):
    resolution: float
    mode: str
    origin: t.List
    negate: int
    occupied_thresh: float
    free_thresh: float

class UpdateMapMessage(BaseModel):
    displayable_image: str
    yaml_file: YamlFile




