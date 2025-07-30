import utime

from picolib import PwmBuzzer
from reflexesgame.SoundEffectUnit import SoundEffectUnit, SoundEffectUnitTester


class SoundEffectUnitByPwm(SoundEffectUnit):
    """圧電ブザー使用による効果音再生ユニット"""

    def __init__(self, pwm_buzzer: PwmBuzzer):
        """コンストラクタ

        Args:
            pin_no: 圧電ブザー接続ピン番号
        """
        self.__buzzer = pwm_buzzer

    def __ng(self):
        """お手付き音"""
        self.__buzzer.off()
        utime.sleep_ms(10)
        self.__buzzer.hz_beep(50, 500)
        self.__ng_thread_exectng = False

    def ok(self):
        """正解音"""
        self.__buzzer.hz_beep(100, 4000)

    def highscore(self):
        """ハイスコア更新メロディ"""
        self.__buzzer.hz_beep(100, 1000)
        utime.sleep_ms(10)
        self.__buzzer.hz_beep(100, 2000)
        utime.sleep_ms(10)
        self.__buzzer.hz_beep(100, 3000)
        utime.sleep_ms(10)
        self.__buzzer.hz_beep(100, 4000)
        utime.sleep_ms(10)

    def gameclear(self):
        """ゲームクリアメロディ"""
        self.__buzzer.hz_beep(100, 4000)
        utime.sleep_ms(100)
        self.__buzzer.hz_beep(1000, 4000)
        utime.sleep_ms(10)

    def gameover(self):
        """ゲームオーバーメロディ"""
        self.__buzzer.hz_beep(100, 2000)
        utime.sleep_ms(100)
        self.__buzzer.hz_beep(1000, 500)

    def pickup(self):
        """点灯音"""
        self.__buzzer.hz_beep(100, 2000)

    def gamestart(self):
        """ゲーム開始メロディ"""
        self.__buzzer.hz_beep(1000, 4000)

    def signal_ready(self):
        """信号機カウントダウン音"""
        self.__buzzer.hz_beep(100, 2000)

    def signal_go(self):
        """信号機GO音"""
        self.__buzzer.hz_beep(100, 4000)

    def check(self):
        """確認"""
        self.__buzzer.hz_beep(100, 2000)
        self.__buzzer.hz_beep(100, 4000)


# ==================
# テストコード
# ==================
if __name__ == "__main__":
    print("test start ----")
    se_unit = SoundEffectUnitByPwm(PwmBuzzer(0))
    tester = SoundEffectUnitTester(se_unit)
    tester.test()
    print("test end   ----")
