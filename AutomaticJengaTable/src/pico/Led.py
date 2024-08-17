from machine import Pin

# LEDクラス
class Led:
    """LED制御クラス
    pin番号を渡してインスタンス化する。
    点灯と消灯が行える。
    """
    def __init__(self, pin_no):
        """コンストラクタ
        Args:
            pin_no (int): 制御ピン番号
        """
        self.l = Pin(pin_no, Pin.OUT)

    def on(self):
        """点灯
        """
        self.l.value(1)

    def off(self):
        """消灯
        """
        self.l.value(0)
