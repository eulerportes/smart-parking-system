from flask import Flask, request, jsonify
from app.services.parking_service import ParkingService

app = Flask(__name__)
parking = ParkingService()


@app.route("/")
def home():
    return "Smart Parking API Running"


@app.route("/entry", methods=["POST"])
def vehicle_entry():
    data = request.json
    plate = data.get("plate")

    result = parking.vehicle_entry(plate)
    return jsonify({"message": result})


@app.route("/exit", methods=["POST"])
def vehicle_exit():
    data = request.json
    plate = data.get("plate")

    result = parking.vehicle_exit(plate)
    return jsonify(result)


@app.route("/occupancy", methods=["GET"])
def occupancy():
    return jsonify({"occupancy": parking.current_occupancy()})


if __name__ == "__main__":
    app.run(debug=True)
