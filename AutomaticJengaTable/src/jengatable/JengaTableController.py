from machine import ADC, Pin

class JengaTableController:
    def __init__(self, adc_no_elv, adc_no_turn, adc_no_push):
        self.e = ADC(adc_no_elv)
        self.t = ADC(adc_no_turn)
        self.p = ADC(adc_no_push)
        self.vol_rate = 3.3 / 65535
        self.angle_rate = 180 / 65535

    def getVolumeElevetor(self):
        return self.e.read_u16() * self.angle_rate
    
    def getVolumeTurntable(self):
        return self.getAngle(self.t.read_u16())
    
    def getVolumePusher(self):
        return self.getAngle(self.p.read_u16())

    def getAngle(self, u16):
        vol = u16 * self.angle_rate
        # -2.7-3.3-
        if vol < 0.0:
            vol = 0.0
        if vol > 180.0:
            vol = 180.0
        return "{:.1f}".format(vol)