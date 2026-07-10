from __future__ import annotations

from enum import Enum

class ActionStatus(Enum):
    """VDA5050 ``actionStatus`` values for an AGV action."""

    WAITING = ...
    """Received by the AGV, but the trigger node or edge is not yet active."""

    INITIALIZING = ...
    """Triggered; preparatory measures have started."""

    RUNNING = ...
    """The action is currently running."""

    PAUSED = ...
    """Paused by a pause instant action or an external trigger."""

    FINISHED = ...
    """Finished; a result may be reported via ``resultDescription``."""

    FAILED = ...
    """Could not be finished for any reason."""

class EStop(Enum):
    """VDA5050 ``eStop`` acknowledgement type."""

    AUTOACK = ...
    """Auto-acknowledgeable e-stop is activated."""

    MANUAL = ...
    """E-stop must be acknowledged manually at the vehicle."""

    REMOTE = ...
    """Facility e-stop must be acknowledged remotely."""

    NONE = ...
    """No e-stop is activated."""

class ErrorLevel(Enum):
    """VDA5050 ``errorLevel`` severity."""

    WARNING = ...
    """AGV is ready to drive without human intervention."""

    FATAL = ...
    """AGV is not in a running condition."""

class InfoLevel(Enum):
    """VDA5050 ``infoLevel`` classification."""

    DEBUG = ...
    """Used for debugging."""

    INFO = ...
    """Used for visualization."""

class OperatingMode(Enum):
    """VDA5050 ``operatingMode`` of an AGV."""

    AUTOMATIC = ...
    """Fully under master control for driving and actions."""

    SEMIAUTOMATIC = ...
    """Master controls driving and actions; HMI controls speed."""

    MANUAL = ...
    """Not under master control; only location is reported."""

    SERVICE = ...
    """Not under master control; authorized personnel may reconfigure."""

    TEACHIN = ...
    """Not under master control; the AGV is being taught."""

class ActionState:
    """State of an action carried out by the AGV.

    Part of the VDA5050 state message.

    Attributes
    ----------
    action_id : str
        Unique identifier of the action.
    action_type : str or None
        Action type, mainly for visualization.
    action_description : str or None
        Additional information on the current action.
    action_status : ActionStatus
        Current progress of the action.
    result_description : str or None
        Result description when finished. Errors use the errors field.
    """

    action_id: str
    action_type: str | None
    action_description: str | None
    action_status: ActionStatus
    result_description: str | None

    def __init__(self) -> None:
        """Create an empty action state with default field values."""
    def __eq__(self, other: object) -> bool:
        """Return whether two action states are equal.

        Parameters
        ----------
        other : object
            Object to compare against.

        Returns
        -------
        bool
            ``True`` if all fields match.
        """
    def __ne__(self, other: object) -> bool:
        """Return whether two action states differ.

        Parameters
        ----------
        other : object
            Object to compare against.

        Returns
        -------
        bool
            ``True`` if any field differs.
        """

class BatteryState:
    """Battery information reported by the AGV.

    Part of the VDA5050 state message.

    Attributes
    ----------
    battery_charge : float
        State of charge in percent. Coarse good/bad levels may be
        reported as 80 / 20.
    battery_voltage : float or None
        Battery voltage.
    battery_health : int or None
        State of health in percent.
    charging : bool
        ``True`` if charging is in progress.
    reach : int or None
        Estimated reach with the current charge, in meters.
    """

    battery_charge: float
    battery_voltage: float | None
    battery_health: int | None
    charging: bool
    reach: int | None

    def __init__(self) -> None:
        """Create an empty battery state with default field values."""
    def __eq__(self, other: object) -> bool:
        """Return whether two battery states are equal.

        Parameters
        ----------
        other : object
            Object to compare against.

        Returns
        -------
        bool
            ``True`` if all fields match.
        """
    def __ne__(self, other: object) -> bool:
        """Return whether two battery states differ.

        Parameters
        ----------
        other : object
            Object to compare against.

        Returns
        -------
        bool
            ``True`` if any field differs.
        """

