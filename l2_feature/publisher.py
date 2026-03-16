"""
publisher.py

Industrial MQTT Publisher
Auto topic routing
Layered architecture support
Future Sparkplug-ready
"""

import json
import logging
from datetime import datetime


class L2Publisher:

    def __init__(self, mqtt_client, base_topic="vibration"):

        self.client = mqtt_client
        self.base_topic = base_topic

    # ==========================================================
    # LOW LEVEL PUBLISH
    # ==========================================================

    def _pub(self, topic, payload, retain=False):

        try:
            self.client.publish(
                topic,
                json.dumps(payload),
                qos=1,
                retain=retain
            )

            logging.info(f"Published → {topic}")

        except Exception as e:
            logging.error(f"Publish error {topic}: {e}")

    # ==========================================================
    # FEATURES (RAW + EDGE FEATURES)
    # ==========================================================

    def publish_features(self, asset_id, device_id, data):

        topic = f"{self.base_topic}/features/{asset_id}/{device_id}"

        payload = {
            "timestamp": data.get("timestamp"),
            "site": data.get("site"),
            "asset": data.get("asset"),
            "device": data.get("device"),
            "firmware": data.get("firmware"),

            "acc_rms": data.get("acc_rms"),
            "vel_rms": data.get("vel_rms"),
            "crest": data.get("crest"),
            "hf": data.get("hf"),
            "iso_zone": data.get("iso_zone"),
            "health_index": data.get("health_index"),
        }

        self._pub(topic, payload)

    # ==========================================================
    # INTERPRETATION
    # ==========================================================

    def publish_interpretation(self, asset_id, device_id, data):

        topic = f"{self.base_topic}/interpretation/{asset_id}/{device_id}"

        payload = {
            "fault_type": data.get("fault_type"),
            "fault_stage": data.get("fault_stage"),
            "confidence": data.get("confidence"),

            "severity_score": data.get("severity_score"),
            "industrial_severity_index": data.get("industrial_severity_index"),

            "component_scores": data.get("component_scores"),

            "dominant_indicator": data.get("dominant_indicator"),
            "pattern_validation_score": data.get("pattern_validation_score"),

            "root_indicators": data.get("root_indicators"),
            "interpreted_at": data.get("interpreted_at"),
        }

        self._pub(topic, payload)

    # ==========================================================
    # RUL
    # ==========================================================

    def publish_rul(self, asset_id, device_id, data):

        topic = f"{self.base_topic}/rul/{asset_id}/{device_id}"

        payload = {
            "rul_expected_days": data.get("rul_expected_days"),
            "rul_95_lower_bound": data.get("rul_95_lower_bound"),
            "prob_failure_7d": data.get("prob_failure_7d"),
            "rul_confidence": data.get("rul_confidence"),
            "rul_model": data.get("rul_model"),
        }

        self._pub(topic, payload)

    # ==========================================================
    # RECOMMENDATION
    # ==========================================================

    def publish_recommendation(self, asset_id, device_id, data):

        topic = f"{self.base_topic}/recommendation/{asset_id}/{device_id}"

        payload = {
            "state": data.get("state"),
            "final_status": data.get("final_status"),
            "action_code": data.get("action_code"),
            "priority": data.get("priority"),
            "recommended_within_days": data.get("recommended_within_days"),
            "estimated_rul_days": data.get("estimated_rul_days"),
        }

        self._pub(topic, payload)

    # ==========================================================
    # ASSET RISK
    # ==========================================================

    def publish_asset_risk(self, asset_id, data):

        topic = f"{self.base_topic}/asset_risk/{asset_id}"

        payload = {
            "asset_id": asset_id,
            "asset_risk_score": data.get("asset_risk_score"),
            "asset_risk_level": data.get("asset_risk_level"),
        }

        self._pub(topic, payload)
        
    # ==========================================================
    # FLEET RISK
    # ==========================================================

    def publish_fleet_risk(self, fleet_risk):

        topic = f"{self.base_topic}/fleet/risk"

        try:

            self.client.publish(
                topic,
                json.dumps(fleet_risk),
                qos=1,
                retain=False
            )

            logging.info(f"Published → {topic}")

        except Exception as e:

            logging.error(f"Publish error {topic}: {e}")

    # ==========================================================
    # CONSOLIDATED FINAL STATUS
    # ==========================================================

    def publish_final(self, asset_id, device_id, payload):

        topic = f"{self.base_topic}/final_status/{asset_id}/{device_id}"

        self._pub(topic, payload)

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

        self._pub(topic, heartbeat, retain=True)

        logging.info("Heartbeat published.")

