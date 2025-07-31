import utime

from machine import ADC, Pin

class CoreInfo:
    """CPUの電圧と温度を取得するクラス"""

    def __init__(self):
        """コンストラクタ"""
        self.v = ADC(Pin(29, Pin.IN))
        self.t = ADC(4)
        self.vol_rate = 3.3 / 65535

    def get_vsys_voltage(self):
        """VSYS入力電圧取得"""
        val = self.v.read_u16() * 3 * self.vol_rate
        return "{:.2f}v".format(val)

    def get_core_temperature(self):
        """CPU温度取得"""
        val = self.t.read_u16() * self.vol_rate
        temp = 27 - (val-0.706)/0.001721
        return "{:.1f}c".format(temp)

# ==================
# テストコード
# ================== 
if __name__  == "__main__":
    print("test start ----")
    cls = CoreInfo()
    for roop_cnt in range(10):
        print("{0}| {1}:{2}".format(
            roop_cnt, cls.get_vsys_voltage(), cls.get_core_temperature()))
        utime.sleep(1)
    print("test end   ----")
