import utime

from machine import Pin


class InputSwitch:
    """入力スイッチクラス"""

    def __init__(self, pin_no: int):
        """
        Args:
            pin_no: GPIOピン番号
        """
        self._swt = Pin(pin_no, Pin.IN, Pin.PULL_DOWN)
        self._is_before_on: bool = False
        self._on_torriger: bool = False
        self._off_torriger: bool = False

    def is_on(self):
        """スイッチがONかを確認"""
        return self._swt.value() == 1

    def is_off(self):
        """スイッチがOFFかを確認"""
        return self._swt.value() == 0


# ==================
# テストコード
# ==================
if __name__ == "__main__":
    print("test start ----")
    cls = InputSwitch(0)
    keep_on_cnt = 0
    while keep_on_cnt < 4:
        print(
            "btn on:{0}/off:{1}| cnt:{2}".format(cls.is_on(), cls.is_off(), keep_on_cnt)
        )
        if cls.is_on():
            keep_on_cnt += 1
        else:
            keep_on_cnt = 0
        utime.sleep(1)
    print("test end   ----")
