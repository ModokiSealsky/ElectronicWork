import utime

from machine import Pin, PWM

from picolib import Buzzer


class PwmBuzzer(Buzzer):
    """PWMブザークラス"""

    class Note:
        def __init__(self, ms: int, hz: int, end_wait_ms: int = 10):
            """コンストラクタ

            Args:
                ms: 音を鳴らすミリ秒
                hz: 音の高さ(Hz)
                end_wait_ms: 次の音までの待機ミリ秒 省略した場合は10)
            """
            self._ms = ms
            self._hz = hz
            self._end_wait_ms = end_wait_ms

        def __str__(self):
            """音符の情報文を取得する"""
            return "{{ms:{0: >6}, score:{1: >6}, end_wait:{2: >6}}}".format(
                self._ms, self._hz, self._end_wait_ms
            )

    def __init__(self, pwm_pin_no: int):
        """コンストラクタ

        Args:
            pwm_pin_no: ブザー制御に使うGPIOピン番号
        """
        self._buzzer = PWM(Pin(pwm_pin_no))

    def beep(self, ms: int = 100):
        """指定したミリ秒だけ音を鳴らす

        Args:
            ms: 指定ミリ秒(省略した場合は100)
        """
        self.hz_beep(ms)

    def hz_beep(self, ms: int = 100, hz: int = 1000):
        """指定したミリ秒だけ音を鳴らす

        Args:
            ms: 指定ミリ秒(省略した場合は100)
            hz: 周波数(省略した場合は1000)
        """
        self._buzzer.freq(hz)
        self._buzzer.duty_u16(32768)
        utime.sleep_ms(ms)
        self._buzzer.duty_u16(0)

    def play_music(self, music: list[Note]):
        """指定した配列の値を元に曲を再生する

        Args:
            music:
        """
        print("play music start.")
        for note in music:
            self.hz_beep(note._ms, note._hz)
            utime.sleep_ms(note._end_wait_ms)
        print("play music end.")

    def set_hz(self, hz: int):
        """周波数指定

        Args:
            hz: 周波数(Hz)
        """
        self._buzzer.freq(hz)
        self._buzzer.duty_u16(32768)

    def off(self):
        """消音"""
        self._buzzer.freq(0)
        self._buzzer.duty_u16(0)


# ==================
# テストコード
# ==================
if __name__ == "__main__":
    print("test start ----")
    # 音程指定なし
    buzzer = PwmBuzzer(0)
    buzzer.beep()
    utime.sleep(1)
    buzzer.beep(1000)
    utime.sleep(1)
    # 音程指定あり
    buzzer.hz_beep(hz=500)
    utime.sleep(1)
    buzzer.hz_beep(1000, 4000)
    utime.sleep(1)
    # 音楽再生
    music = [
        PwmBuzzer.Note(400, 523),
        PwmBuzzer.Note(400, 523),
        PwmBuzzer.Note(1600, 830, 100),
        PwmBuzzer.Note(530, 880),
        PwmBuzzer.Note(530, 622),
        PwmBuzzer.Note(530, 698),
        PwmBuzzer.Note(1600, 783),
    ]
    [print(note) for note in music]
    buzzer.play_music(music)
    print("test end   ----")
