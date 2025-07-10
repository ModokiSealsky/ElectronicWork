import utime

class ResultLight:
    """結果表示ライトクラス"""

    def __init__(self, led_highscore, led_timeup):
        """コンストラクタ

        Args:
            led_highscore: ハイスコア更新LED
            led_timeup: タイムアップLED
        """
        self._led_highscore = led_highscore
        self._led_timeup = led_timeup

    def show_highscore(self):
        """ハイスコア更新表示"""
        self._led_highscore.on()
        self._led_timeup.off()

    def show_timeup(self):
        """タイムアップ表示"""
        self._led_highscore.off()
        self._led_timeup.on()

    def off_all(self):
        """全消灯"""
        self._led_highscore.off()
        self._led_timeup.off()

# ==================
# テストコード
# ==================
if __name__  == "__main__":
    print("test start ----")
    from PicoLib import Led
    highscore = Led(14)
    timeisup = Led(15)
    result_light = ResultLight(highscore, timeisup)
    result_light.show_highscore()
    utime.sleep(1)
    result_light.show_timeup()
    utime.sleep(1)
    result_light.off_all()
    print("test end   ----")
