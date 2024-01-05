from __future__ import annotations
from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class SettingsInfo:
    id: str
    old_id: str
    title: str
    description: str
    restart_required: bool
    value: bool


@dataclass(frozen=True)
class RobotSettingsInfo:
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
class HealthInfo:
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
class RunInfo:
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


@dataclass(frozen=True)
class ProtocolInfo:
    id: str
    createdAt: str
    files: list[dict]
    protocolType: str
    robotType: str
    metadata: dict
    analyses: list
    analysisSummaries: list[dict]
