import utime

from picolib import Led

class JankenScreen:
    """スクリーンクラス"""

    def __init__(self,
                 leds_gu: list[Led],
                 leds_ch: list[Led],
                 leds_pa: list[Led],
                 led_win: Led,
                 led_drow: Led,
                 led_lose: Led):
        """
        Args:
            leds_gu: グーで点灯するLEDのリスト
            leds_ch: チョキで点灯するLEDのリスト
            leds_pa: パーで点灯するLEDのリスト
            led_win: プレイヤー勝ちで点灯するLED
            led_drow: 引き分けで点灯するLED
            led_lose: プレイヤー敗けで点灯するLED
        """
        self._leds_gu = leds_gu
        self._leds_ch = leds_ch
        self._leds_pa = leds_pa
        self._led_win = led_win
        self._led_drow = led_drow
        self._led_lose = led_lose

    def _gu_off(self):
        """グーを消灯"""
        for led in self._leds_gu:
            led.off()

    def _ch_off(self):
        """チョキを消灯"""
        for led in self._leds_ch:
            led.off()

    def _pa_off(self):
        """パーを消灯"""
        for led in self._leds_pa:
            led.off()

    def hand_off(self):
        """じゃんけんの手を消灯"""
        self._gu_off()
        self._ch_off()
        self._pa_off()

    def result_off(self):
        """結果表示消灯"""
        self._led_win.off()
        self._led_drow.off()
        self._led_lose.off()

    def display_off(self):
        """全消灯"""
        self.hand_off()
        self.result_off()
    
    def show_gu(self):
        """グーを表示"""
        self.hand_off()
        for led in self._leds_gu:
            led.on()

    def show_ch(self):
        """チョキを表示"""
        self.hand_off()
        for led in self._leds_ch:
            led.on()

    def show_pa(self):
        """パーを表示"""
        self.hand_off()
        for led in self._leds_pa:
            led.on()

    def show_win(self):
        """勝ちを表示"""
        self.result_off()
        self._led_win.on()

    def show_drow(self):
        """勝ちを表示"""
        self.result_off()
        self._led_drow.on()

    def show_lose(self):
        """勝ちを表示"""
        self.result_off()
        self._led_lose.on()

    def show_result_full(self):
        """結果全点灯(点検用)"""
        self._led_win.on()
        self._led_drow.on()
        self._led_lose.on()

    def show_hand_full(self):
        """じゃんけんの手全点灯(点検用)"""
        self.show_gu()
        self.show_ch()
        self.show_pa()

    def show_full(self):
        """全店頭(点検用)"""
        self.show_result_full()
        self.show_hand_full()

# ==================
# テストコード
# ================== 
if __name__  == "__main__":
    print("test start -----")
    WAIT_SEC = 2
    # じゃんけんの手用LED
    led_gu = Led(0)
    led_ch = Led(1)
    led_pa = Led(2)
    led_g_c = Led(3)
    led_c_p = Led(4)
    # 結果表示用LED
    led_w = Led(5)
    led_d = Led(6)
    led_l = Led(7)
    # スクリーン初期化
    cls = JankenScreen([led_gu, led_g_c],
                       [led_ch, led_g_c, led_c_p],
                       [led_pa, led_c_p],
                       led_w, led_d, led_l)
    # 各種表示確認
    print("win")
    cls.show_win()
    utime.sleep(WAIT_SEC)

    print("drow")
    cls.show_drow()
    utime.sleep(WAIT_SEC)

    print("lose")
    cls.show_lose()
    utime.sleep(WAIT_SEC)

    print("gu")
    cls.show_win()
    cls.show_gu()
    utime.sleep(WAIT_SEC)

    print("ch")
    cls.show_drow()
    cls.show_ch()
    utime.sleep(WAIT_SEC)

    print("pa")
    cls.show_lose()
    cls.show_pa()
    utime.sleep(WAIT_SEC)

    print("result_off")
    cls.show_gu()
    cls.result_off()
    utime.sleep(WAIT_SEC)

    print("hand_off")
    cls.hand_off()
    utime.sleep(WAIT_SEC)

    print("result_full")
    cls.show_result_full()
    utime.sleep(WAIT_SEC)

    print("hand_off")
    cls.show_hand_full()
    utime.sleep(WAIT_SEC)

    print("display_off")
    cls.display_off()

    print("test end   -----")
