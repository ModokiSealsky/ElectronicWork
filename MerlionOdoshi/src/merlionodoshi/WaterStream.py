import utime
import _thread

from micropython import const

from picolib import Led
from merlionodoshi import WaterStreamSpeed

class WaterStream:
    """LED8個で水流を演出する"""

    class _Animation:
        """水流アニメーション用点灯位置定義"""
        OFF = const(0b00000000)

        DIGIT = {
            0: 0b00000001,
            1: 0b00000010,
            2: 0b00000100,
            3: 0b00001000,
            4: 0b00010000,
            5: 0b00100000,
            6: 0b01000000,
            7: 0b10000000,
        }
        """LED桁対応定義"""

        SLOW = {
            "START": [
                const(0b00000001), # 00
            ],
            "KEEP": [
                const(0b00000011), # 01
                const(0b00000110), # 02
                const(0b00001100), # 03
                const(0b00011000), # 04
                const(0b00110000), # 05
                const(0b01100000), # 06
                const(0b11000000), # 07
                const(0b10000001), # 08 継続の場合、次は01
            ],
            "END": [
                const(0b10000000), # 09 終了の場合、08をスキップして09
            ]
        }
        """低速用アニメーション定義"""

        FAST = {
            "START": [
                const(0b00000001), # 00
                const(0b00000011), # 01
                const(0b00000110), # 02
                const(0b00001100), # 03
                const(0b00011001), # 04
            ],
            "KEEP": [
                const(0b00110011), # 05
                const(0b01100110), # 06
                const(0b11001100), # 07
                const(0b10011001), # 08 継続の場合、次は05
            ],
            "END": [
                const(0b10011000), # 09 終了の場合、08をスキップして09
                const(0b00110000), # 10
                const(0b01100000), # 11
                const(0b11000000), # 12
                const(0b10000000), # 13
            ]
        }
        """高速用アニメーション定義"""
        
        HYPER = {
            "START": [
                const(0b00000001), # 00
                const(0b00000011), # 01
                const(0b00000111), # 02
                const(0b00001111), # 03
                const(0b00011111), # 04
            ],
            "KEEP": [
                const(0b00111111), # 05
                const(0b01111110), # 06
                const(0b11111100), # 07
                const(0b11111001), # 08
                const(0b11110011), # 09
                const(0b11100111), # 10
                const(0b11001111), # 11
                const(0b10011111), # 13 継続の場合、次は05
            ],
            "END": [
                const(0b00111110), # 14 終了の場合、13をスキップして09
                const(0b11111100), # 15
                const(0b11111000), # 16
                const(0b11110000), # 17
                const(0b11100000), # 18
                const(0b11000000), # 19
                const(0b10000000), # 20
            ]
        }
        """爆速用アニメーション定義"""

    _animathon_dorowing: bool = False
    """アニメーション中フラグ"""
    _animation_keep : bool = False
    """アニメーション継続フラグ"""

    def __init__(self,
                 led_0: Led,
                 led_1: Led,
                 led_2: Led,
                 led_3: Led,
                 led_4: Led,
                 led_5: Led,
                 led_6: Led,
                 led_7: Led,
    ):
        """水流アニメーションクラスのセットアップ
        
        Args:
            led_0: 口に１番近いLED
            led_1: 口に２番目に近い近いLED
            led_2: 口に３番目に近い近いLED
            led_3: 口に４番目に近い近いLED
            led_4: 口に５番目に近い近いLED
            led_5: 口に６番目に近い近いLED
            led_6: 口に７番目に近い近いLED
            led_7: 口から１番遠いLED
        """
        self._led_list = [
            led_0, led_1, led_2, led_3, led_4, led_5, led_6, led_7
        ]

    def start(self, speed: int):
        """水流アニメーション開始
        Args:
            speed: 水流の速さ(WaterFlowSpeedの値を使う)
        """
        if self._animathon_dorowing:
            # 多重起動禁止
            print("animation drowing!")
            return
        animation: dict[str, list[int]]
        wait_ms: int
        if speed == WaterStreamSpeed.SLOW:
            animation = WaterStream._Animation.SLOW
            wait_ms = 300
        elif speed == WaterStreamSpeed.FAST:
            animation = WaterStream._Animation.FAST
            wait_ms = 200
        elif speed == WaterStreamSpeed.HYPER:
            animation = WaterStream._Animation.HYPER
            wait_ms = 100
        else:
            print("error unkwoun speed.")
            return
        print("animation thread start.")        
        _thread.start_new_thread(self._animation, (animation, wait_ms)) 
        
    
    def stop(self):
        """水流アニメーション停止"""
        self._animation_keep = False
        print("animation thread end requested.")        

    def is_drowing(self) -> bool:
        """アニメーション中かを確認"""
        return self._animathon_dorowing

    def _animation(self, animation: dict[str, list[int]], wait_ms: int):
        self._animathon_dorowing = True
        self._animation_keep = True
        print("start animation.")
        for start_anime_pattern in animation["START"]:
            self._light_edit(start_anime_pattern, wait_ms)

        print("kepp animation.")
        animation_index = 0
        keep_animation = animation["KEEP"]
        keep_animation_len = len(keep_animation)
        keep_animation_limit = keep_animation_len - 1
        while self._animation_keep or animation_index < keep_animation_limit:
            self._light_edit(keep_animation[animation_index], wait_ms)
            animation_index = (animation_index + 1) % keep_animation_len

        print("end animation.")
        for end_anime_pattern in animation["END"]:
            self._light_edit(end_anime_pattern, wait_ms)

        self._light_edit(WaterStream._Animation.OFF, wait_ms)
        self._animathon_dorowing = False
        print("animation thread end.")

    def _light_edit(self, pattern: int, wait_ms:int):
        """ライト点灯消灯制御
        
        Args:
            pattern: ライト点灯消灯パターン
            wait_ms: 点灯時間(ミリ秒)
        """
        for digit in range (8):
            if pattern & WaterStream._Animation.DIGIT[digit]:
                self._led_list[digit].on()
            else:
                self._led_list[digit].off()

        utime.sleep_ms(wait_ms)

# ==================
# テストコード
# ================== 
if __name__  == "__main__":
    print("test start -----")
    cls = WaterStream(
        Led(0), Led(1), Led(2), Led(3),
        Led(4), Led(5), Led(6), Led(7)
    )

    print("slow -----------")
    cls.start(WaterStreamSpeed.SLOW)
    utime.sleep(6)
    cls.stop()
    utime.sleep(5)

    print("fast -----------")
    cls.start(WaterStreamSpeed.FAST)
    utime.sleep(6)
    cls.stop()
    utime.sleep(5)

    print("hyper ----------")
    cls.start(WaterStreamSpeed.HYPER)
    utime.sleep(6)
    cls.stop()
    utime.sleep(10)

    print("test end   -----")
