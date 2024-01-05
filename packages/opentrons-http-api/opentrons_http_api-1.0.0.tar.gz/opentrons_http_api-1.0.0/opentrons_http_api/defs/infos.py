from __future__ import annotations
from dataclasses import dataclass
from typing import List, Dict, Optional


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
class HealthInfo:
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
class RunInfo:
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
    completedAt: Optional[str] = None
    startedAt: Optional[str] = None


@dataclass(frozen=True)
class ProtocolInfo:
    id: str
    createdAt: str
    files: List[Dict]
    protocolType: str
    robotType: str
    metadata: Dict
    analyses: List
    analysisSummaries: List[Dict]
