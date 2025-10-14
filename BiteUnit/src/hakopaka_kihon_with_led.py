from machine import Pin, PWM
import time
import neopixel

# ==== つかうピンと変数 ====
BTN_PIN   = 9     # ボタン
TRIG_PIN  = 10    # 超音波を出す
ECHO_PIN  = 11    # 超音波をうける
SERVO_PIN = 12    # サーボモーター
LED_PIN   = 16    # LED

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

# ==== LEDを光らせるクラス ====
class Led:
    def __init__(self, pin_no):
        self.__np = neopixel.NeoPixel(Pin(pin_no), 1)

    def __on(self, r, g, b):
        self.__np[0] = (r, g, b)
        self.__np.write()

    def on_red(self):
        self.__on(0x80, 0x00, 0x00)

    def on_blue(self):
        self.__on(0x00, 0x60, 0x80)

# ==== ピンのせってい ====
BTN  = Pin(BTN_PIN, Pin.IN, Pin.PULL_UP)
TRIG = Pin(TRIG_PIN, Pin.OUT)
ECHO = Pin(ECHO_PIN, Pin.IN)
servo = PWM(Pin(SERVO_PIN)); servo.freq(50)
led = Led(LED_PIN)

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
led.on_blue()
opened = False  

# ==== ずっとくり返す ====
print("start")
while True:
    distance = dist()
    print(f"{distance:06.2f}cm")
    trigger = (BTN() == 0) or (distance < THRESHOLD)

    if trigger and not opened:
        servo.duty_u16(OPEN)   # ボタンが押された or 手が近づいた → 開く
        opened = True
        print("open")
        led.on_red()
    elif opened:
        time.sleep(DELAY)      # 開いたあと少しまって閉じる
        servo.duty_u16(CLOSE)
        opened = False
        print("close")
        led.on_blue()

    time.sleep(INTERVAL)       # センサーをよむ間かく
