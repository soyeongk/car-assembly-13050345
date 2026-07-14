import sys
import time

from builder import CarBuilder
from models import Engine
from rules import CAR_TYPE_LABELS, ENGINE_LABELS, evaluate_run, evaluate_test

CLEAR_SCREEN = "\033[H\033[2J"

BRAKE_SELECT_LABELS = {1: "MANDO", 2: "CONTINENTAL", 3: "BOSCH"}
STEERING_SELECT_LABELS = {1: "BOSCH", 2: "MOBIS"}


def delay(ms):
    t = ms / 1000.0
    time.sleep(t)


def clear():
    sys.stdout.write(CLEAR_SCREEN)
    sys.stdout.flush()


def show_menu(step):
    clear()
    if step == 0:
        print("        ______________")
        print("       /|            |")
        print("  ____/_|_____________|____")
        print(" |                      O  |")
        print(" '-(@)----------------(@)--'")
        print("===============================")
        print("어떤 차량 타입을 선택할까요?")
        print("1. Sedan")
        print("2. SUV")
        print("3. Truck")
    elif step == 1:
        print("어떤 엔진을 탑재할까요?")
        print("0. 뒤로가기")
        print("1. GM")
        print("2. TOYOTA")
        print("3. WIA")
        print("4. 고장난 엔진")
    elif step == 2:
        print("어떤 제동장치를 선택할까요?")
        print("0. 뒤로가기")
        print("1. MANDO")
        print("2. CONTINENTAL")
        print("3. BOSCH")
    elif step == 3:
        print("어떤 조향장치를 선택할까요?")
        print("0. 뒤로가기")
        print("1. BOSCH")
        print("2. MOBIS")
    elif step == 4:
        print("멋진 차량이 완성되었습니다.")
        print("0. 처음 화면으로 돌아가기")
        print("1. RUN")
        print("2. Test")
    print("===============================")


def is_valid_range(step, ans):
    if step == 0:
        if ans < 1 or ans > 3:
            print("ERROR :: 차량 타입은 1 ~ 3 범위만 선택 가능")
            return False
    if step == 1:
        if ans < 0 or ans > 4:
            print("ERROR :: 엔진은 1 ~ 4 범위만 선택 가능")
            return False
    if step == 2:
        if ans < 0 or ans > 3:
            print("ERROR :: 제동장치는 1 ~ 3 범위만 선택 가능")
            return False
    if step == 3:
        if ans < 0 or ans > 2:
            print("ERROR :: 조향장치는 1 ~ 2 범위만 선택 가능")
            return False
    if step == 4:
        if ans < 0 or ans > 2:
            print("ERROR :: Run 또는 Test 중 하나를 선택 필요")
            return False
    return True


def select_car_type(builder, ans):
    car_type = builder.select_car_type(ans)
    print(f"차량 타입으로 {CAR_TYPE_LABELS[car_type]}을 선택하셨습니다.")


def select_engine(builder, ans):
    engine = builder.select_engine(ans)
    if engine == Engine.BROKEN:
        print("고장난 엔진을 선택하셨습니다.")
    else:
        print(f"{ENGINE_LABELS[engine]} 엔진을 선택하셨습니다.")


def select_brake(builder, ans):
    brake = builder.select_brake(ans)
    print(f"{BRAKE_SELECT_LABELS[brake]} 제동장치를 선택하셨습니다.")


def select_steering(builder, ans):
    steering = builder.select_steering(ans)
    print(f"{STEERING_SELECT_LABELS[steering]} 조향장치를 선택하셨습니다.")


def run_produced_car(builder):
    result = evaluate_run(builder.build())
    for line in result.lines:
        print(line)


def test_produced_car(builder):
    result = evaluate_test(builder.build())
    print(result.message)


def main():
    step = 0
    builder = CarBuilder()
    while True:
        show_menu(step)
        buf = input("INPUT > ").strip()

        if buf == "exit":
            print("바이바이")
            break

        try:
            ans = int(buf)
        except ValueError:
            print("ERROR :: 숫자만 입력 가능")
            delay(800)
            continue

        if not is_valid_range(step, ans):
            delay(800)
            continue

        if ans == 0:
            if step == 4:
                step = 0
            elif step > 0:
                step = step - 1
            continue

        if step == 0:
            select_car_type(builder, ans)
            delay(800)
            step = 1
        elif step == 1:
            select_engine(builder, ans)
            delay(800)
            step = 2
        elif step == 2:
            select_brake(builder, ans)
            delay(800)
            step = 3
        elif step == 3:
            select_steering(builder, ans)
            delay(800)
            step = 4
        elif step == 4:
            if ans == 1:
                run_produced_car(builder)
                delay(2000)
            elif ans == 2:
                print("Test...")
                delay(1500)
                test_produced_car(builder)
                delay(2000)


if __name__ == "__main__":
    main()
