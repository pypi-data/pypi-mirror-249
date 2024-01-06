"""
Dataclasses for easier creation and handling of data usually represented by a dict. Some classes with nested dicts also
provide a property representing the nested dict as a class, with a trailing underscore following its name.
"""

from __future__ import annotations
from dataclasses import dataclass, asdict
from typing import Optional


@dataclass(frozen=True)
class _DictData:
    def dict(self) -> dict:
        return asdict(self)


@dataclass(frozen=True)
class Vector(_DictData):
    x: float
    y: float
    z: float


@dataclass(frozen=True)
class LabwareOffset(_DictData):
    # Leave empty when posting
    id: str
    createdAt: str

    definitionUri: str
    location: dict[str, str]
    vector: dict[str, float]

    @property
    def vector_(self) -> Vector:
        return Vector(**self.vector)


@dataclass(frozen=True)
class Setting(_DictData):
    id: str
    old_id: str
    title: str
    description: str
    restart_required: bool
    value: bool


@dataclass(frozen=True)
class RobotSettings(_DictData):
    model: str
    name: str
    version: int
    gantry_steps_per_mm: dict
    acceleration: dict
    serial_speed: int
    default_pipette_configs: dict
    default_current: dict
    low_current: dict
    high_current: dict
    default_max_speed: dict
    log_level: str
    z_retract_distance: int
    left_mount_offset: list[int]


@dataclass(frozen=True)
class HealthInfo(_DictData):
    name: str
    robot_model: str
    api_version: str
    fw_version: str
    board_revision: str
    logs: list[str]
    system_version: str
    maximum_protocol_api_version: list[int]
    minimum_protocol_api_version: list[int]
    robot_serial: str
    links: dict[str, str]


@dataclass(frozen=True)
class RunInfo(_DictData):
    id: str
    createdAt: str
    status: str
    current: bool
    actions: list[dict]
    errors: list[dict]
    pipettes: list[dict]
    modules: list[dict]
    labware: list[dict]
    liquids: list[dict]
    labwareOffsets: list[dict]
    protocolId: str
    completedAt: Optional[str] = None
    startedAt: Optional[str] = None

    @property
    def labwareOffsets_(self) -> list[LabwareOffset]:
        return [LabwareOffset(**offset)
                for offset in self.labwareOffsets]


@dataclass(frozen=True)
class ProtocolInfo(_DictData):
    id: str
    createdAt: str
    files: list[dict]
    protocolType: str
    robotType: str
    metadata: dict
    analyses: list
    analysisSummaries: list[dict]
