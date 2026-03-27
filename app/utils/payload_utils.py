from datetime import datetime


def normalize_payload(data):
    """
    Normaliza diferentes formatos de payload para um padrão interno.
    """

    def get_value(*keys, default=None):
        for key in keys:
            if key in data and data[key] not in (None, ""):
                return data[key]
        return default

    plate = get_value("plate", "PlateNumber", "plateNo", "license", default="")
    confidence = get_value("confidence", "score", "plateConfidence", default=0)
    timestamp = get_value("timestamp", "SnapTime", "eventTime", default=None)
    direction = get_value("direction", "Direction", "eventType", default="in")
    device = get_value("device", "DeviceName", "DevName", default="SIM")

    try:
        confidence = float(confidence)
    except (TypeError, ValueError):
        confidence = 0.0

    if not timestamp:
        timestamp = datetime.now().isoformat()

    return {
        "plate": str(plate).strip().upper(),
        "confidence": confidence,
        "timestamp": timestamp,
        "direction": str(direction).strip().lower(),
        "device": str(device).strip(),
        "raw": data
    }