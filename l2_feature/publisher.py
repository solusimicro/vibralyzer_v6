"""
publisher.py

L2 Publishing Layer
Industrial-safe version
"""

import json
import logging
from datetime import datetime


class L2Publisher:

    def __init__(self, mqtt_client, base_topic="vibration"):

        self.client = mqtt_client
        self.base_topic = base_topic

    # ==========================================================
    # INTERNAL SAFE PUBLISH
    # ==========================================================

    def _safe_publish(self, topic, payload, qos=1, retain=False):

        try:
            result = self.client.publish(
                topic,
                json.dumps(payload),
                qos=qos,
                retain=retain
            )

            if result.rc != 0:
                logging.error(f"Publish failed → {topic} | RC={result.rc}")
            else:
                logging.debug(f"Published → {topic}")

        except Exception as e:
            logging.exception(f"MQTT Publish Exception → {topic} | {str(e)}")

    # ==========================================================
    # CONSOLIDATED FINAL STATUS
    # ==========================================================

    def publish_final(self, asset_id, device_id, payload):

        topic = f"{self.base_topic}/final_status/{asset_id}/{device_id}"
        self._safe_publish(topic, payload, qos=1)

    # ==========================================================
    # LAYERED SUPPORT
    # ==========================================================

    def publish_interpretation(self, asset_id, device_id, payload):

        topic = f"{self.base_topic}/interpretation/{asset_id}/{device_id}"
        self._safe_publish(topic, payload, qos=1)

    def publish_rul(self, asset_id, device_id, payload):

        topic = f"{self.base_topic}/rul/{asset_id}/{device_id}"
        self._safe_publish(topic, payload, qos=1)

    def publish_fleet_risk(self, fleet_data):

        topic = f"{self.base_topic}/fleet/risk"
        self._safe_publish(topic, fleet_data, qos=1)

    # ==========================================================
    # ERROR CHANNEL (Dead Letter)
    # ==========================================================

    def publish_error(self, error_message, raw_payload=None):

        topic = f"{self.base_topic}/l2/error"

        payload = {
            "error": error_message,
            "raw_payload": raw_payload,
            "timestamp": datetime.utcnow().isoformat()
        }

        self._safe_publish(topic, payload, qos=1)

    # ==========================================================
    # HEARTBEAT
    # ==========================================================

    def publish_heartbeat(self):

        topic = f"{self.base_topic}/system/heartbeat"

        heartbeat = {
            "service": "L2_FEATURE_ENGINE",
            "status": "RUNNING",
            "timestamp": datetime.utcnow().isoformat()
        }

        self._safe_publish(topic, heartbeat, qos=1, retain=True)

        logging.info("Heartbeat published.")
