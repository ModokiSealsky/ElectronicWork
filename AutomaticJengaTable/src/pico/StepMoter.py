from machine import Pin
import utime

class StepMoter:
    """ステップモーター制御クラス
    ピン4本を指定してインスタンス化。
    回転方向フラグを指定して1ステップ分だけ回転させる。
    """
    # ステップモーター励磁パターン指定
    full_signal = [
        [1, 1, 0, 0],
        [0, 1, 1, 0],
        [0, 0, 1, 1],
        [1, 0, 0, 1],
        [1, 1, 0, 0],
        [0, 1, 1, 0],
        [0, 0, 1, 1],
        [1, 0, 0, 1]
    ]
    wave_signal = [
        [1, 0, 0, 0],
        [1, 1, 0, 0],
        [0, 1, 0, 0],
        [0, 1, 1, 0],
        [0, 0, 1, 0],
        [0, 0, 1, 1],
        [0, 0, 0, 1],
        [1, 0, 0, 1]
    ]

    def __init__(self, pin_no1, pin_no2, pin_no3, pin_no4):
        """コンストラクタ
        Args:
            pin_no1 (int): 制御ピン番号
            pin_no2 (int): 制御ピン番号
            pin_no3 (int): 制御ピン番号
            pin_no4 (int): 制御ピン番号
        """
        self.p1 = Pin(pin_no1, Pin.OUT)
        self.p2 = Pin(pin_no2, Pin.OUT)
        self.p3 = Pin(pin_no3, Pin.OUT)
        self.p4 = Pin(pin_no4, Pin.OUT)
        self.pos = 0

    def step(self, step_count):
        """コンストラクタ
        Args:
            step_count (int): 回転ステップ数（負数は逆転方向）
        """
        if step_count == 0:
            return
        signal = self.full_signal
        pos = self.pos
        add = 9
        if step_count < 0:
            add = 7
            step_count = step_count * -1
        for i in range(step_count):
            self.p1.value(signal[pos][0])
            self.p2.value(signal[pos][1])
            self.p3.value(signal[pos][2])
            self.p4.value(signal[pos][3])
            utime.sleep_ms(10)
            pos = (pos + add) % 8
        self.pos = pos
