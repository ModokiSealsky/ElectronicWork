import utime
import _thread

from picolib import Buzzer
from reflexesgame.SoundEffectUnit import SoundEffectUnit, SoundEffectUnitTester


class SoundEffectUnitByTwinBuzzer(SoundEffectUnit):
    """圧電ブザー使用による効果音再生ユニット"""

    def __init__(self, buzzer_h: Buzzer, buzzer_l: Buzzer):
        """コンストラクタ

        Args:
            buzzer_h: 高音ブザー
            buzzer_l: 低音ブザー
        """
        self.__buzzer_h = buzzer_h
        self.__buzzer_l = buzzer_l

    def ng(self):
        """お手付き音"""
        # カウントダウンを止めないためにスレッド使用
        _thread.start_new_thread(self.__ng, ())

    def __ng(self):
        """お手付き音"""
        utime.sleep_ms(10)
        self.__buzzer_l.beep(50)

    def ok(self):
        """正解音"""
        self.__buzzer_h.beep(100)

    def highscore(self):
        """ハイスコア更新メロディ"""
        self.__buzzer_h.beep(1000)
        utime.sleep_ms(100)
        self.__buzzer_h.beep(1000)

    def gameclear(self):
        """ゲームクリアメロディ"""
        self.__buzzer_l.beep(100)
        utime.sleep_ms(100)
        self.__buzzer_h.beep(1000)

    def gameover(self):
        """ゲームオーバーメロディ"""
        self.__buzzer_l.beep(100)
        utime.sleep_ms(100)
        self.__buzzer_l.beep(1000)

    def pickup(self):
        """点灯音"""
        self.__buzzer_h.beep(100)

    def gamestart(self):
        """ゲーム開始メロディ"""
        self.__buzzer_h.beep(1000)

    def signal_ready(self):
        """信号機カウントダウン音"""
        self.__buzzer_l.beep(100)

    def signal_go(self):
        """信号機GO音"""
        self.__buzzer_h.beep(500)

    def check(self):
        """確認"""
        self.__buzzer_l.beep(500)
        utime.sleep_ms(100)
        self.__buzzer_h.beep(500)


# ==================
# テストコード
# ==================
if __name__ == "__main__":
    print("test start ----")
    se_unit = SoundEffectUnitByTwin(Buzzer(0), Buzzer(1))
    tester = SoundEffectUnitTester(se_unit)
    tester.test()
    print("test end   ----")
