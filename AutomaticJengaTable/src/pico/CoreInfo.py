from machine import ADC, Pin

class CoreInfo:
    def __init__(self):
        self.v = ADC(Pin(29, Pin.IN))
        self.t = ADC(4)
        self.vol_rate = 3.3 / 65535

    def getVoltage(self):
        val = self.v.read_u16() * 3 * self.vol_rate
        return "{:.2f}v".format(val)

    def getTemperature(self):
        val = self.t.read_u16() * self.vol_rate
        temp = 27 - (val-0.706)/0.001721
        return "{:.1f}c".format(temp)