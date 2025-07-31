import utime

from machine import Pin

from picolib.StepMotor import StepMotor, StepMotorTester


class StepMotorUnipolar(StepMotor):
    """ユニポーラステッピングモーター制御クラス"""

    # ステップモーター励磁パターン指定
    __FULL_SIGNAL = [
        [1, 1, 0, 0],
        [0, 1, 1, 0],
        [0, 0, 1, 1],
        [1, 0, 0, 1],
        [1, 1, 0, 0],
        [0, 1, 1, 0],
        [0, 0, 1, 1],
        [1, 0, 0, 1],
    ]
    __WAVE_SIGNAL = [
        [1, 0, 0, 0],
        [1, 1, 0, 0],
        [0, 1, 0, 0],
        [0, 1, 1, 0],
        [0, 0, 1, 0],
        [0, 0, 1, 1],
        [0, 0, 0, 1],
        [1, 0, 0, 1],
    ]

    def __init__(
        self,
        pin_no1,
        pin_no2,
        pin_no3,
        pin_no4,
        is_counter: bool = False,
        one_lap_step: int = 200,
    ):
        """コンストラクタ
        Args:
            pin_no1 (int): 制御ピン番号
            pin_no2 (int): 制御ピン番号
            pin_no3 (int): 制御ピン番号
            pin_no4 (int): 制御ピン番号
        """
        super().__init__(is_counter, one_lap_step)
        self.__p1 = Pin(pin_no1, Pin.OUT)
        self.__p2 = Pin(pin_no2, Pin.OUT)
        self.__p3 = Pin(pin_no3, Pin.OUT)
        self.__p4 = Pin(pin_no4, Pin.OUT)
        self.__pos = 0
        self.__signal = self.__WAVE_SIGNAL
        print("StepMotorUnipolar init end")

    def use_full_signal(self):
        """"""
        self.__signal = self.__FULL_SIGNAL

    def use_wave_signal(self):
        """"""
        self.__signal = self.__WAVE_SIGNAL

    def __turn_step(self, step: int):
        print(f"turn_step:{step}")
        if step == 0:
            return
        signal = self.__signal
        pos = self.__pos
        add = 1
        if step < 0:
            add = 7
            step = step * -1
        print("add:{0} cnt:{1} pos:{2}".format(add, step, pos))
        for i in range(step):
            self.__p1.value(signal[pos][0])
            self.__p2.value(signal[pos][1])
            self.__p3.value(signal[pos][2])
            self.__p4.value(signal[pos][3])
            utime.sleep_ms(5)
            pos = (pos + add) % 8
        self.__pos = pos


# ==================
# テストコード
# ==================
if __name__ == "__main__":
    print("test start ----")
    step_motor = StepMotorUnipolar(2, 3, 4, 5)
    tester = StepMotorTester(step_motor)
    tester.turn_test()
    print("test end   ----")
