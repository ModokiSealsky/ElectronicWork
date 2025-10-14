from machine import Pin, PWM
import time
from ColorLed import ColorLed

# ==== つかうピンと変数 ====
BTN_PIN   = 9     # ボタン
TRIG_PIN  = 10    # 超音波を出す
ECHO_PIN  = 11    # 超音波をうける
SERVO_PIN = 12    # サーボモーター
COLOR_PIN   = 16    # カラーLED

# サーボの動く範囲（だいたいの目安）
# duty_u16 の数字が大きいほど 角度がひらく
#   0°   → 1638 (500us)
#   90°  → 4915 (1500us)
#   180° → 8192 (2500us)
CLOSE = 1638   # とじるとき
OPEN  = 6000   # ひらくとき
BITE  = 3000   # かむとき

THRESHOLD_OPEN = 20    # センサーの反応きょり ひらくとき (cm)
THRESHOLD_BITE = 10    # センサーの反応きょり かむとき (cm)
DELAY = 2         # とじるまでの時間 (秒)
INTERVAL = 0.2    # センサーをよむ間かく (秒)

# ==== ピンのせってい ====
BTN  = Pin(BTN_PIN, Pin.IN, Pin.PULL_UP)
TRIG = Pin(TRIG_PIN, Pin.OUT)
ECHO = Pin(ECHO_PIN, Pin.IN)
servo = PWM(Pin(SERVO_PIN)); servo.freq(50)
color = ColorLed(COLOR_PIN)

# ==== センサーできょりをはかる ====
def dist():
    TRIG(0); time.sleep_us(2)
    TRIG(1); time.sleep_us(10); TRIG(0)  # 超音波を出す
    while not ECHO(): pass        # 超音波をうける
    s = time.ticks_us()
    while ECHO(): pass
    return (time.ticks_us() - s) / 58.2  # きょりを計算する

# ==== 状態を示す文字をつくる ====
def get_status_text(servo_status):
    if servo_status == BITE:
        return "BITE"
    elif servo_status < BITE:
        return "CLOSE"
    else:
        return "OPEN"

# ==== さいしょはフタを閉じる ====
servo.duty_u16(CLOSE)
servo_status = CLOSE # 状態を記録する
color.on_blue()

# ==== ずっとくり返す ====
while True:
    dist_value = dist() # きょりをはかる
    print(f"{dist_value}cm|status:{get_status_text(servo_status)}")
    open_trigger = (BTN() == 0) or (dist_value < THRESHOLD_OPEN)
    bite_trigger = dist_value < THRESHOLD_BITE

    if bite_trigger:
        if servo_status != BITE:
            print("-> BITE")
            color.on_red()
            servo.duty_u16(BITE)   # さらに手が近づいた → 噛む
            servo_status = BITE
            time.sleep(DELAY)
    elif open_trigger:
        if servo_status != OPEN:
            print("-> OPEN")
            color.on_yellow()
            servo.duty_u16(OPEN)   # ボタンが押された or 手が近づいた → 開く
            servo_status = OPEN
            time.sleep(DELAY)
    elif not (bite_trigger or open_trigger):
        if servo_status != CLOSE:
            print("-> CLOSE")
            color.on_blue()
            servo.duty_u16(CLOSE) # 閉じる
            servo_status = CLOSE
            time.sleep(DELAY)

    time.sleep(INTERVAL)       # センサーをよむ間かく