class AGVPosition:
    """AGV pose on a map in the world coordinate system.

    Part of the VDA5050 state message.

    Attributes
    ----------
    x : float
        X-position on the map, in meters.
    y : float
        Y-position on the map, in meters.
    theta : float
        Orientation in radians, typically in ``[-pi, pi]``.
    position_initialized : bool
        ``True`` if the AGV position is initialized.
    map_id : str
        Unique map identifier the pose is referenced in.
    map_description : str or None
        Additional information on the map.
    localization_score : float or None
        Localization quality from ``0.0`` (unknown) to ``1.0`` (known).
    deviation_range : float or None
        Position deviation in meters, if estimated.
    """

    x: float
    y: float
    theta: float
    position_initialized: bool
    map_id: str
    map_description: str | None
    localization_score: float | None
    deviation_range: float | None

    def __init__(self) -> None:
        """Create an empty AGV position with default field values."""
    def __eq__(self, other: object) -> bool:
        """Return whether two AGV positions are equal.

        Parameters
        ----------
        other : object
            Object to compare against.

        Returns
        -------
        bool
            ``True`` if all fields match.
        """
    def __ne__(self, other: object) -> bool:
        """Return whether two AGV positions differ.

        Parameters
        ----------
        other : object
            Object to compare against.

        Returns
        -------
        bool
            ``True`` if any field differs.
        """

class Velocity:
    """AGV velocity in the vehicle coordinate frame.

    Attributes
    ----------
    vx : float or None
        Velocity in the x direction, in meters per second.
    vy : float or None
        Velocity in the y direction, in meters per second.
    omega : float or None
        Turning speed around the z axis, in radians per second.
    """

    vx: float | None
    vy: float | None
    omega: float | None

    def __init__(self) -> None:
        """Create an empty velocity with default field values."""
    def __eq__(self, other: object) -> bool:
        """Return whether two velocities are equal.

        Parameters
        ----------
        other : object
            Object to compare against.

        Returns
        -------
        bool
            ``True`` if all fields match.
        """
    def __ne__(self, other: object) -> bool:
        """Return whether two velocities differ.

        Parameters
        ----------
        other : object
            Object to compare against.

        Returns
        -------
        bool
            ``True`` if any field differs.
        """

class SafetyState:
    """Safety state of the AGV.

    Part of the VDA5050 state message.

    Attributes
    ----------
    e_stop : EStop
        Acknowledgement type of the emergency stop.
    field_violation : bool
        ``True`` if a protective field is violated.
    """

    e_stop: EStop
    field_violation: bool

    def __init__(self) -> None:
        """Create an empty safety state with default field values."""
    def __eq__(self, other: object) -> bool:
        """Return whether two safety states are equal.

        Parameters
        ----------
        other : object
            Object to compare against.

        Returns
        -------
        bool
            ``True`` if all fields match.
        """
    def __ne__(self, other: object) -> bool:
        """Return whether two safety states differ.

        Parameters
        ----------
        other : object
            Object to compare against.

        Returns
        -------
        bool
            ``True`` if any field differs.
        """

class ErrorReference:
    """Key/value reference identifying the source of an error.

    Attributes
    ----------
    reference_key : str
        Reference type (for example ``nodeId``, ``edgeId``, ``orderId``).
    reference_value : str
        Value belonging to ``reference_key``.
    """

    reference_key: str
    reference_value: str

    def __init__(self) -> None:
        """Create an empty error reference with default field values."""
    def __eq__(self, other: object) -> bool:
        """Return whether two error references are equal.

        Parameters
        ----------
        other : object
            Object to compare against.

        Returns
        -------
        bool
            ``True`` if all fields match.
        """
    def __ne__(self, other: object) -> bool:
        """Return whether two error references differ.

        Parameters
        ----------
        other : object
            Object to compare against.

        Returns
        -------
        bool
            ``True`` if any field differs.
        """

class Error:
    """Error information conveyed by the AGV.

    Part of the VDA5050 state message.

    Attributes
    ----------
    error_type : str
        Type or name of the error.
    error_references : list of ErrorReference or None
        References identifying the source of the error.
    error_description : str or None
        Verbose description of details and possible causes.
    error_level : ErrorLevel
        Severity of the error.
    """

    error_type: str
    error_references: list[ErrorReference] | None
    error_description: str | None
    error_level: ErrorLevel

    def __init__(self) -> None:
        """Create an empty error with default field values."""
    def __eq__(self, other: object) -> bool:
        """Return whether two errors are equal.

        Parameters
        ----------
        other : object
            Object to compare against.

        Returns
        -------
        bool
            ``True`` if all fields match.
        """
    def __ne__(self, other: object) -> bool:
        """Return whether two errors differ.

        Parameters
        ----------
        other : object
            Object to compare against.

        Returns
        -------
        bool
            ``True`` if any field differs.
        """

