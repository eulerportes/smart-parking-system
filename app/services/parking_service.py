from datetime import datetime


class ParkingService:
    def __init__(self):
        self.vehicles_inside = {}

    def vehicle_entry(self, plate: str):
        if plate in self.vehicles_inside:
            return f"Vehicle {plate} already inside"

        self.vehicles_inside[plate] = datetime.now()
        return f"Vehicle {plate} entered at {self.vehicles_inside[plate]}"

    def vehicle_exit(self, plate: str):
        if plate not in self.vehicles_inside:
            return f"Vehicle {plate} not found"

        entry_time = self.vehicles_inside.pop(plate)
        exit_time = datetime.now()

        duration = exit_time - entry_time

        return {
            "plate": plate,
            "entry": entry_time,
            "exit": exit_time,
            "duration": str(duration)
        }

    def current_occupancy(self):
        return len(self.vehicles_inside)
