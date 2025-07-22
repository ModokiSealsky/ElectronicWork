import time


class StepMotor:
    """ステッピングモーター制御(抽象)クラス"""

    def __init__(self, is_counter: bool = False, one_lap_step: int = 200):
        """コンストラクタ

        Args:
            is_counter: 反時計回り(正負逆転)指定
            one_lap_step: 1回転ステップ数
        """
        print("init start")
        self.set_counterclockwise(is_counter)
        self.set_one_lap_step(one_lap_step)
        print("init end")

    def set_counterclockwise(self, is_counter: bool):
        """反時計回り(正負逆転)指定

        Args:
            is_counter: ステップ数がプラス値で反時計回りならTrue
        """
        self.__is_counter = is_counter
        print(f"set_counterclockwise:{self.__is_counter}")

    def set_one_lap_step(self, step: int):
        """1回転ステップ数指定

        Args:
            step: 1回転に必要なステップ数
        """
        self.__one_lap_step = step
        self.__angle_racio = 360 / self.__one_lap_step
        print(
            f"set_one_lap_step:{self.__one_lap_step} | angle_racio:{self.__angle_racio}"
        )

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

    def __turn_step(self, step: int):
        """指定ステップ数回転（子クラスで実装する）

        Args:
            step: 回転ステップ数（正の値は時計回り）
        """
        print(f"turn_step:{step}")


class StepMotorTester:
    """テスタークラス"""

    def __init__(self, target: StepMotor):
        self.__target_clz = target

    def turn_test(self):
        # turn step
        print("turn_step(100)")
        self.__target_clz.turn_step(100)
        time.sleep(1)
        print("turn_step(-100)")
        self.__target_clz.turn_step(-100)
        time.sleep(1)
        print("set_counterclockwise(True)")
        self.__target_clz.set_counterclockwise(True)
        print("turn_step(100)")
        self.__target_clz.turn_step(100)
        time.sleep(1)
        print("turn_step(-100)")
        self.__target_clz.turn_step(-100)
        time.sleep(1)
        self.__target_clz.set_counterclockwise(False)
        # turn angle
        print("turn_angle(90)")
        self.__target_clz.turn_angle(90)
        time.sleep(1)
        print("turn_angle(-90)")
        self.__target_clz.turn_angle(-90)
        time.sleep(1)
        self.__target_clz.set_one_lap_step(400)
        print("turn_angle(90)")
        self.__target_clz.turn_angle(90)
        time.sleep(1)
        print("turn_angle(-90)")
        self.__target_clz.turn_angle(-90)
        time.sleep(1)
        self.__target_clz.set_counterclockwise(True)
        print("turn_angle(90)")
        self.__target_clz.turn_angle(90)
        time.sleep(1)
        print("turn_angle(-90)")
        self.__target_clz.turn_angle(-90)


# ==================
# テストコード
# ==================
if __name__ == "__main__":
    print("test start ----")
    step_motor = StepMotor()
    tester = StepMotorTester(step_motor)
    tester.turn_test()
    print("--------")
    step_motor = StepMotor(True, 500)
    print("test end   ----")
