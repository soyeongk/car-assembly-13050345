import pytest

import cli
from builder import CarBuilder
from models import Brake, CarType, Engine, Steering


@pytest.fixture(autouse=True)
def no_delay(monkeypatch):
    monkeypatch.setattr(cli, "delay", lambda ms: None)


class TestIsValidRange:
    @pytest.mark.parametrize("ans", [1, 2, 3])
    def test_step0_valid(self, ans):
        assert cli.is_valid_range(0, ans) is True

    @pytest.mark.parametrize("ans", [0, 4])
    def test_step0_invalid(self, ans):
        assert cli.is_valid_range(0, ans) is False

    @pytest.mark.parametrize("ans", [0, 1, 2, 3, 4])
    def test_step1_valid(self, ans):
        assert cli.is_valid_range(1, ans) is True

    @pytest.mark.parametrize("ans", [-1, 5])
    def test_step1_invalid(self, ans):
        assert cli.is_valid_range(1, ans) is False

    @pytest.mark.parametrize("ans", [0, 1, 2, 3])
    def test_step2_valid(self, ans):
        assert cli.is_valid_range(2, ans) is True

    @pytest.mark.parametrize("ans", [-1, 4])
    def test_step2_invalid(self, ans):
        assert cli.is_valid_range(2, ans) is False

    @pytest.mark.parametrize("ans", [0, 1, 2])
    def test_step3_valid(self, ans):
        assert cli.is_valid_range(3, ans) is True

    @pytest.mark.parametrize("ans", [-1, 3])
    def test_step3_invalid(self, ans):
        assert cli.is_valid_range(3, ans) is False

    @pytest.mark.parametrize("ans", [0, 1, 2])
    def test_step4_valid(self, ans):
        assert cli.is_valid_range(4, ans) is True

    @pytest.mark.parametrize("ans", [-1, 3])
    def test_step4_invalid(self, ans):
        assert cli.is_valid_range(4, ans) is False


class TestSelectFunctions:
    def test_select_car_type_prints_and_sets_builder(self, capsys):
        builder = CarBuilder()
        cli.select_car_type(builder, CarType.SUV)
        assert builder.car_type == CarType.SUV
        assert "차량 타입으로 SUV을 선택하셨습니다." in capsys.readouterr().out

    def test_select_engine_prints_and_sets_builder(self, capsys):
        builder = CarBuilder()
        cli.select_engine(builder, Engine.TOYOTA)
        assert builder.engine == Engine.TOYOTA
        assert "TOYOTA 엔진을 선택하셨습니다." in capsys.readouterr().out

    def test_select_broken_engine_prints_broken_message(self, capsys):
        builder = CarBuilder()
        cli.select_engine(builder, Engine.BROKEN)
        assert builder.engine == Engine.BROKEN
        assert "고장난 엔진을 선택하셨습니다." in capsys.readouterr().out

    def test_select_brake_prints_and_sets_builder(self, capsys):
        builder = CarBuilder()
        cli.select_brake(builder, Brake.CONTINENTAL)
        assert builder.brake == Brake.CONTINENTAL
        assert "CONTINENTAL 제동장치를 선택하셨습니다." in capsys.readouterr().out

    def test_select_steering_prints_and_sets_builder(self, capsys):
        builder = CarBuilder()
        cli.select_steering(builder, Steering.MOBIS)
        assert builder.steering == Steering.MOBIS
        assert "MOBIS 조향장치를 선택하셨습니다." in capsys.readouterr().out


class TestRunAndTestProducedCar:
    def _built_builder(self, car_type=CarType.SEDAN, engine=Engine.GM, brake=Brake.MANDO, steering=Steering.MOBIS):
        builder = CarBuilder()
        builder.select_car_type(car_type)
        builder.select_engine(engine)
        builder.select_brake(brake)
        builder.select_steering(steering)
        return builder

    def test_test_produced_car_prints_pass(self, capsys):
        cli.test_produced_car(self._built_builder())
        assert "PASS" in capsys.readouterr().out

    def test_test_produced_car_prints_fail(self, capsys):
        builder = self._built_builder(car_type=CarType.SEDAN, brake=Brake.CONTINENTAL)
        cli.test_produced_car(builder)
        assert "FAIL" in capsys.readouterr().out

    def test_run_produced_car_stops_on_broken_engine(self, capsys):
        cli.run_produced_car(self._built_builder(engine=Engine.BROKEN))
        assert "자동차가 움직이지 않습니다" in capsys.readouterr().out

    def test_run_produced_car_stops_on_invalid_combination(self, capsys):
        builder = self._built_builder(car_type=CarType.TRUCK, brake=Brake.MANDO)
        cli.run_produced_car(builder)
        assert "자동차가 동작되지 않습니다" in capsys.readouterr().out

    def test_run_produced_car_runs_on_valid_combination(self, capsys):
        cli.run_produced_car(self._built_builder())
        assert "자동차가 동작됩니다." in capsys.readouterr().out


class TestMainSmoke:
    def test_full_flow_to_run(self, monkeypatch, capsys):
        inputs = iter(["1", "1", "1", "2", "1", "exit"])
        monkeypatch.setattr("builtins.input", lambda prompt="": next(inputs))
        cli.main()
        out = capsys.readouterr().out
        assert "자동차가 동작됩니다." in out
        assert "바이바이" in out

    def test_back_navigation_returns_to_previous_step(self, monkeypatch, capsys):
        # 차량 타입(1) 선택 후 엔진 단계에서 뒤로가기(0) -> 다시 차량 타입 선택 화면
        inputs = iter(["1", "0", "exit"])
        monkeypatch.setattr("builtins.input", lambda prompt="": next(inputs))
        cli.main()
        out = capsys.readouterr().out
        assert out.count("어떤 차량 타입을 선택할까요?") == 2

    def test_invalid_input_shows_error_and_repeats_step(self, monkeypatch, capsys):
        inputs = iter(["abc", "1", "exit"])
        monkeypatch.setattr("builtins.input", lambda prompt="": next(inputs))
        cli.main()
        out = capsys.readouterr().out
        assert "ERROR :: 숫자만 입력 가능" in out
