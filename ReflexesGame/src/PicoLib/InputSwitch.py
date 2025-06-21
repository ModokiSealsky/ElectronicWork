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

    def _check_torriger(self):
        """トリガー検知"""
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

    def is_on_trriger(self, torriger_check = True):
        """スイッチがONになった瞬間かを確認

        Args:
            torriger_check: in_on_torrigerとis_off_torrigerの両方を使う場合、後実行側はFalseを指定する
        """
        if torriger_check:
            self._check_torriger()
        return self._on_torriger

    def is_off_trriger(self, torriger_check = True):
        """スイッチがOFFになった瞬間かを確認

        Args:
            torriger_check: in_on_torrigerとis_off_torrigerの両方を使う場合、後実行側はFalseを指定する
        """
        if torriger_check:
            self._check_torriger()
        return self._off_torriger

# ==================
# テストコード
# ==================
if __name__  == "__main__":
    print("test start ----")
    btn = InputSwitch(19)
    btn_cnt = 0
    while btn_cnt < 4:
        print("btn on:{0}/off:{1} | trriger on:{2}/off:{3} | cnt:{4}".format(
            btn.is_on(), btn.is_off(),
            btn.is_on_trriger(), btn.is_off_trriger(False),
            btn_cnt))
        if btn.is_on():
            btn_cnt +=1
        else:
            btn_cnt = 0
        utime.sleep(1)
    print("test end   ----")
