from dataclasses import dataclass
from enum import IntEnum


class CarType(IntEnum):
    SEDAN = 1
    SUV = 2
    TRUCK = 3


class Engine(IntEnum):
    GM = 1
    TOYOTA = 2
    WIA = 3
    BROKEN = 4


class Brake(IntEnum):
    MANDO = 1
    CONTINENTAL = 2
    BOSCH = 3


class Steering(IntEnum):
    BOSCH = 1
    MOBIS = 2


@dataclass(frozen=True)
class Car:
    car_type: CarType
    engine: Engine
    brake: Brake
    steering: Steering
