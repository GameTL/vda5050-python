from __future__ import annotations

from enum import Enum

from ._client import ActionState, AGVPosition, BatteryState, Error, OperatingMode

class MqttClient:
    """Opaque shared MQTT client used by :class:`VDA5050Master`.

    Create instances with :func:`create_default_mqtt_client`.
    """

def create_default_mqtt_client(broker_address: str, client_id: str) -> MqttClient:
    """Create a Paho-backed MQTT client.

    Parameters
    ----------
    broker_address : str
        MQTT broker URI, for example ``tcp://localhost:1883``.
    client_id : str
        MQTT client identifier used by the master connection.
    """

class BlockingType(Enum):
    """VDA5050 action blocking behavior."""

    NONE = ...
    """The action does not block driving or other actions."""

    SOFT = ...
    """The action may run with other actions, but the AGV must not drive."""

    HARD = ...
    """The AGV must not drive or run another action in parallel."""

class ConnectionState(Enum):
    """Connection state reported by an AGV."""

    ONLINE = ...
    """The AGV is connected and communicating."""

    OFFLINE = ...
    """The AGV disconnected normally."""

    CONNECTIONBROKEN = ...
    """The broker reported an unexpected AGV connection loss."""

class AGVState(Enum):
    """Master-side operational state derived from AGV heartbeats."""

    STATE_UNKNOWN = ...
    AVAILABLE = ...
    UNAVAILABLE = ...
    ERROR = ...

class AssignmentDecision(Enum):
    """Synchronous result category for assigning an order."""

    ASSIGNED = ...
    AGV_NOT_ONBOARDED = ...
    AGV_OFFLINE = ...
    AGV_NOT_READY = ...
    AGV_MODE_NOT_AUTO = ...
    AGV_POSITION_NOT_INITIALIZED = ...
    AGV_NO_STATE_YET = ...
    STITCH_REJECTED = ...
    STITCH_QUEUED = ...

class InstantActionDecision(Enum):
    """Synchronous result category for assigning instant actions."""

    ASSIGNED = ...
    AGV_NOT_ONBOARDED = ...
    AGV_OFFLINE = ...
    DUPLICATE_ACTION_ID = ...
    AGV_QUEUE_FULL = ...
    HARD_ACTION_BLOCKED = ...
    ACTION_BLOCKED_BY_DRIVING = ...
    AGV_MODE_NOT_AUTO_FOR_ACTION = ...

class ActionParameter:
    """Key/value parameter attached to an action."""

    key: str
    value: str

    def __init__(self) -> None:
        """Create an empty action parameter."""
    def __eq__(self, other: object) -> bool: ...
    def __ne__(self, other: object) -> bool: ...

class Action:
    """Action contained in an order node, edge, or instant-action batch."""

    action_type: str
    action_id: str
    blocking_type: BlockingType
    action_description: str | None
    action_parameters: list[ActionParameter] | None

    def __init__(self) -> None:
        """Create an empty action with default field values."""
    def __eq__(self, other: object) -> bool: ...
    def __ne__(self, other: object) -> bool: ...

class NodePosition:
    """Position and allowed deviation of an order node."""

    x: float
    y: float
    theta: float | None
    allowed_deviation_x_y: float | None
    allowed_deviation_theta: float | None
    map_id: str
    map_description: str | None

    def __init__(self) -> None:
        """Create an empty node position."""
    def __eq__(self, other: object) -> bool: ...
    def __ne__(self, other: object) -> bool: ...

class Node:
    """Node in a VDA5050 order graph."""

    node_id: str
    sequence_id: int
    released: bool
    actions: list[Action]
    node_position: NodePosition | None
    node_description: str | None

    def __init__(self) -> None:
        """Create an empty order node."""
    def __eq__(self, other: object) -> bool: ...
    def __ne__(self, other: object) -> bool: ...

class Header:
    """Common VDA5050 message header fields exposed by this binding."""

    header_id: int
    version: str
    manufacturer: str
    serial_number: str

    def __init__(self) -> None:
        """Create an empty message header."""
    def __eq__(self, other: object) -> bool: ...
    def __ne__(self, other: object) -> bool: ...

class Edge:
    """Edge joining two nodes in a VDA5050 order graph."""

    edge_id: str
    sequence_id: int
    start_node_id: str
    end_node_id: str
    released: bool
    actions: list[Action]
    max_speed: float | None

    def __init__(self) -> None:
        """Create an empty order edge."""
    def __eq__(self, other: object) -> bool: ...
    def __ne__(self, other: object) -> bool: ...

class Order:
    """Order sent by the master to an AGV."""

    header: Header
    order_id: str
    order_update_id: int
    nodes: list[Node]
    edges: list[Edge]
    zone_set_id: str | None

    def __init__(self) -> None:
        """Create an empty order."""
    def __eq__(self, other: object) -> bool: ...
    def __ne__(self, other: object) -> bool: ...

class InstantActions:
    """Batch of instant actions sent by the master to an AGV."""

    header: Header
    actions: list[Action]

    def __init__(self) -> None:
        """Create an empty instant-action batch."""
    def __eq__(self, other: object) -> bool: ...
    def __ne__(self, other: object) -> bool: ...

class NodeState:
    """Remaining or active node reported in an AGV state message."""

    node_id: str
    sequence_id: int
    released: bool
    node_position: NodePosition | None

    def __init__(self) -> None:
        """Create an empty node state."""
    def __eq__(self, other: object) -> bool: ...
    def __ne__(self, other: object) -> bool: ...

