import utime

from machine import Pin
from micropython import const


class InputSwitch(object):
    """入力スイッチクラス"""

    __swt: Pin
    """スイッチのピンオブジェクト"""
    __on_val: int
    """ボタンON値"""

    def __init__(self, pin_no: int, is_pull_up: bool = False, is_reverse: bool = False):
        """
        Args:
            pin_no: GPIOピン番号
            is_pull_up: PullUp指定(回路をプルアップ、スイッチの先がGNDで組む場合にTrue)
            is_reverse: ON/OFF逆転指定
        """
        if is_pull_up:
            self.__swt = Pin(pin_no, Pin.IN, Pin.PULL_UP)
        else:
            self.__swt = Pin(pin_no, Pin.IN, Pin.PULL_DOWN)
        if is_reverse:
            self.__on_val = const(0)
        else:
            self.__on_val = const(1)

    def is_on(self):
        """スイッチがONかを確認"""
        return self.__swt.value() == self.__on_val

    def is_off(self):
        """スイッチがOFFかを確認"""
        return self.__swt.value() != self.__on_val

    def test(self, test_time: int = 10):
        """テストコード"""
        print("test start ----")
        cnt = 0
        while cnt < test_time:
            self.__print_value(cnt)
            cnt += 1
            utime.sleep(1)
        print("test end   ----")

    def __print_value(self, cnt: int):
        print("btn on:{0}/off:{1}| cnt:{2}".format(self.is_on(), self.is_off(), cnt))


# ==================
# テストコード
# ==================
if __name__ == "__main__":
    print("test down normal ----")
    cls = InputSwitch(0)
    cls.test()
    print("test up normal ----")
    cls = InputSwitch(0, True)
    cls.test()
    print("test down reverse ----")
    cls = InputSwitch(0, False, True)
    cls.test()
    print("test up reverse ----")
    cls = InputSwitch(0, True, True)
    cls.test()
