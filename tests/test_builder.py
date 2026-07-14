import pytest

from builder import CarBuilder
from models import Brake, Car, CarType, Engine, Steering


@pytest.fixture
def builder():
    return CarBuilder()


class TestSelectMethods:
    def test_select_car_type_sets_field_and_returns_value(self, builder):
        result = builder.select_car_type(CarType.SUV)
        assert builder.car_type == CarType.SUV
        assert result == CarType.SUV

    def test_select_engine_sets_field_and_returns_value(self, builder):
        result = builder.select_engine(Engine.TOYOTA)
        assert builder.engine == Engine.TOYOTA
        assert result == Engine.TOYOTA

    def test_select_brake_sets_field_and_returns_value(self, builder):
        result = builder.select_brake(Brake.MANDO)
        assert builder.brake == Brake.MANDO
        assert result == Brake.MANDO

    def test_select_steering_sets_field_and_returns_value(self, builder):
        result = builder.select_steering(Steering.MOBIS)
        assert builder.steering == Steering.MOBIS
        assert result == Steering.MOBIS


class TestBuild:
    def test_build_returns_car_with_selected_parts(self, builder):
        builder.select_car_type(CarType.SEDAN)
        builder.select_engine(Engine.GM)
        builder.select_brake(Brake.MANDO)
        builder.select_steering(Steering.MOBIS)

        car = builder.build()

        assert car == Car(CarType.SEDAN, Engine.GM, Brake.MANDO, Steering.MOBIS)

    def test_build_fails_when_incomplete(self, builder):
        builder.select_car_type(CarType.SEDAN)
        with pytest.raises(AssertionError):
            builder.build()