class EdgeState:
    """Remaining or active edge reported in an AGV state message."""

    edge_id: str
    sequence_id: int
    released: bool

    def __init__(self) -> None:
        """Create an empty edge state."""
    def __eq__(self, other: object) -> bool: ...
    def __ne__(self, other: object) -> bool: ...

class State:
    """Master-visible subset of the latest VDA5050 AGV state."""

    order_id: str
    order_update_id: int
    last_node_id: str
    last_node_sequence_id: int
    node_states: list[NodeState]
    edge_states: list[EdgeState]
    agv_position: AGVPosition | None
    driving: bool
    paused: bool | None
    distance_since_last_node: float | None
    action_states: list[ActionState]
    battery_state: BatteryState
    operating_mode: OperatingMode
    errors: list[Error]

    def __init__(self) -> None:
        """Create an empty AGV state."""
    def __eq__(self, other: object) -> bool: ...
    def __ne__(self, other: object) -> bool: ...

class AssignmentResult:
    """Outcome of :meth:`VDA5050Master.assign_order`."""

    @property
    def decision(self) -> AssignmentDecision:
        """Assignment outcome category."""
    @property
    def errors(self) -> list[Error]:
        """Diagnostic errors for a rejected assignment."""
    def __bool__(self) -> bool:
        """Return ``True`` only when the decision is ``ASSIGNED``."""

class InstantActionAssignmentResult:
    """Outcome of :meth:`VDA5050Master.assign_instant_actions`."""

    @property
    def decision(self) -> InstantActionDecision:
        """Instant-action assignment outcome category."""
    @property
    def errors(self) -> list[Error]:
        """Diagnostic errors for a rejected assignment."""
    def __bool__(self) -> bool:
        """Return ``True`` only when the decision is ``ASSIGNED``."""

class AGV:
    """Handle to an AGV onboarded by :class:`VDA5050Master`.

    Instances are returned by :meth:`VDA5050Master.get_agv` and cannot be
    constructed directly from Python.
    """

    def get_manufacturer(self) -> str:
        """Return the AGV manufacturer."""
    def get_serial_number(self) -> str:
        """Return the AGV serial number."""
    def get_agv_id(self) -> str:
        """Return the ``manufacturer/serial_number`` identifier."""
    def is_connected(self) -> bool:
        """Return whether the AGV currently reports ``ONLINE``."""
    def get_connection_status(self) -> ConnectionState:
        """Return the latest AGV connection state."""
    def get_operational_state(self) -> AGVState:
        """Return the heartbeat-derived operational state."""
    def get_last_state(self) -> State | None:
        """Return the last received state, or ``None`` if unavailable."""
    def has_active_order(self) -> bool:
        """Return whether the master tracks an active order for this AGV."""
    def get_pending_order_count(self) -> int:
        """Return the number of orders waiting in the outbound queue."""
    def cancel_pending_orders(self) -> None:
        """Clear queued orders and instant actions without contacting the AGV."""

class VDA5050Master:
    """FMS-side facade managing multiple AGVs over one MQTT client.

    Subclass this class to implement supported event hooks such as
    ``on_state(agv_id, state)``, ``on_node_reached(agv_id, node_id)``,
    ``on_errors_appeared(agv_id, errors)``, and connection/heartbeat hooks.
    """

    def __init__(self, mqtt_client: MqttClient) -> None:
        """Construct a master using a shared MQTT client."""
    @staticmethod
    def make(mqtt_client: MqttClient) -> VDA5050Master:
        """Construct a master with default no-op callbacks."""
    def connect(self) -> None:
        """Connect the shared MQTT client to its broker."""
    def disconnect(self) -> None:
        """Disconnect the shared MQTT client."""
    def is_connected(self) -> bool:
        """Return whether the master MQTT client is connected."""
    def onboard_agv(
        self,
        manufacturer: str,
        serial_number: str,
        max_queue_size: int = 10,
        drop_oldest: bool = True,
    ) -> None:
        """Register an AGV for message routing and outbound commands."""
    def offboard_agv(self, manufacturer: str, serial_number: str) -> None:
        """Remove an AGV from this master."""
    def is_agv_onboarded(self, manufacturer: str, serial_number: str) -> bool:
        """Return whether the AGV is registered with this master."""
    def get_onboarded_agvs(self) -> list[tuple[str, str]]:
        """Return ``(manufacturer, serial_number)`` pairs for onboarded AGVs."""
    def get_agv(self, manufacturer: str, serial_number: str) -> AGV | None:
        """Return an onboarded AGV handle, or ``None`` when not found."""
    def assign_order(
        self, manufacturer: str, serial_number: str, order: Order
    ) -> AssignmentResult:
        """Run synchronous readiness checks and assign an order."""
    def publish_order(
        self, manufacturer: str, serial_number: str, order: Order
    ) -> bool:
        """Queue an order without the synchronous assignment preflight."""
    def assign_instant_actions(
        self,
        manufacturer: str,
        serial_number: str,
        actions: InstantActions,
    ) -> InstantActionAssignmentResult:
        """Run preflight checks and assign an instant-action batch."""
    def publish_instant_actions(
        self,
        manufacturer: str,
        serial_number: str,
        actions: InstantActions,
    ) -> bool:
        """Queue instant actions without the synchronous preflight."""
    def load_layout_from_config(self, path: str) -> tuple[bool, list[str]]:
        """Load a topology layout, returning success and error descriptions."""
