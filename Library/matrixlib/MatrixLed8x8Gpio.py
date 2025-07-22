import time

from machine import Pin, Timer

from matrixlib.MatrixLed import MatrixLed, MatrixLedTester


class MatrixLed8x8Gpio(MatrixLed):
    """8x8サイズGPIO接続マトリクスLEDクラス"""

    __SIZE = 8
    """マトリクスサイズ"""
    __COLS_BIT_MASK_LIST = [
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

    def __init__(self, rows_power_pin_list: list[int], cols_gnd_pin_list: list[int]):
        """コンストラクタ

        Args:
            rows_power_pin_list (list[int]): 行用電力出力ピンリスト(上から下の順に指定)
            cols_gnd_pin_list (list[int]): 列用GNDピンリスト（左から右の順に指定）
        """
        super().__init__()
        super().set_size(self.__SIZE, self.__SIZE)
        self.__rows_power_pin_list = [
            Pin(pin_no, Pin.OUT) for pin_no in rows_power_pin_list
        ]
        self.__cols_gnd_pin_list = [
            Pin(pin_no, Pin.OUT) for pin_no in cols_gnd_pin_list
        ]
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
                # 全行の電源をoff
                [pin.off() for pin in self.__rows_power_pin_list]
                # 全列を消灯(GND側をONで電位差が無くなるので消灯となる)
                [pin.on() for pin in self.__cols_gnd_pin_list]
                # 該当業に電力を供給
                self.__rows_power_pin_list[row_idx].on()
                # 該当業の各列のonとoffを設定
                row_pattern = pattern[row_idx]
                for col_idx in range(self.__SIZE):
                    # GND側をOFFで電位差が発生するので点灯となる
                    if row_pattern & self.__COLS_BIT_MASK_LIST[col_idx]:
                        self.__cols_gnd_pin_list[col_idx].off()
                time.sleep(0.001)
        self.__hidden()

    def __hidden(self):
        """消灯(各クラスで実装すること)"""
        print("gpio display off")
        [pin.off() for pin in self.__rows_power_pin_list]
        [pin.on() for pin in self.__cols_gnd_pin_list]

    def __cut_flip(self, timer):
        self.__is_flipping = False


# ==================
# テストコード
# ==================
if __name__ == "__main__":
    print("test start")
    testtarget = MatrixLed8x8Gpio(
        [0, 1, 2, 3, 4, 5, 6, 7], [8, 9, 10, 11, 12, 13, 14, 15]
    )
    tester = MatrixLedTester(testtarget)
    tester.test()
    print("test end")
