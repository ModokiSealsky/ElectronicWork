import utime

from machine import Pin

from picolib.StepMotor import StepMotor, StepMotorTester


class StepMotorBipolarWithTb6600(StepMotor):
    """TB6600ドライバによるバイポーラステッピングモーター制御クラス"""

    def __init__(
        self,
        pin_ena: int,
        pin_dir: int,
        pin_pul: int,
        is_counter: bool = False,
        one_lap_step: int = 200,
    ):
        """コンストラクタ
        Args:
            pin_ena (int): ENA制御ピン番号
            pin_dir (int): DIR制御ピン番号
            pin_pul (int): PUL制御ピン番号
            is_counter: 反時計回り(正負逆転)指定
            one_lap_step: 1回転ステップ数
        """
        super().__init__(is_counter, one_lap_step)
        self._p_ena = Pin(pin_ena, Pin.OUT)
        self._p_ena.value(0)
        self._p_dir = Pin(pin_dir, Pin.OUT)
        self._p_dir.value(0)
        self._p_pul = Pin(pin_pul, Pin.OUT)
        self._p_pul.value(0)
        print("StepMotorBipolar init end")

    def __turn_step(self, step_count: int):
        print(f"turn_step:{step_count}")
        if step_count == 0:
            return
        dir_val = 1
        if step_count < 0:
            dir_val = 0
            step_count = step_count * -1

        for i in range(step_count):
            self._p_ena.value(1)
            self._p_dir.value(dir_val)
            self._p_pul.value(0)
            utime.sleep_ms(self.__puls_wait_ms)
            self._p_pul.value(1)
            utime.sleep_ms(self.__puls_wait_ms)
        utime.sleep_ms(1000)


# ==================
# テストコード
# ==================
if __name__ == "__main__":
    print("test start ----")
    step_motor = StepMotorBipolarWithTb6600(2, 3, 4)
    tester = StepMotorTester(step_motor)
    tester.turn_test()
    print("test end   ----")
