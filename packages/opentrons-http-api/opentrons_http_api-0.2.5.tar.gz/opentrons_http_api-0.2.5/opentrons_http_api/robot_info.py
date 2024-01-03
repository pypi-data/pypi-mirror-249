from __future__ import annotations
from abc import ABC
from dataclasses import dataclass
from typing import List, Dict


class _Info(ABC):
    def __init__(self, args, kwargs):
        pass

    @classmethod
    def from_dict(cls, d: dict) -> _Info:
        return cls(**d)


@dataclass(frozen=True)
class SettingsInfo(_Info):
    id: str
    old_id: str
    title: str
    description: str
    restart_required: bool
    value: bool


@dataclass(frozen=True)
class RobotSettingsInfo(_Info):
    model: str
    name: str
    version: int
    gantry_steps_per_mm: Dict
    acceleration: Dict
    serial_speed: int
    default_pipette_configs: Dict
    default_current: Dict
    low_current: Dict
    high_current: Dict
    default_max_speed: Dict
    log_level: str
    z_retract_distance: int
    left_mount_offset: List[int]


@dataclass(frozen=True)
class HealthInfo(_Info):
    name: str
    robot_model: str
    api_version: str
    fw_version: str
    board_revision: str
    logs: List[str]
    system_version: str
    maximum_protocol_api_version: List[int]
    minimum_protocol_api_version: List[int]
    robot_serial: str
    links: Dict[str, str]


@dataclass(frozen=True)
class RunInfo(_Info):
    id: str
    createdAt: str
    status: str
    current: bool
    actions: List[dict]
    errors: List[dict]
    pipettes: List[dict]
    modules: List[dict]
    labware: List[dict]
    liquids: List[dict]
    labwareOffsets: List[dict]
    protocolId: str


@dataclass(frozen=True)
class ProtocolInfo(_Info):
    id: str
    createdAt: str
    files: List[Dict]
    protocolType: str
    robotType: str
    metadata: Dict
    analyses: List
    analysisSummaries: List[Dict]
