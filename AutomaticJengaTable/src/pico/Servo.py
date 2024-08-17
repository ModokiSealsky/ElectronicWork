from machine import PWM, Pin

class Servo:
    """サーボ制御クラス
    pin番号を渡してインスタンス化する。
    角度の指定のみ行える。
    """
    SV_MAX_DUTY = 65025
    SV_FREQ = 50
    def __init__(self, pin_no):
        """コンストラクタ
        Args:
            pin_no (int): 制御用PWMピン番号
        """
        self.s = PWM(Pin(pin_no))
        self.s.freq(self.SV_FREQ)
    def turn(self, angle):
        """角度変更
        Args:
            angle (int): 0～180の角度値
        """
        if angle < 0:
            angle = 0
        if angle > 180:
            angle = 180
        duty = int((angle * 9.5 / 180 + 2.5) * 65535 / 100)
        self.s.duty_u16(duty)
        