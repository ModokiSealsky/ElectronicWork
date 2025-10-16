import neopixel
from machine import Pin

class ColorLed:
    """カラーLED(neopixcel利用版)クラス"""

    def __init__(self, pin_no: int, pixcel_count: int = 1):
        """コンストラクタ
        Args:
            pin_no: 制御に利用するピン番号
            pixcel_count: NeoPixelのLED数
        """
        cnt = pixcel_count
        if pixcel_count < 1:
            cnt = 1
        self.__pixcel_count = cnt
        self.__np = neopixel.NeoPixel(Pin(pin_no), cnt)

    def __rounding(self, color_value):
        """値の丸め処理
        0x00-0xFFの範囲内になるように値を補正する
        """
        if color_value > 0xFF:
            return 0xFF
        elif color_value < 0x00:
            return 0x00
        else:
            return color_value

    def on_rgb(self, red_value: int, green_value: int, blue_value: int):
        """RGB値指定で点灯
        Args:
            red_valie:   赤の値(0x00-0xFF)
            green_valie: 緑の値(0x00-0xFF)
            blue_valie:  青の値(0x00-0xFF)
        """
        self.__on_rgb(
            self.__rounding(red_value),
            self.__rounding(green_value),
            self.__rounding(blue_value),
        )

    def __on_rgb(self, red_value: int, green_value: int, blue_value: int):
        for i in range(self.__pixcel_count):
            self.__np[i] = (red_value, green_value, blue_value)
        self.__np.write()

    def off(self):
        """消灯"""
        self.__on_rgb(0x00, 0x00, 0x00)

    def on_color(self, color: int):
        """カラー指定で点灯"""
        self.__on_rgb(
            (color >> 16) & 0xFF,
            (color >> 8) & 0xFF,
            color & 0xFF
        )

# ==================
# テストコード
# ==================
class ColorLedTester:

    def __init__(self, pin_no: int, pixcel_count: int = 1):
        self.__cl = ColorLed(pin_no, pixcel_count)
        self.__cl.off()

    def test(self):
        print("test start ----")
        WAIT = 1
        self.__cl.on_rgb(0xFF, 0x00, 0x00)
        time.sleep(WAIT)
        self.__cl.on_rgb(0x00, 0xFF, 0x00)
        time.sleep(WAIT)
        self.__cl.on_rgb(0x00, 0x00, 0xFF)
        time.sleep(WAIT)
        self.__cl.on_color(0xFFFFFF)
        time.sleep(WAIT)
        self.__cl.off()
        print("test end   ----")

    def test_outvalue(self):
        print("test start ----")
        WAIT = 1
        self.__cl.on_rgb(-1, 256, 0x90)
        time.sleep(WAIT)
        il.off()
        print("test end   ----")

if __name__ == "__main__":
    import time
    print("test start ----")
    print("test default ----")
    t = ColorLedTester(16)
    t.test()
    t.test_outvalue
    print("test any pixcel ----")
    t = ColorLedTester(16, 3)
    t.test()
    print("test minus pixcel ----")
    t = ColorLedTester(16, 0)
    t.test()
    print("test end   ----")