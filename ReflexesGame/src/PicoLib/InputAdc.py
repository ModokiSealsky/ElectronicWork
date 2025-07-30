import utime

from machine import Pin, ADC


class InputAdc:
    """アナログ入力クラス"""

    def __init__(self, pin_no: int, vref_volt: float = 3.3):
        """
        Args:
            pin_no: GPIOピン番号
        """
        self.__adc = ADC(Pin(pin_no))
        self.__VREF_VOLT = vref_volt

    def get_u16_value(self):
        """アナログ値を取得"""
        return self.__adc.read_u16()

    def get_volt_value(self):
        """アナログ値を電圧に変換して取得"""
        return round(self.__adc.read_u16() / 65535 * self.__VREF_VOLT, 2)

    def get_parcents_value(self):
        """アナログ値をパーセントに変換して取得"""
        return round(self.__adc.read_u16() * 100 / 65535, 2)


# ==================
# テストコード
# ==================
if __name__ == "__main__":
    print("test start ----")
    adc = InputAdc(28)
    for _ in range(10):
        print("-------------------")
        print("adc u16 value: {0}".format(adc.get_u16_value()))
        print("adc volt value: {0}".format(adc.get_volt_value()))
        print("adc parcents value: {0}".format(adc.get_parcents_value()))
        utime.sleep(2)
    print("test end   ----")
