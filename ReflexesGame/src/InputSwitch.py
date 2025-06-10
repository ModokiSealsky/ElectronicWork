from machine import Pin
import utime

class InputSwitch:
    """入力スイッチクラス"""
    def __init__(self, pin_no:int):
        """
        Args:
            pin_no: GPIOピン番号
        """
        self._swt = Pin(pin_no, Pin.IN, Pin.PULL_DOWN)
    
    def isOn(self):
        """スイッチがONかを確認"""
        return self._swt.value() == 1

    def isOff(self):
        """スイッチがOFFかを確認"""
        return self._swt.value() == 0

# ==================
# テストコード
# ==================
if __name__  == "__main__":
    print("test start ----")
    btn = InputSwitch(3)
    btn_cnt = 0
    while btn_cnt < 4:
        print("btn on:{0}/off:{1} | cnt:{2}".format(btn.isOn(), btn.isOff(), btn_cnt))
        if btn.isOn():
            btn_cnt +=1
        else:
            btn_cnt = 0
        utime.sleep(1)
    print("test end   ----")
