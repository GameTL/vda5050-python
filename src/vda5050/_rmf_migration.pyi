from __future__ import annotations

from collections.abc import Callable
from typing import Any

from ._client import StateManager

class ActivityIdentifier:
    """Identifier for an order and/or action activity.

    Parameters
    ----------
    order_id : str or None, optional
        Order identifier, if any.
    action_id : str or None, optional
        Action identifier, if any.

    Attributes
    ----------
    order_id : str or None
        Order identifier, if any.
    action_id : str or None
        Action identifier, if any.
    """

    def __init__(
        self,
        order_id: str | None = None,
        action_id: str | None = None,
    ) -> None: ...
    @property
    def order_id(self) -> str | None:
        """Order identifier, if any."""
    @property
    def action_id(self) -> str | None:
        """Action identifier, if any."""
    def __eq__(self, other: object) -> bool:
        """Return whether two activity identifiers are equal.

        Parameters
        ----------
        other : object
            Object to compare against.

        Returns
        -------
        bool
            ``True`` if both identifiers match.
        """
    def __ne__(self, other: object) -> bool:
        """Return whether two activity identifiers differ.

        Parameters
        ----------
        other : object
            Object to compare against.

        Returns
        -------
        bool
            ``True`` if either identifier differs.
        """

class RobotState:
    """Snapshot of a robot pose and battery level.

    Parameters
    ----------
    map : str
        Map identifier the pose is expressed in.
    position : tuple of float
        Pose as ``(x, y, yaw)``.
    battery_soc : float
        Battery state of charge in the range ``[0, 1]``.

    Attributes
    ----------
    map : str
        Map identifier.
    position : tuple of float
        Pose as ``(x, y, yaw)``.
    battery_state_of_charge : float
        Battery state of charge in the range ``[0, 1]``.
    """

    def __init__(
        self,
        map: str,
        position: tuple[float, float, float],
        battery_soc: float,
    ) -> None: ...
    @property
    def map(self) -> str:
        """Map identifier."""
    @map.setter
    def map(self, value: str) -> None:
        """Set the map identifier.

        Parameters
        ----------
        value : str
            Map identifier.
        """
    @property
    def position(self) -> tuple[float, float, float]:
        """Pose as ``(x, y, yaw)``."""
    @position.setter
    def position(self, value: tuple[float, float, float]) -> None:
        """Set the pose.

        Parameters
        ----------
        value : tuple of float
            Pose as ``(x, y, yaw)``.
        """
    @property
    def battery_state_of_charge(self) -> float:
        """Battery state of charge in the range ``[0, 1]``."""
    @battery_state_of_charge.setter
    def battery_state_of_charge(self, value: float) -> None:
        """Set the battery state of charge.

        Parameters
        ----------
        value : float
            Battery state of charge in the range ``[0, 1]``.
        """

class RobotConfiguration:
    """Static configuration for a VDA5050 robot.

    Parameters
    ----------
    manufacturer : str
        Manufacturer name used in VDA5050 topics and headers.
    serial_number : str
        Serial number used in VDA5050 topics and headers.
    interface_name : str, optional
        Interface name prefix. The default is ``"uagv"``.
    version : str, optional
        Protocol version. The default is ``"2.0.0"``.

    Attributes
    ----------
    manufacturer : str
        Manufacturer name.
    serial_number : str
        Serial number.
    interface_name : str
        Interface name prefix.
    version : str
        Protocol version.
    factsheet : Any or None
        Optional factsheet payload. Not bound as a typed Python class.
    """

    manufacturer: str
    serial_number: str
    interface_name: str
    version: str
    factsheet: Any | None

    def __init__(
        self,
        manufacturer: str,
        serial_number: str,
        interface_name: str = "uagv",
        version: str = "2.0.0",
    ) -> None: ...

class Destination:
    """Navigation or localization destination request.

    Attributes
    ----------
    map : str
        Map identifier.
    position : tuple of float
        Pose as ``(x, y, yaw)``.
    xy : tuple of float
        Planar position as ``(x, y)``.
    yaw : float
        Orientation in radians.
    graph_index : int
        Graph index associated with the destination.
    name : str
        Destination name.
    speed_limit : float or None
        Optional speed limit in meters per second.
    """

    @property
    def map(self) -> str:
        """Map identifier."""
    @property
    def position(self) -> tuple[float, float, float]:
        """Pose as ``(x, y, yaw)``."""
    @property
    def xy(self) -> tuple[float, float]:
        """Planar position as ``(x, y)``."""
    @property
    def yaw(self) -> float:
        """Orientation in radians."""
    @property
    def graph_index(self) -> int:
        """Graph index associated with the destination."""
    @property
    def name(self) -> str:
        """Destination name."""
    @property
    def speed_limit(self) -> float | None:
        """Optional speed limit in meters per second."""

class CommandExecution:
    """Handle for reporting progress of a requested command."""

    def finished(self) -> None:
        """Mark the command as successfully finished."""
    def failed(self, reason: str) -> None:
        """Mark the command as failed.

        Parameters
        ----------
        reason : str
            Human-readable failure reason.
        """
    def okay(self) -> bool:
        """Return whether the command is still okay to continue.

        Returns
        -------
        bool
            ``True`` if the command has not failed.
        """
    def is_finished(self) -> bool:
        """Return whether the command has finished.

        Returns
        -------
        bool
            ``True`` if finished was reported.
        """
    @property
    def identifier(self) -> ActivityIdentifier:
        """Activity identifier associated with this command."""

