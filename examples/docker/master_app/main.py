"""Run a VDA5050 master that observes the paired robot adapter."""

from __future__ import annotations

import logging
import os
import time
# import uvicorn 
# from  fastapi import FastAPI
# import dotenv
# from pydantic import BaseField, Field
from vda5050 import VDA5050Master, create_default_mqtt_client

BROKER_URI = os.environ.get("MQTT_BROKER", "tcp://localhost:1883")
MQTT_CLIENT_ID = os.environ.get("MASTER_MQTT_CLIENT_ID", "example-master")
MANUFACTURER = os.environ.get("VDA5050_MANUFACTURER", "ACME")
SERIAL_NUMBER = os.environ.get("VDA5050_SERIAL_NUMBER", "AGV-001")
LOGGER = logging.getLogger(__name__)


class ExampleMaster(VDA5050Master):
    def on_connect(self, agv_id) -> None:
        LOGGER.info("AGV online: %s", agv_id)

    def on_offline(self, agv_id) -> None:
        LOGGER.info("AGV offline: %s", agv_id)

    def on_connection_broken(self, agv_id) -> None:
        LOGGER.warning("AGV connection broken: %s", agv_id)

    def on_state(self, agv_id, state) -> None:
        position = state.agv_position
        pose = None if position is None else (position.x, position.y, position.theta)
        LOGGER.info(
            "State: %s pose=%s battery=%s",
            agv_id,
            pose,
            state.battery_state.battery_charge,
        )


def main() -> None:
    # app = FastAPI()
    # @app.get("/")
    # async def root():
    #     return {"message": "Hello World"}

    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s"
    )
    mqtt_client = create_default_mqtt_client(BROKER_URI, MQTT_CLIENT_ID)
    master = ExampleMaster(mqtt_client)
    master.connect()
    master.onboard_agv(MANUFACTURER, SERIAL_NUMBER)
    LOGGER.info(
        "Master listening for %s/%s via %s",
        MANUFACTURER,
        SERIAL_NUMBER,
        BROKER_URI,
    )
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        pass
    finally:
        master.offboard_agv(MANUFACTURER, SERIAL_NUMBER)
        master.disconnect()


if __name__ == "__main__":

    main()
