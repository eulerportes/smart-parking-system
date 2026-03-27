import json
import os
import time
from app.services.gate_service import open_gate


class ParkingService:
    def __init__(
        self,
        ttl_seconds=10,
        min_confidence=80.0,
        capacity=10,
        state_file="logs/parking_state.json",
        whitelist_file="logs/whitelist.json"
    ):
        self.vehicles_inside = set()
        self.last_seen = {}
        self.ttl_seconds = ttl_seconds
        self.min_confidence = min_confidence
        self.capacity = capacity
        self.whitelist = set()
        self.state_file = state_file
        self.whitelist_file = whitelist_file

        self._ensure_dirs()
        self.load_whitelist()
        self.load_state()

    def _ensure_dirs(self):
        state_dir = os.path.dirname(self.state_file)
        if state_dir:
            os.makedirs(state_dir, exist_ok=True)

        whitelist_dir = os.path.dirname(self.whitelist_file)
        if whitelist_dir:
            os.makedirs(whitelist_dir, exist_ok=True)

    def load_whitelist(self):
        if not os.path.exists(self.whitelist_file):
            self.whitelist = set()
            return

        try:
            with open(self.whitelist_file, "r", encoding="utf-8") as f:
                data = json.load(f)

            if isinstance(data, list):
                self.whitelist = {
                    str(plate).strip().upper()
                    for plate in data
                    if str(plate).strip()
                }
            else:
                print("[WHITELIST] formato inválido: esperado JSON array")
                self.whitelist = set()

            print(f"[WHITELIST] carregada com {len(self.whitelist)} placa(s)")

        except Exception as e:
            print(f"[WHITELIST] load error: {e}")
            self.whitelist = set()

    def save_state(self):
        data = {
            "vehicles_inside": sorted(list(self.vehicles_inside)),
            "last_seen": self.last_seen,
            "ttl_seconds": self.ttl_seconds,
            "min_confidence": self.min_confidence,
            "capacity": self.capacity
        }

        with open(self.state_file, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def load_state(self):
        if not os.path.exists(self.state_file):
            return

        try:
            with open(self.state_file, "r", encoding="utf-8") as f:
                data = json.load(f)

            self.vehicles_inside = set(data.get("vehicles_inside", []))
            self.last_seen = data.get("last_seen", {})
            self.ttl_seconds = data.get("ttl_seconds", self.ttl_seconds)
            self.min_confidence = data.get("min_confidence", self.min_confidence)
            self.capacity = data.get("capacity", self.capacity)

        except Exception as e:
            print(f"[STATE] load error: {e}")

    def get_status(self):
        inside_list = sorted(list(self.vehicles_inside))
        inside_count = len(inside_list)

        return {
            "inside_count": inside_count,
            "capacity": self.capacity,
            "available_spots": max(self.capacity - inside_count, 0),
            "vehicles_inside": inside_list,
            "ttl_seconds": self.ttl_seconds,
            "min_confidence": self.min_confidence,
            "whitelist_count": len(self.whitelist),
            "whitelist": sorted(list(self.whitelist))
        }

    def process_event(self, event):
        plate = event.get("plate", "").strip().upper()
        direction = event.get("direction", "").strip().lower()
        confidence = float(event.get("confidence", 0) or 0)
        now = time.time()

        if not plate:
            return {
                "status": "error",
                "reason": "missing_plate"
            }

        if confidence < self.min_confidence:
            return {
                "status": "ignored",
                "reason": "low_confidence",
                "plate": plate,
                "confidence": confidence,
                "min_confidence": self.min_confidence
            }

        last_time = self.last_seen.get(plate)
        if last_time and (now - last_time) < self.ttl_seconds:
            return {
                "status": "ignored",
                "reason": "duplicate_ttl",
                "plate": plate,
                "ttl_seconds": self.ttl_seconds
            }

        self.last_seen[plate] = now

        if direction == "in":
            if plate in self.vehicles_inside:
                return {
                    "status": "ignored",
                    "reason": "already_inside",
                    "plate": plate,
                    "inside_count": len(self.vehicles_inside),
                    "capacity": self.capacity,
                    "whitelisted": plate in self.whitelist
                }

            if len(self.vehicles_inside) >= self.capacity and plate not in self.whitelist:
                return {
                    "status": "denied",
                    "reason": "parking_full",
                    "plate": plate,
                    "inside_count": len(self.vehicles_inside),
                    "capacity": self.capacity,
                    "whitelisted": False
                }

            self.vehicles_inside.add(plate)
            self.save_state()
            open_gate(reason="entry_allowed", plate=plate)

            return {
                "status": "entry",
                "plate": plate,
                "inside_count": len(self.vehicles_inside),
                "capacity": self.capacity,
                "gate_opened": True,
                "whitelisted": plate in self.whitelist
            }

        if direction == "out":
            if plate not in self.vehicles_inside:
                return {
                    "status": "ignored",
                    "reason": "not_found_inside",
                    "plate": plate,
                    "inside_count": len(self.vehicles_inside),
                    "capacity": self.capacity,
                    "whitelisted": plate in self.whitelist
                }

            self.vehicles_inside.remove(plate)
            self.save_state()
            open_gate(reason="exit_allowed", plate=plate)

            return {
                "status": "exit",
                "plate": plate,
                "inside_count": len(self.vehicles_inside),
                "capacity": self.capacity,
                "gate_opened": True,
                "whitelisted": plate in self.whitelist
            }

        return {
            "status": "error",
            "reason": "invalid_direction",
            "plate": plate,
            "direction": direction
        }