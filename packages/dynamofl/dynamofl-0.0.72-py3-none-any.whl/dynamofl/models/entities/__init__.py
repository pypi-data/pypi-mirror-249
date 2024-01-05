"""DynamoFL Model"""
from dataclasses import dataclass


@dataclass
class BaseModel:
    """Base Model Data class"""

    id: str
    key: str
    name: str
    config: object


@dataclass
class RemoteModel(BaseModel):
    """Remote Model Data class"""

    type: str = "REMOTE"


@dataclass
class LocalModel(BaseModel):
    """Local Model Data class"""

    size: int
    type: str = "LOCAL"
