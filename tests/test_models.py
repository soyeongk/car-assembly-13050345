from models import Brake, Car, CarType, Engine, Steering


class TestEnumValues:
    def test_car_type_values(self):
        assert CarType.SEDAN == 1
        assert CarType.SUV == 2
        assert CarType.TRUCK == 3

    def test_engine_values(self):
        assert Engine.GM == 1
        assert Engine.TOYOTA == 2
        assert Engine.WIA == 3
        assert Engine.BROKEN == 4

    def test_brake_values(self):
        assert Brake.MANDO == 1
        assert Brake.CONTINENTAL == 2
        assert Brake.BOSCH == 3

    def test_steering_values(self):
        assert Steering.BOSCH == 1
        assert Steering.MOBIS == 2


class TestCar:
    def test_car_holds_all_selected_parts(self):
        car = Car(CarType.SEDAN, Engine.GM, Brake.MANDO, Steering.MOBIS)
        assert car.car_type == CarType.SEDAN
        assert car.engine == Engine.GM
        assert car.brake == Brake.MANDO
        assert car.steering == Steering.MOBIS

    def test_car_is_immutable(self):
        car = Car(CarType.SEDAN, Engine.GM, Brake.MANDO, Steering.MOBIS)
        try:
            car.car_type = CarType.SUV
            assert False, "Car는 frozen dataclass여야 합니다"
        except AttributeError:
            pass
