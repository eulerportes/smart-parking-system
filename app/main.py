from flask import Flask, request, jsonify
from app.services.parking_service import ParkingService
from app.utils.payload_utils import normalize_payload
import os
import json
from datetime import datetime

ADMIN_API_KEY = "123456"

app = Flask(__name__)
service = ParkingService()

LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)


def log_event(event, result):
    filename = os.path.join(LOG_DIR, "events.log")

    log_line = {
        "received_at": datetime.now().isoformat(),
        "event": event,
        "result": result
    }

    with open(filename, "a", encoding="utf-8") as f:
        f.write(json.dumps(log_line, ensure_ascii=False) + "\n")


@app.route("/lpr", methods=["POST"])
def lpr():
    try:
        data = request.get_json(force=True, silent=True) or {}
        normalized = normalize_payload(data)

        if not normalized["plate"]:
            return jsonify({"error": "missing_plate"}), 400

        result = service.process_event(normalized)
        log_event(normalized, result)

        print(f"[LPR] {normalized['plate']} -> {result}")

        return jsonify({
            "ok": True,
            "normalized": normalized,
            "result": result
        }), 200

    except Exception as e:
        return jsonify({
            "ok": False,
            "error": str(e)
        }), 500


@app.route("/status", methods=["GET"])
def status():
    return jsonify({
        "ok": True,
        "status": service.get_status()
    }), 200


@app.route("/vehicles", methods=["GET"])
def vehicles():
    status_data = service.get_status()
    return jsonify({
        "ok": True,
        "vehicles_inside": status_data["vehicles_inside"]
    }), 200

@app.route("/admin/reload-whitelist", methods=["POST"])
def reload_whitelist():
    try:
        api_key = request.headers.get("X-API-KEY", "").strip()

        if api_key != ADMIN_API_KEY:
            return jsonify({
                "ok": False,
                "error": "unauthorized"
            }), 401

        service.load_whitelist()

        return jsonify({
            "ok": True,
            "message": "whitelist reloaded",
            "whitelist_count": len(service.whitelist),
            "whitelist": sorted(list(service.whitelist))
        }), 200

    except Exception as e:
        return jsonify({
            "ok": False,
            "error": str(e)
        }), 500