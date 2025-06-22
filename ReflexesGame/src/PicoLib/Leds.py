import utime

from PicoLib import Led

class Leds(Led):
    """複数LED同時管理クラス"""
    def __init__(self, pin_no_list: list[int]):
        """"
        Args:
            pin_no: GPIOピン番号
        """
        
        self._leds = [Led(pin_no) for pin_no in pin_no_list]
        self._led_count = len(self._leds)

    def on(self):
        """LED点灯"""
        for idx in range(self._led_count):
            self._leds[idx].on()
    
    def off(self):
        """LED消灯"""
        for idx in range(self._led_count):
            self._leds[idx].off()

# ==================
# テストコード
# ==================
if __name__  == "__main__":
    print("test start ----")
    leds = Leds([14, 15])
    leds.on()
    utime.sleep(1)
    leds.off()
    print("test end   ----")
