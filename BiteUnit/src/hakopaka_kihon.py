from machine import Pin, PWM
import time

# ==== つかうピンと変数 ====
BTN_PIN   = 9     # ボタン
TRIG_PIN  = 10    # 超音波を出す
ECHO_PIN  = 11    # 超音波をうける
SERVO_PIN = 12    # サーボモーター

# サーボの動く範囲（だいたいの目安）
# duty_u16 の数字が大きいほど 角度がひらく
#   0°   → 1638 (500us)
#   90°  → 4915 (1500us)
#   180° → 8192 (2500us)
CLOSE = 1638   # とじるとき
OPEN  = 4915   # ひらくとき

THRESHOLD = 10    # センサーの反応きょり (cm)
DELAY = 2         # とじるまでの時間 (秒)
INTERVAL = 0.2    # センサーをよむ間かく (秒)

# ==== ピンのせってい ====
BTN  = Pin(BTN_PIN, Pin.IN, Pin.PULL_UP)
TRIG = Pin(TRIG_PIN, Pin.OUT)
ECHO = Pin(ECHO_PIN, Pin.IN)
servo = PWM(Pin(SERVO_PIN)); servo.freq(50)

# ==== センサーできょりをはかる ====
def dist():
    TRIG(0); time.sleep_us(2)
    TRIG(1); time.sleep_us(10); TRIG(0)  # 超音波を出す
    while not ECHO(): pass        # 超音波をうける
    s = time.ticks_us()
    while ECHO(): pass
    return (time.ticks_us() - s) / 58.2  # きょりを計算する

# ==== さいしょはフタを閉じる ====
servo.duty_u16(CLOSE)
opened = False  

# ==== ずっとくり返す ====
while True:
    trigger = (BTN() == 0) or (dist() < THRESHOLD)

    if trigger:
        servo.duty_u16(OPEN)   # ボタンが押された or 手が近づいた → 開く
        opened = True
    elif opened:
        time.sleep(DELAY)      # 開いたあと少しまって閉じる
        servo.duty_u16(CLOSE)
        opened = False

    time.sleep(INTERVAL)       # センサーをよむ間かく
