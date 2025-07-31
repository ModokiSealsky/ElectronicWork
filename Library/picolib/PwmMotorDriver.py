from machine import Pin, PWM


class PwmMotorDriver:
    """PWMモータードライバクラス"""

    def __init__(self, pin_a_no: int, pin_b_no: int, freq: int = 50):
        """コンストラクタ

        Args:
            pin_a_no: モーター制御に使うA側PWMピン番号
            pin_b_no: モーター制御に使うB側PWMピン番号
            freq: PWM周波数
        """
        self.__pwm_pin_a = PWM(Pin(pin_a_no))
        self.__pwm_pin_a.freq(freq)
        self.__pwm_pin_b = PWM(Pin(pin_b_no))
        self.__pwm_pin_b.freq(freq)

    def set_speed(self, speed_percent: float):
        """回転速度比率を設定

        Args:
            speed_percent: 回転速度比(マイナス値は逆転)
        """
        # 範囲外は最大値に丸める
        if speed_percent > 100:
            speed_percent = 100
        elif speed_percent < -100:
            speed_percent = -100
        # 回転方向によって出力先を変更
        if speed_percent >= 0:
            self.__pwm_pin_a.duty_u16(int(speed_percent * 65535 / 100))
            self.__pwm_pin_b.duty_u16(0)
        else:
            self.__pwm_pin_a.duty_u16(0)
            self.__pwm_pin_b.duty_u16(int(-speed_percent * 65535 / 100))

    def brake(self):
        """モーターを制動"""
        self.__pwm_pin_a.duty_u16(65535)
        self.__pwm_pin_b.duty_u16(65535)

    def off(self):
        """モーターを停止"""
        self.__pwm_pin_a.duty_u16(0)
        self.__pwm_pin_b.duty_u16(0)


# ==================
# テストコード
# ==================
if __name__ == "__main__":
    import time

    print("test start ----")
    motor = PwmMotorDriver(0, 1)
    print("+33.3")
    motor.set_speed(33.3)
    time.sleep(1)
    print("+90")
    motor.set_speed(90)
    time.sleep(1)
    motor.brake()
    time.sleep(1)
    print("-50")
    motor.set_speed(-50)
    time.sleep(1)
    print("-100")
    motor.set_speed(-100)
    time.sleep(1)
    motor.off()
    print("test end   ----")
