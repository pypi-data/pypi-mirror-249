"""Test entity"""
from dataclasses import dataclass
from typing import Dict, List


@dataclass
class TestEntity:
    """Test entity"""

    id: str
    name: str
    model_key: str
    dataset_id: str
    test_type: str
    attacks: List[Dict]
    config: List[Dict]
