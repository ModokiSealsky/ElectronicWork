import time

from machine import Pin


class StepMotor:
    """ステッピングモーター制御(抽象)クラス"""

    def __init__(
        self, is_counter: bool = False, one_lap_step: int = 200, puls_wait_ms: int = 5
    ):
        """コンストラクタ

        Args:
            is_counter: 反時計回り(正負逆転:ステップ数がプラス値で反時計回りならTrue)指定
            one_lap_step: 1回転ステップ数
            puls_wait_ms: ステップ間隔ミリ秒
        """
        print("init start")
        self.__is_counter = is_counter
        print(f"set_counterclockwise:{self.__is_counter}")
        self.__one_lap_step = one_lap_step
        self.__angle_racio = 360 / self.__one_lap_step
        print(
            f"set_one_lap_step:{self.__one_lap_step} | angle_racio:{self.__angle_racio}"
        )
        self.__puls_wait_ms = puls_wait_ms
        print(f"set_puls_wait_ms:{self.__puls_wait_ms}")
        print("init end")

    def turn_step(self, step: int):
        """指定ステップ数回転

        Args:
            step: 回転ステップ数（正の値は時計回り）
        """
        if self.__is_counter:
            step = -step
        self.__turn_step(step)

    def turn_angle(self, angle: float):
        """指定角度回転

        Args:
            angle: 回転角度（正の値は時計回り）
        """
        step = int(angle / self.__angle_racio)
        self.turn_step(step)

    def off(self):
        """回転停止"""
        print("off")

    def __turn_step(self, step: int):
        """指定ステップ数回転（子クラスで実装する）

        Args:
            step: 回転ステップ数（正の値は時計回り）
        """
        print(f"turn_step:{step}")


class StepMotorUnipolarWithUnl2003(StepMotor):
    """UNL2003ドライバによるユニポーラステッピングモーター制御クラス"""

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
    """フルステップ信号"""
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
    """ウェーブドライブ信号"""

    def __init__(
        self,
        pin_no1,
        pin_no2,
        pin_no3,
        pin_no4,
        is_wave_signal: bool = True,
        is_counter: bool = False,
        one_lap_step: int = 200,
        puls_wait_ms: int = 5,
    ):
        """コンストラクタ
        Args:
            pin_no1 (int): 制御ピン番号
            pin_no2 (int): 制御ピン番号
            pin_no3 (int): 制御ピン番号
            pin_no4 (int): 制御ピン番号
            is_wave_signal: ウェーブドライブ指定(False指定でフルステップ)
            is_counter: 反時計回り(正負逆転:ステップ数がプラス値で反時計回りならTrue)指定
            one_lap_step: 1回転ステップ数
            puls_wait_ms: ステップ間隔ミリ秒
        """
        print("StepMotorUnipolar init start")
        super().__init__(is_counter, one_lap_step, puls_wait_ms)
        self.__p1 = Pin(pin_no1, Pin.OUT)
        self.__p2 = Pin(pin_no2, Pin.OUT)
        self.__p3 = Pin(pin_no3, Pin.OUT)
        self.__p4 = Pin(pin_no4, Pin.OUT)
        self.off()
        self.__pos = 0
        if is_wave_signal:
            self.__signal = self.__WAVE_SIGNAL
        else:
            self.__signal = self.__FULL_SIGNAL
        print("StepMotorUnipolar init end")

    def off(self):
        self.__p1.value(0)
        self.__p2.value(0)
        self.__p3.value(0)
        self.__p4.value(0)
        print("off")

    def __turn_step(self, step: int):
        print(f"turn_step:{step}")
        if step == 0:
            return
        pos = self.__pos
        add = 1
        step_cnt = step
        if step < 0:
            add = 7
            step_cnt = step * -1
        print("add:{0} cnt:{1} pos:{2}".format(add, step, pos))
        for i in range(step_cnt):
            signal = self.__signal[pos]
            self.__p1.value(signal[0])
            self.__p2.value(signal[1])
            self.__p3.value(signal[2])
            self.__p4.value(signal[3])
            time.sleep_ms(self.__puls_wait_ms)
            pos = (pos + add) % 8
        self.__pos = pos


class StepMotorBipolarWithTb6600(StepMotor):
    """TB6600ドライバによるバイポーラステッピングモーター制御クラス"""

    def __init__(
        self,
        pin_ena: int,
        pin_dir: int,
        pin_pul: int,
        is_counter: bool = False,
        one_lap_step: int = 200,
        puls_wait_ms: int = 5,
    ):
        """コンストラクタ
        Args:
            pin_ena (int): ENA制御ピン番号
            pin_dir (int): DIR制御ピン番号
            pin_pul (int): PUL制御ピン番号
            is_counter: 反時計回り(正負逆転)指定
            one_lap_step: 1回転ステップ数
            puls_wait_ms: ステップ間隔ミリ秒
        """
        print("StepMotorBipolar init start")
        super().__init__(is_counter, one_lap_step, puls_wait_ms)
        self._p_ena = Pin(pin_ena, Pin.OUT)
        self._p_dir = Pin(pin_dir, Pin.OUT)
        self._p_pul = Pin(pin_pul, Pin.OUT)
        self.off()
        print("StepMotorBipolar init end")

    def off(self):
        self._p_ena.value(0)
        self._p_dir.value(0)
        self._p_pul.value(0)
        print("off")

    def __turn_step(self, step_count: int):
        print(f"turn_step:{step_count}")
        if step_count == 0:
            return
        dir_val = 1
        if step_count < 0:
            dir_val = 0
            step_count = step_count * -1

        self._p_ena.value(1)
        self._p_dir.value(dir_val)
        self._p_pul.value(1)
        for i in range(step_count):
            # self._p_ena.value(1)
            # self._p_dir.value(dir_val)
            self._p_pul.value(0)
            time.sleep_ms(self.__puls_wait_ms)
            self._p_pul.value(1)
            time.sleep_ms(self.__puls_wait_ms)
        self.off()


# ==================
# テストコード
# ==================
if __name__ == "__main__":
    print("test start ----")
    default_step_motor = StepMotor()
    reverse_step_motor = StepMotor(True)
    step400_step_motor = StepMotor(False, 400)
    wait100_step_motor = StepMotor(False, 200, 100)
    print("turn_step(100)")
    default_step_motor.turn_step(100)
    time.sleep(1)
    reverse_step_motor.turn_step(100)
    time.sleep(1)
    step400_step_motor.turn_step(100)
    time.sleep(1)
    wait100_step_motor.turn_step(10)
    time.sleep(1)
    print("turn_step(-100)")
    default_step_motor.turn_step(-100)
    time.sleep(1)
    reverse_step_motor.turn_step(-100)
    time.sleep(1)
    step400_step_motor.turn_step(-100)
    time.sleep(1)
    wait100_step_motor.turn_step(-10)
    time.sleep(1)
    print("turn_angle(90)")
    default_step_motor.turn_angle(90)
    time.sleep(1)
    reverse_step_motor.turn_angle(90)
    time.sleep(1)
    step400_step_motor.turn_angle(90)
    time.sleep(1)
    wait100_step_motor.turn_angle(90)
    time.sleep(1)
    print("turn_angle(-90)")
    default_step_motor.turn_angle(-90)
    time.sleep(1)
    reverse_step_motor.turn_angle(-90)
    time.sleep(1)
    step400_step_motor.turn_angle(-90)
    time.sleep(1)
    wait100_step_motor.turn_angle(-90)
    time.sleep(1)
    print("--------")
    default_step_motor.off()
    print("test end   ----")
