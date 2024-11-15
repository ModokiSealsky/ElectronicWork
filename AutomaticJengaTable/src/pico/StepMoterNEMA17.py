from machine import Pin
import utime

class StepMoterNEMA17:
    """NEMA17（バイボーラステップモーター）制御クラス
    ピン3本を指定してインスタンス化。
    ステップ数を指定して回転。
    マイナスの値は逆回転。
    """
    def __init__(self, pin_ena, pin_dir, pin_pul):
        """コンストラクタ
        Args:
            pin_ena (int): ENA制御ピン番号
            pin_dir (int): DIR制御ピン番号
            pin_pul (int): PUL制御ピン番号
        """
        self._p_ena = Pin(pin_ena, Pin.OUT)
        self._p_ena.value(0)
        self._p_dir = Pin(pin_dir, Pin.OUT)
        self._p_dir.value(0)
        self._p_pul = Pin(pin_pul, Pin.OUT)
        self._p_pul.value(0)
        self._pulsUtime = 5

    def setUtime(self, utime):
        """step間隔指定
        Args:
            utime (int): ステップ間隔ミリ秒
        """
        self._pulsUtime = utime

    def step(self, step_count):
        """指定ステップ数回転
        Args:
            step_count (int): 回転ステップ数（負数は逆転方向）
        """
        if step_count == 0:
            return
        dir_val = 1
        if step_count < 0:
            dir_val = 0
            step_count = step_count * -1

        for i in range(step_count):
            self._p_ena.value(1)
            self._p_dir.value(dir_val)
            self._p_pul.value(0)
            utime.sleep_ms(self._pulsUtime)
            self._p_pul.value(1)
            utime.sleep_ms(self._pulsUtime)
        utime.sleep_ms(1000)
