import utime

from machine import PWM, Pin

class Servo:
    """サーボ制御クラス

        角度を指定してサーボを制御する
        * pin番号を渡してインスタンス化する
        * turnメソッドに0.0から180.0の範囲で角度を指定する
    """
    SV_MAX_DUTY = 65025
    DUTY_RATE = 9.5 / 1800.0

    def __init__(self, pin_no: int, freq: int = 50):
        """コンストラクタ
        Args:
            pin_no: 制御用PWMピン番号
        """
        self.s = PWM(Pin(pin_no))
        self.s.freq(freq)

    def turn(self, angle:float):
        """角度変更
        Args:
            angle: 0.0～180.0の角度値
        """
        if angle < 0.0:
            angle = 0.0
        if angle > 180.0:
            ag = 180.0
        duty = int((angle * 9.5 / 180.0 + 2.5) * 655.35)
        self.s.duty_u16(duty)

# ==================
# テストコード
# ================== 
if __name__  == "__main__":
    print("test start ----")
    target = Servo(0)
    print("angle:0")
    target.turn(0)
    utime.sleep(1)
    print("angle:22.5")
    target.turn(22.5)
    utime.sleep(1)
    print("angle:90")
    target.turn(90)
    utime.sleep(1)
    print("angle:180")
    target.turn(180)
    utime.sleep(1)
    print("angle:122.5")
    target.turn(122.5)
    utime.sleep(1)
    print("angle:180.1")
    target.turn(180.1)
    utime.sleep(1)
    print("angle:-0.1")
    target.turn(-0.1)
    utime.sleep(1)
    print("test end   ----")
