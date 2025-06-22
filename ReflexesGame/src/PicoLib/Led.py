import utime

from machine import Pin

class Led:
    """LEDクラス"""
    def __init__(self, pin_no: int):
        """"
        Args:
            pin_no: GPIOピン番号
        """
        self._led = Pin(pin_no, Pin.OUT, Pin.PULL_DOWN)

    def on(self):
        """LED点灯"""
        self._led.on()
    
    def off(self):
        """LED消灯"""
        self._led.off()

# ==================
# テストコード
# ==================
if __name__  == "__main__":
    print("test start ----")
    highscore = Led(14)
    timeisup = Led(15)
    highscore.on()
    utime.sleep(1)
    highscore.off()
    timeisup.on()
    utime.sleep(1)
    timeisup.off()
    print("test end   ----")
