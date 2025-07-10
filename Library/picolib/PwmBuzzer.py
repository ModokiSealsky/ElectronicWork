import utime

from machine import Pin, PWM

from picolib import Buzzer

class PwmBuzzer(Buzzer):
    """PWMブザークラス"""

    class Note:
        SCORE = {
            "A2": 110, "A#2": 116, "B2": 123,
            "C3": 130, "C#3": 138, "D3": 146, "D#3": 155, "E3": 164, "F3": 174, "F#3": 184, "G3": 195, "G#3": 207, "A3": 220, "A#3": 233, "B3": 246,
            "C4": 261, "C#4": 277, "D4": 293, "D#4": 311, "E4": 329, "F4": 349, "F#4": 369, "G4": 391, "G#4": 415, "A4": 440, "A#4": 466, "B4": 493,
            "C5": 523, "C#5": 554, "D5": 587, "D#5": 622, "E5": 659, "F5": 698, "F#5": 739, "G5": 783, "G#5": 830, "A5": 880, "A#5": 932, "B5": 987,
            "C6": 1046, "C#6": 1108, "D6": 1174, "D#6": 1244, "E6": 1318, "F6": 1396, "F#6": 1479, "G6": 1567, "G#6": 1661, "A6": 1760, "A#6": 1864, "B6": 1975,
            "C7": 2093, "C#7": 2217, "D7": 2349, "D#7": 2489, "E7": 2637, "F7": 2793, "F#7": 2959, "G7": 3135, "G#7": 3322,"A7": 3520, "A#7": 3729, "B7": 3951,
            "C8": 4186,
        }

        def __init__(self, ms:int, hz:int, end_wait_ms:int = 10):
            """コンストラクタ

            Args:
                ms: 音を鳴らすミリ秒
                hz: 音の高さ(Hz)
                end_wait_ms: 次の音までの待機ミリ秒 省略した場合は10)
            """
            self._ms = ms
            self._hz = hz
            self._end_wait_ms = end_wait_ms


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


# ==================
# テストコード
# ================== 
if __name__  == "__main__":
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
        PwmBuzzer.Note(400, PwmBuzzer.Note.SCORE["C5"]),
        PwmBuzzer.Note(400, PwmBuzzer.Note.SCORE["C5"]),
        PwmBuzzer.Note(1600, PwmBuzzer.Note.SCORE["G#5"], 100),
        PwmBuzzer.Note(530, PwmBuzzer.Note.SCORE["A5"]),
        PwmBuzzer.Note(530, PwmBuzzer.Note.SCORE["D#5"]),
        PwmBuzzer.Note(530, PwmBuzzer.Note.SCORE["F5"]),
        PwmBuzzer.Note(1600, PwmBuzzer.Note.SCORE["G5"])
    ]
    buzzer.play_music(music)
    print("test end   ----")
