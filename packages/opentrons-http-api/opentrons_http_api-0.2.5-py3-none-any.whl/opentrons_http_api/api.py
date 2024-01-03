from typing import Sequence, BinaryIO, Dict, Optional
import urllib
from enum import Enum

import requests

from opentrons_http_api.paths import Paths


class SettingId(str, Enum):
    SHORT_FIXED_TRASH = 'shortFixedTrash'
    DECK_CALIBRATION_DOTS = 'deckCalibrationDots'
    DISABLE_HOME_ON_BOOT = 'disableHomeOnBoot'
    USE_OLD_ASPIRATION_FUNCTIONS = 'useOldAspirationFunctions'
    ENABLE_DOOR_SAFETY_SWITCH = 'enableDoorSafetySwitch'
    DISABLE_FAST_PROTOCOL_UPLOAD = 'disableFastProtocolUpload'


class Axis(str, Enum):
    X = 'x'
    Y = 'y'
    Z_L = 'z_l'
    Z_R = 'z_r'
    Z_G = 'z_g'
    P_L = 'p_l'
    P_R = 'p_r'
    Q = 'q'
    G = 'g'
    Z = 'z'
    A = 'a'
    B = 'b'
    C = 'c'


class Action(str, Enum):
    PLAY = 'play'
    PAUSE = 'pause'
    STOP = 'stop'


