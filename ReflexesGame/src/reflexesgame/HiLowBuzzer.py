import utime

class HiLowBuzzer:
    """高低音ブザー制御クラス"""

    def __init__(self, buzzer_h, buzzer_l):
        """コンストラクタ

        Args:
            buzzer_h: 高音ブザー
            buzzer_l: 低音ブザー
        """
        self._buzzer_h = buzzer_h
        self._buzzer_l = buzzer_l

    def hi_beep(self, ms: int = 100):
        """高音ブザー音を鳴らす
        
        Args:
            ms: 指定ミリ秒(省略した場合は100)
        """
        self._buzzer_h.beep(ms)

    def low_beep(self, ms: int = 100):
        """低音ブザー音を鳴らす

        Args:
            ms: 指定ミリ秒(省略した場合は100)
        """
        self._buzzer_l.beep(ms)

    def play_clear(self):
        """ゲームクリア音"""
        self._buzzer_l.beep(50)
        utime.sleep_ms(50)
        self._buzzer_h.beep(50)
        utime.sleep_ms(50)
        self._buzzer_l.beep(50)
        utime.sleep_ms(50)
        self._buzzer_h.beep(50)

    def play_foul(self):
        """ゲーム失敗音"""
        self._buzzer_h.beep(50)
        utime.sleep_ms(50)
        self._buzzer_l.beep(50)
        utime.sleep_ms(50)
        self._buzzer_h.beep(50)
        utime.sleep_ms(50)
        self._buzzer_l.beep(50)

# ==================
# テストコード
# ================== 
if __name__  == "__main__":
    print("test start ----")
    from PicoLib import Buzzer
    buzzer_l = Buzzer(17)
    buzzer_h = Buzzer(16)
    hl_buzzer = HiLowBuzzer(buzzer_l, buzzer_h)
    hl_buzzer.hi_beep()
    utime.sleep(1)
    hl_buzzer.low_beep()
    utime.sleep(1)
    hl_buzzer.play_clear()
    utime.sleep(1)
    hl_buzzer.play_foul()
    print("test end   ----")