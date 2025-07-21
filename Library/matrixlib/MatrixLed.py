import time
import _thread

from matrixlib import MatrixCharactor


class MatrixLed:
    __width: int = 8
    """マトリクスLEDの横方向LED数"""
    __height: int = 8
    """マトリクスLEDの縦方向LED数"""
    __charactor_size = 8
    """文字サイズ(8か16)"""
    __per_ms: int = 1000
    """１文字を流しきる時間(ミリ秒)"""
    __between_px: int = 8
    """文字間のピクセル数"""
    __is_drowing: bool = False
    """描画中かどうか"""
    __is_drow_stop_exec = False
    """描画停止中かどうか"""
    __char_pettern_list: list[list[int]] = []
    """表示文字のマトリクスパターン配列"""
    __MASK_8PX_CHAR = 0b11111111
    """文字サイズ8用ビットマスク"""
    __MASK_16PX_CHAR = 0b1111111111111111
    """文字サイズ16用ビットマスク"""
    __char_bit_mask = __MASK_8PX_CHAR
    """文字描画用ビットマスク"""

    def set_size(self, width: int, height: int):
        """マトリクスサイズを設定する

        Args:
            width (int): 幅
            height (int): 高さ
        """
        if self.__can_not_change():
            return
        # マトリクスLEDと文字サイズを指定された値に設定
        self.__width = width
        self.__height = height
        if height >= 16:
            self.__charactor_size = 16
            self.__between_px = 16
            self.__char_bit_mask = self.__MASK_16PX_CHAR
        else:
            self.__charactor_size = 8
            self.__between_px = 8
            self.__char_bit_mask = self.__MASK_8PX_CHAR

    def set_message(self, message: str):
        """メッセージを設定する

        Args:
            message (str): メッセージ
        """
        if self.__is_drowing:
            # 描画中の変更禁止
            print("drowing... need off first.")
            return
        # 文字パターン配列を生成する
        pattern = MatrixCharactor()
        char_pettern_list = []
        for ch in list(message):
            char_pettern_list.append(pattern.get_pattern(ch))
        self.__char_pettern_list = char_pettern_list

    def set_per_ms(self, per_ms: int):
        """１文字を流しきる時間を設定する

        Args:
            per_ms (int): ミリ秒
        """
        self.__per_ms = per_ms

    def set_between_px(self, between_px: int):
        """文字間のピクセル数を設定する

        Args:
            between_px (int): ピクセル数
        """
        self.__between_px = between_px

    def show(self):
        """描画"""
        if self.__is_drowing:
            print("drowing...")
            return

        # 文字の長さ(文字数、ピクセル数)
        msg_len = len(self.__char_pettern_list)
        msg_width = msg_len * self.__height
        # 描画開始
        self.__is_drowing = True
        _thread.start_new_thread(self.__show, (msg_len, msg_width))

    def __show(self, msg_len, msg_width):
        """描画処理ループ

        Args:
            msg_len (int): 文字列の長さ
            msg_width (int): 文字列のピクセル数
        """
        flip_ms: float = (self.__per_ms / self.__charactor_size) / 1000
        now_idx: int = 0
        while self.__is_drowing:
            self.__drow(self.__calc_show_pattern(now_idx, msg_len))
            now_idx = (now_idx + 1) % msg_width
            time.sleep(flip_ms)
        print("show loop end")
        self.__is_drow_stop_exec = False

    def off(self):
        """消灯"""
        self.__is_drow_stop_exec = True
        self.__is_drowing = False
        self.__hidden()
        print("drow stoped.")

    def __calc_show_pattern(self, start_idx: int, msg_len: int):
        """表示パターンを計算する"""
        primary_char_idx = 0
        if start_idx != 0:
            primary_char_idx = int(start_idx / self.__charactor_size)
        ch_diff = start_idx % self.__charactor_size
        print(f"ch_diff:{ch_diff}, p_char_idx:{primary_char_idx}")
        if ch_diff == 0:
            # その文字のみ表示
            return self.__char_pettern_list[primary_char_idx]
        else:
            # 次の文字も含めて表示
            dorw_pettern = []
            for row_bit in self.__char_pettern_list[primary_char_idx]:
                # 1文字目をずれた分だけ左シフトし、表示幅に収まるように&演算で補正
                dorw_pettern.append((row_bit << ch_diff) & self.__char_bit_mask)
            # 次の文字を取得してずれた分だけ右シフトし、1文字目の値に加算
            next_ch_idx = (primary_char_idx + 1) % msg_len
            next_ch_pettern = self.__char_pettern_list[next_ch_idx]
            if next_ch_idx == 0:
                # 次の文字が最初の文字になる場合は空白を入れる
                for i in range(8):
                    dorw_pettern[i] = dorw_pettern[i] | next_ch_pettern[i] >> (
                        8 - ch_diff + self.__between_px
                    )
            else:
                for i in range(8):
                    dorw_pettern[i] = dorw_pettern[i] | next_ch_pettern[i] >> (
                        8 - ch_diff
                    )
            return dorw_pettern

    def __drow(self, pattern: list[int]):
        """指定パターンを描画する(各クラスで実装すること)

        Args:
            pattern (list[int]): マトリクスパターン
        """
        print("--------")
        [print(f"{row_bit:08b}") for row_bit in pattern]

    def __hidden(self):
        """消灯(各クラスで実装すること)"""
        print("display off")

    def __can_not_change(self):
        """変更不可チェック"""
        if self.__is_drowing:
            print("drowing... need off first.")
            return True
        return False

    def off_with_wait(self):
        """消灯(終了待ち)"""
        self.off()
        while not self.__is_drow_stop_exec:
            time.sleep(0.5)
        print("drow stoped.")


if __name__ == "__main__":
    print("test start")
    msg = "ABA"
    print(msg)
    time.sleep(2)
    m_led = MatrixLed()
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
