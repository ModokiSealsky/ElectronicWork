import utime

from machine import Pin

class Buzzer:
    """ブザークラス"""

    def __init__(self, gpio_pin_no: int):
        """コンストラクタ

        Args:
            goio_pin_no: ブザー制御に使うGPIOピン番号
        """
        self._buzzer = Pin(gpio_pin_no, Pin.OUT)
    
    def beep(self, ms: int = 100):
        """指定したミリ秒だけ音を鳴らす
        
        Args:
            ms: 指定ミリ秒(省略した場合は100)
        """
        self._buzzer.on()
        utime.sleep_ms(ms)
        self._buzzer.off()

# ==================
# テストコード
# ================== 
if __name__  == "__main__":
    print("test start ----")
    # 低音
    buzzer_l = Buzzer(17)
    buzzer_l.beep()
    utime.sleep_ms(1000)
    buzzer_l.beep(500)
    utime.sleep_ms(1000)
    # 高音
    buzzer_h = Buzzer(16)
    buzzer_h.beep()
    utime.sleep_ms(1000)
    buzzer_h.beep(500)
    print("test end   ----")
