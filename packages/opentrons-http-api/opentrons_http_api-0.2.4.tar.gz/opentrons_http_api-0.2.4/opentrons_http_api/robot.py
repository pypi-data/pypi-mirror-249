from __future__ import annotations
from typing import Tuple, BinaryIO, Optional, Sequence

from opentrons_http_api.api import API, SettingId, Action
from opentrons_http_api.robot_info import SettingsInfo, RobotSettingsInfo, HealthInfo, RunInfo, ProtocolInfo


class Robot:
    """
    A friendlier interface for the Opentrons HTTP API.
    """
    def __init__(self, host: str = 'localhost'):
        self._api = API(host)

    def identify(self, seconds: int) -> None:
        self._api.post_identify(seconds)

    def lights(self) -> bool:
        return self._api.get_robot_lights()['on']

    def set_lights(self, on: bool) -> None:
        self._api.post_robot_lights(on)

    def settings(self) -> Tuple[SettingsInfo, ...]:
        d = self._api.get_settings()
        return tuple(SettingsInfo.from_dict(setting)
                     for setting in d['settings'])

    def set_setting(self, id_: SettingId, value: bool) -> None:
        self._api.post_settings(id_.value, value)

    def robot_settings(self) -> RobotSettingsInfo:
        d = self._api.get_robot_settings()
        return RobotSettingsInfo.from_dict(d)

    def health(self) -> HealthInfo:
        info = self._api.get_health()
        return HealthInfo.from_dict(info)

    def create_run(self, protocol_id: str, labware_offsets: Optional[Sequence[dict]] = None) -> RunInfo:
        d = self._api.post_runs(protocol_id, labware_offsets)
        return RunInfo.from_dict(d['data'])

    def action_run(self, run_id: str, action: Action) -> None:
        self._api.post_runs_run_id_actions(run_id, action)

    def upload_protocol(self, protocol_file: BinaryIO,
                        labware_definitions: Optional[Sequence[BinaryIO]] = None) -> ProtocolInfo:
        """
        Upload a protocol with optional labware definitions to the robot.
        :param protocol_file: A Python or JSON protocol binary file object.
        :param labware_definitions: An optional sequence of JSON labware definition binary file objects, only if the
        protocol_file is in Python format.
        :return: ProtocolInfo object containing information about the protocol.
        """
        d = self._api.post_protocols(protocol_file, labware_definitions)
        return ProtocolInfo.from_dict(d['data'])
