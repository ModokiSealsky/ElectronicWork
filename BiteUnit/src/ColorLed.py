import neopixel
from machine import Pin

class ColorLed:
    """カラーLED(neopixcel利用版)クラス"""

    def __init__(self, pin_no: int):
        """コンストラクタ
        Args:
            pin_no: 制御に利用するピン番号
        """
        self.__np = neopixel.NeoPixel(Pin(pin_no), 1)
    
    def __rounding(self, color_value):
        """値の丸め処理
        0x00～0xFFの範囲内になるように値を補正する
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
            red_valie:   赤の値（0x00～0xFF）
            green_valie: 緑の値（0x00～0xFF）
            blue_valie:  青の値（0x00～0xFF）
        """
        self.__on_rgb(self.__rounding(red_value),
                      self.__rounding(green_value),
                      self.__rounding(blue_value))
    
    def __on_rgb(self, red_value: int, green_value: int, blue_value: int):
        self.__np[0] = (red_value, green_value, blue_value)
        self.__np.write()
    
    def off(self):
        """消灯"""
        self.__on_rgb(0x00, 0x00, 0x00)

    def on_aqua(self):
        self.__on_rgb(0x00, 0xFF, 0xFF)

    def on_blue(self):
        self.__on_rgb(0x00, 0x00, 0xFF)

    def on_fuchsia(self):
        self.__on_rgb(0xFF, 0x00, 0xFF)

    def on_gray(self):
        self.__on_rgb(0x80, 0x80, 0x80)

    def on_green(self):
        self.__on_rgb(0x00, 0x80, 0x00)

    def on_lime(self):
        self.__on_rgb(0x00, 0xFF, 0x00)

    def on_maroon(self):
        self.__on_rgb(0x80, 0x00, 0x00)

    def on_navy(self):
        self.__on_rgb(0x00, 0x00, 0x80)

    def on_olive(self):
        self.__on_rgb(0x80, 0x80, 0x00)

    def on_purple(self):
        self.__on_rgb(0x80, 0x00, 0x80)

    def on_red(self):
        self.__on_rgb(0xFF, 0x00, 0x00)

    def on_silver(self):
        self.__on_rgb(0xC0, 0xC0, 0xC0)

    def on_teal(self):
        self.__on_rgb(0x00, 0x80, 0x80)

    def on_white(self):
        self.__on_rgb(0xFF, 0xFF, 0xFF)

    def on_yellow(self):
        self.__on_rgb(0xFF, 0xFF, 0x00)

    def on_orange(self):
        self.__on_rgb(0xFF, 0xA5, 0x00)

    def on_orangered(self):
        self.__on_rgb(0xFF, 0x45, 0x00)

# ==================
# テストコード
# ================== 
if __name__  == "__main__":
    import time
    print("test start ----")
    WAIT = 1
    il = ColorLed(16)
    il.off()
    time.sleep(WAIT)
    print("aqua")
    il.on_aqua()
    time.sleep(WAIT)
    print("blue")
    il.on_blue()
    time.sleep(WAIT)
    print("fuchsia")
    il.on_fuchsia()
    time.sleep(WAIT)
    print("gray")
    il.on_gray()
    time.sleep(WAIT)
    print("green")
    il.on_green()
    time.sleep(WAIT)
    print("lime")
    il.on_lime()
    time.sleep(WAIT)
    print("maroon")
    il.on_maroon()
    time.sleep(WAIT)
    print("navy")
    il.on_navy()
    time.sleep(WAIT)
    print("olive")
    il.on_olive()
    time.sleep(WAIT)
    print("purple")
    il.on_purple()
    time.sleep(WAIT)
    print("red")
    il.on_red()
    time.sleep(WAIT)
    print("silver")
    il.on_silver()
    time.sleep(WAIT)
    print("teal")
    il.on_teal()
    time.sleep(WAIT)
    print("white")
    il.on_white()
    time.sleep(WAIT)
    print("yellow")
    il.on_yellow()
    time.sleep(WAIT)
    print("orange")
    il.on_orange()
    time.sleep(WAIT)
    print("orangered")
    il.on_orangered()
    time.sleep(WAIT)
    print("rgb")
    il.on_rgb(-1, 256, 0x90)
    time.sleep(WAIT)
    il.off()
    print("test end   ----")
