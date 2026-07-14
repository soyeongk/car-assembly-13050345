# car-assembly

`assemble.py`는 콘솔 메뉴 기반의 자동차 조립 시뮬레이터다.

## 조립 순서

1. **자동차 타입 선택**: 세단(Sedan) / SUV / 트럭(Truck)
2. **부품 선택** (순서대로 진행)
   - 엔진: GM / TOYOTA / WIA / 고장난 엔진
   - 제동장치: MANDO / CONTINENTAL / BOSCH
   - 조향장치: BOSCH / MOBIS
3. **완성 차량 테스트**: 선택한 부품이 선택한 차량 타입에 사용 가능한지 검사 (RUN 또는 Test)

## 제한 조건 (`rules.py`의 `RULES` 테이블)

**제한조건 1**
- 제동장치에 Bosch 제품을 사용했다면, 조향장치도 Bosch 제품을 사용해야 한다. (타사 제품과 호환되지 않는다.)

**제한조건 2**
- Continental은 Sedan용 제동장치를 만들지 않는다. (세단에 Continental 제품 사용 불가)
- TOYOTA는 SUV용 엔진을 만들지 않는다.
- WIA는 Truck용 엔진을 만들지 않는다.
- Mando는 Truck용 제동장치(brake system)를 만들지 않는다.

## 리팩토링 이력

기존에는 전역 변수(`q0~q4`)로 상태를 관리하는 절차지향 코드였고, 아래 문제가 있었다.
- 절차지향식 코드로, 유지보수가 어려운 구조
- 안전하지 않은 문법들이 사용됨 (bare `except:` 등)
- 확장성이 고려되지 않음 (호환성 규칙이 `is_valid_check`/`test_produced_car`에 중복 하드코딩)
- 유닛테스트가 없음

이 문제들을 해결하기 위해 아래 구조로 리팩토링했다.

```
assemble.py   # 얇은 진입점 (python assemble.py 실행 방식 유지, cli.main()만 호출)
models.py     # CarType/Engine/Brake/Steering IntEnum, Car frozen dataclass
rules.py      # 호환성 규칙 테이블(RULES) + is_compatible/evaluate_run/evaluate_test
builder.py    # CarBuilder — 부품 선택 상태를 캡슐화 (전역 변수 대체)
cli.py        # show_menu/is_valid_range/main() — input/print I/O 전담
tests/        # test_models.py, test_rules.py, test_builder.py, test_cli.py
```

### 새 차종/부품을 추가하려면
1. `models.py`의 해당 enum에 멤버 추가
2. `rules.py`의 `RULES` 리스트에 `CompatibilityRule` 한 줄 추가 (기존 규칙은 건드릴 필요 없음)
3. `cli.py`의 라벨 딕셔너리와 메뉴 텍스트에 항목 추가

### 알아두어야 할 기존 동작 특성
- 호환성 규칙(제한조건 1·2)에는 **고장난 엔진(`Engine.BROKEN`)이 포함되지 않는다.** 따라서 `evaluate_test`(Test 메뉴)는 엔진이 고장나도 다른 조건만 맞으면 PASS를 반환한다. 고장난 엔진은 `evaluate_run`(RUN 메뉴)에서만 별도로 막는다. 리팩토링 전 원본 동작을 그대로 보존한 것이다.

### 테스트 실행
```
.venv/Scripts/python.exe -m pytest -v
```
