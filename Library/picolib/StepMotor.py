from enum import Enum

from machine import Pin

class StepMortorType(Enum):
    _28BY48 = "28BY48"
    _NAME17 = "NAME1"


class StepMotor:
    """ステップモーターのインターフェース"""
    def setBaseVolPin(self, pin_no):
        """基準電圧ピン設定

        GPIOを3.3V出力として使用する場合、ピン番号を指定する

        Args:
            pin_no (int): 基準電圧ピン番号
        """
        Pin(pin_no, Pin.OUT).value(1)

    def step(self, step_count: int):
        """指定ステップ数回転
        Args:
            step_count (int): 回転ステップ数（負数は逆転方向）
        """
        print("step_count:{0}".format(step_count))

    def turn_angle(self, angle: float):
        """指定角度回転)
        Args:
            angle: 回転角度（負数は反時計回り）
        """
        print("angle:{0}".format(angle))
