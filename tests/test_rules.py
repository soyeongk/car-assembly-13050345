from models import Brake, Car, CarType, Engine, Steering
from rules import evaluate_run, evaluate_test, is_compatible


def make_car(car_type=CarType.SEDAN, engine=Engine.GM, brake=Brake.MANDO, steering=Steering.MOBIS):
    return Car(car_type, engine, brake, steering)


class TestIsCompatible:
    def test_bosch_brake_with_bosch_steering_ok(self):
        car = make_car(brake=Brake.BOSCH, steering=Steering.BOSCH)
        assert is_compatible(car) is True

    def test_bosch_brake_with_non_bosch_steering_fails(self):
        car = make_car(brake=Brake.BOSCH, steering=Steering.MOBIS)
        assert is_compatible(car) is False

    def test_sedan_with_continental_brake_fails(self):
        car = make_car(car_type=CarType.SEDAN, brake=Brake.CONTINENTAL)
        assert is_compatible(car) is False

    def test_suv_with_toyota_engine_fails(self):
        car = make_car(car_type=CarType.SUV, engine=Engine.TOYOTA)
        assert is_compatible(car) is False

    def test_truck_with_wia_engine_fails(self):
        car = make_car(car_type=CarType.TRUCK, engine=Engine.WIA, brake=Brake.CONTINENTAL)
        assert is_compatible(car) is False

    def test_truck_with_mando_brake_fails(self):
        car = make_car(car_type=CarType.TRUCK, brake=Brake.MANDO)
        assert is_compatible(car) is False

    def test_valid_combination_passes(self):
        car = make_car()
        assert is_compatible(car) is True


class TestEvaluateTest:
    def test_pass_for_valid_combination(self):
        result = evaluate_test(make_car())
        assert result.ok is True
        assert result.message == "PASS"

    def test_fail_for_sedan_continental(self):
        result = evaluate_test(make_car(car_type=CarType.SEDAN, brake=Brake.CONTINENTAL))
        assert result.ok is False
        assert result.message == "FAIL\nSedan에는 Continental제동장치 사용 불가"

    def test_pass_even_when_engine_is_broken(self):
        # 원본 test_produced_car()의 실제 동작: 고장난 엔진은 호환성 규칙에 없어 PASS로 처리된다.
        result = evaluate_test(make_car(engine=Engine.BROKEN))
        assert result.ok is True
        assert result.message == "PASS"


class TestEvaluateRun:
    def test_stops_on_broken_engine(self):
        result = evaluate_run(make_car(engine=Engine.BROKEN))
        assert result.ok is False
        assert result.lines == ["엔진이 고장나있습니다.", "자동차가 움직이지 않습니다."]

    def test_stops_on_invalid_combination(self):
        result = evaluate_run(make_car(car_type=CarType.TRUCK, brake=Brake.MANDO))
        assert result.ok is False
        assert result.lines == ["자동차가 동작되지 않습니다"]

    def test_runs_on_valid_combination(self):
        result = evaluate_run(make_car())
        assert result.ok is True
        assert result.lines[-1] == "자동차가 동작됩니다."
        assert "Car Type : Sedan" in result.lines
        assert "Engine   : GM" in result.lines
        assert "Brake    : Mando" in result.lines
        assert "Steering : Mobis" in result.lines

    def test_invalid_combination_checked_before_broken_engine(self):
        # 원본 순서: is_valid_check()가 먼저 검사되고, 그 다음 고장난 엔진 체크
        result = evaluate_run(make_car(car_type=CarType.TRUCK, engine=Engine.BROKEN, brake=Brake.MANDO))
        assert result.ok is False
        assert result.lines == ["자동차가 동작되지 않습니다"]
