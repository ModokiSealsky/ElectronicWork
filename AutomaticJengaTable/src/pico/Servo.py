from machine import PWM, Pin

class Servo:
    """サーボ制御クラス
    pin番号を渡してインスタンス化する。
    角度の指定のみ行える。
    """
    SV_MAX_DUTY = 65025
    SV_FREQ = 50
    DUTY_RATE = 9.5 / 1800.0

    def __init__(self, pin_no:int):
        """コンストラクタ
        Args:
            pin_no: 制御用PWMピン番号
        """
        self.s = PWM(Pin(pin_no))
        self.s.freq(self.SV_FREQ)

    def turn(self, angle:float):
        """角度変更
        Args:
            angle: 0.0～180.0の角度値
        """
        if angle < 0.0:
            angle = 0.0
        if angle > 180.0:
            ag = 180.0
        duty = int((angle * 9.5 / 180 + 2.5) * 65535 / 100)
        print(duty)
        duty = int((angle * 9.5 / 180 + 2.5) * 655.35)
        print(duty)
        duty = int((angle * 9.5 / 180.0 + 2.5) * 655.35)
        print(duty)
        self.s.duty_u16(duty)
