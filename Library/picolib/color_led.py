import neopixel
from machine import Pin
from micropython import const


class ColorCode:
    """カラーコード定義"""

    aqua = const(0x00FFFF)
    blue = const(0x0000FF)
    fuchsia = const(0xFF00FF)
    gray = const(0x808080)
    green = const(0x008000)
    lime = const(0x00FF00)
    maroon = const(0x800000)
    navy = const(0x000080)
    olive = const(0x808000)
    purple = const(0x800080)
    red = const(0xFF0000)
    silver = const(0xC0C0C0)
    teal = const(0x008080)
    white = const(0xFFFFFF)
    yellow = const(0xFFFF00)
    orange = const(0xFFA500)
    orangered = const(0xFF4500)


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
        self.__on_rgb((color >> 16) & 0xFF, (color >> 8) & 0xFF, color & 0xFF)


class ColorSliderLed(ColorLed):
    """スライドアニメーションカラーLED(neopixcel利用版)クラス"""

    def __init__(self, pin_no: int, pixcel_count: int = 1):
        """コンストラクタ
        Args:
            pin_no: 制御に利用するピン番号
            pixcel_count: NeoPixelのLED数
        """
        super().__init__(pin_no, pixcel_count)

    def on_rgblist(self, rgblist: list[int]):
        """RGB値リスト指定で点灯
        Args:
            rgblist:   RGB(0x000000-0xFFFFFF)のリスト
        """
        for idx in range(self.__pixcel_count):
            color = rgblist[idx]
            self.__np[idx] = ((color >> 16) & 0xFF, (color >> 8) & 0xFF, color & 0xFF)
        self.__np.write()


# ==================
# テストコード
# ==================
class ColorLedTester:
    def __init__(self, pin_no: int, pixcel_count: int = 1):
        print(f"init pixcel_count:{pixcel_count}")
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
        print("test outvalue start ----")
        WAIT = 1
        self.__cl.on_rgb(-1, 256, 0x90)
        time.sleep(WAIT)
        self.__cl.off()
        print("test outvalue end   ----")


if __name__ == "__main__":
    import time

    WAIT = 1
    print("test start ----")

    print("color_led default ----")
    t = ColorLedTester(16)
    t.test()
    t.test_outvalue()
    print("color_led any pixcel ----")
    t = ColorLedTester(16, 3)
    t.test()
    print("color_led minus pixcel ----")
    t = ColorLedTester(16, 0)
    t.test()

    print("ColorCode test ----")
    colors = {
        "aqua": ColorCode.aqua,
        "blue": ColorCode.blue,
        "fuchsia": ColorCode.fuchsia,
        "gray": ColorCode.gray,
        "green": ColorCode.green,
        "lime": ColorCode.lime,
        "maroon": ColorCode.maroon,
        "navy": ColorCode.navy,
        "olive": ColorCode.olive,
        "purple": ColorCode.purple,
        "red": ColorCode.red,
        "silver": ColorCode.silver,
        "teal": ColorCode.teal,
        "white": ColorCode.white,
        "yellow": ColorCode.yellow,
        "orange": ColorCode.orange,
        "orangered": ColorCode.orangered,
    }
    il = ColorLed(16, 2)
    for color_name in colors.keys():
        print(f"{color_name}")
        il.on_color(colors[color_name])
        time.sleep(WAIT)
    il.off()

    print("ColorSliderLed start ----")
    csl = ColorSliderLed(16, 5)
    csl.on_rgb(0xFF, 0xFF, 0xFF)
    time.sleep(WAIT)
    csl.off()
    anime = [
        [0xFF0000, 0xFF0000, 0xFF0000, 0xFF0000, 0xFF0000],
        [0xFFFF00, 0xFF0000, 0xFF0000, 0xFF0000, 0xFF0000],
        [0xFFFF00, 0xFFFF00, 0xFF0000, 0xFF0000, 0xFF0000],
        [0x00FF00, 0xFFFF00, 0xFFFF00, 0xFF0000, 0xFF0000],
        [0xFFFF00, 0x00FF00, 0xFFFF00, 0xFFFF00, 0xFF0000],
        [0xFFFF00, 0xFFFF00, 0x00FF00, 0xFFFF00, 0xFFFF00],
        [0xFF0000, 0xFFFF00, 0xFFFF00, 0x00FF00, 0xFFFF00],
        [0xFF0000, 0xFF0000, 0xFFFF00, 0xFFFF00, 0x00FF00],
        [0xFF0000, 0xFF0000, 0xFF0000, 0xFFFF00, 0xFFFF00],
        [0xFF0000, 0xFF0000, 0xFF0000, 0xFF0000, 0xFFFF00],
        [0xFF0000, 0xFF0000, 0xFF0000, 0xFF0000, 0xFF0000],
    ]
    for idx in range(len(anime)):
        print(f"--{idx}--{anime[idx]}")
        csl.on_rgblist(anime[idx])
        time.sleep(WAIT)
    csl.off()

    print("test end   ----")
