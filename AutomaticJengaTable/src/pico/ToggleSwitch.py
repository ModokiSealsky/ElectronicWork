from machine import Pin

class ToggleSwitch:
    """トグルスイッチ状態取得クラス

        ON/OFFを切り替えられるスイッチからの入力を取得    
        * pin番号を渡してインスタンス化する
        * スイッチがON(isOn)かOFF(isOff)かを取得する
    """
    def __init__(self, pin_no:int):
        """コンストラクタ
        Args:
            pin_no: スイッチの入力に使うGPIOピン番号
        """
        self._pin = Pin(pin_no, Pin.IN, Pin.PULL_DOWN)
    
    def isOn(self) -> bool:
        """スイッチがONならTrueを返す"""
        return self._pin.value() == 1

    def isOff(self) -> bool:
        """スイッチがOFFならTrueを返す"""
        return self._pin.value() == 0
