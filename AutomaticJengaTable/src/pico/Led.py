from machine import Pin

class Led:
    """LED制御クラス

        * pin番号を渡してインスタンス化する
        * 点灯(on)と消灯(off)が行える。
    """
    def __init__(self, pin_no):
        """コンストラクタ
        Args:
            pin_no (int): 制御ピン番号
        """
        self._pin = Pin(pin_no, Pin.OUT)

    def on(self):
        """点灯
        """
        self._pin.value(1)

    def off(self):
        """消灯
        """
        self._pin.value(0)
