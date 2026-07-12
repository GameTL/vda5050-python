from __future__ import annotations

import vda5050._core as core

import vda5050 as vda


def test_version():
    assert vda.__version__ == "0.0.1"


def test_master_submodule_and_shared_types():
    assert core.master.Error is core.client.Error
    assert core.master.OperatingMode is core.client.OperatingMode
    assert core.master.ActionState is core.client.ActionState

    for name in (
        "VDA5050Master",
        "AGV",
        "Order",
        "InstantActions",
        "AssignmentResult",
        "AssignmentDecision",
        "ConnectionState",
        "AGVState",
    ):
        assert hasattr(core.master, name), name


def test_build_master_order_types():
    position = vda.NodePosition()
    position.x = 1.0
    position.y = 2.0
    position.map_id = "test-map"

    start = vda.Node()
    start.node_id = "start"
    start.sequence_id = 0
    start.released = True
    start.node_position = position

    finish = vda.Node()
    finish.node_id = "finish"
    finish.sequence_id = 2
    finish.released = True

    edge = vda.Edge()
    edge.edge_id = "start-finish"
    edge.sequence_id = 1
    edge.start_node_id = "start"
    edge.end_node_id = "finish"
    edge.released = True

    order = vda.Order()
    order.order_id = "test-order"
    order.nodes = [start, finish]
    order.edges = [edge]

    assert order.nodes[0].node_position == position
    assert order.edges[0].end_node_id == "finish"


def test_master_factory_and_non_onboarded_assignment(tmp_path):
    mqtt = vda.create_default_mqtt_client(
        "tcp://localhost:1883", "vda5050-python-test-master"
    )
    master = vda.VDA5050Master.make(mqtt)

    result = master.assign_order("missing", "missing", vda.Order())

    assert master.is_connected() is False
    assert result.decision == vda.AssignmentDecision.AGV_NOT_ONBOARDED
    assert bool(result) is False
    assert result.errors

    loaded, errors = master.load_layout_from_config(
        str(tmp_path / "missing-layout.json")
    )
    assert loaded is False
    assert errors


def test_master_can_be_subclassed_for_callbacks():
    class RecordingMaster(vda.VDA5050Master):
        def on_state(self, agv_id, state):
            self.last_state = (agv_id, state)

    mqtt = vda.create_default_mqtt_client(
        "tcp://localhost:1883", "vda5050-python-test-subclass"
    )
    master = RecordingMaster(mqtt)

    assert master.is_connected() is False
    assert not hasattr(master, "last_state")
