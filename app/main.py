from services.parking_service import ParkingService


def main():
    parking = ParkingService()

    print("=== Smart Parking System ===")

    # Simulação de entrada
    print(parking.vehicle_entry("ABC1234"))
    print(parking.vehicle_entry("XYZ9876"))

    print("\nOcupação atual:", parking.current_occupancy())

    # Simulação de saída
    result = parking.vehicle_exit("ABC1234")
    print("\nSaída:", result)

    print("\nOcupação final:", parking.current_occupancy())


if __name__ == "__main__":
    main()
