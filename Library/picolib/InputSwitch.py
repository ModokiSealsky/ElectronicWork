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

    def refresh_torriger(self):
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

# ==================
# テストコード
# ==================
if __name__  == "__main__":
    print("test start ----")
    cls = InputSwitch(0)
    keep_on_cnt = 0
    while keep_on_cnt < 4:
        cls.refresh_torriger()
        print("btn on:{0}/off:{1} | trriger on:{2}/off:{3} | cnt:{4}".format(
            cls.is_on(), cls.is_off(),
            cls.is_on_trriger(), cls.is_off_trriger(),
            keep_on_cnt))
        if cls.is_on():
            keep_on_cnt +=1
        else:
            keep_on_cnt = 0
        utime.sleep(1)
    print("test end   ----")
