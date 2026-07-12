# MQTT Master/Adapter Pair

These two scripts demonstrate one VDA5050 robot adapter and one
`VDA5050Master` communicating through the same anonymous MQTT broker.

## Prerequisites

Install the package:

```bash
cd vda5050-python
uv sync --reinstall-package vda5050 --no-cache
```

The current Python transport surface does not expose MQTT username, password,
or TLS configuration, so this example expects an anonymous local broker.

## Run

Start the master first:

```bash
# Terminal 1
mosquitto -v
```

Start the master first:

```bash
# Terminal 2
uv run examples/mqtt_pair/master.py
```

In another terminal, start the robot adapter:

```bash
# Terminal 3
uv run examples/mqtt_pair/robot_adapter.py
```

Both scripts use this identity and topic prefix:

```text
manufacturer: ACME
serial number: AGV-001
topics: uagv/v2/ACME/AGV-001/...
```

The master should print an `AGV online` event. The current internal client
adapter publishes its periodic state every 30 seconds, so the first state line
may take up to 30 seconds to appear. Stop either process with `Ctrl+C`.

The broker and identity can be changed for both scripts with:

```bash
export MQTT_BROKER=tcp://localhost:1883
export VDA5050_MANUFACTURER=ACME
export VDA5050_SERIAL_NUMBER=AGV-001
```

MQTT client IDs must remain unique. Override them independently with
`MASTER_MQTT_CLIENT_ID` and `ROBOT_MQTT_CLIENT_ID`.