class RobotCallbacks:
    """Callbacks the adapter invokes for robot commands.

    Parameters
    ----------
    navigate : callable
        Called with ``(destination, execution)`` to start navigation.
    stop : callable
        Called with no arguments to request an immediate stop.
    action_executor : callable
        Called with ``(action_category, action_description, execution)``
        to start an action.

    Attributes
    ----------
    navigate : callable
        Navigation request callback.
    stop : callable
        Stop request callback.
    action_executor : callable
        Action execution callback.
    localize : callable or None
        Optional localization callback set via the property setter.
    """

    def __init__(
        self,
        navigate: Callable[[Destination, CommandExecution], None],
        stop: Callable[[], None],
        action_executor: Callable[[str, str, CommandExecution], None],
    ) -> None: ...
    @property
    def navigate(self) -> Callable[[Destination, CommandExecution], None]:
        """Navigation request callback."""
    @property
    def stop(self) -> Callable[[], None]:
        """Stop request callback."""
    @property
    def action_executor(
        self,
    ) -> Callable[[str, str, CommandExecution], None]:
        """Action execution callback."""
    @property
    def localize(
        self,
    ) -> Callable[[Destination, CommandExecution], None] | None:
        """Optional localization callback."""
    @localize.setter
    def localize(self, value: Callable[[Destination, CommandExecution], None]) -> None:
        """Set the localization callback.

        Parameters
        ----------
        value : callable
            Called with ``(destination, execution)`` to localize.
        """

class RobotUpdateHandle:
    """Handle for pushing robot state updates into the adapter."""

    def update(self, state: RobotState, identifier: ActivityIdentifier) -> None:
        """Publish an updated robot state.

        Parameters
        ----------
        state : RobotState
            Latest robot pose and battery snapshot.
        identifier : ActivityIdentifier
            Activity associated with this update.
        """
    def more(self) -> StateManager:
        """Return the underlying state manager for finer updates.

        Returns
        -------
        StateManager
            Mutable handle for VDA5050 state fields.
        """

class FleetConfiguration:
    """MQTT and identity configuration for a VDA5050 fleet.

    Parameters
    ----------
    fleet_name : str
        Logical fleet name.
    broker_uri : str
        MQTT broker URI.
    client_id_prefix : str
        Prefix used when constructing MQTT client IDs.
    update_interval : int, optional
        State update interval in seconds. The default is ``30``.

    Attributes
    ----------
    fleet_name : str
        Logical fleet name.
    broker_uri : str
        MQTT broker URI.
    client_id_prefix : str
        MQTT client ID prefix.
    update_interval : int
        State update interval in seconds.
    known_robots : list of str
        Names of robots with known configurations.
    """

    def __init__(
        self,
        fleet_name: str,
        broker_uri: str,
        client_id_prefix: str,
        update_interval: int = 30,
    ) -> None: ...
    @property
    def fleet_name(self) -> str:
        """Logical fleet name."""
    @fleet_name.setter
    def fleet_name(self, value: str) -> None:
        """Set the logical fleet name.

        Parameters
        ----------
        value : str
            Fleet name.
        """
    @property
    def broker_uri(self) -> str:
        """MQTT broker URI."""
    @broker_uri.setter
    def broker_uri(self, value: str) -> None:
        """Set the MQTT broker URI.

        Parameters
        ----------
        value : str
            Broker URI.
        """
    @property
    def client_id_prefix(self) -> str:
        """MQTT client ID prefix."""
    @client_id_prefix.setter
    def client_id_prefix(self, value: str) -> None:
        """Set the MQTT client ID prefix.

        Parameters
        ----------
        value : str
            Client ID prefix.
        """
    @property
    def update_interval(self) -> int:
        """State update interval in seconds."""
    @update_interval.setter
    def update_interval(self, value: int) -> None:
        """Set the state update interval.

        Parameters
        ----------
        value : int
            Interval in seconds.
        """
    @property
    def known_robots(self) -> list[str]:
        """Names of robots with known configurations."""
    def add_known_robot_configuration(
        self, robot_name: str, config: RobotConfiguration
    ) -> None:
        """Register a known robot configuration.

        Parameters
        ----------
        robot_name : str
            Robot name key.
        config : RobotConfiguration
            Configuration to associate with ``robot_name``.
        """
    def get_known_robot_configuration(self, name: str) -> RobotConfiguration | None:
        """Look up a known robot configuration.

        Parameters
        ----------
        name : str
            Robot name key.

        Returns
        -------
        RobotConfiguration or None
            Matching configuration, or ``None`` if absent.
        """

class FleetUpdateHandle:
    """Handle for adding robots to a configured VDA5050 fleet."""

    def add_robot(
        self,
        name: str,
        initial_state: RobotState,
        configuration: RobotConfiguration,
        callbacks: RobotCallbacks,
    ) -> RobotUpdateHandle:
        """Add a robot to the fleet.

        Parameters
        ----------
        name : str
            Robot name.
        initial_state : RobotState
            Initial pose and battery snapshot.
        configuration : RobotConfiguration
            Static robot configuration.
        callbacks : RobotCallbacks
            Command callbacks for the robot.

        Returns
        -------
        RobotUpdateHandle
            Handle for subsequent state updates.
        """

class Adapter:
    """Top-level Open-RMF style adapter for VDA5050 fleets."""

    @staticmethod
    def make() -> Adapter:
        """Create a new adapter instance.

        Returns
        -------
        Adapter
            Fresh adapter that has not yet been started.
        """
    def add_vda5050_fleet(self, configuration: FleetConfiguration) -> FleetUpdateHandle:
        """Register a VDA5050 fleet with this adapter.

        Parameters
        ----------
        configuration : FleetConfiguration
            Fleet MQTT and identity configuration.

        Returns
        -------
        FleetUpdateHandle
            Handle for adding robots to the fleet.
        """
    def start(self) -> None:
        """Start the adapter event loop and MQTT clients."""
    def stop(self) -> None:
        """Stop the adapter and disconnect MQTT clients."""
