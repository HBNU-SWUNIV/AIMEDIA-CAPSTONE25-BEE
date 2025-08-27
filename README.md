# 한밭대학교 지능미디어공학과 BEE팀

**팀 구성**
- 20221095 민현선 
- 20221110 이다은

## <u>Teamate</u> Project Background
- ### 필요성
  - 웨어러블 기기는 보통ﾠ편의성과 호환성 위주로 개발되며 보안 업데이트나 암호화 프로토콜 적용이 부족한 경우가 많아ﾠ공격자가 쉽게 통신을 가로채거나 변조 가능
  - AR과 연동되는 수트는 전용 앱으로만 제어되어야 하지만 통신이 조작되면 공격자가 진동을 임의로 제어할 수 있어 제어 권한 탈취와 개인정보 유출 위험 발생
  - 공격자가 수트의 진동을 임의로 제어하면 착용자에게 불쾌감, 통증, 피부 자극, 근육 긴장, 장비 손상 등ﾠ신체적 위험 초래 가능
  - 출시된 지 오래되지 않은 AR/VR연동 웨어러블 수트는 기능 중심 개발로 인해 보안 검증이 미흡해 블루투스 취약점 등 보안 우려가 존재하여 해결 방안 필요
  
- ### 기존 해결책의 문제점
  - OOO
  - OOO
  
## System Design
- ### System Requirements
  + ### 공통 실험 환경 구축
    <img width="516" height="252" alt="image" src="https://github.com/user-attachments/assets/6f83e3a5-d1bb-438d-b3a3-b5c1f973edcd" />
    + 칼리 리눅스 기반 공격 환경 세팅
    + BLE 지원 동글을 장착한 컴퓨터 A(피해자), 컴퓨터 B(공격자) 구성
    + BLE 기반 조명 장치 및 AR 수트(진동센서 장착) 연결
    + Bluepy, BtleJuice 등 오픈소스 툴을 활용한 통신 분석 및 공격 시나리오 설계

  + ### 실험 1: BLE 조명 장치 공격
    ![image](https://github.com/user-attachments/assets/67cd45d0-8f7d-493a-8ac9-ca3f80eda263)
    1) 특정 BLE 장치(KocoaFab_BLE)를 스캔하여 UUID 기반 Write Characteristic을 식별
    2) 값 "2\n" 전송 시 조명의 색상 제어 가능함을 확인
    3) bleak를 통해 A-PC가 조명과 연결 유지, 연결이 끊기면 B-PC가 즉시 재연결되는 무결성 취약점 실험 수행

  + ### 실험 2: AR 수트 진동 센서 공격
    <img width="409" height="230" alt="image" src="https://github.com/user-attachments/assets/75c2afff-5150-4e20-b9fa-af7fa3925012" />
    1) 실험 1에서 세팅한 환경을 BLE 조명이 아닌 촉각 수트에 적용하여 실험
    2) 공격자가 PC 동글을 통해 수트와 모바일 앱 사이의 Bluetooth 통신을 가로채는 환경 구성
    3) Bluepy를 활용하여 수트의 GATT Characteristic(UUID)에 임의 바이트 payload를 Write → 수트가 이를 진동 세기로 해석하여 동작
    4) 자동 연결 해제 및 재주입(inject) 코드를 통해 지속적으로 통신 세션을 제어
    5) 개별 센서 제어 및 세기 조절 가능성을 검증

    
## Case Study
- ### 블루투스 프로토콜의 보안 취약점에 대한 연구 동향(한국통신학회 학술 대회 논문 발표)
  - BtleJuice: BtleJuice는 BLE 프로토콜의 구조적 취약점을 동시에 악용하는 능동형 중간자(MITM) 공격 기법이다. 일반적으로 BLE 장치는 한 번에 하나의 연결만 가능하지만, BtleJuice는 이를 우회하여 피해자의 앱과 기기 사이에 ‘가짜 앱’과 ‘가짜 장치’를 각각 만들어 세션을 중계한다. 이 과정에서 공격자는 SMP 계층의 키 교환 취약점(Temporary Key를 0으로 설정하는 Just Works 페어링 방식)을 이용해 암호화되지 않은 키 교환을 가로채고, GATT 계층의 인증 부재를 이용해 Write·Notify 요청을 변조하거나 재전송 하여 기기의 정상 동작을 교란할 수 있다.
  - GATTacker: GATTacker는 BLE 프로토콜의 핵심 계층인 GATT(Generic Attribute Profile) 구조를 악용하는 공격이다. 공격자는 먼저 정상 BLE 장치를 흉내 낸 가짜 BLE 장치를 만들어 피해자의 앱이 이를 진짜 장치로 오인하도록 유도한다. 이후 실제 장치에서 제공하는 GATT 서비스와 특성을 복제하고, 피해자의 앱이 해당 가짜 장치와 통신하도록 연결을 가로챈다. 이를 통해 공격자는 읽기, 쓰기, 알림 이벤트를 변조하거나 중간에서 가로채어 사용자 정보의 기밀성과 무결성을 침해할 수 있다.
  - InjectaBLE: InjectaBLE은 기존 공격 기법과 달리 이미 연결이 완료된 BLE 세션에서도 공격을 수행할 수 있는 점이 특징이다. 이 공격은 링크 계층의 윈도우 확장(Window Widening) 메커니즘을 악용하여 프레임 전송 타이밍에서 경쟁 조건(Race Condition)을 만들어내고 이 틈을 이용해 악성 패킷을 주입한다. 공격자는 ATT 요청(읽기·쓰기), LL 제어 프레임, CONNECTION UPDATE PDU 등 다양한 메시지를 삽입할 수 있으며, 이를 통해 기기의 특정 기능을 강제로 실행(Trigger)하거나 Master/Slave 역할을 탈취할 수 있다. 또한 기존 연결을 끊지 않고도 공격이 가능하기 때문에 사용자가 눈치채지 못한 상태에서 지속적인 MITM 공격이 가능하다. 이로 인해 BLE 보안 위협 범위가 기존 연결 이전 단계에서 연결 이후 단계로까지 확장되었다는 점에서 중요한 의미가 있다.
  
  
## Conclusion
  - ### OOO
  - ### OOO
  
## Project Outcome
- ### 2025년도 한국통신학회 하계학술대회 논문 발표
