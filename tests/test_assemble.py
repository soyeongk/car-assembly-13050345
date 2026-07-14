import pytest

import assemble


@pytest.fixture(autouse=True)
def reset_globals():
    assemble.q0 = 0
    assemble.q1 = 0
    assemble.q2 = 0
    assemble.q3 = 0
    assemble.q4 = 0
    yield
    assemble.q0 = 0
    assemble.q1 = 0
    assemble.q2 = 0
    assemble.q3 = 0
    assemble.q4 = 0


class TestIsValidRange:
    @pytest.mark.parametrize("ans", [1, 2, 3])
    def test_step0_valid(self, ans):
        assert assemble.is_valid_range(0, ans) is True

    @pytest.mark.parametrize("ans", [0, 4])
    def test_step0_invalid(self, ans):
        assert assemble.is_valid_range(0, ans) is False

    @pytest.mark.parametrize("ans", [0, 1, 2, 3, 4])
    def test_step1_valid(self, ans):
        assert assemble.is_valid_range(1, ans) is True

    @pytest.mark.parametrize("ans", [-1, 5])
    def test_step1_invalid(self, ans):
        assert assemble.is_valid_range(1, ans) is False

    @pytest.mark.parametrize("ans", [0, 1, 2, 3])
    def test_step2_valid(self, ans):
        assert assemble.is_valid_range(2, ans) is True

    @pytest.mark.parametrize("ans", [-1, 4])
    def test_step2_invalid(self, ans):
        assert assemble.is_valid_range(2, ans) is False

    @pytest.mark.parametrize("ans", [0, 1, 2])
    def test_step3_valid(self, ans):
        assert assemble.is_valid_range(3, ans) is True

    @pytest.mark.parametrize("ans", [-1, 3])
    def test_step3_invalid(self, ans):
        assert assemble.is_valid_range(3, ans) is False

    @pytest.mark.parametrize("ans", [0, 1, 2])
    def test_step4_valid(self, ans):
        assert assemble.is_valid_range(4, ans) is True

    @pytest.mark.parametrize("ans", [-1, 3])
    def test_step4_invalid(self, ans):
        assert assemble.is_valid_range(4, ans) is False


class TestSelectFunctions:
    def test_select_car_type_sets_q0(self):
        assemble.select_car_type(assemble.SUV)
        assert assemble.q0 == assemble.SUV

    def test_select_engine_sets_q1(self):
        assemble.select_engine(assemble.TOYOTA)
        assert assemble.q1 == assemble.TOYOTA

    def test_select_brake_sets_q2(self):
        assemble.select_brake(assemble.MANDO)
        assert assemble.q2 == assemble.MANDO

    def test_select_steering_sets_q3(self):
        assemble.select_steering(assemble.MOBIS)
        assert assemble.q3 == assemble.MOBIS


class TestIsValidCheck:
    # 제한조건 1: Bosch 제동장치는 Bosch 조향장치와만 호환
    def test_bosch_brake_with_bosch_steering_ok(self):
        assemble.select_car_type(assemble.SEDAN)
        assemble.select_engine(assemble.GM)
        assemble.select_brake(assemble.BOSCH_B)
        assemble.select_steering(assemble.BOSCH_S)
        assert assemble.is_valid_check() is True

    def test_bosch_brake_with_non_bosch_steering_fails(self):
        assemble.select_car_type(assemble.SEDAN)
        assemble.select_engine(assemble.GM)
        assemble.select_brake(assemble.BOSCH_B)
        assemble.select_steering(assemble.MOBIS)
        assert assemble.is_valid_check() is False

    # 제한조건 2: 차량 타입별 사용 불가 부품
    def test_sedan_with_continental_brake_fails(self):
        assemble.select_car_type(assemble.SEDAN)
        assemble.select_engine(assemble.GM)
        assemble.select_brake(assemble.CONTINENTAL)
        assemble.select_steering(assemble.MOBIS)
        assert assemble.is_valid_check() is False

    def test_suv_with_toyota_engine_fails(self):
        assemble.select_car_type(assemble.SUV)
        assemble.select_engine(assemble.TOYOTA)
        assemble.select_brake(assemble.MANDO)
        assemble.select_steering(assemble.MOBIS)
        assert assemble.is_valid_check() is False

    def test_truck_with_wia_engine_fails(self):
        assemble.select_car_type(assemble.TRUCK)
        assemble.select_engine(assemble.WIA)
        assemble.select_brake(assemble.CONTINENTAL)
        assemble.select_steering(assemble.MOBIS)
        assert assemble.is_valid_check() is False

    def test_truck_with_mando_brake_fails(self):
        assemble.select_car_type(assemble.TRUCK)
        assemble.select_engine(assemble.GM)
        assemble.select_brake(assemble.MANDO)
        assemble.select_steering(assemble.MOBIS)
        assert assemble.is_valid_check() is False

    def test_valid_combination_passes(self):
        assemble.select_car_type(assemble.SEDAN)
        assemble.select_engine(assemble.GM)
        assemble.select_brake(assemble.MANDO)
        assemble.select_steering(assemble.MOBIS)
        assert assemble.is_valid_check() is True


class TestProducedCar:
    def test_produced_car_prints_pass_for_valid_combination(self, capsys):
        assemble.select_car_type(assemble.SEDAN)
        assemble.select_engine(assemble.GM)
        assemble.select_brake(assemble.MANDO)
        assemble.select_steering(assemble.MOBIS)
        assemble.test_produced_car()
        assert "PASS" in capsys.readouterr().out

    def test_produced_car_prints_fail_for_sedan_continental(self, capsys):
        assemble.select_car_type(assemble.SEDAN)
        assemble.select_engine(assemble.GM)
        assemble.select_brake(assemble.CONTINENTAL)
        assemble.select_steering(assemble.MOBIS)
        assemble.test_produced_car()
        assert "FAIL" in capsys.readouterr().out

    def test_run_produced_car_stops_on_broken_engine(self, capsys):
        assemble.select_car_type(assemble.SEDAN)
        assemble.select_engine(4)  # 고장난 엔진
        assemble.select_brake(assemble.MANDO)
        assemble.select_steering(assemble.MOBIS)
        assemble.run_produced_car()
        out = capsys.readouterr().out
        assert "자동차가 움직이지 않습니다" in out

    def test_run_produced_car_stops_on_invalid_combination(self, capsys):
        assemble.select_car_type(assemble.TRUCK)
        assemble.select_engine(assemble.GM)
        assemble.select_brake(assemble.MANDO)
        assemble.select_steering(assemble.MOBIS)
        assemble.run_produced_car()
        out = capsys.readouterr().out
        assert "자동차가 동작되지 않습니다" in out

    def test_run_produced_car_runs_on_valid_combination(self, capsys):
        assemble.select_car_type(assemble.SEDAN)
        assemble.select_engine(assemble.GM)
        assemble.select_brake(assemble.MANDO)
        assemble.select_steering(assemble.MOBIS)
        assemble.run_produced_car()
        out = capsys.readouterr().out
        assert "자동차가 동작됩니다" in out
