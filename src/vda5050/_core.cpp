/*
 * Copyright (C) 2026 ROS-Industrial Consortium Asia Pacific
 * Advanced Remanufacturing and Technology Centre
 * A*STAR Research Entities (Co. Registration No. 199702110H)
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *      http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

#include <pybind11/functional.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

#include <memory>
#include <string>
#include <utility>
#include <vector>

#include "vda5050_core/client/adapter/state_manager.hpp"
#include "vda5050_core/master/actions/instant_action_assignment_result.hpp"
#include "vda5050_core/master/agv.hpp"
#include "vda5050_core/master/assignment_result.hpp"
#include "vda5050_core/master/master.hpp"
#include "vda5050_core/transport/mqtt_client_interface.hpp"
#include "vda5050_core/types/action.hpp"
#include "vda5050_core/types/action_parameter.hpp"
#include "vda5050_core/types/action_state.hpp"
#include "vda5050_core/types/action_status.hpp"
#include "vda5050_core/types/agv_position.hpp"
#include "vda5050_core/types/battery_state.hpp"
#include "vda5050_core/types/blocking_type.hpp"
#include "vda5050_core/types/connection_state.hpp"
#include "vda5050_core/types/e_stop.hpp"
#include "vda5050_core/types/edge.hpp"
#include "vda5050_core/types/edge_state.hpp"
#include "vda5050_core/types/error.hpp"
#include "vda5050_core/types/error_level.hpp"
#include "vda5050_core/types/error_reference.hpp"
#include "vda5050_core/types/header.hpp"
#include "vda5050_core/types/info.hpp"
#include "vda5050_core/types/info_level.hpp"
#include "vda5050_core/types/info_reference.hpp"
#include "vda5050_core/types/instant_actions.hpp"
#include "vda5050_core/types/node.hpp"
#include "vda5050_core/types/node_position.hpp"
#include "vda5050_core/types/node_state.hpp"
#include "vda5050_core/types/operating_mode.hpp"
#include "vda5050_core/types/order.hpp"
#include "vda5050_core/types/safety_state.hpp"
#include "vda5050_core/types/state.hpp"
#include "vda5050_core/types/velocity.hpp"

#include "rmf_migration.hpp"

#define STRINGIFY(x) #x
#define MACRO_STRINGIFY(x) STRINGIFY(x)

namespace py = pybind11;

using vda5050_core::python::rmf_migration::ActionExecutor;
using vda5050_core::python::rmf_migration::ActivityIdentifier;
using vda5050_core::python::rmf_migration::Adapter;  
using vda5050_core::python::rmf_migration::CommandExecution;
using vda5050_core::python::rmf_migration::Destination;
using vda5050_core::python::rmf_migration::FleetConfiguration;
using vda5050_core::python::rmf_migration::FleetUpdateHandle;
using vda5050_core::python::rmf_migration::LocalizationRequest;
using vda5050_core::python::rmf_migration::NavigationRequest;
using vda5050_core::python::rmf_migration::RobotCallbacks;
using vda5050_core::python::rmf_migration::RobotConfiguration;
using vda5050_core::python::rmf_migration::RobotState;
using vda5050_core::python::rmf_migration::RobotUpdateHandle;
using vda5050_core::python::rmf_migration::StopRequest;

using vda5050_core::client::adapter::StateManager;
using vda5050_core::master::AGV;
using vda5050_core::master::AGVState;
using vda5050_core::master::AssignmentDecision;
using vda5050_core::master::AssignmentResult;
using vda5050_core::master::InstantActionAssignmentResult;
using vda5050_core::master::InstantActionDecision;
using vda5050_core::master::VDA5050Master;
using vda5050_core::transport::MqttClientInterface;
using vda5050_core::types::Action;
using vda5050_core::types::ActionParameter;
using vda5050_core::types::ActionState;
using vda5050_core::types::ActionStatus;
using vda5050_core::types::AGVPosition;
using vda5050_core::types::BatteryState;
using vda5050_core::types::BlockingType;
using vda5050_core::types::ConnectionState;
using vda5050_core::types::Edge;
using vda5050_core::types::EdgeState;
using vda5050_core::types::Error;
using vda5050_core::types::ErrorLevel;
using vda5050_core::types::ErrorReference;
using vda5050_core::types::EStop;
using vda5050_core::types::Header;
using vda5050_core::types::Info;
using vda5050_core::types::InfoLevel;
using vda5050_core::types::InfoReference;
using vda5050_core::types::InstantActions;
using vda5050_core::types::Node;
using vda5050_core::types::NodePosition;
using vda5050_core::types::NodeState;
using vda5050_core::types::OperatingMode;
using vda5050_core::types::Order;
using vda5050_core::types::SafetyState;
using vda5050_core::types::State;
using vda5050_core::types::Velocity;

namespace {

void discard_callback_error(
  py::error_already_set& error, const char* callback_name)
{
  py::gil_scoped_acquire gil;
  error.discard_as_unraisable(callback_name);
}

class PyVDA5050Master : public VDA5050Master
{
public:
  using VDA5050Master::VDA5050Master;

  void on_state(const std::string& agv_id, const State& state) override
  {
    try
    {
      PYBIND11_OVERRIDE(void, VDA5050Master, on_state, agv_id, state);
    }
    catch (py::error_already_set& error)
    {
      discard_callback_error(error, "VDA5050Master.on_state");
    }
  }

  void on_node_reached(
    const std::string& agv_id, const std::string& node_id) override
  {
    try
    {
      PYBIND11_OVERRIDE(
        void, VDA5050Master, on_node_reached, agv_id, node_id);
    }
    catch (py::error_already_set& error)
    {
      discard_callback_error(error, "VDA5050Master.on_node_reached");
    }
  }

  void on_errors_appeared(
    const std::string& agv_id, const std::vector<Error>& errors) override
  {
    try
    {
      PYBIND11_OVERRIDE(
        void, VDA5050Master, on_errors_appeared, agv_id, errors);
    }
    catch (py::error_already_set& error)
    {
      discard_callback_error(error, "VDA5050Master.on_errors_appeared");
    }
  }

  void on_errors_resolved(
    const std::string& agv_id, const std::vector<Error>& errors) override
  {
    try
    {
      PYBIND11_OVERRIDE(
        void, VDA5050Master, on_errors_resolved, agv_id, errors);
    }
    catch (py::error_already_set& error)
    {
      discard_callback_error(error, "VDA5050Master.on_errors_resolved");
    }
  }

  void on_new_base_requested(const std::string& agv_id) override
  {
    try
    {
      PYBIND11_OVERRIDE(
        void, VDA5050Master, on_new_base_requested, agv_id);
    }
    catch (py::error_already_set& error)
    {
      discard_callback_error(error, "VDA5050Master.on_new_base_requested");
    }
  }

  void on_mode_changed(
    const std::string& agv_id, OperatingMode new_mode,
    OperatingMode previous_mode) override
  {
    try
    {
      PYBIND11_OVERRIDE(
        void, VDA5050Master, on_mode_changed, agv_id, new_mode, previous_mode);
    }
    catch (py::error_already_set& error)
    {
      discard_callback_error(error, "VDA5050Master.on_mode_changed");
    }
  }

  void on_paused(const std::string& agv_id, bool paused) override
  {
    try
    {
      PYBIND11_OVERRIDE(void, VDA5050Master, on_paused, agv_id, paused);
    }
    catch (py::error_already_set& error)
    {
      discard_callback_error(error, "VDA5050Master.on_paused");
    }
  }

  void on_driving(const std::string& agv_id, bool driving) override
  {
    try
    {
      PYBIND11_OVERRIDE(void, VDA5050Master, on_driving, agv_id, driving);
    }
    catch (py::error_already_set& error)
    {
      discard_callback_error(error, "VDA5050Master.on_driving");
    }
  }

  void on_connect(const std::string& agv_id) override
  {
    try
    {
      PYBIND11_OVERRIDE(void, VDA5050Master, on_connect, agv_id);
    }
    catch (py::error_already_set& error)
    {
      discard_callback_error(error, "VDA5050Master.on_connect");
    }
  }

  void on_offline(const std::string& agv_id) override
  {
    try
    {
      PYBIND11_OVERRIDE(void, VDA5050Master, on_offline, agv_id);
    }
    catch (py::error_already_set& error)
    {
      discard_callback_error(error, "VDA5050Master.on_offline");
    }
  }

  void on_connection_broken(const std::string& agv_id) override
  {
    try
    {
      PYBIND11_OVERRIDE(
        void, VDA5050Master, on_connection_broken, agv_id);
    }
    catch (py::error_already_set& error)
    {
      discard_callback_error(error, "VDA5050Master.on_connection_broken");
    }
  }

  void on_state_timeout(const std::string& agv_id) override
  {
    try
    {
      PYBIND11_OVERRIDE(void, VDA5050Master, on_state_timeout, agv_id);
    }
    catch (py::error_already_set& error)
    {
      discard_callback_error(error, "VDA5050Master.on_state_timeout");
    }
  }

  void on_state_resumed(const std::string& agv_id) override
  {
    try
    {
      PYBIND11_OVERRIDE(void, VDA5050Master, on_state_resumed, agv_id);
    }
    catch (py::error_already_set& error)
    {
      discard_callback_error(error, "VDA5050Master.on_state_resumed");
    }
  }
};

}  // namespace

PYBIND11_MODULE(_core, m)
{
  m.doc() = "VDA5050 Core Python bindings";
#ifdef VERSION_INFO
  m.attr("__version__") = MACRO_STRINGIFY(VERSION_INFO);
#else
  m.attr("__version__") = "dev";
#endif

  auto m_client = m.def_submodule("client", "Native VDA5050 client API");

  py::enum_<ActionStatus>(m_client, "ActionStatus")
    .value("WAITING", ActionStatus::WAITING)
    .value("INITIALIZING", ActionStatus::INITIALIZING)
    .value("RUNNING", ActionStatus::RUNNING)
    .value("PAUSED", ActionStatus::PAUSED)
    .value("FINISHED", ActionStatus::FINISHED)
    .value("FAILED", ActionStatus::FAILED);

  py::enum_<EStop>(m_client, "EStop")
    .value("AUTOACK", EStop::AUTOACK)
    .value("MANUAL", EStop::MANUAL)
    .value("REMOTE", EStop::REMOTE)
    .value("NONE", EStop::NONE);

  py::enum_<ErrorLevel>(m_client, "ErrorLevel")
    .value("WARNING", ErrorLevel::WARNING)
    .value("FATAL", ErrorLevel::FATAL);

  py::enum_<InfoLevel>(m_client, "InfoLevel")
    .value("DEBUG", InfoLevel::DEBUG)
    .value("INFO", InfoLevel::INFO);

  py::enum_<OperatingMode>(m_client, "OperatingMode")
    .value("AUTOMATIC", OperatingMode::AUTOMATIC)
    .value("SEMIAUTOMATIC", OperatingMode::SEMIAUTOMATIC)
    .value("MANUAL", OperatingMode::MANUAL)
    .value("SERVICE", OperatingMode::SERVICE)
    .value("TEACHIN", OperatingMode::TEACHIN);

  py::class_<ActionState>(m_client, "ActionState")
    .def(py::init<>())
    .def_readwrite("action_id", &ActionState::action_id)
    .def_readwrite("action_type", &ActionState::action_type)
    .def_readwrite("action_description", &ActionState::action_description)
    .def_readwrite("action_status", &ActionState::action_status)
    .def_readwrite("result_description", &ActionState::result_description)
    .def("__eq__", &ActionState::operator==)
    .def("__ne__", &ActionState::operator!=);

  py::class_<BatteryState>(m_client, "BatteryState")
    .def(py::init<>())
    .def_readwrite("battery_charge", &BatteryState::battery_charge)
    .def_readwrite("battery_voltage", &BatteryState::battery_voltage)
    .def_readwrite("battery_health", &BatteryState::battery_health)
    .def_readwrite("charging", &BatteryState::charging)
    .def_readwrite("reach", &BatteryState::reach)
    .def("__eq__", &BatteryState::operator==)
    .def("__ne__", &BatteryState::operator!=);

  py::class_<AGVPosition>(m_client, "AGVPosition")
    .def(py::init<>())
    .def_readwrite("x", &AGVPosition::x)
    .def_readwrite("y", &AGVPosition::y)
    .def_readwrite("theta", &AGVPosition::theta)
    .def_readwrite("position_initialized", &AGVPosition::position_initialized)
    .def_readwrite("map_id", &AGVPosition::map_id)
    .def_readwrite("map_description", &AGVPosition::map_description)
    .def_readwrite("localization_score", &AGVPosition::localization_score)
    .def_readwrite("deviation_range", &AGVPosition::deviation_range)
    .def("__eq__", &AGVPosition::operator==)
    .def("__ne__", &AGVPosition::operator!=);

  py::class_<Velocity>(m_client, "Velocity")
    .def(py::init<>())
    .def_readwrite("vx", &Velocity::vx)
    .def_readwrite("vy", &Velocity::vy)
    .def_readwrite("omega", &Velocity::omega)
    .def("__eq__", &Velocity::operator==)
    .def("__ne__", &Velocity::operator!=);

  py::class_<SafetyState>(m_client, "SafetyState")
    .def(py::init<>())
    .def_readwrite("e_stop", &SafetyState::e_stop)
    .def_readwrite("field_violation", &SafetyState::field_violation)
    .def("__eq__", &SafetyState::operator==)
    .def("__ne__", &SafetyState::operator!=);

  py::class_<ErrorReference>(m_client, "ErrorReference")
    .def(py::init<>())
    .def_readwrite("reference_key", &ErrorReference::reference_key)
    .def_readwrite("reference_value", &ErrorReference::reference_value)
    .def("__eq__", &ErrorReference::operator==)
    .def("__ne__", &ErrorReference::operator!=);

  py::class_<Error>(m_client, "Error")
    .def(py::init<>())
    .def_readwrite("error_type", &Error::error_type)
    .def_readwrite("error_references", &Error::error_references)
    .def_readwrite("error_description", &Error::error_description)
    .def_readwrite("error_level", &Error::error_level)
    .def("__eq__", &Error::operator==)
    .def("__ne__", &Error::operator!=);

  py::class_<InfoReference>(m_client, "InfoReference")
    .def(py::init<>())
    .def_readwrite("reference_key", &InfoReference::reference_key)
    .def_readwrite("reference_value", &InfoReference::reference_value)
    .def("__eq__", &InfoReference::operator==)
    .def("__ne__", &InfoReference::operator!=);

  py::class_<Info>(m_client, "Info")
    .def(py::init<>())
    .def_readwrite("info_type", &Info::info_type)
    .def_readwrite("info_references", &Info::info_references)
    .def_readwrite("info_description", &Info::info_description)
    .def_readwrite("info_level", &Info::info_level)
    .def("__eq__", &Info::operator==)
    .def("__ne__", &Info::operator!=);

  py::class_<StateManager, std::shared_ptr<StateManager>>(
    m_client, "StateManager")
    //TODO .def_static("make", &StateManager::make) // need to construct a standalone `StateManager` 
    .def("set_position", &StateManager::set_position)
    .def("set_velocity", &StateManager::set_velocity)
    .def("set_driving", &StateManager::set_driving)
    .def("set_paused", &StateManager::set_paused)
    .def("set_new_base_request", &StateManager::set_new_base_request)
    .def(
      "set_distance_since_last_node",
      &StateManager::set_distance_since_last_node)
    .def("set_battery_state", &StateManager::set_battery_state)
    .def("set_operating_mode", &StateManager::set_operating_mode)
    .def("set_safety_state", &StateManager::set_safety_state)
    .def("add_action_state", &StateManager::add_action_state)
    .def("set_action_states", &StateManager::set_action_states)
    .def("clear_action_states", &StateManager::clear_action_states)
    .def("add_error", &StateManager::add_error)
    .def("set_errors", &StateManager::set_errors)
    .def("clear_errors", &StateManager::clear_errors)
    .def("add_information", &StateManager::add_information)
    .def("set_information", &StateManager::set_information)
    .def("remove_information", &StateManager::remove_information);

  auto m_master = m.def_submodule("master", "Native VDA5050 master API");

  // These types are shared by the client and master APIs. Alias the existing
  // Python objects so one C++ type is never registered twice.
  m_master.attr("ActionStatus") = m_client.attr("ActionStatus");
  m_master.attr("ActionState") = m_client.attr("ActionState");
  m_master.attr("BatteryState") = m_client.attr("BatteryState");
  m_master.attr("AGVPosition") = m_client.attr("AGVPosition");
  m_master.attr("OperatingMode") = m_client.attr("OperatingMode");
  m_master.attr("ErrorLevel") = m_client.attr("ErrorLevel");
  m_master.attr("ErrorReference") = m_client.attr("ErrorReference");
  m_master.attr("Error") = m_client.attr("Error");

  py::class_<MqttClientInterface, std::shared_ptr<MqttClientInterface>>(
    m_master, "MqttClient");

  m_master.def(
    "create_default_mqtt_client",
    &vda5050_core::transport::create_default_client_shared,
    py::arg("broker_address"), py::arg("client_id"));

  py::enum_<BlockingType>(m_master, "BlockingType")
    .value("NONE", BlockingType::NONE)
    .value("SOFT", BlockingType::SOFT)
    .value("HARD", BlockingType::HARD);

  py::enum_<ConnectionState>(m_master, "ConnectionState")
    .value("ONLINE", ConnectionState::ONLINE)
    .value("OFFLINE", ConnectionState::OFFLINE)
    .value("CONNECTIONBROKEN", ConnectionState::CONNECTIONBROKEN);

  py::enum_<AGVState>(m_master, "AGVState")
    .value("STATE_UNKNOWN", AGVState::STATE_UNKNOWN)
    .value("AVAILABLE", AGVState::AVAILABLE)
    .value("UNAVAILABLE", AGVState::UNAVAILABLE)
    .value("ERROR", AGVState::ERROR);

  py::enum_<AssignmentDecision>(m_master, "AssignmentDecision")
    .value("ASSIGNED", AssignmentDecision::ASSIGNED)
    .value("AGV_NOT_ONBOARDED", AssignmentDecision::AGV_NOT_ONBOARDED)
    .value("AGV_OFFLINE", AssignmentDecision::AGV_OFFLINE)
    .value("AGV_NOT_READY", AssignmentDecision::AGV_NOT_READY)
    .value("AGV_MODE_NOT_AUTO", AssignmentDecision::AGV_MODE_NOT_AUTO)
    .value(
      "AGV_POSITION_NOT_INITIALIZED",
      AssignmentDecision::AGV_POSITION_NOT_INITIALIZED)
    .value("AGV_NO_STATE_YET", AssignmentDecision::AGV_NO_STATE_YET)
    .value("STITCH_REJECTED", AssignmentDecision::STITCH_REJECTED)
    .value("STITCH_QUEUED", AssignmentDecision::STITCH_QUEUED);

  py::enum_<InstantActionDecision>(m_master, "InstantActionDecision")
    .value("ASSIGNED", InstantActionDecision::ASSIGNED)
    .value(
      "AGV_NOT_ONBOARDED", InstantActionDecision::AGV_NOT_ONBOARDED)
    .value("AGV_OFFLINE", InstantActionDecision::AGV_OFFLINE)
    .value(
      "DUPLICATE_ACTION_ID", InstantActionDecision::DUPLICATE_ACTION_ID)
    .value("AGV_QUEUE_FULL", InstantActionDecision::AGV_QUEUE_FULL)
    .value(
      "HARD_ACTION_BLOCKED", InstantActionDecision::HARD_ACTION_BLOCKED)
    .value(
      "ACTION_BLOCKED_BY_DRIVING",
      InstantActionDecision::ACTION_BLOCKED_BY_DRIVING)
    .value(
      "AGV_MODE_NOT_AUTO_FOR_ACTION",
      InstantActionDecision::AGV_MODE_NOT_AUTO_FOR_ACTION);

  py::class_<ActionParameter>(m_master, "ActionParameter")
    .def(py::init<>())
    .def_readwrite("key", &ActionParameter::key)
    .def_readwrite("value", &ActionParameter::value)
    .def("__eq__", &ActionParameter::operator==)
    .def("__ne__", &ActionParameter::operator!=);

  py::class_<Action>(m_master, "Action")
    .def(py::init<>())
    .def_readwrite("action_type", &Action::action_type)
    .def_readwrite("action_id", &Action::action_id)
    .def_readwrite("blocking_type", &Action::blocking_type)
    .def_readwrite("action_description", &Action::action_description)
    .def_readwrite("action_parameters", &Action::action_parameters)
    .def("__eq__", &Action::operator==)
    .def("__ne__", &Action::operator!=);

  py::class_<NodePosition>(m_master, "NodePosition")
    .def(py::init<>())
    .def_readwrite("x", &NodePosition::x)
    .def_readwrite("y", &NodePosition::y)
    .def_readwrite("theta", &NodePosition::theta)
    .def_readwrite(
      "allowed_deviation_x_y", &NodePosition::allowed_deviation_x_y)
    .def_readwrite(
      "allowed_deviation_theta", &NodePosition::allowed_deviation_theta)
    .def_readwrite("map_id", &NodePosition::map_id)
    .def_readwrite("map_description", &NodePosition::map_description)
    .def("__eq__", &NodePosition::operator==)
    .def("__ne__", &NodePosition::operator!=);

  py::class_<Node>(m_master, "Node")
    .def(py::init<>())
    .def_readwrite("node_id", &Node::node_id)
    .def_readwrite("sequence_id", &Node::sequence_id)
    .def_readwrite("released", &Node::released)
    .def_readwrite("actions", &Node::actions)
    .def_readwrite("node_position", &Node::node_position)
    .def_readwrite("node_description", &Node::node_description)
    .def("__eq__", &Node::operator==)
    .def("__ne__", &Node::operator!=);

  py::class_<Header>(m_master, "Header")
    .def(py::init<>())
    .def_readwrite("header_id", &Header::header_id)
    .def_readwrite("version", &Header::version)
    .def_readwrite("manufacturer", &Header::manufacturer)
    .def_readwrite("serial_number", &Header::serial_number)
    .def("__eq__", &Header::operator==)
    .def("__ne__", &Header::operator!=);

  py::class_<Edge>(m_master, "Edge")
    .def(py::init<>())
    .def_readwrite("edge_id", &Edge::edge_id)
    .def_readwrite("sequence_id", &Edge::sequence_id)
    .def_readwrite("start_node_id", &Edge::start_node_id)
    .def_readwrite("end_node_id", &Edge::end_node_id)
    .def_readwrite("released", &Edge::released)
    .def_readwrite("actions", &Edge::actions)
    .def_readwrite("max_speed", &Edge::max_speed)
    .def("__eq__", &Edge::operator==)
    .def("__ne__", &Edge::operator!=);

  py::class_<Order>(m_master, "Order")
    .def(py::init<>())
    .def_readwrite("header", &Order::header)
    .def_readwrite("order_id", &Order::order_id)
    .def_readwrite("order_update_id", &Order::order_update_id)
    .def_readwrite("nodes", &Order::nodes)
    .def_readwrite("edges", &Order::edges)
    .def_readwrite("zone_set_id", &Order::zone_set_id)
    .def("__eq__", &Order::operator==)
    .def("__ne__", &Order::operator!=);

  py::class_<InstantActions>(m_master, "InstantActions")
    .def(py::init<>())
    .def_readwrite("header", &InstantActions::header)
    .def_readwrite("actions", &InstantActions::actions)
    .def("__eq__", &InstantActions::operator==)
    .def("__ne__", &InstantActions::operator!=);

  py::class_<NodeState>(m_master, "NodeState")
    .def(py::init<>())
    .def_readwrite("node_id", &NodeState::node_id)
    .def_readwrite("sequence_id", &NodeState::sequence_id)
    .def_readwrite("released", &NodeState::released)
    .def_readwrite("node_position", &NodeState::node_position)
    .def("__eq__", &NodeState::operator==)
    .def("__ne__", &NodeState::operator!=);

  py::class_<EdgeState>(m_master, "EdgeState")
    .def(py::init<>())
    .def_readwrite("edge_id", &EdgeState::edge_id)
    .def_readwrite("sequence_id", &EdgeState::sequence_id)
    .def_readwrite("released", &EdgeState::released)
    .def("__eq__", &EdgeState::operator==)
    .def("__ne__", &EdgeState::operator!=);

  py::class_<State>(m_master, "State")
    .def(py::init<>())
    .def_readwrite("order_id", &State::order_id)
    .def_readwrite("order_update_id", &State::order_update_id)
    .def_readwrite("last_node_id", &State::last_node_id)
    .def_readwrite("last_node_sequence_id", &State::last_node_sequence_id)
    .def_readwrite("node_states", &State::node_states)
    .def_readwrite("edge_states", &State::edge_states)
    .def_readwrite("agv_position", &State::agv_position)
    .def_readwrite("driving", &State::driving)
    .def_readwrite("paused", &State::paused)
    .def_readwrite(
      "distance_since_last_node", &State::distance_since_last_node)
    .def_readwrite("action_states", &State::action_states)
    .def_readwrite("battery_state", &State::battery_state)
    .def_readwrite("operating_mode", &State::operating_mode)
    .def_readwrite("errors", &State::errors)
    .def("__eq__", &State::operator==)
    .def("__ne__", &State::operator!=);

  py::class_<AssignmentResult>(m_master, "AssignmentResult")
    .def_readonly("decision", &AssignmentResult::decision)
    .def_readonly("errors", &AssignmentResult::errors)
    .def(
      "__bool__",
      [](const AssignmentResult& result) {
        return static_cast<bool>(result);
      });

  py::class_<InstantActionAssignmentResult>(
    m_master, "InstantActionAssignmentResult")
    .def_readonly("decision", &InstantActionAssignmentResult::decision)
    .def_readonly("errors", &InstantActionAssignmentResult::errors)
    .def(
      "__bool__",
      [](const InstantActionAssignmentResult& result) {
        return static_cast<bool>(result);
      });

  py::class_<AGV, std::shared_ptr<AGV>>(m_master, "AGV")
    .def("get_manufacturer", &AGV::get_manufacturer)
    .def("get_serial_number", &AGV::get_serial_number)
    .def("get_agv_id", &AGV::get_agv_id)
    .def("is_connected", &AGV::is_connected)
    .def("get_connection_status", &AGV::get_connection_status)
    .def("get_operational_state", &AGV::get_operational_state)
    .def("get_last_state", &AGV::get_last_state)
    .def("has_active_order", &AGV::has_active_order)
    .def("get_pending_order_count", &AGV::get_pending_order_count)
    .def(
      "cancel_pending_orders", &AGV::cancel_pending_orders,
      py::call_guard<py::gil_scoped_release>());

  py::class_<
    VDA5050Master, PyVDA5050Master, std::shared_ptr<VDA5050Master>>(
    m_master, "VDA5050Master")
    .def(
      py::init<std::shared_ptr<MqttClientInterface>>(),
      py::arg("mqtt_client"))
    .def_static(
      "make",
      [](std::shared_ptr<MqttClientInterface> mqtt_client)
        -> std::shared_ptr<VDA5050Master> {
        return std::make_shared<PyVDA5050Master>(std::move(mqtt_client));
      },
      py::arg("mqtt_client"))
    .def(
      "connect", &VDA5050Master::connect,
      py::call_guard<py::gil_scoped_release>())
    .def(
      "disconnect", &VDA5050Master::disconnect,
      py::call_guard<py::gil_scoped_release>())
    .def("is_connected", &VDA5050Master::is_connected)
    .def(
      "onboard_agv",
      py::overload_cast<
        const std::string&, const std::string&, std::size_t, bool>(
        &VDA5050Master::onboard_agv),
      py::arg("manufacturer"), py::arg("serial_number"),
      py::arg("max_queue_size") = 10, py::arg("drop_oldest") = true,
      py::call_guard<py::gil_scoped_release>())
    .def(
      "offboard_agv", &VDA5050Master::offboard_agv,
      py::arg("manufacturer"), py::arg("serial_number"),
      py::call_guard<py::gil_scoped_release>())
    .def(
      "is_agv_onboarded", &VDA5050Master::is_agv_onboarded,
      py::arg("manufacturer"), py::arg("serial_number"))
    .def("get_onboarded_agvs", &VDA5050Master::get_onboarded_agvs)
    .def(
      "get_agv", &VDA5050Master::get_agv, py::arg("manufacturer"),
      py::arg("serial_number"))
    .def(
      "assign_order", &VDA5050Master::assign_order,
      py::arg("manufacturer"), py::arg("serial_number"), py::arg("order"),
      py::call_guard<py::gil_scoped_release>())
    .def(
      "publish_order", &VDA5050Master::publish_order,
      py::arg("manufacturer"), py::arg("serial_number"), py::arg("order"),
      py::call_guard<py::gil_scoped_release>())
    .def(
      "assign_instant_actions", &VDA5050Master::assign_instant_actions,
      py::arg("manufacturer"), py::arg("serial_number"),
      py::arg("actions"), py::call_guard<py::gil_scoped_release>())
    .def(
      "publish_instant_actions", &VDA5050Master::publish_instant_actions,
      py::arg("manufacturer"), py::arg("serial_number"),
      py::arg("actions"), py::call_guard<py::gil_scoped_release>())
    .def(
      "load_layout_from_config",
      [](VDA5050Master& self, const std::string& path) {
        const auto result = self.load_layout_from_config(path);
        std::vector<std::string> errors;
        errors.reserve(result.errors.size());
        for (const auto& error : result.errors)
        {
          errors.push_back(error.description);
        }
        return std::make_pair(static_cast<bool>(result), std::move(errors));
      },
      py::arg("path"), py::call_guard<py::gil_scoped_release>());

  auto m_rmf_migration =
    m.def_submodule("rmf_migration", "Open-RMF style migration API");

  py::class_<ActivityIdentifier>(m_rmf_migration, "ActivityIdentifier")
    .def(
      py::init<std::optional<std::string>, std::optional<std::string>>(),
      py::arg("order_id") = std::nullopt, py::arg("action_id") = std::nullopt)
    .def_property_readonly("order_id", &ActivityIdentifier::order_id)
    .def_property_readonly("action_id", &ActivityIdentifier::action_id)
    .def("__eq__", &ActivityIdentifier::operator==)
    .def("__ne__", &ActivityIdentifier::operator!=);

  py::class_<RobotState>(m_rmf_migration, "RobotState")
    .def(
      py::init<std::string, std::array<double, 3>, double>(), py::arg("map"),
      py::arg("position"), py::arg("battery_soc"))
    .def_property("map", &RobotState::map, &RobotState::set_map)
    .def_property("position", &RobotState::position, &RobotState::set_position)
    .def_property(
      "battery_state_of_charge", &RobotState::battery_state_of_charge,
      &RobotState::set_battery_state_of_charge);

  py::class_<RobotConfiguration>(m_rmf_migration, "RobotConfiguration")
    .def(
      py::init<std::string, std::string, std::string, std::string>(),
      py::arg("manufacturer"), py::arg("serial_number"),
      py::arg("interface_name") = "uagv", py::arg("version") = "2.0.0")
    .def_readwrite("manufacturer", &RobotConfiguration::manufacturer)
    .def_readwrite("serial_number", &RobotConfiguration::serial_number)
    .def_readwrite("interface_name", &RobotConfiguration::interface_name)
    .def_readwrite("version", &RobotConfiguration::version)
    .def_readwrite("factsheet", &RobotConfiguration::factsheet);

  py::class_<Destination>(m_rmf_migration, "Destination")
    .def_property_readonly("map", &Destination::map)
    .def_property_readonly("position", &Destination::position)
    .def_property_readonly("xy", &Destination::xy)
    .def_property_readonly("yaw", &Destination::yaw)
    .def_property_readonly("graph_index", &Destination::graph_index)
    .def_property_readonly("name", &Destination::name)
    .def_property_readonly("speed_limit", &Destination::speed_limit);

  py::class_<CommandExecution>(m_rmf_migration, "CommandExecution")
    .def("finished", &CommandExecution::finished)
    .def("failed", &CommandExecution::failed)
    .def("okay", &CommandExecution::okay)
    .def("is_finished", &CommandExecution::is_finished)
    .def_property_readonly("identifier", &CommandExecution::identifier);

  py::class_<RobotCallbacks>(m_rmf_migration, "RobotCallbacks")
    .def(
      py::init<NavigationRequest, StopRequest, ActionExecutor>(),
      py::arg("navigate"), py::arg("stop"), py::arg("action_executor"))
    .def_property_readonly("navigate", &RobotCallbacks::navigate)
    .def_property_readonly("stop", &RobotCallbacks::stop)
    .def_property_readonly("action_executor", &RobotCallbacks::action_executor)
    .def_property(
      "localize", &RobotCallbacks::localize,
      &RobotCallbacks::with_localization);

  py::class_<RobotUpdateHandle, std::shared_ptr<RobotUpdateHandle>>(
    m_rmf_migration, "RobotUpdateHandle")
    .def("update", &RobotUpdateHandle::update)
    .def("more", [](RobotUpdateHandle& self) { return self.more(); });

  py::class_<FleetConfiguration>(m_rmf_migration, "FleetConfiguration")
    .def(
      py::init<std::string, std::string, std::string, int>(),
      py::arg("fleet_name"), py::arg("broker_uri"), py::arg("client_id_prefix"),
      py::arg("update_interval") = 30)
    .def_property(
      "fleet_name", &FleetConfiguration::fleet_name,
      &FleetConfiguration::set_fleet_name)
    .def_property(
      "broker_uri", &FleetConfiguration::broker_uri,
      &FleetConfiguration::set_broker_uri)
    .def_property(
      "client_id_prefix", &FleetConfiguration::client_id_prefix,
      &FleetConfiguration::set_client_id_prefix)
    .def_property(
      "update_interval", &FleetConfiguration::update_interval,
      &FleetConfiguration::set_update_interval)
    .def_property_readonly("known_robots", &FleetConfiguration::known_robots)
    .def(
      "add_known_robot_configuration",
      &FleetConfiguration::add_known_robot_configuration)
    .def(
      "get_known_robot_configuration",
      &FleetConfiguration::get_known_robot_configuration);

  py::class_<FleetUpdateHandle, std::shared_ptr<FleetUpdateHandle>>(
    m_rmf_migration, "FleetUpdateHandle")
    .def("add_robot", &FleetUpdateHandle::add_robot);

  py::class_<Adapter, std::shared_ptr<Adapter>>(m_rmf_migration, "Adapter")
    .def_static("make", &Adapter::make)
    .def(
      "add_vda5050_fleet", &Adapter::add_vda5050_fleet,
      py::arg("configuration"))
    .def("start", &Adapter::start)
    .def("stop", &Adapter::stop);
}
