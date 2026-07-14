# car-assembly

`assemble.py`는 콘솔 메뉴 기반의 자동차 조립 시뮬레이터다.

## 조립 순서

1. **자동차 타입 선택**: 세단(Sedan) / SUV / 트럭(Truck)
2. **부품 선택** (순서대로 진행)
   - 엔진: GM / TOYOTA / WIA / 고장난 엔진
   - 제동장치: MANDO / CONTINENTAL / BOSCH
   - 조향장치: BOSCH / MOBIS
3. **완성 차량 테스트**: 선택한 부품이 선택한 차량 타입에 사용 가능한지 검사 (RUN 또는 Test)

## 제한 조건 (`is_valid_check` / `test_produced_car`)

**제한조건 1**
- 제동장치에 Bosch 제품을 사용했다면, 조향장치도 Bosch 제품을 사용해야 한다. (타사 제품과 호환되지 않는다.)

**제한조건 2**
- Continental은 Sedan용 제동장치를 만들지 않는다. (세단에 Continental 제품 사용 불가)
- TOYOTA는 SUV용 엔진을 만들지 않는다.
- WIA는 Truck용 엔진을 만들지 않는다.
- Mando는 Truck용 제동장치(brake system)를 만들지 않는다.

## 기존 시스템의 아쉬운 점

- 절차지향식 코드로, 유지보수가 어려운 구조
- 안전하지 않은 문법들이 사용됨
- 확장성이 고려되지 않음
- 유닛테스트가 없음
