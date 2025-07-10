import utime

from machine import Pin, PWM

from picolib import Buzzer

class PwmBuzzer(Buzzer):
    """PWMブザークラス"""

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
    print("test end   ----")
