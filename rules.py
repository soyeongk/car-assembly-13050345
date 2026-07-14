from dataclasses import dataclass
from typing import Callable, Optional

from models import Brake, Car, CarType, Engine, Steering


@dataclass(frozen=True)
class CompatibilityRule:
    name: str
    violates: Callable[[Car], bool]
    message: str


RULES: list[CompatibilityRule] = [
    CompatibilityRule(
        "sedan_no_continental",
        lambda c: c.car_type == CarType.SEDAN and c.brake == Brake.CONTINENTAL,
        "Sedan에는 Continental제동장치 사용 불가",
    ),
    CompatibilityRule(
        "suv_no_toyota",
        lambda c: c.car_type == CarType.SUV and c.engine == Engine.TOYOTA,
        "SUV에는 TOYOTA엔진 사용 불가",
    ),
    CompatibilityRule(
        "truck_no_wia",
        lambda c: c.car_type == CarType.TRUCK and c.engine == Engine.WIA,
        "Truck에는 WIA엔진 사용 불가",
    ),
    CompatibilityRule(
        "truck_no_mando",
        lambda c: c.car_type == CarType.TRUCK and c.brake == Brake.MANDO,
        "Truck에는 Mando제동장치 사용 불가",
    ),
    CompatibilityRule(
        "bosch_brake_needs_bosch_steering",
        lambda c: c.brake == Brake.BOSCH and c.steering != Steering.BOSCH,
        "Bosch제동장치에는 Bosch조향장치 이외 사용 불가",
    ),
]


def first_violation(car: Car) -> Optional[CompatibilityRule]:
    for rule in RULES:
        if rule.violates(car):
            return rule
    return None


def is_compatible(car: Car) -> bool:
    return first_violation(car) is None


@dataclass(frozen=True)
class RunResult:
    ok: bool
    lines: list[str]


@dataclass(frozen=True)
class TestResult:
    ok: bool
    message: str


CAR_TYPE_LABELS = {CarType.SEDAN: "Sedan", CarType.SUV: "SUV", CarType.TRUCK: "Truck"}
ENGINE_LABELS = {Engine.GM: "GM", Engine.TOYOTA: "TOYOTA", Engine.WIA: "WIA"}
BRAKE_LABELS = {Brake.MANDO: "Mando", Brake.CONTINENTAL: "Continental", Brake.BOSCH: "Bosch"}
STEERING_LABELS = {Steering.BOSCH: "Bosch", Steering.MOBIS: "Mobis"}


def evaluate_run(car: Car) -> RunResult:
    if not is_compatible(car):
        return RunResult(False, ["자동차가 동작되지 않습니다"])
    if car.engine == Engine.BROKEN:
        return RunResult(False, ["엔진이 고장나있습니다.", "자동차가 움직이지 않습니다."])
    return RunResult(
        True,
        [
            f"Car Type : {CAR_TYPE_LABELS[car.car_type]}",
            f"Engine   : {ENGINE_LABELS[car.engine]}",
            f"Brake    : {BRAKE_LABELS[car.brake]}",
            f"Steering : {STEERING_LABELS[car.steering]}",
            "자동차가 동작됩니다.",
        ],
    )


def evaluate_test(car: Car) -> TestResult:
    violation = first_violation(car)
    if violation is not None:
        return TestResult(False, f"FAIL\n{violation.message}")
    return TestResult(True, "PASS")
