from machine import Pin

class ToggleSwitch:
    """トグルスイッチ状態取得クラス

        ON/OFFを切り替えられるスイッチからの入力を取得    
        * pin番号を渡してインスタンス化する
        * スイッチがON(is_on)かOFF(is_off)かを取得する
    """
    def __init__(self, pin_no: int):
        """コンストラクタ
        Args:
            pin_no: スイッチの入力に使うGPIOピン番号
        """
        self._pin = Pin(pin_no, Pin.IN, Pin.PULL_DOWN)
    
    def is_on(self) -> bool:
        """スイッチがONならTrueを返す"""
        return self._pin.value() == 1

    def is_off(self) -> bool:
        """スイッチがOFFならTrueを返す"""
        return self._pin.value() == 0

# ==================
# テストコード
# ================== 
if __name__  == "__main__":
    print("test start ----")
    cls = ToggleSwitch(0)
    print("on:{0}/off:{1}".format(cls.is_on(), cls.is_off()))
    print("test end   ----")
