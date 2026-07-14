from dataclasses import dataclass
from typing import Optional

from models import Brake, Car, CarType, Engine, Steering


@dataclass
class CarBuilder:
    car_type: Optional[CarType] = None
    engine: Optional[Engine] = None
    brake: Optional[Brake] = None
    steering: Optional[Steering] = None

    def select_car_type(self, value: int) -> CarType:
        self.car_type = CarType(value)
        return self.car_type

    def select_engine(self, value: int) -> Engine:
        self.engine = Engine(value)
        return self.engine

    def select_brake(self, value: int) -> Brake:
        self.brake = Brake(value)
        return self.brake

    def select_steering(self, value: int) -> Steering:
        self.steering = Steering(value)
        return self.steering

    def build(self) -> Car:
        assert self.car_type is not None
        assert self.engine is not None
        assert self.brake is not None
        assert self.steering is not None
        return Car(self.car_type, self.engine, self.brake, self.steering)
