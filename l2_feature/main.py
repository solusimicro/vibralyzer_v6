"""
main.py

L2 Feature Processing Layer
Industrial Clean Architecture
"""

import yaml
import json

from mqtt_client import MQTTClient
from data_buffer import DataBuffer
from trend_engine import TrendEngine
from rule_engine import RuleEngine
from final_status import FinalStatus
from recommendation import RecommendationEngine
from rul_engine import ProbabilisticRUL
from interpretation import InterpretationEngine
from publisher import L2Publisher
from fleet_risk import FleetRiskEngine
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

# ==========================================================
# LOAD CONFIG
# ==========================================================

config = yaml.safe_load(open("config.yaml"))

# ==========================================================
# INIT ENGINES
# ==========================================================

buffer = DataBuffer(config["trend"]["window_size"])
trend_engine = TrendEngine()

class_cfg = config["machine_classes"]["CLASS_II"]

rule_engine = RuleEngine(class_cfg)
interpret_engine = InterpretationEngine(class_cfg)

final_engine = FinalStatus(
    class_cfg,
    config["health"]["failure_threshold"]
)

recommend_engine = RecommendationEngine(class_cfg)

rul_engine = ProbabilisticRUL(
    config["health"]["failure_threshold"]
)

fleet_engine = FleetRiskEngine()

# ==========================================================
# MQTT CALLBACK
# ==========================================================

def on_message(client, userdata, msg):

    payload = json.loads(msg.payload.decode())

    asset_id = payload.get("asset")
    device_id = payload.get("device")

    if not asset_id or not device_id:
        return

    # -------------------------
    # BUFFER
    # -------------------------
    buffer.update(asset_id, device_id, payload)
    data = buffer.get(asset_id, device_id)

    if not data:
        return

    # -------------------------
    # TREND
    # -------------------------
    trend = trend_engine.analyze(data)

    # -------------------------
    # RULE
    # -------------------------
    rule_out = rule_engine.evaluate(payload, trend)

    # -------------------------
    # INTERPRETATION
    # -------------------------
    interpret_out = interpret_engine.interpret(
        payload,
        trend,
        rule_out
    )

    # -------------------------
    # RUL
    # -------------------------
    health_series = list(data["health"])
    rul_output = rul_engine.calculate(health_series)

    # -------------------------
    # FINAL STATUS (Use Interpretation)
    # -------------------------
    final_status = final_engine.determine(
        payload,
        interpret_out
    )

    # -------------------------
    # RECOMMENDATION
    # -------------------------
    recommendation = recommend_engine.generate(
        asset_id=asset_id,
        final_status=final_status,
        fault_type=interpret_out.get("fault_type"),
        fault_stage=interpret_out.get("fault_stage"),
        estimated_rul_days=rul_output.get("rul_expected_days"),
    )
    
    # -------------------------
    # ASSET RISK
    # --------------------------
    asset_risk = fleet_engine.calculate_asset_risk(
        asset_id=asset_id,
        severity_score=interpret_out.get("severity_score", 0),
        prob_failure_7d=rul_output.get("prob_failure_7d", 0),
        final_status=final_status,
    )

    fleet_risk = fleet_engine.calculate_fleet_risk()

    if fleet_risk:
        publisher.publish_fleet_risk(fleet_risk)

    # -------------------------
    # OUTPUT MERGE (Clean)
    # -------------------------
    output = {
        **payload,
        **interpret_out,   # Already includes fault_type & confidence refined
        **rul_output,
        "final_status": final_status,
        **recommendation,
        **asset_risk,
    }

    # -------------------------
    # PUBLISH
    # -------------------------
    mode = config["publish"]["mode"]

    if mode == "layered":
        #publisher.publish_rule(asset_id, device_id, rule_out) --> add topic in publsher
        publisher.publish_interpretation(asset_id, device_id, interpret_out)
        publisher.publish_rul(asset_id, device_id, rul_output)
        #publisher.publish_recommendation(asset_id, device_id, recommendation) --> add topic in publsher

    publisher.publish_final(asset_id, device_id, output)

# ==========================================================
# START MQTT
# ==========================================================

mqtt_client = MQTTClient(
    config["broker"]["host"],
    config["broker"]["port"],
    config["broker"]["topic_sub"],
    on_message,
)

publisher = L2Publisher(
    mqtt_client.client,
    base_topic="vibration"
)

publisher.publish_heartbeat()

mqtt_client.loop_forever()


