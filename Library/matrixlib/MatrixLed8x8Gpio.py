import time

from machine import Pin, Timer

from matrixlib import MatrixLed


class MatrixLed8x8Gpio(MatrixLed):
    """8x8サイズGPIO接続マトリクスLEDクラス"""

    __SIZE = 8
    """マトリクスサイズ"""
    __COL_BIT_MASK_LIST = [
        0b10000000,
        0b01000000,
        0b00100000,
        0b00010000,
        0b00001000,
        0b00000100,
        0b00000010,
        0b00000001,
    ]
    """点灯列判定用ビットマスク配列"""

    def __init__(self, on_pin_list: list[int], gnd_pin_list: list[int]):
        """コンストラクタ

        Args:
            on_pin_list (list[int]): 点灯ピンリスト(左から右の順に指定)
            gnd_pin_list (list[int]): GNDピンリスト（上から下の順に指定）
        """
        super().__init__()
        super().set_size(self.__SIZE, self.__SIZE)
        self.__on_pin_list = [Pin(pin_no, Pin.OUT) for pin_no in on_pin_list]
        self.__gnd_pin_list = [Pin(pin_no, Pin.OUT) for pin_no in gnd_pin_list]
        self.__timer = Timer(-1)
        self.__flip_ms = int(self.__per_ms / self.__SIZE)
        self.__is_flipping = False

    def set_size(self, width: int, height: int):
        """マトリクスサイズを設定する
        ※8x8GPIOは指定を無視して8x8固定

        Args:
            width (int): 幅
            height (int): 高さ
        """
        super().set_size(self.__SIZE, self.__SIZE)

    def set_per_ms(self, per_ms: int):
        """１文字を流しきる時間を設定する

        Args:
            per_ms (int): ミリ秒
        """
        super().set_per_ms(per_ms)
        self.__flip_ms = int(per_ms / self.__SIZE)

    def __drow(self, pattern: list[int]):
        """指定パターンを描画する(各クラスで実装すること)

        Args:
            pattern (list[int]): マトリクスパターン
        """
        print("--GPIO--")
        [print(f"{row_bit:08b}") for row_bit in pattern]
        self.__is_flipping = True
        self.__timer.init(
            mode=Timer.ONE_SHOT, period=self.__flip_ms, callback=self.__cut_flip
        )
        # ドットが一瞬で消えるので、指定期間ループする処理が必要
        while self.__is_flipping:
            for row_idx in range(self.__SIZE):
                self.__chabge_row(row_idx)
                row_pattern = pattern[row_idx]
                for col_idx in range(self.__SIZE):
                    if row_pattern & self.__COL_BIT_MASK_LIST[col_idx]:
                        self.__on_pin_list[col_idx].on()
                    else:
                        self.__on_pin_list[col_idx].off()

    def __hidden(self):
        """消灯(各クラスで実装すること)"""
        print("gpio display off")
        [pin.off() for pin in self.__on_pin_list]
        [pin.on() for pin in self.__gnd_pin_list]

    def __chabge_row(self, row_idx: int):
        """描画行変更

        Args:
            row_no (int): 描画行番号
        """
        for list_idx in range(self.__SIZE):
            if list_idx == row_idx:
                self.__gnd_pin_list[list_idx].off()
            else:
                self.__gnd_pin_list[list_idx].on()

    def __cut_flip(self, timer):
        self.__is_flipping = False


if __name__ == "__main__":
    print("test start")
    msg = "ABA"
    print(msg)
    time.sleep(2)
    m_led = MatrixLed8x8Gpio([0, 1, 2, 3, 4, 5, 6, 7], [15, 14, 13, 12, 11, 10, 9, 8])
    m_led.set_message(msg)
    m_led.show()
    time.sleep(3)
    m_led.off_with_wait()
    msg = "ひやしカレー始めました!?"
    print(msg)
    time.sleep(2)
    m_led.set_message(msg)
    m_led.set_per_ms(500)
    m_led.show()
    time.sleep(15)
    m_led.off_with_wait()
    msg = "あたたか～いビールあります。"
    print(msg)
    time.sleep(2)
    m_led.set_message(msg)
    m_led.set_per_ms(300)
    m_led.show()
    time.sleep(10)
    m_led.off()
    print("called off")
    time.sleep(2)
    print("test end")
