import neopixel
from machine import Pin

from color_led import ColorLed

class ColorSliderLed(ColorLed):
    """スライドアニメーションカラーLED(neopixcel利用版)クラス"""

    def __init__(self, pin_no: int, pixcel_count: int = 1):
        """コンストラクタ
        Args:
            pin_no: 制御に利用するピン番号
            pixcel_count: NeoPixelのLED数
        """
        super().__init__(pin_no, pixcel_count)

    def on_rgblist(self, rgblist: list(int)):
        """RGB値リスト指定で点灯
        Args:
            rgblist:   RGB(0x000000-0xFFFFFF)のリスト
        """
        for idx in range(self.__pixcel_count):
            color = rgblist[idx]
            self.__np[idx] = (
                (color >> 16) & 0xFF,
                (color >> 8) & 0xFF,
                color & 0xFF
            )
        self.__np.write()
    
# ==================
# テストコード
# ==================
if __name__ == "__main__":
    import time
    WAIT = 1
    print("test start ----")
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
        [0xFF0000, 0xFF0000, 0xFF0000, 0xFF0000, 0xFF0000]
    ]
    for idx in range(len(anime)):
        print(f"--{idx}--{anime[idx]}")
        csl.on_rgblist(anime[idx])
        time.sleep(WAIT)
    csl.off()
    print("test end   ----")
