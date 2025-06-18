import utime

from machine import Pin

from PicoLib import Led, InputSwitch

Pin(18, Pin.OUT).on

led_s = [Led(2), Led(4), Led(6), Led(8), Led(10), Led(12)]
swt_s = [
    InputSwitch(3),
    InputSwitch(5),
    InputSwitch(7),
    InputSwitch(9),
    InputSwitch(11),
    InputSwitch(13)
    ]

start_button = InputSwitch(19)

testing = True
led_idx = 0
start_button_count = 0
print("Test Start ----")
while testing:
    # LED点灯
    print("led:{0}".format(led_idx))
    led_s[led_idx].on()

    # ボタン状態確認
    for btn_idx in range(6):
        print("swt{0}:{1}".format(btn_idx, swt_s[btn_idx].is_on()))

    # LED消灯
    utime.sleep(1)
    led_s[led_idx].off()
    led_idx = (led_idx + 1) %6

    # テスト終了チェック
    if start_button.is_on():
       start_button_count += 1
    else:
        tart_button_count = 0
    print("st_btn:{0}".format(start_button_count))
    if start_button_count > 1:
        testing = False
for led_off_idx in range(6):
    led_s[led_off_idx].off()    
print("Test End   ----")