class InfoReference:
    """Key/value reference identifying the source of an info message.

    Attributes
    ----------
    reference_key : str
        Reference type (for example ``nodeId``, ``edgeId``, ``orderId``).
    reference_value : str
        Value belonging to ``reference_key``.
    """

    reference_key: str
    reference_value: str

    def __init__(self) -> None:
        """Create an empty info reference with default field values."""
    def __eq__(self, other: object) -> bool:
        """Return whether two info references are equal.

        Parameters
        ----------
        other : object
            Object to compare against.

        Returns
        -------
        bool
            ``True`` if all fields match.
        """
    def __ne__(self, other: object) -> bool:
        """Return whether two info references differ.

        Parameters
        ----------
        other : object
            Object to compare against.

        Returns
        -------
        bool
            ``True`` if any field differs.
        """

class Info:
    """Information message for visualization or debugging.

    Part of the VDA5050 state message.

    Attributes
    ----------
    info_type : str
        Type or name of the information.
    info_references : list of InfoReference or None
        References identifying the source of the information.
    info_description : str or None
        Verbose description of the information.
    info_level : InfoLevel
        Classification of the information.
    """

    info_type: str
    info_references: list[InfoReference] | None
    info_description: str | None
    info_level: InfoLevel

    def __init__(self) -> None:
        """Create an empty info message with default field values."""
    def __eq__(self, other: object) -> bool:
        """Return whether two info messages are equal.

        Parameters
        ----------
        other : object
            Object to compare against.

        Returns
        -------
        bool
            ``True`` if all fields match.
        """
    def __ne__(self, other: object) -> bool:
        """Return whether two info messages differ.

        Parameters
        ----------
        other : object
            Object to compare against.

        Returns
        -------
        bool
            ``True`` if any field differs.
        """

class StateManager:
    """Mutable handle for updating published VDA5050 AGV state fields."""

    def set_position(
        self, x: float, y: float, theta: float, map_id: str
    ) -> None:
        """Set the AGV pose on a map.

        Parameters
        ----------
        x : float
            X-position in meters.
        y : float
            Y-position in meters.
        theta : float
            Orientation in radians.
        map_id : str
            Map identifier the pose is referenced in.
        """
    def set_velocity(self, velocity: Velocity) -> None:
        """Set the AGV velocity.

        Parameters
        ----------
        velocity : Velocity
            Velocity in the vehicle coordinate frame.
        """
    def set_driving(self, driving: bool) -> None:
        """Set whether the AGV is currently driving.

        Parameters
        ----------
        driving : bool
            ``True`` if the AGV is driving.
        """
    def set_paused(self, paused: bool) -> None:
        """Set whether the AGV is paused.

        Parameters
        ----------
        paused : bool
            ``True`` if the AGV is paused.
        """
    def set_new_base_request(self, request: bool) -> None:
        """Set whether a new base is requested.

        Parameters
        ----------
        request : bool
            ``True`` if a new base is requested.
        """
    def set_distance_since_last_node(self, distance: float) -> None:
        """Set distance traveled since the last node.

        Parameters
        ----------
        distance : float
            Distance in meters.
        """
    def set_battery_state(self, battery: BatteryState) -> None:
        """Set the battery state.

        Parameters
        ----------
        battery : BatteryState
            Battery information to publish.
        """
    def set_operating_mode(self, mode: OperatingMode) -> None:
        """Set the operating mode.

        Parameters
        ----------
        mode : OperatingMode
            Current operating mode.
        """
    def set_safety_state(self, safety_state: SafetyState) -> None:
        """Set the safety state.

        Parameters
        ----------
        safety_state : SafetyState
            Current safety state.
        """
    def add_action_state(self, action_state: ActionState) -> None:
        """Append one action state.

        Parameters
        ----------
        action_state : ActionState
            Action state to append.
        """
    def set_action_states(self, action_states: list[ActionState]) -> None:
        """Replace all action states.

        Parameters
        ----------
        action_states : list of ActionState
            Complete list of action states.
        """
    def clear_action_states(self) -> None:
        """Remove all action states."""
    def add_error(self, error: Error) -> None:
        """Append one error.

        Parameters
        ----------
        error : Error
            Error to append.
        """
    def set_errors(self, errors: list[Error]) -> None:
        """Replace all errors.

        Parameters
        ----------
        errors : list of Error
            Complete list of errors.
        """
    def clear_errors(self) -> None:
        """Remove all errors."""
    def add_information(self, information: Info) -> None:
        """Append one information message.

        Parameters
        ----------
        information : Info
            Information message to append.
        """
    def set_information(self, information: list[Info]) -> None:
        """Replace all information messages.

        Parameters
        ----------
        information : list of Info
            Complete list of information messages.
        """
    def remove_information(self) -> None:
        """Remove all information messages."""
