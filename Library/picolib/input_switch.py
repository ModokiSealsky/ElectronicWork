"""入力スイッチパッケージ"""

import utime

from machine import Pin
from micropython import const


class InputSwitch:
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


class TriggerButton(InputSwitch):
    """トリガー判定付き入力スイッチクラス"""

    def __init__(self, pin_no: int, is_pull_up: bool = False, is_reverse: bool = False):
        """
        Args:
            pin_no: GPIOピン番号
            is_pull_up: PullUp指定(回路をプルアップ、スイッチの先がGNDで組む場合にTrue)
            is_reverse: ON/OFF逆転指定
        """
        super().__init__(pin_no, is_pull_up, is_reverse)
        self._is_before_on: bool = False
        self._on_torriger: bool = False
        self._off_torriger: bool = False

    def refresh(self):
        """トリガー更新"""
        is_on = self.is_on()
        if self._is_before_on == is_on:
            self._on_torriger = False
            self._off_torriger = False
        elif is_on:
            self._on_torriger = True
            self._off_torriger = False
        else:
            self._on_torriger = False
            self._off_torriger = True
        self._is_before_on = is_on

    def is_on_trriger(self):
        """スイッチがONになった瞬間かを確認

        refresh_torrigerでトリガー更新済みの状態で実行する。
        """
        return self._on_torriger

    def is_off_trriger(self):
        """スイッチがOFFになった瞬間かを確認

        refresh_torrigerでトリガー更新済みの状態で実行する。
        """
        return self._off_torriger

    def __print_value(self, cnt: int):
        self.refresh()
        print(
            "btn on:{0}/off:{1} | trriger on:{2}/off:{3} | cnt:{4}".format(
                self.is_on(),
                self.is_off(),
                self.is_on_trriger(),
                self.is_off_trriger(),
                cnt,
            )
        )


# ==================
# テストコード
# ==================
if __name__ == "__main__":
    print("test start ----")
    print("InputSwitch ----")
    print("test down normal ----")
    i_s = InputSwitch(0)
    i_s.test()
    print("test up normal ----")
    i_s = InputSwitch(0, True)
    i_s.test()
    print("test down reverse ----")
    i_s = InputSwitch(0, False, True)
    i_s.test()
    print("test up reverse ----")
    i_s = InputSwitch(0, True, True)
    i_s.test()

    print("TriggerButton ----")
    print("test down normal ----")
    t_b = TriggerButton(0)
    t_b.test()
    print("test up normal ----")
    t_b = TriggerButton(0, True)
    t_b.test()
    print("test down reverse ----")
    t_b = TriggerButton(0, False, True)
    t_b.test()
    print("test up reverse ----")
    t_b = TriggerButton(0, True, True)
    t_b.test()
    print("test fin ----")