class API:
    """
    Basic Python client for Opentrons HTTP API.

    Use the Robot class for a friendlier interface.
    """
    _HEADERS = {'Opentrons-Version': '3'}
    _PORT = 31950
    _BASE = 'http://{host}:{port}'

    def __init__(self, host: str = 'localhost'):
        self._base = self._BASE.format(host=host, port=self._PORT)

    def _url(self, path):
        return urllib.parse.urljoin(self._base, path)

    @staticmethod
    def _check_response(response: requests.Response):
        response.raise_for_status()

    def _get(self, path: str) -> Dict:
        """
        :param path: Path to call (not the full URL).
        :return: The response as a dictionary.
        """
        response = requests.get(self._url(path), headers=self._HEADERS)
        self._check_response(response)
        return response.json()

    def _post(self, path: str, query: Optional[Dict] = None, body: Optional[Dict] = None, **kwargs) -> Dict:
        """
        :param path: Path to call (not the full URL).
        :param query: Parameters to use as a query.
        :param body: A JSON serializable Python object to send in the body of the request.
        :param kwargs: Any specific kwargs to send, e.g. "files".
        :return: The response as a dictionary.
        """
        response = requests.post(self._url(path), headers=self._HEADERS, params=query, json=body, **kwargs)
        self._check_response(response)
        return response.json()

    # v1

    # NETWORKING

    # CONTROL

    def post_identify(self, seconds: int) -> Dict:
        """
        Blink the OT-2's gantry lights so you can pick it out of a crowd.
        """
        query = {'seconds': seconds}
        return self._post(Paths.IDENTIFY, query=query)

    def get_robot_lights(self) -> Dict:
        """
        Get the current status of the OT-2's rail lights.
        """
        return self._get(Paths.ROBOT_LIGHTS)

    def post_robot_lights(self, on: bool) -> Dict:
        """
        Turn the rail lights on or off.
        """
        body = {'on': on}
        return self._post(Paths.ROBOT_LIGHTS, body=body)

    # SETTINGS

    def get_settings(self) -> Dict:
        """
        Get a list of available advanced settings (feature flags) and their values.
        """
        return self._get(Paths.SETTINGS)

    def post_settings(self, id_: SettingId, value: bool) -> Dict:
        """
        Change an advanced setting (feature flag).
        """
        body = {'id': id_, 'value': value}
        return self._post(Paths.SETTINGS, body=body)

    def get_robot_settings(self) -> Dict:
        """
        Get the current robot config.
        """
        return self._get(Paths.SETTINGS_ROBOT)

    # DECK CALIBRATION

    def get_calibration_status(self) -> Dict:
        """
        Get the calibration status.
        """
        return self._get(Paths.CALIBRATION_STATUS)

    # MODULES

    # PIPETTES

    # MOTORS

    def get_motors_engaged(self) -> Dict:
        """
        Query which motors are engaged and holding.
        """
        return self._get(Paths.MOTORS_ENGAGED)

    def post_motors_disengage(self, axes: Sequence[Axis]) -> Dict:
        """
        Disengage a motor or set of motors.
        """
        body = {'axes': axes}
        return self._post(Paths.MOTORS_DISENGAGE, body=body)

    # CAMERA

    # LOGS

    # HEALTH

    def get_health(self) -> Dict:
        """
        Get information about the health of the robot server.

        Use the health endpoint to check that the robot server is running and ready to operate. A 200 OK response means
        the server is running. The response includes information about the software and system.
        """
        return self._get(Paths.HEALTH)

    # RUN MANAGEMENT

    def get_runs(self) -> Dict:
        """
        Get a list of all active and inactive runs.
        """
        return self._get(Paths.RUNS)

    def post_runs(self, protocol_id: str, labware_offsets: Optional[Sequence[dict]] = None) -> Dict:
        """
        Create a new run to track robot interaction.

        When too many runs already exist, old ones will be automatically deleted to make room for the new one.
        """
        if labware_offsets is None:
            labware_offsets = []

        body = {
            'data': {
                'protocolId': protocol_id,
                'labwareOffsets': labware_offsets,
            }
        }
        return self._post(Paths.RUNS, body=body)

    def get_runs_run_id(self, run_id: str) -> Dict:
        """
        Get a specific run by its unique identifier.
        """
        path = Paths.RUNS_RUN_ID.format(run_id=run_id)
        return self._get(path)

    def get_runs_run_id_commands(self, run_id: str) -> Dict:
        """
        Get a list of all commands in the run and their statuses. This endpoint returns command summaries. Use GET
        /runs/{runId}/commands/{commandId} to get all information available for a given command.
        """
        path = Paths.RUNS_RUN_ID_COMMANDS.format(run_id=run_id)
        return self._get(path)

    def get_runs_run_id_commands_command_id(self, run_id: str, command_id: str) -> Dict:
        """
        Get a command along with any associated payload, result, and execution information.
        """
        path = Paths.RUNS_RUN_ID_COMMANDS_COMMAND_ID.format(run_id=run_id, command_id=command_id)
        return self._get(path)

    def post_runs_run_id_actions(self, run_id: str, action: Action) -> Dict:
        """
        Provide an action in order to control execution of the run.
        """
        path = Paths.RUNS_RUN_ID_ACTIONS.format(run_id=run_id)
        body = {
            'data': {
                'actionType': action
            }
        }
        return self._post(path, body=body)

    # MAINTENANCE RUN MANAGEMENT

    # PROTOCOL MANAGEMENT

    def get_protocols(self) -> Dict:
        """
        Get a list of all currently uploaded protocols.
        """
        return self._get(Paths.PROTOCOLS)

    def post_protocols(self, protocol_file: BinaryIO, labware_definitions: Optional[Sequence[BinaryIO]] = None) -> Dict:
        """
        Upload a protocol to your device. You may include the following files:

        * A single Python protocol file and 0 or more custom labware JSON files
        * A single JSON protocol file (any additional labware files will be ignored)

        When too many protocols already exist, old ones will be automatically deleted to make room for the new one. A
        protocol will never be automatically deleted if there's a run referring to it, though.
        """
        all_files = (protocol_file, ) if labware_definitions is None else (protocol_file, *labware_definitions)
        files = [('files', f) for f in all_files]
        return self._post(Paths.PROTOCOLS, files=files)

    def get_protocols_protocol_id(self, protocol_id: str) -> Dict:
        """
        Get an uploaded protocol by ID.
        """
        path = Paths.PROTOCOLS_PROTOCOL_ID.format(protocol_id=protocol_id)
        return self._get(path)

    # SIMPLE COMMANDS

    # DECK CONFIGURATION

    # ATTACHED MODULES

    # ATTACHED INSTRUMENTS

    # SESSION MANAGEMENT

    # LABWARE CALIBRATION MANAGEMENT

    # PIPETTE OFFSET CALIBRATION MANAGEMENT

    # TIP LENGTH CALIBRATION MANAGEMENT

    # SYSTEM CONTROL

    # SUBSYSTEM MANAGEMENT
